from enum import Enum
import logging
from typing import Any

from scrapping_playbook_framework.lib.chronos import Chronos
from scrapping_playbook_framework.playbook_reader import PlaybookDict, PlaybookTask, PlaybookTask_ATTRIBUTES
from scrapping_playbook_framework.task.task import ScrappingTask
from scrapping_playbook_framework.execution_context import ExecutionContext
from scrapping_playbook_framework.worker_strategies.selenium_worker_strategy import SeleniumWorkerStrategy
from scrapping_playbook_framework.worker_strategies.worker_strategy import WorkerStrategy

need_break = False

class WorkerEngine(Enum):
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"

strategies : dict[WorkerEngine, type[WorkerStrategy]] = {
    WorkerEngine.SELENIUM: SeleniumWorkerStrategy,
}

class TaskInvoker:
    def __init__(self, name : str, action: str, ctx: ExecutionContext, tasks_availables_dict : dict[str, ScrappingTask[Any]]):
        self.name = name
        self.action = action
        self.ctx = ctx
        self.tasks_availables_dict = tasks_availables_dict

    def __call__(self) -> Any:
        if self.action.startswith("$"):
            return self.invoke_variable_method()
        return self.invoke_standard_task()

    def invoke_variable_method(self) -> Any:
        task_name = self.name
        task_action = self.action
        ctx = self.ctx

        variable_name_with_method = task_action[1:]
        variable_name = variable_name_with_method.split(".")[0]
        method_name = variable_name_with_method.split(".")[1]
        variable_value = ctx.get_variable(variable_name)
        if not variable_value:
            logging.warning(f"Variable not found for task {task_name}: {variable_name}")
            return None
        method = getattr(variable_value, method_name, None)
        if not method:
            logging.warning(f"Method {method_name} not found on variable {variable_name} for task {task_name}")
            return None
        return method(ctx.provide_variables()) # type: ignore
    
    def invoke_standard_task(self) -> Any:
        task_name = self.name
        task_action = self.action
        ctx = self.ctx
        tasks_availables_dict = self.tasks_availables_dict

        executor_task = tasks_availables_dict.get(task_action)
        if not executor_task:
            logging.warning(f"Task action not found: {task_action} for task {task_name}")
            return None
        return executor_task.execute(ctx.provide_variables())


class Worker:
    def __init__(self, playbook_dict: PlaybookDict, engine: WorkerEngine):
        self.playbook_dict = playbook_dict
        self.engine = engine
        self.context = ExecutionContext()
        
    def get_strategy(self) -> WorkerStrategy:
        strategy_class = strategies.get(self.engine)
        if not strategy_class:
            raise ValueError(f"No strategy found for engine: {self.engine}")
        return strategy_class()
    
    def start(self) -> dict[str, Any]:
        strategy = self.get_strategy()

        def replace_variable_placeholders(params: dict[str, Any], context: ExecutionContext) -> dict[str, Any]:
            for key, value in params.items():
                if isinstance(value, str) and value.startswith("$"):
                    variable_name = value[1:]
                    variable_value = context.get_variable(variable_name)
                    if variable_value is not None:
                        params[key] = variable_value
                    else:
                        logging.warning(f"Variable {variable_name} not found in context for parameter {key}")

            return params
    

        
        def worker_loop(tasks_to_execute : list[PlaybookTask], context: ExecutionContext, tasks_availables_dict : dict[str, ScrappingTask[Any]]) -> dict[str, Any]:
            global need_break
            outputs : dict[str, Any] = {}
            
            for task_dict in tasks_to_execute:
                with Chronos() as chrono:
                    task_name = task_dict.name
                    task_action = task_dict.action
                    task_conditions = task_dict.when or []
                    #if need_break:
                        #breakpoint()
                    # Update the context with task variables
                    params = {k: v for k, v in task_dict.model_dump().items() if k not in PlaybookTask_ATTRIBUTES}
                    params = replace_variable_placeholders(params, context)
                    context.inject_variables(params)

                    # Evaluate conditions
                    conditions_met = len(task_conditions) == 0 or all(condition.evaluate(context) for condition in task_conditions)
                    if not conditions_met:
                        logging.info(f"Skipping task {task_name} due to unmet conditions.")
                        continue
                    
                    output = None
                    if task_dict.map is not None and task_dict.tasks is not None:
                        list_to_map = context.get_variable(task_dict.map)
                        if not isinstance(list_to_map, list):
                            raise ValueError(f"Variable to map is not a list: {task_dict.map}")
                        logging.info(f"Mapping over list: {len(list_to_map)} items for task {task_name}") # type: ignore
                        output= []
                        need_break = True
                        for item in list_to_map: # type: ignore
                            sub_context = context.clone()
                            sub_context.set_variable(task_dict.item_name or "item", item)
                            outputs_from_sub = worker_loop(task_dict.tasks, sub_context, tasks_availables_dict)
                            output.append(outputs_from_sub) # type: ignore
                    else :  
                        logging.info(f"Invoking task {task_name} with action {task_action}")
                        logging.info('value de attribute_name: ' + str(context.get_variable('attribute_name')))
                        invoker = TaskInvoker(task_name, task_action, context, tasks_availables_dict)
                        output = invoker()

                    task_output = task_dict.output
                    if task_output and output is not None:
                        context.set_variable(task_output, output)
                        if(not task_output.startswith('_')):
                            outputs[task_output] = output

                logging.info(f"Finished task {task_name} in {chrono.elapsed_time:.2f}s")

            return outputs


        return worker_loop(self.playbook_dict.tasks, self.context, strategy.get_available_tasks())


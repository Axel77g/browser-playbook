from enum import Enum
import logging
from typing import Any

from scrapping_playbook_framework.core.post_processor import PostProcessorFactory
from scrapping_playbook_framework.lib import value_resolver
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
        self.context = ExecutionContext().inject_variables(self.playbook_dict.config)
        
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
                    variable_path = value[1:]
                    parts = variable_path.split('.')
                    variable_name = parts[0]
                    variable_value = context.get_variable(variable_name)
                    """
                    Can handle variables with a simple "." path like "variable.property" with depth of 1, usefull tu acces return by iterate task
                    """
                    if variable_value is not None and len(parts) > 1:
                        for part in parts[1:]:
                            if hasattr(variable_value, part): # type: ignore
                                variable_value = getattr(variable_value, part) # type: ignore
                            elif isinstance(variable_value, dict) and part in variable_value:
                                variable_value = variable_value[part] # type: ignore
                            else:
                                logging.warning(f"Could not resolve {part} in {variable_path}")
                                variable_value = None
                                break

                    if variable_value is not None:
                        params[key] = variable_value
                    else:
                        logging.warning(f"Variable {variable_name} not found in context for parameter {key}")

            return params
    
        def apply_post_processors(value: Any, processors_config: list[dict[str, Any]]) -> Any:
            """Apply a chain of post-processors to a value"""
            result = value
            for processor_config in processors_config:
                processor = PostProcessorFactory.create(processor_config)
                result = processor.process(result)
            
            return result

        
        def worker_loop(tasks_to_execute : list[PlaybookTask], context: ExecutionContext, tasks_availables_dict : dict[str, ScrappingTask[Any]]) -> dict[str, Any]:
            
            global need_break
            outputs : dict[str, Any] = {}
            
            for task_dict in tasks_to_execute:
                with Chronos() as chrono:
                    logging.info(f"Starting task {task_dict.name}")
                    task_name = task_dict.name
                    task_action = task_dict.action
                    task_conditions = task_dict.when or []
                    params = {k: v for k, v in task_dict.model_dump().items() if k not in PlaybookTask_ATTRIBUTES}
                    params = replace_variable_placeholders(params, context)
                    context.inject_variables(params)

                    if(task_dict.debug):
                        logging.info(f"Debugging task {task_dict.name} - Start Point")
                        breakpoint()

                    # Evaluate conditions
                    conditions_met = len(task_conditions) == 0 or all(condition.evaluate(context) for condition in task_conditions)
                    if not conditions_met:
                        logging.info(f"Skipping task {task_name} due to unmet conditions.")
                        continue
                    
                    output = None
                    
                    if task_dict.map is not None and task_dict.tasks is not None:
                        """
                        A Map loop create a subcontext, all var created in the loop is in a sub context, the result can be outputed
                        """
                        list_to_map = context.get_variable(task_dict.map)

                        if not isinstance(list_to_map, list):
                            raise ValueError(f"Variable to map is not a list: {task_dict.map}")
                        logging.debug(f"Mapping over list: {len(list_to_map)} items for task {task_name}") # type: ignore
                        output= []
                        for index, item in enumerate(list_to_map): # type: ignore
                            if(task_dict.debug):
                                logging.info(f"Debugging task {task_dict.name} - Iteration {index}")
                                breakpoint()
                            sub_context = context.clone()
                            sub_context.set_variable('INDEX',index)
                            sub_context.set_variable(task_dict.item_name or "item", item)
                            if(task_dict.filters is not None):
                                if not all(f.evaluate(sub_context) for f in task_dict.filters):
                                    continue

                            outputs_from_sub = worker_loop(task_dict.tasks, sub_context, tasks_availables_dict)
                            if(task_dict.flatten): # type:ignore
                                output = None
                                outputs.update(outputs_from_sub) # type: ignore
                            else:
                                output.append(outputs_from_sub) # type: ignore
                    else :  
                        logging.debug(f"Invoking task {task_name} with action {task_action}")
                        invoker = TaskInvoker(task_name, task_action, context, tasks_availables_dict)
                        output = invoker()


                    if task_dict.post_process is not None and output is not None:
                        output = apply_post_processors(output, task_dict.post_process)
                    
                    task_output_var_name = value_resolver.resolve(context, task_dict.output)
                    if task_output_var_name and output is not None:
                        context.set_variable(task_output_var_name, output)
                        if(not task_output_var_name.startswith('_')):
                            outputs[task_output_var_name] = output

                    if(task_dict.debug):
                        logging.info(f"Debugging task {task_dict.name} - End Point")
                        breakpoint()

                logging.info(f"Finished task {task_name} in {chrono.elapsed_time:.2f}s")

            return outputs


        return worker_loop(self.playbook_dict.tasks, self.context, strategy.get_available_tasks())


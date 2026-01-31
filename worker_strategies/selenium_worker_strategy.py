
from typing import Any
from scrapping_playbook_framework.selenium.selenium_bootstrap import get_driver, get_selenium_tasks
from scrapping_playbook_framework.task.task import ScrappingTask
from scrapping_playbook_framework.worker_strategies.worker_strategy import WorkerStrategy

class SeleniumWorkerStrategy(WorkerStrategy):
    def get_available_tasks(self) -> dict[str, ScrappingTask[Any]]:
        driver = get_driver()
        tasks_availables = get_selenium_tasks(driver)
        tasks_availables_dict = {task.get_task_action_name(): task for task in tasks_availables}
        return tasks_availables_dict
        
        
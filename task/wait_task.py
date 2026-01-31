
from abc import abstractmethod
import logging
from typing import TypedDict

from scrapping_playbook_framework.task.dom_task import DOMElement, GetElementTask
from scrapping_playbook_framework.task.task import ScrappingTask


class WaitTaskParams(TypedDict):
    duration: float

class WaitTask(ScrappingTask): # type: ignore
    def get_task_action_name(self):
        return 'wait'

    @abstractmethod
    def execute(self, ctx: WaitTaskParams) -> None:
        pass

class WaitForElementTaskParams(TypedDict):
    selector: str
    timeout: float

class WaitForElementTask(ScrappingTask[DOMElement]):
    def __init__(self, _get_element_task: GetElementTask, _wait_task: WaitTask):
        self._get_element_task = _get_element_task
        self._wait_task = _wait_task

    def get_task_action_name(self) -> str:
        return 'wait.for_element'

    def execute(self, ctx: WaitForElementTaskParams) -> DOMElement:
        self._wait_task.execute({'duration': ctx['timeout']})
        element = self._get_element_task.execute(ctx)
        if element is None:
            logging.warning(f"Element with selector '{ctx['selector']}' not found after waiting {ctx['timeout']} seconds")
            raise Exception(f"Element with selector '{ctx['selector']}' not found within {ctx['timeout']} seconds")
        return element

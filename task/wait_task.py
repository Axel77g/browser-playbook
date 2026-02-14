
from abc import abstractmethod
from typing import TypedDict

from scrapping_playbook_framework.task.dom_task import DOMElement
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

    def get_task_action_name(self) -> str:
        return 'wait.for_element'
    
    @abstractmethod
    def execute(self, ctx: WaitForElementTaskParams) -> DOMElement:
        pass

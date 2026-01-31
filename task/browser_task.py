from abc import abstractmethod
from typing import TypedDict
from scrapping_playbook_framework.task.task import ScrappingTask


class GoToParams(TypedDict):
    url: str
    
class GoToTask(ScrappingTask[None]):
    def get_task_action_name(self) -> str:
        return "browser.goto"
    
    @abstractmethod
    def execute(self, ctx: GoToParams) -> None:
        pass

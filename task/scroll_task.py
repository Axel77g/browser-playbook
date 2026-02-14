from abc import abstractmethod
from typing import TypedDict
from enum import Enum

from scrapping_playbook_framework.task.task import ScrappingTask

class ScrollDirection(str,Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"

class ScrollTaskParams(TypedDict):
    direction: ScrollDirection
    amount: int

class ScrollTask(ScrappingTask[None]):
    def get_task_action_name(self):
        return "browser.scroll"

    @abstractmethod
    def execute(self, ctx: ScrollTaskParams) -> None:
        pass

from abc import abstractmethod
from typing import TypedDict
from scrapping_playbook_framework.position import Position
from scrapping_playbook_framework.task.task import ScrappingTask


class ClickParams(TypedDict):
    click_position: Position

class ClickTask(ScrappingTask[None]):
    def get_task_action_name(self):
        return "mouse.click"

    @abstractmethod
    def execute(self, ctx: ClickParams) -> None:
        pass

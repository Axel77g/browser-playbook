from abc import ABC, abstractmethod
from typing import Any, Optional, TypedDict

from scrapping_playbook_framework.position import Position
from scrapping_playbook_framework.task.task import ScrappingTask

class DOMElementGetAttributeParams(TypedDict):
    attribute_name: str

class DOMElement(ABC):
    @abstractmethod
    def get_text(self, ctx: Any) -> str | None:
        pass

    @abstractmethod
    def get_attribute(self, ctx: DOMElementGetAttributeParams) -> str | None:
        pass

    @abstractmethod
    def get_position(self, ctx: Any) -> Position | None:
        pass

    @abstractmethod
    def click(self, ctx: Any) -> None:
        pass

    @abstractmethod
    def get_element(self, ctx: 'SelectorParams') -> Optional['DOMElement']:
        pass
    @abstractmethod
    def get_elements(self, ctx: 'SelectorParams') -> list['DOMElement']:
        pass

    @abstractmethod
    def get_shadow_root(self, ctx: Any) -> Optional['DOMElement']:
        pass

class SelectorParams(TypedDict):
    selector: str

class GetElementTask(ScrappingTask[DOMElement]):
    def get_task_action_name(self) -> str:
        return "dom.get_element"

    @abstractmethod
    def execute(self, ctx: SelectorParams) -> Optional[DOMElement]:
        pass

class GetElementsTask(ScrappingTask[list[DOMElement]]):
    def get_task_action_name(self):
        return "dom.get_elements"

    @abstractmethod
    def execute(self, ctx: SelectorParams) -> list[DOMElement]:
        pass
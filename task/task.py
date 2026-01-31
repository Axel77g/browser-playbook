from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Optional

T = TypeVar("T")


class ScrappingTask(ABC, Generic[T]):
    @abstractmethod
    def get_task_action_name(self) -> str:
        pass

    @abstractmethod
    def execute(self, ctx: Any) -> Optional[T]:
        """Execute the task. Default implementation returns None."""
        return None

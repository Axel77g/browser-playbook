from abc import ABC, abstractmethod
from typing import Any

from scrapping_playbook_framework.task.task import ScrappingTask

class WorkerStrategy(ABC):
    @abstractmethod
    def get_available_tasks(self) -> dict[str, ScrappingTask[Any]]:
        pass
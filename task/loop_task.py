
from typing import Any, TypedDict
from scrapping_playbook_framework.task.task import ScrappingTask


class IterateTaskParams(TypedDict):
    tasks: list[ScrappingTask[Any]]
    items: list[Any]

class IterateTask(ScrappingTask[dict[str, Any]]):
    def get_task_action_name(self):
        return 'iterate'

    def execute(self, ctx: IterateTaskParams) -> dict[str, Any]:
        results : dict[str, Any] = {}
        for item in ctx['items']:
            for task in ctx['tasks']:
                result = task.execute({'item': item})
                results.update(result) # type: ignore
        return results 
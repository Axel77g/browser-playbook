from abc import abstractmethod
import os
from typing import Any, TypedDict
from scrapping_playbook_framework.task.task import ScrappingTask
from requests import get

class GoToParams(TypedDict):
    url: str
    
class GoToTask(ScrappingTask[None]):
    def get_task_action_name(self) -> str:
        return "browser.goto"
    
    @abstractmethod
    def execute(self, ctx: GoToParams) -> None:
        pass


class GoBackTask(ScrappingTask[None]):
    def get_task_action_name(self):
        return "browser.go_back"
    
    @abstractmethod
    def execute(self, ctx: Any) -> None:
        pass


class ScreenshotParams(TypedDict):
    path: str

class ScreenshotTask(ScrappingTask[None]):
    def get_task_action_name(self):
        return "browser.screenshot"
    
    @abstractmethod
    def execute(self, ctx : ScreenshotParams):
        pass

class DownloadUrlParams(TypedDict):
    url: str
    path: str

class DownloadUrl(ScrappingTask[None]):
    def get_task_action_name(self):
        return "browser.download_url"
    
    def execute(self, ctx: DownloadUrlParams):
        # make download and store in file
        
        path = ctx['path']
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        response = get(ctx["url"])

        with open(ctx["path"], "wb") as f:
            f.write(response.content)
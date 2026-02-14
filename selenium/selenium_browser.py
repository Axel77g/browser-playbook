import os
from typing import Any
from scrapping_playbook_framework.task.browser_task import GoBackTask, GoToParams, GoToTask, ScreenshotParams, ScreenshotTask
from selenium.webdriver.remote.webdriver import WebDriver

class SeleniumGoToTask(GoToTask):
    def __init__(self, driver : WebDriver):
        super().__init__()
        self.driver = driver

    def execute(self, ctx : GoToParams) -> None:
        self.driver.get(ctx['url'])


class SeleniumGoBackTask(GoBackTask):
    def __init__(self, driver: WebDriver):
        super().__init__()
        self.driver = driver

    def execute(self, ctx: Any) -> None:
        self.driver.back()

class SeleniumScreenshotTask(ScreenshotTask):
    def __init__(self, driver:WebDriver):
        super().__init__()
        self.driver = driver

    def execute(self, ctx : ScreenshotParams) -> None:
        path = ctx['path']
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        if not self.driver.save_screenshot(path): # type:ignore
            raise Exception(f"Could not save screenshot to {path}")
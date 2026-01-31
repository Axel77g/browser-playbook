from scrapping_playbook_framework.task.browser_task import GoToParams, GoToTask
from selenium.webdriver.remote.webdriver import WebDriver

class SeleniumGoToTask(GoToTask):
    def __init__(self, driver : WebDriver):
        super().__init__()
        self.driver = driver

    def execute(self, ctx : GoToParams) -> None:
        self.driver.get(ctx['url'])
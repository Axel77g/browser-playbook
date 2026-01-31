
import time
from selenium.webdriver.remote.webdriver import WebDriver
from scrapping_playbook_framework.task.wait_task import WaitTask, WaitTaskParams

class SeleniumWaitTask(WaitTask):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def execute(self, ctx: WaitTaskParams) -> None:
        time.sleep(ctx['duration'])

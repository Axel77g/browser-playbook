
import logging
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapping_playbook_framework.task.dom_task import DOMElement, GetElementTask
from scrapping_playbook_framework.task.wait_task import WaitTask, WaitTaskParams,WaitForElementTask,WaitForElementTaskParams

class SeleniumWaitTask(WaitTask):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def execute(self, ctx: WaitTaskParams) -> None:
        time.sleep(ctx['duration'])

class SeleniumWaitForElementTask(WaitForElementTask):
    def __init__(self, driver: WebDriver, _get_element_task: GetElementTask):
        self.driver = driver
        self._get_element_task = _get_element_task

    def execute(self, ctx: WaitForElementTaskParams) -> DOMElement:
        timeout = ctx.get('timeout', 10) 
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ctx['selector']))
        )

        element = self._get_element_task.execute(ctx)
        if element is None:
            logging.warning(f"Element with selector '{ctx['selector']}' not found after waiting {ctx['timeout']} seconds")
            raise Exception(f"Element with selector '{ctx['selector']}' not found within {ctx['timeout']} seconds")
        return element
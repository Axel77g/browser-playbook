from scrapping_playbook_framework.task.loop_task import IterateTask
from selenium.webdriver.remote.webdriver import WebDriver

class SeleniumIterateTask(IterateTask):
    def __init__(self, driver: WebDriver):
        self.driver = driver
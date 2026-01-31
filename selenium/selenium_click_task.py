from scrapping_playbook_framework.task.click_task import ClickParams, ClickTask
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

class SeleniumClickTask(ClickTask):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def execute(self, ctx: ClickParams) -> None:
        position = ctx.get('click_position')
        ActionChains(self.driver).move_by_offset(position.get('x'), position.get('y')).click().perform()
        
from scrapping_playbook_framework.task.keyboard_task import KeyboardPressTask, KeyboardPressTaskParams, KeyboardTypeTask

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
class SeleniumKeyboardPressTask(KeyboardPressTask):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def execute(self, ctx: KeyboardPressTaskParams) -> None:
        key = ctx['key']
        if key == "#enter":
            ActionChains(self.driver).send_keys("\ue007").perform()
        else:   
            self.driver.switch_to.active_element.send_keys(key)

class SeleniumKeyboardTypeTask(KeyboardTypeTask):
    def __init__(self, driver: WebDriver, _keyboard_press_task: SeleniumKeyboardPressTask):
        super().__init__(_keyboard_press_task)
        self.driver = driver
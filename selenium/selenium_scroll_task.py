
import logging
from scrapping_playbook_framework.task.scroll_task import ScrollDirection, ScrollTask, ScrollTaskParams
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

class SeleniumScrollTask(ScrollTask):
    def __init__(self, driver: WebDriver):
        self.driver=driver

    def execute(self, ctx : ScrollTaskParams):
        if ctx.get('direction') == ScrollDirection.BOTTOM or ctx.get('direction') == ScrollDirection.TOP:
            delta_y = ctx.get('amount') if ctx.get('direction') == ScrollDirection.BOTTOM else -ctx.get('amount')
            ActionChains(self.driver).scroll_by_amount(0, delta_y).perform() # type: ignore
        elif ctx.get('direction') == ScrollDirection.LEFT or ctx.get('direction') == ScrollDirection.RIGHT:
            delta_x = ctx.get('amount') if ctx.get('direction') == ScrollDirection.RIGHT else -ctx.get('amount')
            ActionChains(self.driver).scroll_by_amount(delta_x, 0).perform() # type: ignore
        else:
            logging.warning('Invalid scroll direction')
            raise Exception('Invalid scroll direction')
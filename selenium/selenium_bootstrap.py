from typing import Any
from scrapping_playbook_framework.selenium.selenium_browser import SeleniumGoBackTask, SeleniumGoToTask, SeleniumScreenshotTask
from scrapping_playbook_framework.selenium.selenium_click_task import SeleniumClickTask
from scrapping_playbook_framework.selenium.selenium_dom_task import SeleniumGetElementTask, SeleniumGetElementsTask, WebDriverElementFinder
from scrapping_playbook_framework.selenium.selenium_keyboard_task import SeleniumKeyboardPressTask, SeleniumKeyboardTypeTask
from scrapping_playbook_framework.selenium.selenium_scroll_task import SeleniumScrollTask
from scrapping_playbook_framework.selenium.selenium_wait_task import SeleniumWaitForElementTask, SeleniumWaitTask
from scrapping_playbook_framework.task.browser_task import DownloadUrl
from scrapping_playbook_framework.task.export_task import CSVExportTask
from scrapping_playbook_framework.task.task import ScrappingTask
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from scrapping_playbook_framework.task.wait_task import WaitForElementTask

def get_driver() -> WebDriver:
    options = Options()
    # options.add_argument('--headless')  # Mode sans interface graphique
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Make the browser appear more human-like
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Add realistic user agent
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument('--referer=https://www.google.com/')

    driver = webdriver.Chrome(options=options)
    
    # Remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Pollute browsing history with random navigation
    history_urls = [
        'https://www.google.com',
        'https://www.wikipedia.org',
        'https://www.github.com',
        'https://www.twitter.com',
        'https://www.reddit.com',
        'https://www.facebook.com',
        'https://www.linkedin.com',
        'https://www.youtube.com',
        'https://www.stackoverflow.com',
        'https://www.google.com',
    ]
    #for url in history_urls:
    #    driver.get(url)
    
    return driver

def get_selenium_tasks(driver: WebDriver) -> list[ScrappingTask[Any]]:
    _keyboard_press_task = SeleniumKeyboardPressTask(driver)
    _wait_task = SeleniumWaitTask(driver)
    _get_element_task = SeleniumGetElementTask(driver,WebDriverElementFinder(driver))

    return [
        SeleniumGoToTask(driver),
        SeleniumGoBackTask(driver),
        SeleniumClickTask(driver), # type: ignore
        _keyboard_press_task,
        _wait_task,
        _get_element_task,
        SeleniumGetElementsTask(driver,WebDriverElementFinder(driver)),
        SeleniumKeyboardTypeTask(driver, _keyboard_press_task),
        SeleniumWaitForElementTask(driver, _get_element_task),
        SeleniumScrollTask(driver),
        SeleniumScreenshotTask(driver),
        DownloadUrl(),
        CSVExportTask()
    ]

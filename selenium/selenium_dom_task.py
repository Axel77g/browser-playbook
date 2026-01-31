from abc import ABC, abstractmethod
from typing import Any, Optional
from scrapping_playbook_framework.position import Position
from scrapping_playbook_framework.task.dom_task import DOMElement, DOMElementGetAttributeParams, GetElementTask, GetElementsTask, SelectorParams

from selenium.webdriver.common.by import By,ByType
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot

class SeleniumDOMElement(DOMElement):
    def __init__(self, web_driver : WebDriver, web_element: WebElement | ShadowRoot):
        self.web_element = web_element
        self.web_driver = web_driver

    def get_text(self, ctx: Any) -> str:
        if isinstance(self.web_element, ShadowRoot):
            return ""
        return self.web_element.text

    def get_attribute(self, ctx: DOMElementGetAttributeParams) -> str | None:
        print("Getting attribute:", ctx.get('attribute_name'))
        return self.web_element.get_attribute(ctx.get('attribute_name')) # type: ignore

    def get_position(self, ctx: Any) -> Position | None:
        if not self.web_element:
            return None
        location = self.web_element.location # type: ignore
        return location # type: ignore

    def click(self, ctx: Any) -> None:
        #si shadow root, on ne peut pas cliquer
        if isinstance(self.web_element, ShadowRoot):
            return
        self.web_element.click()

    def get_element(self, ctx: SelectorParams) -> DOMElement | None:
        return SeleniumGetElementTask(self.web_driver, WebElementFinder(self.web_element)).execute(ctx)

    def get_elements(self, ctx: SelectorParams) -> list[DOMElement]:
        return SeleniumGetElementsTask(self.web_driver, WebElementFinder(self.web_element)).execute(ctx)

    def get_shadow_root(self, ctx: Any) -> DOMElement | None: 
        # Selenium does not support shadow DOM natively
        dom = self.web_driver.execute_script("return arguments[0].shadowRoot", self.web_element) # type: ignore
        return SeleniumDOMElement(self.web_driver, dom)

class SeleniumElementFinder(ABC):
    @abstractmethod
    def find_element(self, by: ByType, value: str | None) -> WebElement | None:
        pass

    @abstractmethod
    def find_elements(self, by: ByType, value: str | None) -> list[WebElement]:
        pass

class WebDriverElementFinder(SeleniumElementFinder):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def find_element(self, by: ByType, value: str | None) -> WebElement | None:
        try:
            return self.driver.find_element(by, value)
        except:
            return None

    def find_elements(self, by: ByType, value: str | None) -> list[WebElement]:
        try:
            return self.driver.find_elements(by, value)
        except:
            return []

class WebElementFinder(SeleniumElementFinder):
    def __init__(self, web_element: WebElement | ShadowRoot):
        self.web_element = web_element

    def find_element(self, by: ByType, value: str | None) -> WebElement | None:
        try:
            return self.web_element.find_element(by, value) # type: ignore
        except:
            return None

    def find_elements(self, by: ByType, value: str | None) -> list[WebElement]:
        try:
            return self.web_element.find_elements(by, value) # type: ignore
        except:
            return []        

class SeleniumGetElementTask(GetElementTask):
    def __init__(self, web_driver: WebDriver, base: SeleniumElementFinder):
        self.web_driver = web_driver
        self.base = base

    def execute(self, ctx: SelectorParams) -> Optional[DOMElement]:
        element = self.base.find_element(By.CSS_SELECTOR, ctx.get('selector'))
        if element is None:
            return None
        return SeleniumDOMElement(self.web_driver, element)
    
class SeleniumGetElementsTask(GetElementsTask):
    def __init__(self, web_driver: WebDriver, base: SeleniumElementFinder):
        self.web_driver = web_driver
        self.base = base

    def execute(self, ctx: SelectorParams) -> list[DOMElement]:
        elements = self.base.find_elements(By.CSS_SELECTOR, ctx.get('selector'))
        return [SeleniumDOMElement(self.web_driver, el) for el in elements if el]
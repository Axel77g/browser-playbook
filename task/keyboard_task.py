from abc import abstractmethod
from typing import TypedDict
from scrapping_playbook_framework.task.task import ScrappingTask
import time
import random

class KeyboardPressTaskParams(TypedDict):
    key: str

class KeyboardPressTask(ScrappingTask[None]):
    def get_task_action_name(self):
        return "keyboard.press"

    @abstractmethod
    def execute(self, ctx: KeyboardPressTaskParams) -> None:
        pass

class KeyboardTypeParams(TypedDict):
    text: str

class KeyboardTypeTask(ScrappingTask[None]):
    def __init__(self, _keyboard_press_task: KeyboardPressTask):
        self._keyboard_press_task = _keyboard_press_task

    def get_task_action_name(self):
        return "keyboard.type"

    def execute(self, ctx: KeyboardTypeParams) -> None:
        text = ctx.get('text', '')
        for char in text:
            # press the key
            self._keyboard_press_task.execute({'key': char})

            # small, slightly random delay to mimic human typing
            delay = random.uniform(0.1, 0.6)
            if char == ' ':
                # a bit longer pause for spaces
                delay += random.uniform(0.05, 0.25)
            time.sleep(delay)

            # occasional longer "thinking" pause
            if random.random() < 0.06:
                time.sleep(random.uniform(0.5, 1.2))
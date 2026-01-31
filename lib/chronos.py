import time
from typing import Any


class Chronos:

    def __init__(self):
        self.start_time : float = .0
        self.end_time : float = .0
        self.elapsed_time : float = .0

    def __enter__(self):
        """
        Start the timer for synchronous context.
        :return: self
        """
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type : Any, exc_value: Any, traceback: Any):
        """
        Stop the timer and calculate the elapsed time for synchronous context.
        :param exc_type: The type of exception raised, if any.
        :param exc_value: The value of the exception raised, if any.
        :param traceback: The traceback object, if any.
        """
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    async def __aenter__(self):
        """
        Start the timer for asynchronous context.
        :return: self
        """
        self.start_time = time.time()
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        """
        Stop the timer and calculate the elapsed time for asynchronous context.
        :param exc_type: The type of exception raised, if any.
        :param exc_value: The value of the exception raised, if any.
        :param traceback: The traceback object, if any.
        """
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time


    def start(self) -> None:
        """
        Start or restart the timer.
        """
        self.start_time = time.time()
        self.end_time = .0
        self.elapsed_time = .0

    def take(self) -> float:
        """
        Take the current elapsed time without stopping the timer.
        :return: The current elapsed time in seconds.
        """
        current_time = time.time()
        return current_time - self.start_time
    
    def is_started(self) -> bool:
        """
        Check if the timer has been started.
        :return: True if the timer has been started, False otherwise.
        """
        return self.start_time != .0
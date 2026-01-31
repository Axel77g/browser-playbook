import logging
from typing import Any

class ExecutionContext():
    def __init__(self):
        self._variables: dict[str, Any] = {}
        logging.debug("Initialized new execution context.")

    def set_variable(self, key: str, value: Any) -> None:
        self._variables[key] = value
    
    def get_variable(self, key: str, default: Any = None) -> Any:
        return self._variables.get(key, default)
    
    def delete(self, key: str) -> None:
        if key in self._variables:
            del self._variables[key]
            logging.debug(f"Deleted variable: {key}")
            

    def inject_variables(self, dict: dict[str, Any]):
        for key, value in dict.items():
            self.set_variable(key, value)
            logging.info(f"Injected variable: {key} with value: {value}, addr memory: {self}")

    def provide_variables(self) -> dict[str, Any]:
        return self._variables.copy()
    
    def clone(self) -> 'ExecutionContext':
        new_context = ExecutionContext()
        new_context._variables = self.provide_variables().copy()
        return new_context
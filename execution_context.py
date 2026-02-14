import logging
from typing import Any

from scrapping_playbook_framework.lib import value_resolver

class ExecutionContext():
    def __init__(self):
        self._variables: dict[str, Any] = {}
        logging.debug("Initialized new execution context.")

    def set_variable(self, key: str, value: Any) -> None:
        self._variables[key] = value
    
    def get_variable(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        current_value = self._variables
        try:
            for k in keys:
                if isinstance(current_value, dict): # type:ignore
                    current_value = current_value[k] # type:ignore
                else:
                    return default
            
            return value_resolver.resolve(self, current_value)
        except (KeyError, TypeError):
            return default
    
    def delete(self, key: str) -> None:
        if key in self._variables:
            del self._variables[key]
            logging.debug(f"Deleted variable: {key}")
    def inject_variables(self, dict: dict[str, Any]) -> 'ExecutionContext':
        for key, value in dict.items():
            self.set_variable(key, value)
        return self

    def provide_variables(self) -> dict[str, Any]:
        resolved_vars : dict[str, Any] = {}
        for key in self._variables.keys():
            resolved_vars[key] = self.get_variable(key)
        return resolved_vars
    
    def get_keys(self) -> list[str]:
        return list(self._variables.keys())
    
    def clone(self) -> 'ExecutionContext':
        new_context = ExecutionContext()
        new_context._variables = self.provide_variables().copy()
        return new_context
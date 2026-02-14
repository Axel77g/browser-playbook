import re
from typing import Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scrapping_playbook_framework.execution_context import ExecutionContext


def resolve(context: ExecutionContext, current_value: Any) -> Any:
    if(not isinstance(current_value, str)):
        return current_value
    

    def replace_match(match : Any):
        var_key = match.group(1).strip() # type:ignore
        resolved_value = context.get_variable(var_key, '') # type:ignore
        if(resolved_value == None):
            breakpoint()
            raise Exception(f"Interpolated variable '{var_key}' not found in context")
        return str(resolved_value) 

    # Recursively resolve templates in the string
    # We loop until no more templates are found
    while re.search(r'\{\{([^}]+)\}\}', current_value):
        new_value = re.sub(r'\{\{([^}]+)\}\}', replace_match, current_value)
        if new_value == current_value: # Avoid infinite loops if a variable resolves to itself
            break
        current_value = new_value
    return current_value
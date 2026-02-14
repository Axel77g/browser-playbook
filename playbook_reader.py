from typing import Any, Optional
from pydantic import BaseModel, Field
import yaml

from scrapping_playbook_framework.execution_context import ExecutionContext
from scrapping_playbook_framework.lib import value_resolver

class PlaybookCondition(BaseModel):
    variable: str
    is_defined: Optional[bool] = Field(default=None)
    equals: Optional[Any] = Field(default=None)
    not_equals: Optional[Any] = Field(default=None)
    greater_than: Optional[Any] = Field(default=None)
    less_than: Optional[Any] = Field(default=None)

    def evaluate(self, context: ExecutionContext) -> bool:
        value = context.get_variable(self.variable)
        res = True
        if self.is_defined is not None:
            res = res and (value is not None) if self.is_defined else (value is None)
        if self.equals is not None:
            equals = value_resolver.resolve(context, self.equals)
            res = res and (value == equals)
        if self.not_equals is not None:
            not_equals = value_resolver.resolve(context, self.not_equals)
            res = res and (value != float(not_equals))
        if self.greater_than is not None:
            greater_than = value_resolver.resolve(context, self.greater_than)
            res = res and (float(value) > float(greater_than))
        if self.less_than is not None:
            less_than  = value_resolver.resolve(context, self.less_than)
            res = res and (float(value) < float(less_than))
        return res

PlaybookTask_ATTRIBUTES = ["name", "action", "output", "when", "map", "tasks", "item_name",'post_process','filters','debug']

class PlaybookTask(BaseModel):
    name: str
    action: str
    output : Optional[str] = Field(default=None)
    when: Optional[list[PlaybookCondition]] = Field(default=[])
    filters : Optional[list[PlaybookCondition]] = Field(default=None)
    # for loops
    flatten: Optional[bool] = Field(default=False)
    map: Optional[str]  = Field(default=None) # on wich variable to map the tasks
    tasks: Optional[list["PlaybookTask"]] = Field(default=None) # nested tasks for loops 
    item_name: Optional[str] = Field(default="item") # name of the variable for each item in the loop
    post_process: Optional[list[dict[str, Any]]] = Field(default=None) # post processing value before store
    debug: Optional[bool] = Field(default=False)

    class Config:
        extra = 'allow'

class PlaybookDict(BaseModel):
    tasks: list[PlaybookTask]
    config: dict[str, Any]

def yaml_playbook_to_dict(yaml_content: str) -> PlaybookDict:
    playbook_dict_not_safe = yaml.safe_load(yaml_content)
    playbook_model = PlaybookDict(**playbook_dict_not_safe)
    return playbook_model

def from_yaml_file(file_path: str) -> PlaybookDict:
    with open(file_path, 'r') as file:
        yaml_content = file.read()
    return yaml_playbook_to_dict(yaml_content)
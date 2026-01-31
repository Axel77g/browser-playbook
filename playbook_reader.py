from typing import Optional
from pydantic import BaseModel, Field
import yaml

from scrapping_playbook_framework.execution_context import ExecutionContext

class PlaybookCondition(BaseModel):
    variable: str
    is_defined: Optional[bool] = Field(default=None)
    equals: Optional[str] = Field(default=None)
    not_equals: Optional[str] = Field(default=None)
    greater_than: Optional[float] = Field(default=None)
    less_than: Optional[float] = Field(default=None)

    def evaluate(self, context: ExecutionContext) -> bool:
        value = context.get_variable(self.variable)
        if self.is_defined is not None:
            return (value is not None) if self.is_defined else (value is None)
        if self.equals is not None:
            return value == self.equals
        if self.not_equals is not None:
            return value != self.not_equals
        if self.greater_than is not None:
            return float(value) > self.greater_than
        if self.less_than is not None:
            return float(value) < self.less_than
        return True

PlaybookTask_ATTRIBUTES = ["name", "action", "output", "when", "map", "tasks", "item_name"]

class PlaybookTask(BaseModel):
    name: str
    action: str
    output : Optional[str] = Field(default=None)
    when: Optional[list[PlaybookCondition]] = Field(default=[])

    # for loops
    map: Optional[str]  = Field(default=None) # on wich variable to map the tasks
    tasks: Optional[list["PlaybookTask"]] = Field(default=None) # nested tasks for loops 
    item_name: Optional[str] = Field(default="item") # name of the variable for each item in the loop

    class Config:
        extra = 'allow'

class PlaybookDict(BaseModel):
    tasks: list[PlaybookTask]

def yaml_playbook_to_dict(yaml_content: str) -> PlaybookDict:
    playbook_dict_not_safe = yaml.safe_load(yaml_content)
    playbook_model = PlaybookDict(**playbook_dict_not_safe)
    return playbook_model

def from_yaml_file(file_path: str) -> PlaybookDict:
    with open(file_path, 'r') as file:
        yaml_content = file.read()
    return yaml_playbook_to_dict(yaml_content)
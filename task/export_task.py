

from abc import abstractmethod
import logging
from typing import Any, TypedDict
from scrapping_playbook_framework.task.task import ScrappingTask
import csv
import os


class ExportTask(ScrappingTask[None]):
    @abstractmethod
    def execute(self, ctx: Any) -> None:
        pass

class ExportParams(TypedDict):
    file_path: str
    variable : str

class CSVExportTask(ExportTask):
    def get_task_action_name(self):
        return "export.csv"

    def execute(self, ctx: ExportParams):
        file_path = ctx["file_path"]
        
        value : Any = ctx[ctx['variable']] # type: ignore
        if not isinstance(value, list) or not all(isinstance(p, dict) for p in value): # type: ignore
            raise Exception(f"Value of variable '{ctx['variable']}' is not a list of dictionaries.")
        value : list[Any, dict] = value # type: ignore
        if len(value) == 0:
            logging.warning(f"Variable '{ctx['variable']}' is empty.")
            return

        # Ensure the directory exists
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        # Get headers that exist in all dictionaries
        if not value:
            return
        
        # Start with the keys of the first item as a base
        headers = set(value[0].keys())
        
        # Find the intersection of keys with all other items
        for item in value[1:]:
            headers.intersection_update(item.keys())

        # Sort headers for consistent column order
        sorted_headers = sorted(list(headers))

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted_headers)
            writer.writeheader()
            # Filter out keys that are not in headers for each row
            cleaned_value = [{k: v for k, v in row.items() if k in sorted_headers} for row in value]
            writer.writerows(cleaned_value)

        print(f"Successfully exported {len(value)} properties to {file_path}")

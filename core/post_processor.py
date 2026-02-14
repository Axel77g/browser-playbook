# task/post_processor.py
from abc import ABC, abstractmethod
from typing import Any
import re

class PostProcessor(ABC):
    @abstractmethod
    def process(self, value: Any) -> Any:
        pass

class RegexExtractProcessor(PostProcessor):
    def __init__(self, pattern: str, group: int = 0):
        self.pattern = re.compile(pattern)
        self.group = group
    
    def process(self, value: Any) -> Any:
        if not isinstance(value, str):
            value = str(value)
        match = self.pattern.search(value)
        if match:
            return match.group(self.group)
        return None

class ReplaceProcessor(PostProcessor):
    def __init__(self, old: str, new: str):
        self.old = old
        self.new = new
    
    def process(self, value: Any) -> Any:
        if not isinstance(value, str):
            value = str(value)
        return value.replace(self.old, self.new)

class CastProcessor(PostProcessor):
    def __init__(self, to: str):
        self.to = to
    
    def process(self, value: Any) -> Any:
        type_map = {
            'int': int,
            'float': float,
            'str': str,
            'bool': bool
        }
        return type_map[self.to](value)

class StripProcessor(PostProcessor):
    def __init__(self, chars: str | None = None):
        self.chars = chars
    
    def process(self, value: Any) -> Any:
        if not isinstance(value, str):
            value = str(value)
        return value.strip(self.chars)

class LowerProcessor(PostProcessor):
    def process(self, value: Any) -> Any:
        if not isinstance(value, str):
            value = str(value)
        return value.lower()

class UpperProcessor(PostProcessor):
    def process(self, value: Any) -> Any:
        if not isinstance(value, str):
            value = str(value)
        return value.upper()

class SplitProcessor(PostProcessor):
    def __init__(self, separator: str, index: int = 0):
        self.separator = separator
        self.index = index
    
    def process(self, value: Any) -> Any:
        if not isinstance(value, str):
            value = str(value)
        parts = value.split(self.separator)
        return parts[self.index]

class SlugifyProcessor(PostProcessor):
    def __init__(self):
        super().__init__()
    def process(self, value : Any) -> Any:
        if not isinstance(value, str):
            value = str(value)
        # Simple slugify implementation
        value = re.sub(r'[^\w\s-]', '', value)
        value = re.sub(r'[-\s]+', '-', value)
        return value.strip('-')

class RegexReplaceProcessor(PostProcessor):
    def __init__(self, pattern: str, replacement: str):
        self.pattern = re.compile(pattern)
        self.replacement = replacement
    
    def process(self, value: Any) -> Any:
        if not isinstance(value, str):
            value = str(value)
        return self.pattern.sub(self.replacement, value)

class ArrayPluckProcessor(PostProcessor):
    def __init__(self, key: str):
        self.key = key

    def process(self, value: list[dict[str, Any]]) -> list[Any]:
        return [item.get(self.key) for item in value if self.key in item]

# Factory pour créer les processors
class PostProcessorFactory:
    @staticmethod
    def create(config: dict[str, Any]) -> PostProcessor:
        processor_type = config.get('type')
        
        if processor_type == 'regex_extract':
            return RegexExtractProcessor(
                pattern=config['pattern'],
                group=config.get('group', 0)
            )
        elif processor_type == 'replace':
            return ReplaceProcessor(
                old=config['old'],
                new=config['new']
            )
        elif processor_type == 'cast':
            return CastProcessor(to=config['to'])
        elif processor_type == 'strip':
            return StripProcessor(chars=config.get('chars', None))
        elif processor_type == 'lower':
            return LowerProcessor()
        elif processor_type == 'upper':
            return UpperProcessor()
        elif processor_type == 'split':
            return SplitProcessor(
                separator=config['separator'],
                index=config.get('index', 0)
            )
        elif processor_type == 'regex_replace':
            return RegexReplaceProcessor(
                pattern=config['pattern'],
                replacement=config['replacement']
            )
        elif processor_type == 'slugify':
            return SlugifyProcessor()
        elif processor_type == 'pluck_array':
            return ArrayPluckProcessor(key=config['key'])
        else:
            raise ValueError(f"Unknown processor type: {processor_type}")
import json
from typing import Optional, Any

from terravacuum.files import PFileLoader

EXTENSION = '.json'


def register_file_loaders() -> tuple[str, PFileLoader]:
    """Function called by the plugin loader to register the file loaders."""
    yield 'json', JsonFileLoader


class JsonFileLoader:
    """Load and save json files."""

    __serializers: list = []

    @staticmethod
    def load_file(filename: str) -> Optional[Any]:
        if not filename.endswith(EXTENSION):
            return

        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def save(filename: str, data: Any) -> bool:
        if not filename.endswith(EXTENSION):
            return False

        with open(filename, 'w') as file:
            file.write(json.dumps(data, default=JsonFileLoader.serialize))
        return True

    @classmethod
    def add_serializer(cls, function):
        cls.__serializers.append(function)

    @classmethod
    def serialize(cls, obj):
        for serializer in cls.__serializers:
            result = serializer(obj)
            if result:
                return result
        return obj

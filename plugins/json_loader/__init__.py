import json
from typing import Optional, Any

from terravacuum import PFileLoader

EXTENSION = '.json'


def register_file_loaders() -> PFileLoader:
    yield JsonFileLoader


class JsonFileLoader:
    """Load and save json files."""

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
            file.write(json.dumps(data))
        return True

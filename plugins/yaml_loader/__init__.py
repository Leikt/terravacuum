import yaml
from typing import Optional, Any

from terravacuum import PFileLoader

EXTENSION = '.yml'

def register_file_loaders() -> PFileLoader:
    yield YamlFileLoader


class YamlFileLoader:
    """Load and save yaml files."""

    @staticmethod
    def load_file(filename: str) -> Optional[Any]:
        if not filename.endswith(EXTENSION):
            return

        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
        return data

    @staticmethod
    def save(filename: str, data: Any) -> bool:
        if not filename.endswith(EXTENSION):
            return False

        with open(filename, 'w') as file:
            file.write(yaml.dump(data))
        return True

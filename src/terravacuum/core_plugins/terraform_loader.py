from typing import Optional, Any

from terravacuum import PFileLoader

EXTENSION = '.tf'


def register_file_loaders() -> PFileLoader:
    """Function called by the plugin loader to register the file loaders."""
    yield YamlFileLoader


class YamlFileLoader:
    """Load and save tf files."""

    @staticmethod
    def load_file(filename: str) -> Optional[Any]:
        if not filename.endswith(EXTENSION):
            return

        with open(filename, 'r') as file:
            data = file.read()
        return data

    @staticmethod
    def save(filename: str, data: Any) -> bool:
        if not filename.endswith(EXTENSION):
            return False

        with open(filename, 'w') as file:
            file.write(data)
        return True

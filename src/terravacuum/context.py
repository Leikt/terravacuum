import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Context:
    data: Any
    variables: dict
    working_directory: str


def create_context(data: Any = None, variables: dict = None, working_directory: str = None) -> Context:
    data = {} if data is None else data
    variables = {} if variables is None else variables
    working_directory = os.getcwd() if data is None else working_directory
    return Context(data, variables, working_directory)

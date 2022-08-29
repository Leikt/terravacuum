import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RenderingContext:
    data: Any
    variables: dict
    working_directory: str


def create_rendering_context(data: Any = None, variables: dict = None, working_directory: str = None,
                             parent: RenderingContext = None) -> RenderingContext:
    if parent is None:
        data = {} if data is None else data
        variables = {} if variables is None else variables
        working_directory = os.getcwd() if working_directory is None else working_directory
    else:
        data = parent.data if data is None else data
        variables = parent.variables if variables is None else variables
        working_directory = parent.working_directory if working_directory is None else working_directory

    return RenderingContext(data, variables, working_directory)
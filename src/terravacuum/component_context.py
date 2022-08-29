import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentContext:
    working_directory: str


def create_rendering_context(working_directory: str = None,
                             parent: ComponentContext = None) -> ComponentContext:
    if parent is None:
        working_directory = os.getcwd() if working_directory is None else working_directory
    else:
        working_directory = parent.working_directory if working_directory is None else working_directory

    return ComponentContext(working_directory)

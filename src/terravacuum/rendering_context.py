import os
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RenderingContext:
    data: Any = field(default_factory=dict)
    variables: dict = field(default_factory=dict)
    working_directory: str = field(default_factory=lambda: os.getcwd())


def create_rendering_context(*_args, **kwargs) -> RenderingContext:
    if kwargs.get('parent') is not None:
        parent = kwargs.get('parent')
        del kwargs['parent']
        kwargs['data'] = kwargs.get('data', parent.data)
        kwargs['variables'] = kwargs.get('variables', parent.variables)
        kwargs['working_directory'] = kwargs.get('working_directory', parent.working_directory)

    return RenderingContext(**kwargs)

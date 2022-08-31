import os
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Context:
    others: dict = field(default_factory=dict)

    def __getitem__(self, item):
        return self.others[item]

    def __setitem__(self, key, value):
        self.others[key] = value


@dataclass(frozen=True)
class ComponentContext(Context):
    working_directory: str = field(default_factory=lambda: os.getcwd())


def create_component_context(*_args, **kwargs) -> ComponentContext:
    parent: ComponentContext = kwargs.get('parent')
    if parent is not None:
        del kwargs['parent']
        kwargs['working_directory'] = kwargs.get('working_directory', parent.working_directory)
        kwargs['others'] = kwargs.get('others', parent.others)

    return ComponentContext(**kwargs)


@dataclass(frozen=True)
class RenderingContext(Context):
    data: Any = field(default_factory=dict)
    variables: dict = field(default_factory=dict)
    working_directory: str = field(default_factory=lambda: os.getcwd())


def create_rendering_context(*_args, **kwargs) -> RenderingContext:
    parent: RenderingContext = kwargs.get('parent')
    if parent is not None:
        del kwargs['parent']
        kwargs['data'] = kwargs.get('data', parent.data)
        kwargs['variables'] = kwargs.get('variables', parent.variables)
        kwargs['working_directory'] = kwargs.get('working_directory', parent.working_directory)
        kwargs['others'] = kwargs.get('others', parent.others)

    return RenderingContext(**kwargs)

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ComponentContext:
    working_directory: str = field(default_factory=lambda : os.getcwd())


def create_component_context(*_args, **kwargs) -> ComponentContext:
    parent: ComponentContext = kwargs.get('parent')
    if parent is not None:
        del kwargs['parent']
        kwargs['working_directory'] = kwargs.get('working_directory', parent.working_directory)

    return ComponentContext(**kwargs)

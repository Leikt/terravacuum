from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Context:
    """Describe a context passed from an object to another."""
    others: dict = field(default_factory=dict)

    def __getitem__(self, item):
        return self.others[item]

    def __setitem__(self, key, value):
        self.others[key] = value


@dataclass(frozen=True)
class ComponentContext(Context):
    pass


def create_component_context(*_args, **kwargs) -> ComponentContext:
    """Create a component context from the given information."""
    parent: ComponentContext = kwargs.get('parent')
    if parent is not None:
        del kwargs['parent']
        kwargs['others'] = kwargs.get('others', parent.others.copy())

    return ComponentContext(**kwargs)


@dataclass(frozen=True)
class RenderingContext(Context):
    data: Any = field(default_factory=dict)
    variables: dict = field(default_factory=dict)


def create_rendering_context(*_args, **kwargs) -> RenderingContext:
    """Create a rendering context from the given information."""
    parent: RenderingContext = kwargs.get('parent')
    if parent is not None:
        del kwargs['parent']
        kwargs['data'] = kwargs.get('data', parent.data)
        kwargs['variables'] = kwargs.get('variables', parent.variables)
        kwargs['others'] = kwargs.get('others', parent.others.copy())

    return RenderingContext(**kwargs)

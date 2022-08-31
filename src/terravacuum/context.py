from dataclasses import dataclass


@dataclass(frozen=True)
class Context(dict):
    """Describe a context passed from an object to another."""


def create_context(parent: Context = None, **kwargs) -> Context:
    """Create a context that inherit from the parent if its given. Kwargs overwrite existing data."""
    context = Context()
    if parent:
        for k, v in parent.items():
            context[k] = kwargs.get(k, v)
    for k, v in kwargs.items():
        context[k] = v
    return context

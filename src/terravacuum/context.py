class FrozenContextError(Exception):
    """Exception raised when the program tries to modify a Context."""


class Context(dict):
    """Describe a context passed from an object to another."""

    def __setitem__(self, key, value):
        raise FrozenContextError('You cannot modify a context.')


def create_context(parent: Context = None, **kwargs) -> Context:
    """Create a context that inherit from the parent if its given. Kwargs overwrite existing data."""
    values = {}
    if parent:
        for k, v in parent.items():
            values[k] = kwargs.get(k, v)
    for k, v in kwargs.items():
        values[k] = v
    context = Context()
    context.update(values)
    return context

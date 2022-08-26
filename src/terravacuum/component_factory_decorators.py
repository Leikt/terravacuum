from typing import Any

from .component_factory import WrongArgumentForComponentConstructor
from .component import PComponent, ComponentPluginSocket


def component_factory(parse_string: bool = False):
    """Decorator that create the concrete component from the returned data"""

    def decorator(function):
        def wrapper(data, *args, **kwargs) -> PComponent:
            data = _parse_string_data(parse_string, data)
            keyword, data = function(data, *args, **kwargs)
            return _create_component(keyword, data)

        return wrapper

    return decorator


def _parse_string_data(parse_string: bool, data: Any):
    if not parse_string:
        return data
    if not isinstance(data, str):
        return data
    # TODO: parse the string to a dict or list
    return data


def _create_component(keyword: str, data: dict) -> PComponent:
    klass = ComponentPluginSocket.get_component_class(keyword)
    try:
        component = klass(**data)
        return component
    except TypeError:
        raise WrongArgumentForComponentConstructor(klass)

import re
from typing import Any

from .component_factory import WrongArgumentForComponentConstructor, get_component_factory
from .component import PComponent, ComponentPluginSocket


class WrongDataTypeError(Exception):
    """Exception raised when the data hase the wrong type."""

    def __init__(self, expected: type, actual: type):
        self.expected_type = expected
        self.actual_type = actual
        self.message = f"Wrong data type.\nExpected type: {expected.__name__}\nActual: {actual.__name__}"
        super().__init__(self.message)


class MissingChildrenDataError(Exception):
    """Exception raised when the factory generate children but there is no "children" key inside the template data."""

    def __init__(self):
        super().__init__('"children" key is missing from the template data.')


class TooManyChildComponents(Exception):
    """Exception raised when a child has the wrong number of keyword."""

    def __init__(self, children_name: list[str]):
        self.children_name = children_name
        self.message = f'Expected a single key in the dict (got {len(children_name)} [{", ".join(children_name)}])'
        super().__init__(self.message)


def component_factory(inline_arguments: bool = False, create_children: bool = False):
    """Decorator that create the concrete component from the returned data"""

    def decorator(function):
        def wrapper(data, *args, **kwargs) -> PComponent:
            if inline_arguments:
                data = _parse_string_arguments(data)
            if create_children:
                data = _create_children(data)
            keyword, data = function(data, *args, **kwargs)
            return _create_component(keyword, data)

        return wrapper

    return decorator


def create_child(data: dict) -> PComponent:
    """Helper function to create a child component."""
    if not isinstance(data, dict):
        raise WrongDataTypeError(dict, type(data))
    if len(data) != 1:
        raise TooManyChildComponents(list(data.keys()))
    keyword = list(data.keys())[0]
    factory = get_component_factory(keyword)
    return factory(data[keyword])


def _create_component(keyword: str, data: dict) -> PComponent:
    klass = ComponentPluginSocket.get_component_class(keyword)
    try:
        component: PComponent = klass(**data)
        return component
    except TypeError:
        raise WrongArgumentForComponentConstructor(klass)


INLINE_STRING_REGEX = r'([\w]+)=([^ "]+|".*?[^\\]")'


def _parse_string_arguments(data: Any) -> Any:
    if not isinstance(data, str):
        return data
    # TODO: check syntax
    matches = re.findall(INLINE_STRING_REGEX, data)
    data = {m[0]: m[1] for m in matches}
    return data


def _create_children(data: dict) -> dict:
    if not isinstance(data, dict):
        raise WrongDataTypeError(dict, type(data))
    if 'children' not in data:
        raise MissingChildrenDataError()
    children: list[PComponent] = []
    for child_data in data['children']:
        children.append(create_child(child_data))
    data['children'] = children
    return data

import re
from enum import Enum
from typing import Any

from .component import PComponent, ComponentPluginSocket
from .component_factory import WrongArgumentForComponentConstructor, get_component_factory


class WrongDataTypeError(Exception):
    """Exception raised when the data hase the wrong type."""

    def __init__(self, expected: str, actual: type):
        self.expected_type = expected
        self.actual_type = actual
        self.message = f"Wrong data type.\nExpected type: {expected}\nActual: {actual.__name__}"
        super().__init__(self.message)


class MissingChildrenDataError(Exception):
    """Exception raised when the factory generate children but there is no "children" key inside the template data."""

    def __init__(self, children_key: str):
        super().__init__(f'"{children_key}" key is missing from the template data.')


class TooManyChildComponents(Exception):
    """Exception raised when a child has the wrong number of keyword."""

    def __init__(self, children_name: list[str]):
        self.children_name = children_name
        self.message = f'Expected a single key in the dict (got {len(children_name)} [{", ".join(children_name)}])'
        super().__init__(self.message)


class WrongInlineArgument(Exception):
    """Exception raised when the inline argument is not valid."""

    def __init__(self, argument: str):
        self.argument = argument
        self.message = f"Wrong inline argument: '{argument}'"
        super().__init__(self.message)


class Inline(Enum):
    DICT = 'dict'
    SINGLE = 'single'
    LIST = 'list'


def create_component(data: dict) -> PComponent:
    """Helper function to create a child component."""
    if not isinstance(data, dict):
        raise WrongDataTypeError("dict", type(data))
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


INLINE_STRING_REGEX = r'(\w+)=(")?(.*?[^\\])(?(2)"|(?: |$))'


def _parse_string_dict(data: Any) -> Any:
    if not isinstance(data, str):
        return data
    matches = re.findall(INLINE_STRING_REGEX, data)
    if len(matches) == 0:
        return None
    data = {m[0]: m[2].replace(r'\"', '"') for m in matches}
    return data


def create_children(data: list[dict]) -> list[PComponent]:
    if not isinstance(data, list):
        raise WrongDataTypeError("list", type(data))
    children: list[PComponent] = []
    for child_data in data:
        children.append(create_component(child_data))
    return children


def _process_inline(inline: list[Inline], data) -> Any:
    if not isinstance(data, str):
        return data

    if Inline.DICT in inline:
        parsed_dict = _parse_string_dict(data)
        if parsed_dict is not None:
            return parsed_dict

    if Inline.LIST in inline:
        pass

    if Inline.SINGLE in inline:
        return data

    raise WrongInlineArgument(data)


def _check_data_type(data, accepted: list[type] = None):
    if accepted is None:
        accepted = [dict, list, str]
    for typ in accepted:
        if isinstance(data, typ):
            return
    raise WrongDataTypeError("[dict, list, str]", type(data))


def component_factory(inline: list[Inline] = None, children: bool = False, children_key: str = 'children'):
    """Decorator that create the concrete component from the returned data"""

    def decorator(function):
        def wrapper(data, *args, **kwargs) -> PComponent:
            _check_data_type(data)
            if inline:
                data = _process_inline(inline, data)
            if children and children_key in data:
                data[children_key] = create_children(data[children_key])
            keyword, data = function(data, *args, **kwargs)
            return _create_component(keyword, data)

        return wrapper

    return decorator

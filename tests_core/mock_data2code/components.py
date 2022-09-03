from dataclasses import dataclass
from typing import Union

from terravacuum.component import ComponentFactoryRegistration, ComponentRegistration, ComponentFactoryReturn, Inline, \
    component_factory, get_component_factory
from terravacuum.context import Context


def register_component_factories() -> ComponentFactoryRegistration:
    yield 'm2d-header', factory_function_header
    yield 'm2d-line', factory_code_line
    yield 'm2d-function', factory_function


def register_components() -> ComponentRegistration:
    yield 'm2d-header', FunctionHeaderComponent
    yield 'm2d-line', CodeLineComponent
    yield 'm2d-function', FunctionComponent


@component_factory(inline=[Inline.SINGLE])
def factory_function_header(_context: Context, data: Union[str, dict]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        data = {'name': data}
    return 'm2d-header', data


@component_factory(inline=[Inline.SINGLE])
def factory_code_line(_context: Context, data: Union[dict, str, list]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        data = {'code': [data]}
    if isinstance(data, list):
        data = {'code': data}
    return 'm2d-line', data


@component_factory(children=True, children_key='lines')
def factory_function(context: Context, data: dict):
    header_factory = get_component_factory('m2d-header')
    header = header_factory(context, data['header'])
    line_factory = get_component_factory('m2d-line')
    quick_lines = [line_factory(context, line) for line in data['quick_lines']]
    final_lines = data['lines'] + quick_lines
    return 'm2d-function', {'header': header, 'lines': final_lines}


@dataclass
class FunctionHeaderComponent:
    name: str
    renderer: str = 'm2d-header'


@dataclass
class CodeLineComponent:
    code: list[str]
    renderer: str = 'm2d-line'


@dataclass
class FunctionComponent:
    header: FunctionHeaderComponent
    lines: list[CodeLineComponent]
    renderer: str = 'm2d-function'

from dataclasses import dataclass
from typing import Union

from terravacuum import ComponentFactoryRegistration, ComponentRegistration, ComponentFactoryReturn, component_factory, \
    get_component_factory, Inline, Context


def register_component_factories() -> ComponentFactoryRegistration:
    yield 'function_header', factory_function_header
    yield 'code_line', factory_code_line
    yield 'function', factory_function


def register_components() -> ComponentRegistration:
    yield 'function_header', FunctionHeaderComponent
    yield 'code_line', CodeLineComponent
    yield 'function', FunctionComponent


@component_factory(inline=[Inline.SINGLE])
def factory_function_header(_context: Context, data: Union[str, dict]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        data = {'name': data}
    return 'function_header', data


@component_factory(inline=[Inline.SINGLE])
def factory_code_line(_context: Context, data: Union[dict, str, list]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        data = {'code': [data]}
    if isinstance(data, list):
        data = {'code': data}
    return 'code_line', data


@component_factory(children=True, children_key='lines')
def factory_function(context: Context, data: dict):
    header_factory = get_component_factory('function_header')
    header = header_factory(context, data['header'])
    line_factory = get_component_factory('code_line')
    quick_lines = [line_factory(context, line) for line in data['quick_lines']]
    final_lines = data['lines'] + quick_lines
    return 'function', {'header': header, 'lines': final_lines}


@dataclass
class FunctionHeaderComponent:
    name: str

    def get_renderer_name(self) -> str:
        return 'function_header'


@dataclass
class CodeLineComponent:
    code: list[str]

    def get_renderer_name(self) -> str:
        return 'code_line'


@dataclass
class FunctionComponent:
    header: FunctionHeaderComponent
    lines: list[CodeLineComponent]

    def get_renderer_name(self) -> str:
        return 'function'

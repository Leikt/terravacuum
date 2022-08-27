from dataclasses import dataclass

from terravacuum import ComponentFactoryRegistration, ComponentRegistration, ComponentFactoryReturn, component_factory, \
    get_component_factory


def register_component_factories() -> ComponentFactoryRegistration:
    yield 'function_header', factory_function_header
    yield 'code_line', factory_code_line
    yield 'function', factory_function


def register_components() -> ComponentRegistration:
    yield 'function_header', FunctionHeaderComponent
    yield 'code_line', CodeLineComponent
    yield 'function', FunctionComponent


@component_factory(inline_arguments=True)
def factory_function_header(data: dict) -> ComponentFactoryReturn:
    return 'function_header', data


@component_factory(inline_arguments=True)
def factory_code_line(data: dict) -> ComponentFactoryReturn:
    return 'code_line', data


@component_factory(create_children=True, children_key='lines')
def factory_function(data: dict):
    header_factory = get_component_factory('function_header')
    header = header_factory(data['header'])
    data = {'header': header, 'lines': data['lines']}
    return 'function', data


@dataclass
class FunctionHeaderComponent:
    name: str

    def get_renderer_name(self) -> str:
        return 'function_header'


@dataclass
class CodeLineComponent:
    code: str

    def get_renderer_name(self) -> str:
        return 'code_line'


@dataclass
class FunctionComponent:
    header: FunctionHeaderComponent
    lines: list[CodeLineComponent]

    def get_renderer_name(self) -> str:
        return 'function'

from typing import Union

from terravacuum import ComponentFactoryRegistration, component_factory, Inline, ComponentFactoryReturn, \
    get_component_factory


def register_component_factories() -> ComponentFactoryRegistration:
    # yield 'project', factory_project
    # yield 'module', factory_module
    yield 'section', factory_section
    yield 'header', factory_header
    yield 'property', factory_property
    # yield 'loop', factory_loop
    # yield 'include', factory_include
    yield 'comment', factory_comment
    yield 'blank_lines', factory_blank_lines


@component_factory(inline=[Inline.SINGLE])
def factory_comment(data: Union[list, str, dict]) -> ComponentFactoryReturn:
    if isinstance(data, list):
        data = {'comments': data}
    if isinstance(data, str):
        data = {'comments': [data]}
    return 'comment', data


@component_factory(inline=[Inline.SINGLE])
def factory_blank_lines(data: Union[dict, str]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        data = {'count': int(data)}
    return 'blank_lines', data


@component_factory(inline=[Inline.DICT])
def factory_property(data: dict) -> ComponentFactoryReturn:
    return 'property', data


@component_factory(inline=[Inline.SINGLE])
def factory_header(data: Union[dict, str]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        data = {'keyword': data}
    return 'header', data


@component_factory(children=True)
def factory_section(data: dict) -> ComponentFactoryReturn:
    header_factory = get_component_factory('header')
    data['header'] = header_factory(data['header'])
    return 'section', data

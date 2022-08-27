from typing import Union

from terravacuum import ComponentFactoryRegistration, component_factory, Inline, ComponentFactoryReturn


def register_component_factories() -> ComponentFactoryRegistration:
    # yield 'project', factory_project
    # yield 'module', factory_module
    # yield 'section', factory_section
    # yield 'property', factory_property
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

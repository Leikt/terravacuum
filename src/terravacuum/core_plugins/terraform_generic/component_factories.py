from typing import Union

from terravacuum import ComponentFactoryRegistration, component_factory, Inline, ComponentFactoryReturn, \
    get_component_factory, load_file, create_children, Context


def register_component_factories() -> ComponentFactoryRegistration:
    """Function called by the plugin loader to register the factories."""
    yield 'project', factory_project
    # yield 'module', factory_module
    yield 'file', factory_file
    yield 'section', factory_section
    yield 'header', factory_header
    yield 'property', factory_property
    yield 'loop', factory_loop
    yield 'include', factory_include
    yield 'comment', factory_comment
    yield 'blank_lines', factory_blank_lines


@component_factory(inline=[Inline.SINGLE])
def factory_comment(_context: Context, data: Union[list, str, dict]) -> ComponentFactoryReturn:
    if isinstance(data, list):
        data = {'comments': data}
    if isinstance(data, str):
        data = {'comments': [data]}
    return 'comment', data


@component_factory(inline=[Inline.SINGLE])
def factory_blank_lines(_context: Context, data: Union[dict, str]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        data = {'count': int(data)}
    return 'blank_lines', data


@component_factory(inline=[Inline.DICT])
def factory_property(_context: Context, data: dict) -> ComponentFactoryReturn:
    return 'property', data


@component_factory(inline=[Inline.SINGLE])
def factory_header(_context: Context, data: Union[dict, str]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        data = {'keyword': data}
    return 'header', data


@component_factory(children=True)
def factory_section(context: Context, data: dict) -> ComponentFactoryReturn:
    header_factory = get_component_factory('header')
    data['header'] = header_factory(context, data['header'])
    return 'section', data


@component_factory(children=True)
def factory_loop(_context: Context, data: dict) -> ComponentFactoryReturn:
    return 'loop', data


@component_factory(inline=[Inline.SINGLE])
def factory_include(context: Context, data: Union[dict, str]) -> ComponentFactoryReturn:
    source = data['source'] if isinstance(data, dict) else data
    children_data = load_file(source)
    if not isinstance(children_data, list):
        children_data = [children_data]

    children = create_children(context, children_data)
    return 'container', {'children': children}


@component_factory(children=True)
def factory_file(_context: Context, data: dict) -> ComponentFactoryReturn:
    return 'file', data


@component_factory(children=True)
def factory_project(_context: Context, data: dict) -> ComponentFactoryReturn:
    return 'project', data

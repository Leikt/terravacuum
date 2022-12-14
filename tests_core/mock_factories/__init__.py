from dataclasses import dataclass
from typing import Union

from terravacuum.component import ComponentRegistration, ComponentFactoryRegistration, ComponentFactoryReturn, \
    get_component_factory, component_factory, Inline, PComponent
from terravacuum.context import Context


def register_component_factories() -> ComponentFactoryRegistration:
    yield 'mock', fabric_mock_component
    yield 'mocks', fabric_mock_parent_component
    yield 'mock_auto_children', fabric_mock_auto_children
    yield 'mock_with_inline_arguments', fabric_mock_with_inline
    yield 'mock_with_inline_dict', fabric_mock_with_inline_dict


def register_components() -> ComponentRegistration:
    yield 'mocker', MockComponent
    yield 'mocker_parent', MockParentComponent
    yield 'mock_with_children', MockWithChildrenComponent


@component_factory()
def fabric_mock_component(_context: Context, data: dict) -> ComponentFactoryReturn:
    return 'mocker', data


@component_factory()
def fabric_mock_parent_component(context: Context, data: dict) -> ComponentFactoryReturn:
    mock_factory = get_component_factory('mock')
    child = mock_factory(context, data['mock_child'])
    data = {
        'destination': data['destination'],
        'child': child
    }
    return 'mocker_parent', data


@component_factory(children=True)
def fabric_mock_auto_children(_context: Context, data: dict) -> ComponentFactoryReturn:
    return 'mock_with_children', data


@component_factory(inline=[Inline.DICT, Inline.SINGLE])
def fabric_mock_with_inline(_context: Context, data: Union[dict, str]) -> ComponentFactoryReturn:
    if isinstance(data, str):
        first_name, last_name = data.split(' ')
        data = {'name': last_name, 'first_name': first_name}
    return 'mocker', data


@component_factory(inline=[Inline.DICT])
def fabric_mock_with_inline_dict(_context: Context, data: dict):
    return 'mocker', data


@dataclass
class MockComponent:
    name: str
    first_name: str
    renderer: str = 'mock'


@dataclass
class MockParentComponent:
    destination: str
    child: PComponent
    renderer: str = 'mock_parent'


@dataclass
class MockWithChildrenComponent:
    children: list[PComponent]
    renderer: str = 'mock_with_children'

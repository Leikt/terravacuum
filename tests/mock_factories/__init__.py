from dataclasses import dataclass

from terravacuum import ComponentFactoryRegistration, ComponentRegistration, component_factory, ComponentFactoryReturn, \
    PComponent, get_component_factory


def register_component_factories() -> ComponentFactoryRegistration:
    yield 'mock', fabric_mock_component
    yield 'mocks', fabric_mock_parent_component
    yield 'mock_auto_children', fabric_mock_auto_children
    yield 'mock_with_inline_arguments', fabric_mock_with_inline


def register_components() -> ComponentRegistration:
    yield 'mocker', MockComponent
    yield 'mocker_parent', MockParentComponent
    yield 'mock_with_children', MockWithChildrenComponent


@component_factory()
def fabric_mock_component(data: dict) -> ComponentFactoryReturn:
    return 'mocker', data


@component_factory()
def fabric_mock_parent_component(data: dict) -> ComponentFactoryReturn:
    mock_factory = get_component_factory('mock')
    child = mock_factory(data['mock_child'])
    data = {
        'destination': data['destination'],
        'child': child
    }
    return 'mocker_parent', data


@component_factory(create_children=True)
def fabric_mock_auto_children(data: dict) -> ComponentFactoryReturn:
    return 'mock_with_children', data


@component_factory(inline_arguments=True)
def fabric_mock_with_inline(data: dict) -> ComponentFactoryReturn:
    return 'mocker', data


@dataclass
class MockComponent:
    name: str
    first_name: str


@dataclass
class MockParentComponent:
    destination: str
    child: PComponent


@dataclass
class MockWithChildrenComponent:
    children: list[PComponent]

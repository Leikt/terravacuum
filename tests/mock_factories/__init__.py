from dataclasses import dataclass

from terravacuum import ComponentFactoryRegistration, ComponentRegistration, component_factory, ComponentFactoryReturn


def register_component_factories() -> ComponentFactoryRegistration:
    yield 'mock', fabric_mock_component


def register_components() -> ComponentRegistration:
    yield 'mocker', MockComponent


@component_factory(parse_string=False)
def fabric_mock_component(data: dict) -> ComponentFactoryReturn:
    return 'mocker', data


@dataclass
class MockComponent:
    name: str
    first_name: str

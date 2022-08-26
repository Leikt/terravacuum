from dataclasses import dataclass
from typing import Union, Optional

from terravacuum import PComponent, ComponentFactoryRegistration


def register_component_factories() -> ComponentFactoryRegistration:
    yield 'mock', fabric_mock_component


def fabric_mock_component(data: Optional[Union[str, list, dict]]) -> PComponent:
    if not isinstance(data, dict):
        raise TypeError("MockComponent only accept data as a dict.")
    return MockComponent(**data)


@dataclass
class MockComponent:
    name: str
    first_name: str

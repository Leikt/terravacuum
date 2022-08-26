import logging
from typing import Protocol, Optional, Callable, Union


class ComponentFactoryNotFound(Exception):
    """Exception raised when a component factory is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No component factory is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


class PComponent(Protocol):
    """A component of the template, it is able to process data to a renderer"""


ComponentFactory = Callable[[Optional[Union[str, list, dict]]], PComponent]
"""Function that create a component from the template data."""

ComponentFactoryRegistration = tuple[str, ComponentFactory]
"""Return type for the registration function"""


class ComponentFactoryPluginSocket:
    """Plugin socket for the file loading."""

    __factories: dict[str, ComponentFactory] = {}

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_component_factories'):
            return
        for keyword, factory in module.register_component_factories():
            if keyword in cls.__factories:
                logging.warning('A component factory is already registered on keyword "{}"'.format(keyword))
                continue

            cls.__factories[keyword] = factory

    @classmethod
    def get_factory(cls, keyword: str) -> ComponentFactory:
        if keyword not in cls.__factories:
            raise ComponentFactoryNotFound(keyword)
        return cls.__factories[keyword]


def create_component(keyword: str, data: Optional[Union[str, list, dict]]) -> PComponent:
    """Collect the data from the given source. A plugin must be registered to this source."""
    return ComponentFactoryPluginSocket.get_factory(keyword)(data)

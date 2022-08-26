import logging
from typing import Optional, Callable, Union

from .component import PComponent


class ComponentFactoryNotFound(Exception):
    """Exception raised when a component factory is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No component factory is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


class WrongArgumentForComponentConstructor(Exception):
    """Exception raised when the wrong arguments are passed to a component constructor."""

    def __init__(self, component_class: type):
        self.component_class = component_class
        self.message = 'Wrong arguments for the component constructor "{}"'.format(component_class)
        super().__init__(self.message)


ComponentFactory = Callable[[Optional[Union[str, list, dict]]], PComponent]
"""Function that create a component from the template data."""

ComponentFactoryRegistration = tuple[str, ComponentFactory]
"""Return type for the registration function"""

ComponentFactoryReturn = tuple[str, dict]
"""Return type when the function uses the component_factory decorator"""


class ComponentFactoryPluginSocket:
    """Plugin socket for the component factories."""

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


def get_component_factory(keyword: str) -> ComponentFactory:
    """Retrieve the component factory associated with the given keyword. Raise a ComponentFactoryNotFound error if
    it's missing."""
    return ComponentFactoryPluginSocket.get_factory(keyword)


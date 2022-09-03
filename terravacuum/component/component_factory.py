from typing import Optional, Callable, Union

from .component import PComponent
from ..context import Context
from ..plugin_system import PluginLoader, PluginItemNotFoundError


class ComponentFactoryNotFound(PluginItemNotFoundError):
    """Exception raised when a component factory is requested but not found."""


class WrongArgumentForComponentConstructor(Exception):
    """Exception raised when the wrong arguments are passed to a component constructor."""

    def __init__(self, component_class: type):
        self.component_class = component_class
        self.message = 'Wrong arguments for the component constructor "{}"'.format(component_class)
        super().__init__(self.message)


ComponentFactory = Callable[[Context, Optional[Union[str, list, dict]]], PComponent]
"""Function that create a component from the template data."""

ComponentFactoryRegistration = tuple[str, ComponentFactory]
"""Return type for the registration function"""

ComponentFactoryReturn = tuple[str, dict]
"""Return type when the function uses the component_factory decorator"""


def get_component_factory(keyword: str) -> ComponentFactory:
    """Retrieve the component factory associated with the given keyword. Raise a ComponentFactoryNotFound error if
    it's missing."""
    return PluginLoader.get('component_factory')[keyword]

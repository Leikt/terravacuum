import logging
from typing import Protocol


class ComponentNotFound(Exception):
    """Exception raised when a component is requested but not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = 'No component is registered to the keyword "{}"'.format(keyword)
        super().__init__(self.message)


class PComponent(Protocol):
    """A component of the template, it is able to process data to a renderer"""

    def get_renderer_name(self) -> str:
        """Return the name of the component's renderer."""


ComponentRegistration = tuple[str, type]


class ComponentPluginSocket:
    """Plugin socket for the components."""

    __components: dict[str, type] = {}

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_components'):
            return
        for keyword, factory in module.register_components():
            if keyword in cls.__components:
                logging.warning('A component factory is already registered on keyword "{}"'.format(keyword))
                continue

            cls.__components[keyword] = factory

    @classmethod
    def get_component_class(cls, keyword: str) -> type:
        if keyword not in cls.__components:
            raise ComponentNotFound(keyword)
        return cls.__components[keyword]


def get_component_class(keyword: str) -> type:
    """Get the component associated with the given keyword. Raise a ComponentNotFound if it's missing"""
    return ComponentPluginSocket.get_component_class(keyword)

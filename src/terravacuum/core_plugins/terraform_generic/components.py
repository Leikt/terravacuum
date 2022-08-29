from dataclasses import dataclass, field
from typing import Union

from terravacuum import ComponentRegistration, PComponent


def register_components() -> ComponentRegistration:
    # yield 'project', InfraComponent
    # yield 'module', ModuleComponent
    yield 'file', FileComponent
    yield 'section', SectionComponent
    yield 'header', HeaderComponent
    yield 'property', PropertyComponent
    yield 'loop', LoopComponent
    yield 'container', ContainerComponent
    yield 'comment', CommentComponent
    yield 'blank_lines', BlankLinesComponent


@dataclass
class CommentComponent:
    """Component containing comments."""
    comments: list[str]

    def get_renderer_name(self) -> str:
        return "comment"


@dataclass
class BlankLinesComponent:
    """Component representing blank lines."""
    count: int = 1

    def get_renderer_name(self) -> str:
        return "blank_lines"


@dataclass
class PropertyComponent:
    """Component that represent a property"""
    name: str
    value: str

    def get_renderer_name(self) -> str:
        return "property"


@dataclass
class HeaderComponent:
    """Component that represent the header of a section"""
    keyword: str
    parameters: list[str] = field(default_factory=list)
    is_property: bool = False

    def get_renderer_name(self) -> str:
        return "header"


@dataclass
class SectionComponent:
    """Component that represent a section with a header and children."""
    header: HeaderComponent
    children: list[PropertyComponent]

    def get_renderer_name(self) -> str:
        return 'section'


@dataclass
class LoopComponent:
    """Component that represent a loop iteration."""
    through: Union[str, list]
    children: list[PComponent]

    def get_renderer_name(self) -> str:
        return 'loop'


@dataclass
class ContainerComponent:
    """Component that represent a component that only contains other components."""
    children: list[PComponent]

    def get_renderer_name(self) -> str:
        return 'container'


@dataclass
class FileComponent:
    destination: str
    children: list[PComponent]

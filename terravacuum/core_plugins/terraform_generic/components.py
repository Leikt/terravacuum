from dataclasses import dataclass, field
from typing import Union

from terravacuum.component import PComponent, ComponentRegistration


def register_components() -> ComponentRegistration:
    """Function called by the plugin loader to register the components."""
    yield 'project', ProjectComponent
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
    renderer: str = 'comment'


@dataclass
class BlankLinesComponent:
    """Component representing blank lines."""
    count: int = 1
    renderer: str = 'blank_lines'


@dataclass
class PropertyComponent:
    """Component that represent a property"""
    name: str
    value: str
    renderer: str = 'property'


@dataclass
class HeaderComponent:
    """Component that represent the header of a section"""
    keyword: str
    parameters: list[str] = field(default_factory=list)
    is_property: bool = False
    renderer: str = 'header'


@dataclass
class SectionComponent:
    """Component that represent a section with a header and children."""
    header: HeaderComponent
    children: list[PropertyComponent]
    renderer: str = 'section'


@dataclass
class LoopComponent:
    """Component that represent a loop iteration."""
    through: Union[str, list]
    children: list[PComponent]
    renderer: str = 'loop'


@dataclass
class ContainerComponent:
    """Component that represent a component that only contains other components."""
    children: list[PComponent]
    renderer: str = 'container'


@dataclass
class FileComponent:
    destination: str
    children: list[PComponent]
    renderer: str = 'file'


@dataclass
class ProjectComponent:
    directory: str
    children: list[PComponent]
    renderer: str = 'project'

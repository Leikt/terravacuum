from dataclasses import dataclass, field

from terravacuum import ComponentRegistration


def register_components() -> ComponentRegistration:
    # yield 'project', InfraComponent
    # yield 'module', ModuleComponent
    # yield 'section', SectionComponent
    yield 'header', HeaderComponent
    yield 'property', PropertyComponent
    # yield 'loop', LoopComponent
    # yield 'include', IncludeComponent
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
        return "blank_line"


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

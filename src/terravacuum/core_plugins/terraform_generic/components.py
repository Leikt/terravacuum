from dataclasses import dataclass

from terravacuum import ComponentRegistration


def register_components() -> ComponentRegistration:
    # yield 'project', InfraComponent
    # yield 'module', ModuleComponent
    # yield 'section', SectionComponent
    # yield 'header', HeaderComponent
    # yield 'property', PropertyComponent
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

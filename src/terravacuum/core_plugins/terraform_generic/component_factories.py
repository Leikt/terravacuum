from typing import Union

from terravacuum import ComponentFactoryRegistration, component_factory, PComponent
from .components import CommentComponent, BlankLinesComponent


def register_component_factories() -> ComponentFactoryRegistration:
    # yield 'project', factory_project
    # yield 'module', factory_module
    # yield 'section', factory_section
    # yield 'property', factory_property
    # yield 'loop', factory_loop
    # yield 'include', factory_include
    yield 'comment', factory_comment
    yield 'blank_lines', factory_blank_lines


@component_factory(inline_arguments=True)
def factory_comment(comments: Union[list, str]) -> PComponent:
    if not isinstance(comments, list):
        comments = [comments]
    return CommentComponent(comments)


@component_factory(inline_arguments=True)
def factory_blank_lines(count: int) -> PComponent:
    return BlankLinesComponent(count)

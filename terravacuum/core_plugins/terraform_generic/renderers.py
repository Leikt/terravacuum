from typing import Any

from .components import BlankLinesComponent, CommentComponent, PropertyComponent, HeaderComponent, SectionComponent, \
    LoopComponent, ContainerComponent, FileComponent, ProjectComponent
from terravacuum.rendering import RendererRegistration, get_renderer, render_components
from terravacuum.files import save_to_file, change_working_directory
from terravacuum.context import create_context, Context
from terravacuum.expression_parsing import parse_expression
from terravacuum.component import PComponent


def register_renderers() -> RendererRegistration:
    """Function called by the plugin loader to register the renderers."""
    yield 'comment', render_comment
    yield 'blank_lines', render_blank_lines
    yield 'property', render_property
    yield 'header', render_header
    yield 'section', render_section
    yield 'loop', render_loop
    yield 'container', render_container
    yield 'file', render_file
    yield 'project', render_project


class DataTypeError(Exception):
    """Exception raised when the data type does not match the requirements."""

    def __init__(self, expected_type, data, original_data):
        self.expected_type = expected_type
        self.data = data
        self.original_data = original_data
        self.message = f"Wrong data type for the expression {original_data}. Expect {expected_type}. Got {type(data)}"
        super().__init__(self.message)


def tab(context: Context) -> str:
    return '\t' * context.get('indentation', 0)


def render_comment(context: Context, component: PComponent) -> str:
    component: CommentComponent
    lines = []
    for comment_template in component.comments:
        comment = parse_expression(comment_template, context)
        line = '{}# {}'.format(tab(context), comment)
        lines.append(line)
    return '\n'.join(lines) + '\n'


def render_blank_lines(context: Context, component: PComponent) -> str:
    component: BlankLinesComponent
    return f'{tab(context)}\n' * component.count


def render_property(context: Context, component: PComponent) -> str:
    component: PropertyComponent
    name = parse_expression(component.name, context, quote_string_with_spaces=True)
    value = parse_expression(component.value, context, quote_string_with_spaces=True)
    return f"{tab(context)}{name} = {value}\n"


def render_header(context: Context, component: PComponent) -> str:
    component: HeaderComponent
    keyword = parse_expression(component.keyword, context, quote_string_with_spaces=True)
    parameters = " ".join([f'"{parse_expression(param, context)}"' for param in component.parameters])
    separator = ' ' if len(parameters) > 0 else ''
    sign = ' =' if component.is_property else ''
    end = ' {\n'
    return f"{tab(context)}{keyword}{separator}{parameters}{sign}{end}"


def render_section(context: Context, component: PComponent) -> str:
    component: SectionComponent
    header_renderer = get_renderer(component.header.renderer)

    children_context = create_context(context, indentation=context.get('indentation', 0) + 1)
    content = [
        header_renderer(context, component.header),
        ''.join(render_components(children_context, component.children)),
        tab(context) + "}\n"
    ]
    return ''.join(content)


def _get_loop_data(context: Context, original_data: Any) -> list:
    data = original_data
    if isinstance(data, str):
        data = parse_expression(data, context)
    if not isinstance(data, list):
        raise DataTypeError('list', data, original_data)
    return data


def render_loop(context: Context, component: PComponent) -> str:
    component: LoopComponent
    data = _get_loop_data(context, component.through)
    content = []
    for d in data:
        child_context = create_context(parent=context, data=d)
        content.append(''.join(render_components(child_context, component.children)))
    return ''.join(content)


def render_container(context: Context, component: PComponent) -> str:
    component: ContainerComponent
    return ''.join(render_components(context, component.children))


def render_file(context: Context, component: PComponent) -> str:
    component: FileComponent
    destination = parse_expression(component.destination, context)
    result = ''.join(render_components(context, component.children))
    save_to_file(destination, result)
    return ''


def render_project(context: Context, component: PComponent) -> str:
    component: ProjectComponent
    with change_working_directory(component.directory):
        render_components(context, component.children)
    return ''

from dataclasses import dataclass
from typing import Any

from terravacuum import RendererRegistration, PComponent, Context, tab, parse_expression, get_renderer_class, \
    create_context, save_to_file, render_components
from .components import BlankLinesComponent, CommentComponent, PropertyComponent, HeaderComponent, SectionComponent, \
    LoopComponent, ContainerComponent, FileComponent, ProjectComponent


def register_renderers() -> RendererRegistration:
    yield 'comment', CommentRenderer
    yield 'blank_lines', BlankLinesRenderer
    yield 'property', PropertyRenderer
    yield 'header', HeaderRenderer
    yield 'section', SectionRenderer
    yield 'loop', LoopRenderer
    yield 'container', ContainerRenderer
    yield 'file', FileRenderer
    yield 'project', ProjectRenderer


class DataTypeError(Exception):
    """Exception raised when the data type does not match the requirements."""

    def __init__(self, expected_type, data, original_data):
        self.expected_type = expected_type
        self.data = data
        self.original_data = original_data
        self.message = f"Wrong data type for the expression {original_data}. Expect {expected_type}. Got {type(data)}"
        super().__init__(self.message)


@dataclass
class CodeRenderer:
    """Base class of the generic renderers. Provide some helpers."""
    indentation: int = 0

    @property
    def indent(self) -> str:
        return tab(self.indentation)


class CommentRenderer(CodeRenderer):
    """Render comment lines."""

    def render(self, context: Context, component: PComponent) -> str:
        component: CommentComponent
        lines = []
        for comment_template in component.comments:
            comment = parse_expression(comment_template, context)
            line = '{}# {}'.format(self.indent, comment)
            lines.append(line)
        return '\n'.join(lines) + '\n'


class BlankLinesRenderer(CodeRenderer):
    """Render blank lines."""

    def render(self, _context: Context, component: PComponent) -> str:
        component: BlankLinesComponent
        return f'{self.indent}\n' * component.count


class PropertyRenderer(CodeRenderer):
    """Render a terraform property."""

    def render(self, context: Context, component: PComponent) -> str:
        component: PropertyComponent
        name = parse_expression(component.name, context, quote_string_with_spaces=True)
        value = parse_expression(component.value, context, quote_string_with_spaces=True)
        return f"{self.indent}{name} = {value}\n"


class HeaderRenderer(CodeRenderer):
    """Render a section header."""

    def render(self, context: Context, component: PComponent) -> str:
        component: HeaderComponent
        keyword = parse_expression(component.keyword, context, quote_string_with_spaces=True)
        parameters = " ".join([f'"{parse_expression(param, context)}"' for param in component.parameters])
        separator = ' ' if len(parameters) > 0 else ''
        sign = ' =' if component.is_property else ''
        end = ' {\n'
        return f"{self.indent}{keyword}{separator}{parameters}{sign}{end}"


class SectionRenderer(CodeRenderer):
    """Render a complete section."""

    def render(self, context: Context, component: PComponent) -> str:
        component: SectionComponent
        header_renderer_c = get_renderer_class(component.header.get_renderer_name())
        header = header_renderer_c(self.indentation)

        content = [
            header.render(context, component.header),
            render_components(context, component.children, self.indentation + 1),
            self.indent + "}\n"
        ]
        return ''.join(content)


class LoopRenderer(CodeRenderer):
    """Loop through the given data and render all the children for each data."""

    @staticmethod
    def initialize_data_loop(context: Context, original_data: Any) -> list:
        data = original_data
        if isinstance(data, str):
            data = parse_expression(data, context)
        if not isinstance(data, list):
            raise DataTypeError('list', data, original_data)
        return data

    def render(self, context: Context, component: PComponent) -> str:
        component: LoopComponent
        data = self.initialize_data_loop(context, component.through)
        content = []
        for d in data:
            child_context = create_context(d, context.variables)
            content.append(render_components(child_context, component.children, self.indentation))
        return ''.join(content)


class ContainerRenderer(CodeRenderer):
    """Render the children of the component"""

    def render(self, context: Context, component: PComponent) -> str:
        component: ContainerComponent
        return render_components(context, component.children, self.indentation)


class FileRenderer(CodeRenderer):
    """Render the children and store it to a file."""

    def render(self, context: Context, component: PComponent) -> str:
        component: FileComponent
        result = render_components(context, component.children, self.indentation)
        destination = parse_expression(component.destination, context)
        save_to_file(destination, result)
        return ''


class ProjectRenderer(CodeRenderer):
    """Render the children inside the directory."""

    def render(self, context: Context, component: PComponent) -> str:
        component: ProjectComponent
        render_components(context, component.children, 0)
        return ''

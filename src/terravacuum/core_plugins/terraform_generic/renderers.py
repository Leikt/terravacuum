from dataclasses import dataclass
from typing import Any

from terravacuum import RendererRegistration, PComponent, Context, tab, parse_expression, get_renderer_class, \
    create_context
from .components import BlankLinesComponent, CommentComponent, PropertyComponent, HeaderComponent, SectionComponent, \
    LoopComponent


def register_renderers() -> RendererRegistration:
    yield 'comment', CommentRenderer
    yield 'blank_lines', BlankLinesRenderer
    yield 'property', PropertyRenderer
    yield 'header', HeaderRenderer
    yield 'section', SectionRenderer
    yield 'loop', LoopRenderer


class DataTypeError(Exception):
    def __init__(self, expected_type, data, original_data):
        self.expected_type = expected_type
        self.data = data
        self.original_data = original_data
        self.message = f"Wrong data type for the expression {original_data}. Expect {expected_type}. Got {type(data)}"
        super().__init__(self.message)


@dataclass
class CodeRenderer:
    indentation: int = 0

    @property
    def indent(self) -> str:
        return tab(self.indentation)


class CommentRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: CommentComponent
        lines = []
        for comment_template in component.comments:
            comment = parse_expression(comment_template, context)
            line = '{}# {}'.format(self.indent, comment)
            lines.append(line)
        return '\n'.join(lines) + '\n'


class BlankLinesRenderer(CodeRenderer):
    def render(self, _context: Context, component: PComponent) -> str:
        component: BlankLinesComponent
        return f'{self.indent}\n' * component.count


class PropertyRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: PropertyComponent
        name = parse_expression(component.name, context, quote_string_with_spaces=True)
        value = parse_expression(component.value, context, quote_string_with_spaces=True)
        return f"{self.indent}{name} = {value}\n"


class HeaderRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: HeaderComponent
        keyword = parse_expression(component.keyword, context, quote_string_with_spaces=True)
        parameters = " ".join([f'"{parse_expression(param, context)}"' for param in component.parameters])
        separator = ' ' if len(parameters) > 0 else ''
        sign = ' =' if component.is_property else ''
        end = ' {\n'
        return f"{self.indent}{keyword}{separator}{parameters}{sign}{end}"


class SectionRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: SectionComponent

        header_renderer_c = get_renderer_class(component.header.get_renderer_name())
        header = header_renderer_c(self.indentation).render(context, component.header)

        children = []
        for child_component in component.children:
            child_renderer_c = get_renderer_class(child_component.get_renderer_name())
            child = child_renderer_c(self.indentation + 1).render(context, child_component)
            children.append(child)

        end = self.indent + "}\n"

        return header + ''.join(children) + end


class LoopRenderer(CodeRenderer):
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
            for child in component.children:
                renderer_c = get_renderer_class(child.get_renderer_name())
                renderer = renderer_c(self.indentation)
                content.append(renderer.render(child_context, child))
        return ''.join(content)

from dataclasses import dataclass

from terravacuum import RendererRegistration, PComponent, Context, tab, parse_expression
from .components import BlankLinesComponent, CommentComponent, PropertyComponent, HeaderComponent


def register_renderers() -> RendererRegistration:
    yield 'comment', CommentRenderer
    yield 'blank_lines', BlankLinesRenderer
    yield 'property', PropertyRenderer
    yield 'header', HeaderRenderer


@dataclass
class CodeRenderer:
    _indent: int = 0

    @property
    def indent(self) -> str:
        return tab(self._indent)


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

from dataclasses import dataclass

from terravacuum import RendererRegistration, PComponent, Context, tab, parse_expression
from .components import BlankLinesComponent, CommentComponent, PropertyComponent


def register_renderers() -> RendererRegistration:
    yield 'comment', CommentRenderer
    yield 'blank_lines', BlankLinesRenderer
    yield 'property', PropertyRenderer


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
        return '{}\n'.format(self.indent) * component.count


class PropertyRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: PropertyComponent
        name = parse_expression(component.name, context, quote_string_with_spaces=True)
        value = parse_expression(component.value, context, quote_string_with_spaces=True)
        return "{}{} = {}\n".format(self.indent, name, value)

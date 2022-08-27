from dataclasses import dataclass

from terravacuum import RendererRegistration, PComponent, Context, tab, parse_expression
from .components import BlankLinesComponent, CommentComponent


def register_renderers() -> RendererRegistration:
    yield 'comment', CommentRenderer
    yield 'blank_lines', BlankLinesRenderer


@dataclass
class CodeRenderer:
    indent: int = 0


class CommentRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: CommentComponent
        lines = []
        for comment_template in component.comments:
            comment = parse_expression(comment_template, context)
            line = '{}# {}'.format(tab(self.indent), comment)
            lines.append(line)
        return '\n'.join(lines) + '\n'


class BlankLinesRenderer(CodeRenderer):
    def render(self, _context: Context, component: PComponent) -> str:
        component: BlankLinesComponent
        return '\n' * component.count

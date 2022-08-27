from dataclasses import dataclass
from typing import Callable

from mock_data2code.components import FunctionHeaderComponent, CodeLineComponent, FunctionComponent
from terravacuum import RendererRegistration, Context, PComponent, parse_expression, get_renderer_class, \
    RendererFactoryRegistration


def register_renderers() -> RendererRegistration:
    yield 'function', FunctionRenderer
    yield 'code_line', CodeLineRenderer
    yield 'function_header', FunctionHeaderRenderer


def register_renderer_factories() -> RendererFactoryRegistration:
    yield 'function', factory_function_renderer


def tab(count: int):
    return '\t' * count


@dataclass
class CodeRenderer:
    indent: int = 0


CodeRendererClass = Callable[[int], CodeRenderer]


class FunctionHeaderRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: FunctionHeaderComponent
        name = parse_expression(component.name, context)
        return "{}function {}() {}".format(tab(self.indent), name, '{')


class CodeLineRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: CodeLineComponent
        lines = []
        for code_line in component.code:
            line = parse_expression(code_line, context)
            lines.append("{}{}".format(tab(self.indent), line))
        return '\n'.join(lines)


class FunctionRenderer(CodeRenderer):
    def render(self, context: Context, component: PComponent) -> str:
        component: FunctionComponent
        header = self.render_header(context, component.header)

        lines = [header]
        for line_component in component.lines:
            lines.append(self.render_line(context, line_component))
        lines.append('{}{}'.format(tab(self.indent), '}'))
        return "\n".join(lines)

    def render_header(self, context: Context, header_component: FunctionHeaderComponent) -> str:
        header_renderer_c = get_renderer_class(header_component.get_renderer_name())  # type: ignore
        header_renderer = header_renderer_c(self.indent)
        return header_renderer.render(context, header_component)

    def render_line(self, context: Context, line_component: CodeLineComponent) -> str:
        line_renderer_c = get_renderer_class(line_component.get_renderer_name())
        line_renderer = line_renderer_c(self.indent + 1)
        return line_renderer.render(context, line_component)


def factory_function_renderer(indent: int = 0) -> FunctionRenderer:
    return FunctionRenderer(indent)

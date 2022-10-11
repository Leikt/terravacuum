from mock_data2code.components import FunctionHeaderComponent, CodeLineComponent, FunctionComponent

from terravacuum.rendering import RendererRegistration, get_renderer
from terravacuum.context import Context, create_context
from terravacuum.component import PComponent
from terravacuum.expression_parsing import parse_expression


def register_renderers() -> RendererRegistration:
    yield 'm2d-function', render_function
    yield 'm2d-line', render_code_line
    yield 'm2d-header', render_function_header


def tab(context: Context):
    return '\t' * context.get('indentation', 0)


def render_function_header(context: Context, component: PComponent) -> str:
    component: FunctionHeaderComponent
    name = parse_expression(component.name, context)
    return "{}function {}() {}".format(tab(context), name, '{')


def render_code_line(context: Context, component: PComponent) -> str:
    component: CodeLineComponent
    lines = []
    for code_line in component.code:
        line = parse_expression(code_line, context)
        lines.append("{}{}".format(tab(context), line))
    return '\n'.join(lines)


def render_function(context: Context, component: PComponent) -> str:
    component: FunctionComponent
    header_renderer = get_renderer(component.header.renderer)

    header = header_renderer(context, component.header)  # type: ignore
    line_context = create_context(context, indentation=context.get('indentation', 0) + 1)
    lines = [header]
    for line_component in component.lines:
        line_renderer = get_renderer(line_component.renderer)
        lines.append(line_renderer(line_context, line_component))  # type: ignore
    lines.append('{}{}'.format(tab(context), '}'))
    return "\n".join(lines)

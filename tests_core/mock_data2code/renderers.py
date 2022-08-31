from mock_data2code.components import FunctionHeaderComponent, CodeLineComponent, FunctionComponent
from terravacuum import RendererRegistration, Context, PComponent, parse_expression, get_renderer, create_context


def register_renderers() -> RendererRegistration:
    yield 'm2d-function', render_function
    yield 'm2d-line', render_code_line
    yield 'm2d-header', render_function_header


#
# def register_renderer_factories() -> RendererFactoryRegistration:
#     yield 'function', factory_function_renderer


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
    header_renderer = get_renderer('m2d-header')
    line_renderer = get_renderer('m2d-line')

    header = header_renderer(context, component.header)
    line_context = create_context(context, indentation=context.get('indentation', 0) + 1)
    lines = [header]
    for line_component in component.lines:
        lines.append(line_renderer(line_context, line_component))
    lines.append('{}{}'.format(tab(context), '}'))
    return "\n".join(lines)

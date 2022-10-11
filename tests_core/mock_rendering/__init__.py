from mock_factories import MockComponent, MockParentComponent
from terravacuum.context import Context
from terravacuum.component import PComponent
from terravacuum.rendering import get_renderer, RendererRegistration
from terravacuum.expression_parsing import parse_expression


def register_renderers() -> RendererRegistration:
    yield 'mock_simple', render_mock_no_expr
    yield 'mock', render_mock_with_expr
    yield 'mock_parent', render_mock_parent


def render_mock_no_expr(_context: Context, component: PComponent) -> str:
    component: MockComponent
    return "Mock[last_name='{}' first_name='{}']".format(component.name, component.first_name)


def render_mock_with_expr(context: Context, component: PComponent) -> str:
    component: MockComponent
    last_name = parse_expression(component.name, context)
    first_name = parse_expression(component.first_name, context)
    return "Mock[last_name='{}' first_name='{}']".format(last_name, first_name)


def render_mock_parent(context: Context, component: PComponent) -> str:
    component: MockParentComponent
    destination = parse_expression(component.destination, context)
    child_renderer = get_renderer(component.child.renderer)
    child_render = child_renderer(context, component.child)
    return "\n".join([
        "mock_parent '{}' ".format(destination) + "{",
        "\t{}".format(child_render),
        "}"
    ])

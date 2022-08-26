from mock_factories import MockComponent
from terravacuum import Renderer, Context, parse_expression


def register_renderers() -> Renderer:
    yield 'mock', render_mock
    yield 'mock_with_expression', render_mock_with_expressions


def render_mock(_context: Context, component: MockComponent) -> str:
    return f"mock_component[name = {component.name} first_name = {component.first_name}]"


def render_mock_with_expressions(context: Context, component: MockComponent) -> str:
    name = parse_expression(component.name, context)
    first_name = parse_expression(component.first_name, context)
    return f"mock_component[name = {name} first_name = {first_name}]"

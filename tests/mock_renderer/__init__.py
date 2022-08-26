from mock_factories import MockComponent
from terravacuum import Context, parse_expression, RendererFactory, TAB, BRACKET_OP, BRACKET_CL, PRenderer, PComponent


def register_renderers() -> tuple[str, type]:
    yield 'mock', MockRenderer
    yield 'mock_with_expression', MockExpressionRenderer


def register_renderer_factories() -> tuple[str, RendererFactory]:
    yield 'mock', factory_root


def factory_root() -> PRenderer:
    return MockRenderer(0)  # type: ignore


class MockRenderer:
    def __init__(self, indent: int = 0):
        self.indent = indent

    def render(self, _context: Context, component: MockComponent) -> str:
        return f"{TAB * self.indent}mock_component {BRACKET_OP} name = {component.name} \
first_name = {component.first_name} {BRACKET_CL}"


class MockExpressionRenderer:
    def __init__(self, indent: int = 0):
        self.indent = indent

    def render(self, context: Context, component: PComponent) -> str:
        component: MockComponent
        name = parse_expression(component.name, context)
        first_name = parse_expression(component.first_name, context)
        return f"{TAB * self.indent}mock_component {BRACKET_OP} name = {name} \
first_name = {first_name} {BRACKET_CL}"

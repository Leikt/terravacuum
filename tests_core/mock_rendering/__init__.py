from mock_factories import MockComponent, MockParentComponent
from terravacuum import RenderingContext, PComponent, parse_expression, get_renderer_class
from terravacuum import RendererRegistration


def register_renderers() -> RendererRegistration:
    yield 'mock_simple', MockRendererNoExpression
    yield 'mock', MockRendererWithExpression
    yield 'mock_parent', MockParentRenderer


class MockRendererNoExpression:
    def render(self, _context: RenderingContext, component: PComponent) -> str:
        component: MockComponent
        return "Mock[last_name='{}' first_name='{}']".format(component.name, component.first_name)


class MockRendererWithExpression:
    def render(self, context: RenderingContext, component: PComponent) -> str:
        component: MockComponent
        last_name = parse_expression(component.name, context)
        first_name = parse_expression(component.first_name, context)
        return "Mock[last_name='{}' first_name='{}']".format(last_name, first_name)


class MockParentRenderer:
    def render(self, context: RenderingContext, component: PComponent) -> str:
        component: MockParentComponent
        destination = parse_expression(component.destination, context)
        child_factory = get_renderer_class(component.child.get_renderer_name())
        child = child_factory()
        child_render = child.render(context, component.child)
        return "\n".join([
            "mock_parent '{}' ".format(destination) + "{",
            "\t{}".format(child_render),
            "}"
        ])

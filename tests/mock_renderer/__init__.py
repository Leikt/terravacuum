from mock_factories import MockComponent
from terravacuum import Renderer, Context


def register_renderers() -> Renderer:
    yield 'mock', render_mock


def render_mock(context: Context, component: MockComponent) -> str:
    return "mock_component {\n" + f"\tname = {component.name}\n" + f"\tfirst_name = {component.first_name}\n" + '}'

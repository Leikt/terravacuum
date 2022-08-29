from terravacuum import PComponent, get_renderer_class, RenderingContext


def tab(count: int) -> str:
    return '\t' * count


def render_components(context: RenderingContext, components: list[PComponent], *args, **kwargs) -> str:
    content = []
    for component in components:
        renderer_c = get_renderer_class(component.get_renderer_name())
        renderer = renderer_c(*args, **kwargs)
        content.append(renderer.render(context, component))
    return ''.join(content)



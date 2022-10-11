def register_plugin_sockets():
    from .component import ComponentNotFound, ComponentFactoryNotFound
    from .rendering import RendererNotFound
    from .plugin_system import PluginLoader

    """Register the core plugin sockets. Call this before loading any plugin."""
    PluginLoader.register_plugin_socket('component', 'register_components', ComponentNotFound)
    PluginLoader.register_plugin_socket('component_factory', 'register_component_factories', ComponentFactoryNotFound)
    PluginLoader.register_plugin_socket('renderer', 'register_renderers', RendererNotFound)
    PluginLoader.register_plugin_socket('file_loader', 'register_file_loaders')
    PluginLoader.register_plugin_socket('expression_parser', 'register_expression_parsers')

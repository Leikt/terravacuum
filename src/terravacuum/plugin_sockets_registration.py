def register_plugin_sockets():
    """Initialize the plugin sockets. Call this before loading any plugin."""
    from .plugin_loader import PluginLoader

    from .file_loader import FileLoaderPluginSocket
    PluginLoader.register_plugin_socket(FileLoaderPluginSocket)

    from .expression_parsing import ExpressionParserPluginSocket
    PluginLoader.register_plugin_socket(ExpressionParserPluginSocket)

    from .data_collector import DataCollectorPluginSocket
    PluginLoader.register_plugin_socket(DataCollectorPluginSocket)

    from .component_factory import ComponentFactoryPluginSocket
    PluginLoader.register_plugin_socket(ComponentFactoryPluginSocket)

    from .component import ComponentPluginSocket
    PluginLoader.register_plugin_socket(ComponentPluginSocket)

    from .renderer import RendererPluginSocket
    PluginLoader.register_plugin_socket(RendererPluginSocket)

    from .renderer_factory import RendererFactoryPluginSocket
    PluginLoader.register_plugin_socket(RendererFactoryPluginSocket)

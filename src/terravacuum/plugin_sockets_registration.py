def register_plugin_sockets():
    """Initialize the plugin sockets. Please call this before loading any plugin."""
    from .plugin_loader import PluginLoader

    from .file_loader import FileLoaderPluginSocket
    PluginLoader.register_plugin_socket(FileLoaderPluginSocket)

    from .expression_parsing import ExpressionParserPluginSocket
    PluginLoader.register_plugin_socket(ExpressionParserPluginSocket)

    from .data_collector import DataCollectorPluginSocket
    PluginLoader.register_plugin_socket(DataCollectorPluginSocket)

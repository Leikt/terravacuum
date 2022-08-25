def register_plugin_sockets():
    from .plugin_loader import PluginLoader

    from .file_loader import FileLoaderPluginSocket
    PluginLoader.register_plugin_socket(FileLoaderPluginSocket)

    from .expression_parsing import ExpressionParserPluginSocket
    PluginLoader.register_plugin_socket(ExpressionParserPluginSocket)

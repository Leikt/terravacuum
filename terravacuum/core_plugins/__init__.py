from terravacuum import PluginLoader, register_plugin_sockets


def register_core_plugins():
    PluginLoader.load_plugin('terravacuum.core_plugins.expression_parser')
    PluginLoader.load_plugin('terravacuum.core_plugins.json_loader')
    PluginLoader.load_plugin('terravacuum.core_plugins.yaml_loader')
    PluginLoader.load_plugin('terravacuum.core_plugins.terraform_loader')
    PluginLoader.load_plugin('terravacuum.core_plugins.terraform_generic')


def initialize():
    register_plugin_sockets()
    register_core_plugins()

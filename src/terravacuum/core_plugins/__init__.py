from terravacuum import PluginLoader


def register_core_plugins():
    PluginLoader.load_plugin('terravacuum.core_plugins.expression_parser')
    PluginLoader.load_plugin('terravacuum.core_plugins.json_loader')
    PluginLoader.load_plugin('terravacuum.core_plugins.yaml_loader')
    # PluginLoader.load_plugin('terravacuum.core_plugins.terraform_generic')
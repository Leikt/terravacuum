# Import standalone modules
from .plugin_system import PluginLoader, PluginSocket, PluginItemNotFoundError
from .context import create_context, Context, FrozenContextError

# Import modules with plugin sockets
from .file_loader import PFileLoader, load_file, save_to_file, change_working_directory
from .expression_parsing import PExpressionParser, parse_expression, ExpressionParsingResult

# Import component related
from .component_factory import ComponentFactory, ComponentFactoryNotFound, PComponent, get_component_factory, \
    ComponentFactoryRegistration, ComponentFactoryReturn, WrongArgumentForComponentConstructor
from .component import ComponentNotFound, PComponent, get_component_class, ComponentRegistration
from .component_factory_helpers import component_factory, WrongDataTypeError, MissingChildrenDataError, \
    TooManyChildComponents, create_component, WrongInlineArgument, Inline, create_children

# Import renderers
from .renderer import Renderer, RendererNotFound, get_renderer, RendererRegistration
from .renderer_helpers import render_components


def register_plugin_sockets():
    PluginLoader.register_plugin_socket('component', 'register_components', ComponentNotFound)
    PluginLoader.register_plugin_socket('component_factory', 'register_component_factories', ComponentFactoryNotFound)
    PluginLoader.register_plugin_socket('renderer', 'register_renderers', RendererNotFound)
    PluginLoader.register_plugin_socket('file_loader', 'register_file_loaders')
    PluginLoader.register_plugin_socket('expression_parser', 'register_expression_parsers')

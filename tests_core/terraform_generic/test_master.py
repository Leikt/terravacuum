import os.path
import shutil
import unittest

from terravacuum import register_plugin_sockets
from terravacuum.context import create_context
from terravacuum.rendering import get_renderer
from terravacuum.component import create_component
from terravacuum.files import load_file, change_working_directory
from terravacuum.core_plugins import register_core_plugins


class TestMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        register_core_plugins()
        if os.path.isdir('data_tests/master_render'):
            shutil.rmtree('data_tests/master_render')

    def _load(self):
        template = load_file('data_tests/master/main.yml')
        data = load_file('data_tests/master/data.json')
        variables = load_file('data_tests/master/variables.json')

        ctx_rendering = create_context(data=data, variables=variables)
        ctx_component = create_context()
        return template, ctx_rendering, ctx_component

    def test_master_components(self):
        template, ctx_rendering, ctx_component = self._load()

        with change_working_directory('data_tests/master/'):
            create_component(ctx_component, template)

    def test_master_rendering(self):
        template, ctx_rendering, ctx_component = self._load()
        with change_working_directory('data_tests/master/'):
            component = create_component(ctx_component, template)

        renderer = get_renderer(component.renderer)
        with change_working_directory('data_tests/'):
            renderer(ctx_rendering, component)


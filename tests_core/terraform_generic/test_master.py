import os.path
import shutil
import unittest

from terravacuum import register_core_plugins, load_file, create_component, get_renderer_class, \
    create_component_context, create_rendering_context, change_working_directory


class TestMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_core_plugins()
        if os.path.isdir('data_tests/master_render'):
            shutil.rmtree('data_tests/master_render')

    def _load(self):
        template = load_file('data_tests/master/main.yml')
        data = load_file('data_tests/master/data.json')
        variables = load_file('data_tests/master/variables.json')

        ctx_rendering = create_rendering_context(data=data, variables=variables)
        ctx_component = create_component_context()
        return template, ctx_rendering, ctx_component

    def test_master_components(self):
        template, ctx_rendering, ctx_component = self._load()

        with change_working_directory('data_tests/master/'):
            create_component(ctx_component, template)

    def test_master_rendering(self):
        template, ctx_rendering, ctx_component = self._load()
        with change_working_directory('data_tests/master/'):
            component = create_component(ctx_component, template)

        renderer = get_renderer_class(component.get_renderer_name())()
        with change_working_directory('data_tests/'):
            renderer.render(ctx_rendering, component)


# import unittest
#
# from terravacuum import register_core_plugins, load_file, create_component, get_renderer_class, create_context
#
#
# class TestMaster(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         register_core_plugins()
#
#     def test_master(self):
#         template = load_file('data_tests/master/main.yml')
#         component = create_component(template)
#         renderer = get_renderer_class(component.get_renderer_name())()
#
#         data = load_file('data_tests/master/data.json')
#         variables = {}
#         context = create_context(data, variables)
#
#         renderer.render(context, component)

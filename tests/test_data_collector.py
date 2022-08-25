import unittest

from terravacuum import register_plugin_sockets, PluginLoader, collect_data, DataCollectorNotFoundError


class TestDataCollector(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        register_plugin_sockets()
        PluginLoader.load_plugin('mock_data_collector')

    def test_mock_data_collector(self):
        data = collect_data('mock')
        self.assertEqual('mock data', data['mock'])

    def test_data_collector_not_found(self):
        with self.assertRaises(DataCollectorNotFoundError):
            collect_data('unknown_source')
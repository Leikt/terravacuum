from typing import Optional, Any

from terravacuum import PDataCollector


def register_data_collectors() -> PDataCollector:
    yield 'mock', MockDataCollector


class MockDataCollector:
    @staticmethod
    def collect() -> Optional[Any]:
        return {'mock': 'mock data'}

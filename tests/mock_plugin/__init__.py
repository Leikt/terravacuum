from dataclasses import dataclass


@dataclass
class Mock:
    value: int = 0


def register_mock() -> Mock:
    yield Mock(12)
    yield Mock(52)
    yield Mock(366)


class MockSocket:
    __plugins: list[Mock] = []

    @classmethod
    def register(cls, module):
        if not hasattr(module, 'register_mock'):
            return
        for mock in module.register_mock():
            cls.__plugins.append(mock)

    @classmethod
    def each(cls):
        return [mock.value for mock in cls.__plugins]

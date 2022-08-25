from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Context:
    data: Any
    variables: dict = field(default_factory=dict)


def create_context(data: Any, variables: dict) -> Context:
    return Context(data, variables)

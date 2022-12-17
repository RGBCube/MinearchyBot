from __future__ import annotations

__all__ = ("override",)

from typing import Callable, TypeVar

T = TypeVar("T", bound=Callable)


def override(function: T) -> T:
    """Basically Java's @Override annotation. Makes stuff less ambiguous."""
    return function

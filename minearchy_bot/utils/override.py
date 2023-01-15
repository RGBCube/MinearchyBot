from __future__ import annotations

__all__ = ("override",)

from typing import Callable, TypeVar

T = TypeVar("T", bound = Callable)


def override(function: T) -> T:
    """Basically Javas @Override annotation. Makes stuff less ambiguous."""
    return function

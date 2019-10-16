import abc
from typing import Type


class Entity(metaclass=abc.ABCMeta):
    """
    Example of usage:

    >>> from dataclasses import dataclass, is_dataclass
    >>> from app.core import entities
    >>>
    >>> @dataclass
    ... class Foo:
    ...     bar: int = 1
    ...     baz: str = ''
    >>>
    >>> entities.register(Foo)

    >>> # it's steel dataclass
    >>> is_dataclass(Foo)
    True
    >>> # the instance is steel a dataclass
    >>> is_dataclass(Foo(bar=123, baz='hello'))
    True
    >>> # mro still works
    >>> isinstance(Foo(bar=123, baz='hello'), Foo)
    True
    >>> # it's an instance of entity
    >>> isinstance(Foo(bar=123, baz='hello'), Entity)
    True
    """
    pass


def register(class_: Type) -> None:
    Entity.register(class_)

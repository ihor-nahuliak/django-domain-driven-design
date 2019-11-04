import abc
import dataclasses


class _DataclassMeta(abc.ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        # pylint: disable=bad-mcs-classmethod-argument
        if bases:
            raise TypeError('Dataclass can not be inherited.')
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        return cls

    def __subclasscheck__(cls, subclass):
        is_subclass = dataclasses.is_dataclass(subclass)
        return is_subclass

    def __instancecheck__(cls, instance):
        is_instance = dataclasses.is_dataclass(type(instance))
        return is_instance


class Dataclass(metaclass=_DataclassMeta):
    """
    Abstract type for all dataclasses.
    It can't be inherited, it's the same like
        dataclasses.is_dataclass(t) method:

    >>> @dataclasses.dataclass
    ... class Foo(Dataclass):
    ...     x: int
    ...     y: str = ''
    >>>
    TypeError: Dataclass can not be inherited.

    >>> @dataclasses.dataclass
    ... class Foo:
    ...     x: int
    ...     y: str = ''
    >>>
    >>> issubclass(Foo, Dataclass)
    True
    >>> foo = Foo(x=1, y='test')
    >>> isinstance(foo, Dataclass) and isinstance(foo, Foo)
    True

    Dataclasses inheritance still works:

    >>> @dataclasses.dataclass
    ... class Bar(Foo):
    ...     z: bool = False
    >>>
    >>> issubclass(Bar, Dataclass) and issubclass(Bar, Foo)
    True
    >>> issubclass(Foo, Bar)
    False
    >>> bar = Bar(x=1, y='test', z=True)
    >>> (isinstance(bar, Dataclass) and
    ...      isinstance(bar, Foo) and
    ...      isinstance(bar, Bar))
    True
    >>> isinstance(foo, Bar)
    False

    """

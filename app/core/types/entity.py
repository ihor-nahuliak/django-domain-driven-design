import dataclasses

from app.core.types._bunch import bunch


class _EntityMeta(type):
    """
    Entity duck typing metaclass.
    """

    def __subclasscheck__(cls, subclass):
        if not dataclasses.is_dataclass(subclass):
            return False
        class_fields_set = cls._get_dataclass_fields_set(cls)
        subclass_fields_set = cls._get_dataclass_fields_set(subclass)
        is_subclass = class_fields_set.issubset(subclass_fields_set)
        return is_subclass

    def __instancecheck__(cls, instance):
        is_instance = cls.__subclasscheck__(type(instance))
        return is_instance

    @classmethod
    def _get_dataclass_fields_set(cls, dataclass):
        fields_set = {(f.name, f.type, f.default)
                      for f in dataclasses.fields(dataclass)}
        return fields_set


@dataclasses.dataclass
class Entity(metaclass=_EntityMeta):
    """
    Abstract type for all entities.
    It can not be inherited. (Nota bene!)

    >>> @dataclasses.dataclass
    ... class Foo(Entity):
    ...     x: int = 0
    ...     y: str = ''
    ...
    Traceback (most recent call last):
    ...
    TypeError: Entity class can not be inherited.

    Any dataclass that you make and
    that contains id fielf can be used as entity:

    >>> @dataclasses.dataclass
    ... class Foo:
    ...     id: int
    ...     x: int = 0
    ...     y: str = ''
    ...
    >>> issubclass(Foo, Entity)
    True
    >>> foo = Foo(id=1, x=123, y='test')
    >>> isinstance(foo, Entity) and isinstance(foo, Foo)
    True

    Dataclasses inheritance still works:

    >>> @dataclasses.dataclass
    ... class Bar(Foo):
    ...     z: bool = False
    ...
    >>> issubclass(Bar, Entity) and issubclass(Bar, Foo)
    True
    >>> issubclass(Foo, Bar)
    False
    >>> bar = Bar(id=1, x=123, y='test', z=True)
    >>> (isinstance(bar, Entity) and
    ...      isinstance(bar, Foo) and
    ...      isinstance(bar, Bar))
    True
    >>> isinstance(foo, Bar)
    False

    Duck typing also works:

    >>> @dataclasses.dataclass
    ... class Baz:
    ...     id: int
    ...     x: int = 0
    ...     y: str = ''
    ...     z: bool = False
    ...
    >>> issubclass(Baz, Entity) and issubclass(Baz, Foo)
    True
    >>> issubclass(Foo, Baz)
    False
    >>> baz = Baz(id=1, x=123, y='test', z=True)
    >>> (isinstance(baz, Entity) and
    ...      isinstance(baz, Foo) and
    ...      isinstance(baz, Baz))
    True
    >>> isinstance(foo, Baz)
    False

    """


class ParaEntity(bunch):
    """
    Partial entity like class.
    Example of usage:

    >>> item = ParaEntity(id=1, username='test')
    >>> item.id
    1
    >>> item.username
    'test'
    >>> item.first_name is dataclasses.MISSING
    True

    """

    @classmethod
    def __missing__(cls, name):
        return dataclasses.MISSING

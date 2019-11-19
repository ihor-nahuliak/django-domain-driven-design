import dataclasses
from collections import OrderedDict
from typing import Any, Dict, Generic, Hashable, Iterator, TypeVar

from django.utils.decorators import classproperty


_EntityT = TypeVar('_EntityT')


@dataclasses.dataclass(frozen=False)
class Entity(Generic[_EntityT], Dict[str, Any]):
    id: Hashable

    @classproperty
    def __fields__(cls):
        fields_tuple = dataclasses.fields(cls)
        dict_class = cls._get_dict_factory()
        fields_dict = dict_class((f.name, f) for f in fields_tuple)
        return fields_dict

    @classproperty
    def __field_names__(cls) -> Iterator[str]:
        field_names = iter(cls.__fields__.keys())
        return field_names

    @classmethod
    def _get_dict_factory(cls):
        is_ordered = cls.__dataclass_params__.order
        dict_class = OrderedDict if is_ordered else dict
        return dict_class

    @classmethod
    def _assert_key_exists(cls, key: str):
        if key not in cls.__field_names__:
            raise KeyError(f'{cls.__name__} has no field {key}')

    def __getitem__(self, key: str) -> Any:
        self._assert_key_exists(key)
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._assert_key_exists(key)
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        self._assert_key_exists(key)
        field = self.__fields__[key]
        if field.default is dataclasses.MISSING:
            raise TypeError(f'{self.__class__.__name__}.{key} is required')
        setattr(self, key, field.default)

    def pop(self, key: str, *args) -> Any:
        if args:
            value = self.get(key, *args)
        else:
            value = self[key]
        if key in self.__field_names__:
            del self[key]
        return value

    def to_dict(self):
        dict_class = self._get_dict_factory()
        d = dataclasses.asdict(self, dict_factory=dict_class)
        return d

    def keys(self):
        d = self.to_dict()
        return d.keys()

    def values(self):
        d = self.to_dict()
        return d.values()

    def items(self):
        d = self.to_dict()
        return d.items()

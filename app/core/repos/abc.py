import abc
from typing import Type, Optional, List

from app.core.types import FilterParams, OrderParams, SliceParams
from app.core.entities import Entity


class Repo(metaclass=abc.ABCMeta):
    entity_class = NotImplemented  # type: Type[Entity]

    @abc.abstractmethod
    def get_count(self, filter_params: Optional[FilterParams] = None) -> int:
        return 0

    @abc.abstractmethod
    def get_list(self, filter_params: Optional[FilterParams] = None,
                 order_params: Optional[OrderParams] = None,
                 slice_params: Optional[SliceParams] = None) -> List[Entity]:
        return []

    @abc.abstractmethod
    def create_list(self, items_list: List[Entity]) -> List[Entity]:
        return []


def register(class_: Type) -> None:
    Repo.register(class_)

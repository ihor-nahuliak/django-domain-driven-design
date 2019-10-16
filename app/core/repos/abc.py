import abc
from typing import Type, Optional, Union, List

from app.core.types import bunch, FilterParams, OrderParams, SliceParams
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

    @abc.abstractmethod
    def update_list(self, items_list: List[Union[Entity, bunch]],
                    filter_params: Optional[FilterParams] = None) -> List[Entity]:
        """
        Set the part of fields taken from update_params
            for all records founded by filter_params.

        :param items_list:
            entities or parted entities to update
        :param filter_params:
            filtering condition (optional)
            if you don't wanna touch some of your entities,
            that probably have already been changed or disabled
            by another process, and some of your items are outdated
        :return list:
            list of updated entities
        """
        return []

    @abc.abstractmethod
    def update_bulk(self, update_params: Union[Entity, bunch],
                    filter_params: Optional[FilterParams] = None,
                    slice_params: Optional[SliceParams] = None) -> int:
        """
        Set the part of fields taken from update_params
            for all entities founded by filter_params.

        :param update_params:
            full entity or part of entity,
            parameters to update
        :param filter_params:
            searching condition
        :param slice_params:
            pagination condition
        :return int:
            count of updated entities
        """
        return 0

    @abc.abstractmethod
    def delete_bulk(self, filter_params: Optional[FilterParams] = None,
                    slice_params: Optional[SliceParams] = None) -> int:
        """
        Delete all entities founded by filter_params.

        :param filter_params:
            searching condition
        :param slice_params:
            pagination condition
        :return int:
            count of deleted entities
        """
        return 0


def register(class_: Type) -> None:
    Repo.register(class_)

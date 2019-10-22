import abc
from typing import Type, List, Union, Optional

from app.core.types import FilterParams
from app.core.types import ScopingParams
from app.core.types import SortingParams
from app.core.types import SlicingParams
from app.core.types import Entity, ParaEntity


class Repo(metaclass=abc.ABCMeta):
    """
    Basic abstract repo class.
    All repo classes should be inherited from this one.

    Note: the difference between Entity and ParaEntity is:
        * ParaEntity contains just a part of Entity attrs scope
        * ParaEntity has just one required attr: primary key
    """
    entity_class = Type[Entity]
    para_entity_class = Type[ParaEntity]

    @abc.abstractmethod
    def get_count(self, filter_params: Optional[FilterParams] = None) -> int:
        """
        Get the total count of entities
        filtered by filter_params.

        :type filter_params: Optional[FilterParams]
        :param filter_params:
            Search parameters.

        :rtype: int
        :return:
            Found entities total count.

        """
        return 0

    @abc.abstractmethod
    def get_list(self, filter_params: Optional[FilterParams] = None,
                 scoping_params: Optional[ScopingParams] = None,
                 sorting_params: Optional[SortingParams] = None,
                 slicing_params: Optional[SlicingParams] = None
                 ) -> List[Union[Entity, ParaEntity]]:
        """
        Get a list of entities (or para-entities)
            * filtered by filter_params,
            * sorted by sorting_params
            * that contain just attributes
              from scoping_params
            * paginated by slicing_params

        :type filter_params: Optional[FilterParams]
        :param filter_params:
            Search parameters.

        :type scoping_params: Optional[ScopingParams]
        :param scoping_params:
            Fill it if you need just some specific
            entity attributes.

        :type sorting_params: Optional[SortingParams]
        :param sorting_params:
            Soring parameters.

        :type slicing_params: Optional[SlicingParams]
        :param slicing_params:
            Pagination parameters.

        :rtype: List[Union[Entity, ParaEntity]]
        :return:
            Found entities list.

        """
        return []

    def get_item(self, filter_params: FilterParams,
                 scoping_params: Optional[ScopingParams] = None
                 ) -> Union[Entity, ParaEntity]:
        """
        Get an entity (or para-entity)
            * found by filter_params
            * that contain just attributes
              from scoping_params.

        Note: It returns None instead of
              NotFound error raising.

        :type filter_params: FilterParams
        :param filter_params:
            Search parameters.

        :type scoping_params: Optional[ScopingParams]
        :param scoping_params:
            Fill it if you need just some specific
            entity attributes.

        :rtype: Union[Entity, ParaEntity, None]
        :return:
            Found entity or none.
            When scoping_params filled returns para-entity.

        """
        found_items_list = self.get_list(
            filter_params=filter_params,
            scoping_params=scoping_params,
            slicing_params=SlicingParams(limit=1),
        )
        if found_items_list:
            found_item = found_items_list[0]
        else:
            found_item = None
        return found_item

    @abc.abstractmethod
    def create_list(self, items_list: List[Entity]) -> List[Entity]:
        """
        Add a list of entities into the storage,
        returns the list of stored entities.

        :type items_list: List[Entity]
        :param items_list:
            List of entities to store.

        :rtype: List[Entity]
        :return:
            Created entities list

        """
        return []

    def create_item(self, item: Entity) -> Entity:
        """
        Add an entity into the storage,
        returns the stored entity.

        :type item: Entity
        :param item:
            Entity to store.

        :rtype: Entity
        :return:
            Created entity.

        """
        created_items_list = self.create_list([item])
        created_item = created_items_list[0]
        return created_item

    @abc.abstractmethod
    def update_list(self, items_list: List[Union[Entity, ParaEntity]]
                    ) -> List[Entity]:
        """
        Update a list of entities in the storage,
        returns the list of updated entities.

        :type items_list: List[Union[Entity, ParaEntity]]
        :param items_list:
            List of entities to update.
            Contains entities (all attributes will be updated)
            or para-entities (some attributes will be updated).

        :rtype: List[Entity]
        :return:
            Updated entities list.

        """
        return []

    def update_item(self, item: Union[Entity, ParaEntity]) -> Entity:
        """
        Update an entity in the storage,
        returns the updated entity.

        :type item: Union[Entity, ParaEntity]
        :param item:
            Entity to update.
            Can be an entity (all attributes will be updated)
            or para-entity (some attributes will be updated).

        :rtype: Entity
        :return:
            Updated entity.

        """
        updated_items_list = self.update_list([item])
        updated_item = updated_items_list[0]
        return updated_item

    @abc.abstractmethod
    def delete_list(self, filter_params: Optional[FilterParams] = None) -> int:
        """
        Removed entities fro mthe storage
        filtered by filter_params.
        Returns removed entities count.

        :type filter_params: Optional[FilterParams]
        :param filter_params:
            Search parameters.

        :rtype: int
        :return:
            Removed entities count.

        """
        return 0

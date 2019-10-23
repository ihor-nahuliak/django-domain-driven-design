import dataclasses
from typing import List, Union

from django.db.models import Model, QuerySet

from app.core.types import FilterParams
from app.core.types import ScopingParams
from app.core.types import SortingParams
from app.core.types import SlicingParams
from app.core.types import Entity, ParaEntity
from app.core.repos import base


class Repo(base.Repo):
    model_class = Model

    @classmethod
    def _get_filter_queryset(cls, q: QuerySet, filter_params: FilterParams):
        # WARNING! by security reasons,
        #   it must be override in a child class
        q = q.filter(**filter_params)
        return q

    @classmethod
    def _check_if_scope_attrs_is_subset_of_entity_attrs(
            cls, scoping_params: ScopingParams):
        attrs_list = cls._get_entity_field_names()
        unknown_attrs_set = set(scoping_params.attrs).difference(attrs_list)
        if unknown_attrs_set:
            raise ValueError('Unknown scoping_params.attrs: '
                             '%s' % tuple(unknown_attrs_set), scoping_params)

    @classmethod
    def _validate_scoping_params(cls, scoping_params: ScopingParams):
        cls._check_if_scope_attrs_is_subset_of_entity_attrs(scoping_params)

    @classmethod
    def _get_scoping_queryset(cls, q: QuerySet, scoping_params: ScopingParams):
        cls._validate_scoping_params(scoping_params)
        q = q.values_list(*scoping_params.attrs, named=True)
        return q

    @classmethod
    def _check_if_sort_by_keys_is_subset_of_entity_attrs(
            cls, sorting_params: SortingParams):
        attrs_list = cls._get_entity_field_names()
        unknown_keys_list = []
        for key in sorting_params.by:
            attr_name = key.lstrip('-')
            if attr_name not in attrs_list:
                unknown_keys_list.append(key)
        if unknown_keys_list:
            raise ValueError('Unknown sorting_params.by: '
                             '%s' % tuple(unknown_keys_list), sorting_params)

    @classmethod
    def _check_if_sort_by_relates_to_db_index(
            cls, sorting_params: SortingParams):
        # WARNING! By security reasons,
        #   you would like to allow just
        #   some indexes for the repo usage.
        #   Check if related db index
        #   defined in the model class
        pass

    @classmethod
    def _validate_sorting_params(cls, sorting_params: SortingParams):
        cls._check_if_sort_by_keys_is_subset_of_entity_attrs(sorting_params)
        cls._check_if_sort_by_relates_to_db_index(sorting_params)

    @classmethod
    def _get_sorting_queryset(cls, q: QuerySet, sorting_params: SortingParams):
        cls._validate_sorting_params(sorting_params)
        q = q.order_by(*sorting_params.by)
        return q

    @classmethod
    def _get_slicing_queryset(cls, q: QuerySet, slicing_params: SlicingParams):
        if slicing_params.offset and slicing_params.limit:
            q = q[slicing_params.offset:
                  slicing_params.offset + slicing_params.limit]
        elif slicing_params.offset:
            q = q[slicing_params.offset:]
        elif slicing_params.limit:
            q = q[:slicing_params.limit]
        return q

    @classmethod
    def _get_queryset(cls, filter_params=None,
                      scoping_params=None,
                      sorting_params=None,
                      slicing_params=None):
        q = cls.model_class.objects.get_queryset()

        if filter_params:
            q = cls._get_filter_queryset(
                q=q, filter_params=filter_params)

        if scoping_params:
            q = cls._get_scoping_queryset(
                q=q, scoping_params=scoping_params)

        if sorting_params:
            q = cls._get_sorting_queryset(
                q=q, sorting_params=sorting_params)

        if slicing_params:
            q = cls._get_slicing_queryset(
                q=q, slicing_params=slicing_params)

        return q

    @classmethod
    def _get_entity_field_names(cls) -> List[str]:
        return [f.name for f in dataclasses.fields(cls.entity_class)]

    @classmethod
    def _model_to_entity(cls, model: Union[Model, QuerySet]
                         ) -> Union[Entity, ParaEntity]:
        """
        Returns an entity class instance
        filled from the model instance fields.
        Override this method to change default behaviour.

        :type model: Union[Model, QuerySet]
        :param model:
            django model instance (or named tuple)

        :rtype: Union[Entity, ParaEntity]
        :return:
            entity or para-entity

        """
        opts = {}
        for k in cls._get_entity_field_names():
            if hasattr(model, k):
                opts[k] = getattr(model, k)
        if isinstance(model, Model):
            item = cls.entity_class(**opts)
        else:
            item = cls.para_entity_class(**opts)
        return item

    @classmethod
    def _entity_to_model(cls, item: Union[Entity, ParaEntity]) -> Model:
        """
        Returns a model class instance
        filled from the entity instance fields.
        Override this method to change default behaviour.

        Note: we don't use dataclasses.asdict(item) function
              because we want to take fields from
              the original entity_class.
              e.g. Making update_list operation it's useful to send
              partially filled bunch instead of full filled entity.

        Note: if you set some required entity field as MISSING,
              django will auto generate the value (e.g. autoincrement field).

        :type item: Union[Entity, ParaEntity]
        :param item:
            entity or para-entity

        :rtype: Model
        :return:
            django model instance

        """
        opts = {}
        for k in cls._get_entity_field_names():
            if hasattr(item, k) and getattr(item, k) != dataclasses.MISSING:
                opts[k] = getattr(item, k)
        model = cls.model_class(**opts)
        return model

    def get_count(self, filter_params=None):
        q = self._get_queryset(filter_params=filter_params)
        total_count = q.count()
        return total_count

    def get_list(self, filter_params=None,
                 scoping_params=None,
                 sorting_params=None,
                 slicing_params=None):
        q = self._get_queryset(filter_params=filter_params,
                               scoping_params=scoping_params,
                               sorting_params=sorting_params,
                               slicing_params=slicing_params)
        items_list = []
        for model in q:
            item = self._model_to_entity(model)
            items_list.append(item)
        return items_list

    def create_list(self, items_list):
        models_list = []
        for item in items_list:
            model = self._entity_to_model(item)
            models_list.append(model)

        models_list = self.model_class.objects.bulk_create(models_list)

        items_list = [self._model_to_entity(model) for model in models_list]
        return items_list

    def update_list(self, items_list):
        return []

    def delete_list(self, filter_params=None):
        return 0

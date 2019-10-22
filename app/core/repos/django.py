import dataclasses
from typing import List, Union

from django.db.models import Model, QuerySet as Row

from . import base


Entity = base.Entity
ParaEntity = base.ParaEntity


class Repo(base.Repo):
    model_class = Model

    @classmethod
    def _get_filter_queryset(cls, q, filter_params):
        q = q.filter(**filter_params)
        return q

    @classmethod
    def _get_scoping_queryset(cls, q, scoping_params):
        q = q.values_list(*scoping_params.attrs, named=True)
        return q

    @classmethod
    def _get_sorting_queryset(cls, q, sorting_params):
        q = q.order_by(*sorting_params.by)
        return q

    @classmethod
    def _get_slicing_queryset(cls, q, slicing_params):
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
    def _model_to_entity(cls, model: Union[Model, Row]
                         ) -> Union[Entity, ParaEntity]:
        """
        Returns an entity class instance
        filled from the model instance fields.
        Override this method to change default behaviour.

        :type model: Union[Model, Raw]
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
        return []

    def update_list(self, items_list):
        return []

    def delete_list(self, filter_params=None):
        return 0

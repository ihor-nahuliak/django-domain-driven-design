import dataclasses

import marshmallow as ma

from app.core import types


class SchemaOpts(ma.SchemaOpts):
    def __init__(self, meta, ordered=False):
        super().__init__(meta=meta, ordered=ordered)
        self.entity_class = getattr(
            meta, 'entity_class', types.Entity)
        self.para_entity_class = getattr(
            meta, 'para_entity_class', types.ParaEntity)


class Schema(ma.Schema):
    OPTIONS_CLASS = SchemaOpts

    def _serialize(self, obj, *, many=False):
        if dataclasses.is_dataclass(obj):
            obj = dataclasses.asdict(obj)
        elif isinstance(obj, dict):
            obj = dict(obj)
        ret = super()._serialize(obj, many=many)
        return ret

    def _deserialize(
        self, data, *,
        error_store,
        many=False,
        partial=False,
        unknown=ma.RAISE,
        index=None
    ):
        ret = super()._deserialize(data=data, error_store=error_store,
                                   many=many, partial=partial,
                                   unknown=unknown, index=index)
        if partial:
            ret = self.opts.para_entity_class(**ret)
        else:
            ret = self.opts.entity_class(**ret)
        return ret

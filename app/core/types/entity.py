import dataclasses

from app.core.types.bunch import bunch


@dataclasses.dataclass
class Entity:
    pass


class ParaEntity(bunch):

    @classmethod
    def __missing__(cls, name):
        return dataclasses.MISSING

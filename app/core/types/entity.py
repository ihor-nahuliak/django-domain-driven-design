import dataclasses

from app.core.types._bunch import bunch


@dataclasses.dataclass
class Entity:
    """Base entity class."""


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

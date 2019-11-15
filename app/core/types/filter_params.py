import dataclasses

from app.core.types._bunch import bunch


class FilterParams(bunch):
    """
    Search parameters collection.
    Example of usage:

    >>> params = FilterParams(id=1)
    >>> params.id
    1
    >>> params = FilterParams(id__in=[1, 2, 3])
    >>> params.id__in
    [1, 2, 3]
    >>> params = FilterParams(
    ...     value__min=0,
    ...     value__max=100,
    ...     is_enabled=True
    ... )
    >>> params.value__min, params.value__max
    (0, 100)
    >>> params.is_enabled
    True
    >>> params.id is dataclasses.MISSING
    True
    """

    @classmethod
    def __missing__(cls, name):
        return dataclasses.MISSING

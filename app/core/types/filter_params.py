from dataclasses import MISSING

from app.core.types.bunch import bunch


class FilterParams(bunch):
    """
    >>> params = FilterParams(id__in=[1, 2, 3], is_enabled=True)
    >>> params.id__in
    [1, 2, 3]
    >>> params.is_enabled
    True
    >>> params.unknown is MISSING
    True
    >>> bool(params.unknown)
    False
    >>> if params.id is not MISSING:
    ...     pass
    >>>
    """

    @classmethod
    def __missing__(cls, name):
        return MISSING

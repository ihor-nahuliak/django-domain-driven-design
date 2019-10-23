import keyword


class bunch(dict):  # pylint: disable=invalid-name
    """
    Named dictionary.
    Example of usage:

    >>> d = bunch({'a': 1, 'b': 2})
    >>> d.a
    1
    >>> d.b
    2
    >>> d.a = 'test'; d.a
    'test'

    You also can create it with kwargs params:
    >>> bunch(a=1, b=2)
    bunch({'a': 1, 'b': 2})
    """

    def __init__(self, *args, **kwds):
        self._validate_keys_list(args[0].keys() if args else kwds.keys())
        super().__init__(*args, **kwds)
        self.__dict__ = self

    def __getattr__(self, name):
        if hasattr(self.__class__, '__missing__') and name not in self:
            return self.__missing__(name)
        return self.__getattribute__(name)

    def __setattr__(self, name, value):
        if name in self:
            return self.__setitem__(name, value)
        return super().__setattr__(name, value)

    def __setitem__(self, key, value):
        self._validate_key(key)
        return super().__setitem__(key, value)

    def __repr__(self):
        ordered_repr = '%s({%s})' % (
            self.__class__.__name__,
            ', '.join([
                "'%s': %s" % (k, self[k])
                for k in sorted(self.keys())
            ])
        )
        return ordered_repr

    __str__ = __repr__

    @classmethod
    def _validate_key(cls, key):
        if not key.isidentifier() or keyword.iskeyword(key):
            raise ValueError(
                "Invalid key: '%s'. Only letters, "
                "natural numbers, underline char allowed. "
                "The first char can not be a number. "
                "Python keywords like: 'if', 'from', etc. "
                "are not allowed, use 'if_', 'from_' instead." % key, key)

    @classmethod
    def _validate_keys_list(cls, keys_list):
        if keys_list:
            for key in keys_list:
                cls._validate_key(key)


class defaultbunch(bunch):
    """
    The same like defaultdict.

    >>> from dataclasses import MISSING
    >>>
    >>> d = defaultbunch(MISSING, {'a': 1, 'b': 2})
    >>> d.a
    1
    >>> d.b
    2
    >>> d.c is MISSING
    True

    Use callable factory:

    >>> def factory(self):
    ...     self.counter += 1
    ...     return self.counter
    >>>
    >>> d = defaultbunch(factory, {'counter': 0})
    >>> d.a
    1
    >>> d.b
    2
    >>> d.c
    3
    """

    def __new__(cls, default_factory, *args, **kwargs):
        class_ = type(cls.__name__, (bunch,), {
            '__factory__': default_factory,
            '__missing__': cls.__missing__
        })
        self_ = class_(*args, **kwargs)
        return self_

    def __missing__(self, name):
        if callable(self.__factory__):
            return self.__factory__()
        return self.__factory__

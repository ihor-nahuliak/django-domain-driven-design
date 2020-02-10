import enum


class KitMeta(enum.EnumMeta):

    def items(cls, reverse=False):  # noqa: N805
        # pylint: disable=no-value-for-parameter
        items_tuple = tuple(
            (item.value, item.name) if reverse else (item.name, item.value)
            for item in cls.__iter__()
        )
        return items_tuple

    def __repr__(cls):  # noqa: N805
        # pylint: disable=no-value-for-parameter
        return '{classname}{members}'.format(
            classname=cls.__name__,
            members=cls.items(),
        )


class Kit(enum.Enum, metaclass=KitMeta):
    """
    Django models friendly Enum class.

    Define your int choices field that's represented as str in the admin:
    ... class Email(models.Email):
    ...     email = models.EmailField()
    ...     email_type = models.IntegerField(
    ...         choices=EmailType.items(reverse=True), null=True, blank=True)

    Example of usage:
    >>> class EmailType(Kit):
    ...     other = 0
    ...     personal = 1
    ...     corporate = 2
    ...
    >>> EmailType
    EmailType(('other', 0), ('personal', 1), ('corporate', 2))

    Has dict-like "items" class method:
    >>> EmailType.items()
    (('other', 0), ('personal', 1), ('corporate', 2))

    Can be reversed:
    >>> EmailType.items(reverse=True)
    ((0, 'other'), (1, 'personal'), (2, 'corporate'))

    Multi type representation:
    >>> int(EmailType.personal)
    1
    >>> str(EmailType.personal)
    'personal'

    Reverse type conversion:
    >>> EmailType(1)
    <EmailType.personal: 1>
    >>> EmailType('personal')
    <EmailType.personal: 1>

    Is fully multi-type comparable:
    >>> EmailType.personal == 1
    True
    >>> EmailType.personal == 2
    False
    >>> EmailType.personal == 'personal'
    True
    >>> EmailType.personal == 'corporate'
    False
    >>> EmailType.personal == EmailType.personal
    True
    >>> EmailType.personal == EmailType.corporate
    False

    """

    @classmethod
    def _missing_(cls, value):
        if value in cls._member_map_:
            return cls._member_map_[value]
        return super()._missing_(value)

    def __str__(self):
        return self.name

    def __int__(self):
        return int(self.value)

    def __eq__(self, other):
        # pylint: disable=comparison-with-callable
        if isinstance(other, int):
            return int(self) == other
        if isinstance(other, str):
            return str(self) == other
        return super().__eq__(other)

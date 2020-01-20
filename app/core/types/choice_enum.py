from enum import Enum, EnumMeta


class ChoiceEnumMeta(EnumMeta):

    def items(cls):  # noqa: N805
        # pylint: disable=no-value-for-parameter
        items_list = [
            (item.name, item.value)
            for item in cls.__iter__()
        ]
        return items_list

    @property
    def choices(cls):  # noqa: N805
        # pylint: disable=no-value-for-parameter
        choices_tuple = tuple(
            (item.value, repr(item))
            for item in cls.__iter__()
        )
        return choices_tuple

    def __repr__(cls):  # noqa: N805
        # pylint: disable=no-value-for-parameter
        return '{classname}({choices})'.format(
            classname=cls.__name__,
            choices=str(cls.items())[1:-1],
        )


class ChoiceEnum(Enum, metaclass=ChoiceEnumMeta):
    """
    Django models friendly Enum class.

    Define your int choice field that's represented as str in the admin:
    ... class Email(models.Email):
    ...     email = models.EmailField()
    ...     email_type = models.IntegerField(
    ...         choices=EmailType.choices, null=True, blank=True)

    Example of usage:
    >>> class EmailType(ChoiceEnum):
    ...     other = 0
    ...     personal = 1
    ...     corporate = 2
    ...
    >>> EmailType
    EmailType(('other', 0), ('personal', 1), ('corporate', 2))

    Has dict-like "items" class method:
    >>> EmailType.items()
    [('other', 0), ('personal', 1), ('corporate', 2)]
    >>> dict(EmailType.items())
    {'other': 0, 'personal': 1, 'corporate': 2}

    Has "choices" class property:
    >>> EmailType.choices
    ((0, 'other'), (1, 'personal'), (2, 'corporate'))

    Multi type representation:
    >>> int(EmailType.personal)
    1
    >>> str(EmailType.personal)
    'personal'

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

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __eq__(self, other):
        # pylint: disable=comparison-with-callable
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, str):
            return self.name == other
        return super().__eq__(other)

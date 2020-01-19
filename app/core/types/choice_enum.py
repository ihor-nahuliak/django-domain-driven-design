import inspect
from enum import Enum, EnumMeta

from django.utils.functional import cached_property


class ChoiceEnumMeta(EnumMeta):

    def __new__(metacls, cls, bases, classdict):  # noqa: N804
        # pylint: disable=bad-mcs-classmethod-argument
        if '__doc__' not in classdict:
            classdict['__doc__'] = cached_property(metacls.__value_doc__)
        return super().__new__(metacls, cls, bases, classdict)

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

    def __value_doc__(cls):  # noqa: N805
        """
        Inspects your ChoiceEnum class
        taking inline comment near the enum value definition.

        :rtype: str | None
        :return: inline comment
        """
        # pylint: disable=no-value-for-parameter
        doc = None

        try:
            lines_list, _ = inspect.getsourcelines(cls.__objclass__)
        except OSError:
            module = inspect.getmodule(cls.__objclass__)
            lines_list, _ = inspect.getsourcelines(module)

        value_def = ' {} = {}'.format(cls.name, cls.value)
        for line in lines_list:
            if value_def in line and '#' in line:
                _, inline_comment = line.split('#')
                doc = inspect.cleandoc(inline_comment)
                break

        return doc


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
    ...     personal = 1    # for home
    ...     corporate = 2   # for work
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
    ((0, 'other'), (1, 'personal (for home)'), (2, 'corporate (for work)'))

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

    Takes inline comments as value docs:
    >>> EmailType.personal.__doc__
    'for home'
    >>> EmailType.corporate.__doc__
    'for work'

    """

    def __repr__(self):
        if self.__doc__:
            return f'{self.name} ({self.__doc__})'
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

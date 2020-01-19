import unittest
from enum import Enum

from app.core.types import ChoiceEnum


class EmailType(ChoiceEnum):
    other = 0
    personal = 1  # for home
    corporate = 2  # for work


class PhoneType(ChoiceEnum):
    other = 0
    personal = 1  # mobile
    corporate = 2  # call center


class TestCase(unittest.TestCase):

    def test_it_is_enum_subtype(self):
        self.assertTrue(issubclass(ChoiceEnum, Enum))

    def test_it_returns_value_by_name(self):
        # pylint: disable=no-member
        #     (Instance of 'int' has no 'name' member)
        self.assertEqual(0, EmailType.other.value)
        self.assertEqual(1, EmailType.personal.value)
        self.assertEqual(2, EmailType.corporate.value)

    def test_it_returns_name(self):
        # pylint: disable=no-member
        #     (Instance of 'int' has no 'name' member)
        self.assertEqual('other', EmailType.other.name)
        self.assertEqual('personal', EmailType.personal.name)
        self.assertEqual('corporate', EmailType.corporate.name)

    def test_it_has_inline_doc(self):
        self.assertIsNone(EmailType.other.__doc__)
        self.assertEqual('for home', EmailType.personal.__doc__)
        self.assertEqual('for work', EmailType.corporate.__doc__)

    def test_it_is_compatible_with_int_value(self):
        self.assertEqual(0, EmailType.other)
        self.assertNotEqual(1, EmailType.other)
        self.assertNotEqual(2, EmailType.other)

        self.assertNotEqual(0, EmailType.personal)
        self.assertEqual(1, EmailType.personal)
        self.assertNotEqual(2, EmailType.personal)

        self.assertNotEqual(0, EmailType.corporate)
        self.assertNotEqual(1, EmailType.corporate)
        self.assertEqual(2, EmailType.corporate)

    def test_it_is_compatible_with_str_value(self):
        self.assertEqual('other', EmailType.other)
        self.assertNotEqual('personal', EmailType.other)
        self.assertNotEqual('corporate', EmailType.other)

        self.assertNotEqual('other', EmailType.personal)
        self.assertEqual('personal', EmailType.personal)
        self.assertNotEqual('corporate', EmailType.personal)

        self.assertNotEqual('other', EmailType.corporate)
        self.assertNotEqual('personal', EmailType.corporate)
        self.assertEqual('corporate', EmailType.corporate)

    def test_it_is_compatible_with_enum_value(self):
        self.assertEqual(EmailType.other, EmailType.other)
        self.assertNotEqual(EmailType.personal, EmailType.other)
        self.assertNotEqual(EmailType.corporate, EmailType.other)

        self.assertNotEqual(EmailType.other, EmailType.personal)
        self.assertEqual(EmailType.personal, EmailType.personal)
        self.assertNotEqual(EmailType.corporate, EmailType.personal)

        self.assertNotEqual(EmailType.other, EmailType.corporate)
        self.assertNotEqual(EmailType.personal, EmailType.corporate)
        self.assertEqual(EmailType.corporate, EmailType.corporate)

    def test_items_method_returns_dict_like_list(self):
        d = dict(EmailType.items())

        self.assertDictEqual({
            'other': 0,
            'personal': 1,
            'corporate': 2,
        }, d)

    def test_choices_property_returns_dict_like_list(self):
        d = dict(EmailType.choices)

        self.assertDictEqual({
            0: 'other',
            1: 'personal (for home)',
            2: 'corporate (for work)',
        }, d)

    def test_it_can_be_represented_with_inline_docs(self):
        self.assertEqual(
            "EmailType(('other', 0), ('personal', 1), ('corporate', 2))",
            repr(EmailType)
        )

    def test_it_founds_right_comment_of_right_class(self):
        self.assertDictEqual({
            0: 'other',
            1: 'personal (for home)',
            2: 'corporate (for work)',
        }, dict(EmailType.choices))

        self.assertDictEqual({
            0: 'other',
            1: 'personal (mobile)',
            2: 'corporate (call center)',
        }, dict(PhoneType.choices))


if __name__ == '__main__':
    unittest.main()

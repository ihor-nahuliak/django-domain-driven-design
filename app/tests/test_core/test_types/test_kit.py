import enum
import timeit
import unittest

from app.core.types import Kit


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class EmailType(Kit):
            other = 0
            personal = 1
            corporate = 2

        cls.EmailType = EmailType

    def test_it_is_enum_subtype(self):
        self.assertTrue(issubclass(Kit, enum.Enum))

    def test_it_returns_value_by_name(self):
        self.assertEqual(0, self.EmailType.other.value)
        self.assertEqual(1, self.EmailType.personal.value)
        self.assertEqual(2, self.EmailType.corporate.value)

    def test_it_returns_name(self):
        self.assertEqual('other', self.EmailType.other.name)
        self.assertEqual('personal', self.EmailType.personal.name)
        self.assertEqual('corporate', self.EmailType.corporate.name)

    def test_it_creates_from_int(self):
        self.assertIs(self.EmailType(0), self.EmailType.other)
        self.assertIs(self.EmailType(1), self.EmailType.personal)
        self.assertIs(self.EmailType(2), self.EmailType.corporate)

        with self.assertRaises(ValueError) as err_ctx:
            self.EmailType(3)

        self.assertEqual('3 is not a valid EmailType',
                         err_ctx.exception.args[0])

    def test_it_creates_from_str(self):
        self.assertIs(self.EmailType('other'), self.EmailType.other)
        self.assertIs(self.EmailType('personal'), self.EmailType.personal)
        self.assertIs(self.EmailType('corporate'), self.EmailType.corporate)

        with self.assertRaises(ValueError) as err_ctx:
            self.EmailType('unknown')

        self.assertEqual("'unknown' is not a valid EmailType",
                         err_ctx.exception.args[0])

    def test_it_is_compatible_with_int_value(self):
        self.assertEqual(0, self.EmailType.other)
        self.assertNotEqual(1, self.EmailType.other)
        self.assertNotEqual(2, self.EmailType.other)

        self.assertNotEqual(0, self.EmailType.personal)
        self.assertEqual(1, self.EmailType.personal)
        self.assertNotEqual(2, self.EmailType.personal)

        self.assertNotEqual(0, self.EmailType.corporate)
        self.assertNotEqual(1, self.EmailType.corporate)
        self.assertEqual(2, self.EmailType.corporate)

    def test_it_is_compatible_with_str_value(self):
        self.assertEqual('other', self.EmailType.other)
        self.assertNotEqual('personal', self.EmailType.other)
        self.assertNotEqual('corporate', self.EmailType.other)

        self.assertNotEqual('other', self.EmailType.personal)
        self.assertEqual('personal', self.EmailType.personal)
        self.assertNotEqual('corporate', self.EmailType.personal)

        self.assertNotEqual('other', self.EmailType.corporate)
        self.assertNotEqual('personal', self.EmailType.corporate)
        self.assertEqual('corporate', self.EmailType.corporate)

    def test_it_is_compatible_with_kit_value(self):
        self.assertEqual(self.EmailType.other, self.EmailType.other)
        self.assertNotEqual(self.EmailType.personal, self.EmailType.other)
        self.assertNotEqual(self.EmailType.corporate, self.EmailType.other)

        self.assertNotEqual(self.EmailType.other, self.EmailType.personal)
        self.assertEqual(self.EmailType.personal, self.EmailType.personal)
        self.assertNotEqual(self.EmailType.corporate, self.EmailType.personal)

        self.assertNotEqual(self.EmailType.other, self.EmailType.corporate)
        self.assertNotEqual(self.EmailType.personal, self.EmailType.corporate)
        self.assertEqual(self.EmailType.corporate, self.EmailType.corporate)

    def test_items_method_returns_dict_like_tuple(self):
        t = self.EmailType.items()

        self.assertTupleEqual((
            ('other', 0),
            ('personal', 1),
            ('corporate', 2),
        ), t)

    def test_items_method_returns_reversed_dict_like_tuple(self):
        t = self.EmailType.items(reverse=True)

        self.assertTupleEqual((
            (0, 'other'),
            (1, 'personal'),
            (2, 'corporate'),
        ), t)

    def test_create_from_int_performance(self):
        class SimpleEnum(enum.Enum):
            other = 0
            personal = 1
            corporate = 2

        t0 = timeit.default_timer()
        for _ in range(1000):
            for i in range(3):
                SimpleEnum(i)
        enum_benchmark = timeit.default_timer() - t0

        t0 = timeit.default_timer()
        for _ in range(1000):
            for i in range(3):
                self.EmailType(i)
        kit_benchmark = timeit.default_timer() - t0

        self.assertLess(kit_benchmark - enum_benchmark, 0.001,
                        '~%.4fs overhead' % (kit_benchmark - enum_benchmark))

    def test_create_from_str_performance(self):
        class SimpleEnum(enum.Enum):
            other = 0
            personal = 1
            corporate = 2

        t0 = timeit.default_timer()
        for _ in range(1000):
            for i in range(3):
                SimpleEnum(i)
        enum_benchmark = timeit.default_timer() - t0

        t0 = timeit.default_timer()
        for _ in range(1000):
            for s in ('other', 'personal', 'corporate'):
                self.EmailType(s)
        kit_benchmark = timeit.default_timer() - t0

        self.assertLess(kit_benchmark - enum_benchmark, 0.005,
                        '~%.4fs overhead' % (kit_benchmark - enum_benchmark))


if __name__ == '__main__':
    unittest.main()

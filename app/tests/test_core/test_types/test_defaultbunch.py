import unittest
from dataclasses import MISSING

from app.core.types.bunch import defaultbunch


class TestCase(unittest.TestCase):

    def test_create_from_args(self):
        d = defaultbunch(MISSING, {'a': 1, 'b': 2})

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)
        self.assertIs(MISSING, d.c)
        self.assertEqual("defaultbunch({'a': 1, 'b': 2})", repr(d))

    def test_create_from_kwargs(self):
        d = defaultbunch(MISSING, a=1, b=2)

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)
        self.assertIs(MISSING, d.c)
        self.assertEqual("defaultbunch({'a': 1, 'b': 2})", repr(d))

    def test_it_returns_none_reading_unknown_key(self):
        d = defaultbunch(default_factory=None, a=1, b=2)

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)
        self.assertIsNone(d.c)

    def test_it_returns_const_reading_unknown_key(self):
        d = defaultbunch(default_factory=1234, a=1, b=2)

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)
        self.assertEqual(1234, d.c)

    def test_it_returns_list_reading_unknown_key(self):
        d = defaultbunch(default_factory=list, a=1, b=2)

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)
        self.assertListEqual([], d.c)

    def test_it_returns_dict_reading_unknown_key(self):
        d = defaultbunch(default_factory=dict, a=1, b=2)

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)
        self.assertDictEqual({}, d.c)

    def test_two_different_instances_do_not_overlap(self):
        d1 = defaultbunch('missing1', {'a': 1, 'b': 2})
        d2 = defaultbunch('missing2', {'b': 1, 'c': 2})

        self.assertEqual(1, d1.a)
        self.assertEqual(2, d1.b)
        self.assertEqual('missing1', d1.c)
        self.assertEqual("defaultbunch({'a': 1, 'b': 2})", repr(d1))

        self.assertEqual('missing2', d2.a)
        self.assertEqual(1, d2.b)
        self.assertEqual(2, d2.c)
        self.assertEqual("defaultbunch({'b': 1, 'c': 2})", repr(d2))

    def test_two_different_classes_do_not_overlap(self):
        class Foo(defaultbunch):
            pass

        class Bar(defaultbunch):
            pass

        d1 = Foo('missing1', {'a': 1, 'b': 2})
        d2 = Bar('missing2', {'b': 1, 'c': 2})

        self.assertEqual(1, d1.a)
        self.assertEqual(2, d1.b)
        self.assertEqual('missing1', d1.c)
        self.assertEqual("Foo({'a': 1, 'b': 2})", repr(d1))

        self.assertEqual('missing2', d2.a)
        self.assertEqual(1, d2.b)
        self.assertEqual(2, d2.c)
        self.assertEqual("Bar({'b': 1, 'c': 2})", repr(d2))


if __name__ == '__main__':
    unittest.main()

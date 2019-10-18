import unittest
from dataclasses import MISSING

from app.core.types.bunch import defaultbunch


class TestCase(unittest.TestCase):

    def test_create_from_args(self):
        d = defaultbunch(MISSING, {'a': 1, 'b': 2})

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)
        self.assertIs(MISSING, d.c)

    def test_create_from_kwargs(self):
        d = defaultbunch(MISSING, a=1, b=2)

        self.assertEqual(1, d.a)
        self.assertEqual(2, d.b)
        self.assertIs(MISSING, d.c)

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


if __name__ == '__main__':
    unittest.main()

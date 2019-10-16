import unittest

from app.core.types.filter_params import FilterParams


class TestCase(unittest.TestCase):

    def test_it_returns_value_reading_known_attr(self):
        params = FilterParams(a=1, b=2, c=3)

        self.assertEqual(1, params.a)
        self.assertEqual(2, params.b)
        self.assertEqual(3, params.c)

    def test_it_returns_none_reading_unknown_attr(self):
        params = FilterParams(a=1, b=2)

        self.assertEqual(1, params.a)
        self.assertEqual(2, params.b)
        self.assertIsNone(params.c)


if __name__ == '__main__':
    unittest.main()

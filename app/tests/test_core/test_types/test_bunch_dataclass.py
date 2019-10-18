import unittest
from dataclasses import dataclass

from app.core.types.bunch import bunch


@dataclass
class Foo(bunch):
    a: int = 0
    b: str = 'default'
    c: str = lambda: 'random'


class TestCase(unittest.TestCase):

    def test_it_overrides_dataclass_default_values_in_constructor(self):
        d = Foo(a=1, b='x', c='y')

        self.assertEqual("Foo(a=1, b='x', c='y')", repr(d))
        self.assertEqual(1, d.a)
        self.assertEqual('x', d.b)
        self.assertEqual('y', d.c)

    def test_it_overrides_dataclass_default_values_on_key_set(self):
        d = Foo()
        d['a'] = 1
        d['b'] = 'x'
        d['c'] = 'y'

        self.assertEqual("Foo(a=1, b='x', c='y')", repr(d))
        self.assertEqual(1, d.a)
        self.assertEqual('x', d.b)
        self.assertEqual('y', d.c)

    def test_it_overrides_dataclass_default_values_on_attr_set(self):
        d = Foo()
        d.a = 1
        d.b = 'x'
        d.c = 'y'

        self.assertEqual("Foo(a=1, b='x', c='y')", repr(d))
        self.assertEqual(1, d.a)
        self.assertEqual('x', d.b)
        self.assertEqual('y', d.c)


if __name__ == '__main__':
    unittest.main()

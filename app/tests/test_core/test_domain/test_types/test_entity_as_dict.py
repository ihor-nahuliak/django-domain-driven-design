import unittest
from dataclasses import dataclass
from typing import ClassVar

from app.core.domain.types.entity import Entity


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        @dataclass(order=True)
        class MyEntity(Entity):
            id: int
            foo: str = ''
            bar: bool = False
            class_var: ClassVar[str] = 'not a field'

        cls.entity_class = MyEntity

    def test_it_gets_attr_by_dict_key(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)

        self.assertEqual(123, my_entity['id'])
        self.assertEqual('abc', my_entity['foo'])
        self.assertIs(True, my_entity['bar'])

    def test_it_raises_key_error_on_unknown_field_getting(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)

        with self.assertRaises(KeyError) as err_ctx:
            my_entity['unknown']

        self.assertEqual('MyEntity has no field unknown',
                         err_ctx.exception.args[0])

    def test_it_raises_key_error_on_class_var_getting(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)

        with self.assertRaises(KeyError) as err_ctx:
            my_entity['class_var']

        self.assertEqual('MyEntity has no field class_var',
                         err_ctx.exception.args[0])

    def test_it_sets_attr_by_dict_key(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        my_entity['id'] = 456
        my_entity['foo'] = 'xyz'
        my_entity['bar'] = False

        self.assertEqual(456, my_entity.id)
        self.assertEqual('xyz', my_entity.foo)
        self.assertIs(False, my_entity.bar)

    def test_it_raises_key_error_on_unknown_field_setting(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)

        with self.assertRaises(KeyError) as err_ctx:
            my_entity['unknown'] = 456

        self.assertEqual('MyEntity has no field unknown',
                         err_ctx.exception.args[0])

    def test_it_raises_key_error_on_class_var_setting(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)

        with self.assertRaises(KeyError) as err_ctx:
            my_entity['class_var'] = 456

        self.assertEqual('MyEntity has no field class_var',
                         err_ctx.exception.args[0])

    def test_it_sets_to_default_attr_on_deleting_by_dict_key(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        del my_entity['foo']
        del my_entity['bar']

        self.assertEqual(123, my_entity.id)
        self.assertEqual('', my_entity.foo)
        self.assertIs(False, my_entity.bar)

    def test_it_raises_type_error_on_deleting_by_dict_key_required_field(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        with self.assertRaises(TypeError) as err_ctx:
            del my_entity['id']

        self.assertEqual('MyEntity.id is required', err_ctx.exception.args[0])

    def test_it_raises_key_error_on_deleting_by_dict_key_unknown_field(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        with self.assertRaises(KeyError) as err_ctx:
            del my_entity['unknown']

        self.assertEqual('MyEntity has no field unknown',
                         err_ctx.exception.args[0])

    def test_it_raises_key_error_on_deleting_by_dict_key_class_var(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        with self.assertRaises(KeyError) as err_ctx:
            del my_entity['class_var']

        self.assertEqual('MyEntity has no field class_var',
                         err_ctx.exception.args[0])

    def test_it_sets_to_default_attr_on_pop_by_dict_key(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        my_entity.pop('foo')
        my_entity.pop('bar')

        self.assertEqual(123, my_entity.id)
        self.assertEqual('', my_entity.foo)
        self.assertIs(False, my_entity.bar)

    def test_it_raises_type_error_on_pop_by_dict_key_required_field(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        with self.assertRaises(TypeError) as err_ctx:
            my_entity.pop('id')

        self.assertEqual('MyEntity.id is required', err_ctx.exception.args[0])

    def test_it_raises_key_error_on_pop_by_dict_key_unknown_field(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        with self.assertRaises(KeyError) as err_ctx:
            my_entity.pop('unknown')

        self.assertEqual('MyEntity has no field unknown',
                         err_ctx.exception.args[0])

    def test_it_raises_key_error_on_pop_by_dict_key_class_var(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        with self.assertRaises(KeyError) as err_ctx:
            my_entity.pop('class_var')

        self.assertEqual('MyEntity has no field class_var',
                         err_ctx.exception.args[0])

    def test_it_returns_default_on_pop_dict_key_unknown_field(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        value = my_entity.pop('unknown', 456)

        self.assertEqual(456, value)

    def test_it_returns_default_on_pop_dict_key_class_var(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        value = my_entity.pop('class_var', 456)

        self.assertEqual(456, value)

    def test_it_makes_iter_items(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        result = {k: v for k, v in my_entity.items()}

        self.assertDictEqual({
            'id': 123,
            'foo': 'abc',
            'bar': True,
        }, result)

    def test_it_makes_iter_keys(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        result = list(my_entity.keys())

        self.assertListEqual([
            'id',
            'foo',
            'bar',
        ], result)

    def test_it_makes_iter_values(self):
        my_entity = self.entity_class(id=123, foo='abc', bar=True)
        result = list(my_entity.values())

        self.assertListEqual([
            123,
            'abc',
            True,
        ], result)


if __name__ == '__main__':
    unittest.main()

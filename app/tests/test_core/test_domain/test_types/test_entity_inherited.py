import unittest
import uuid
from dataclasses import dataclass

from app.core.domain.types.entity import Entity


class TestCase(unittest.TestCase):

    def test_int_id_entity(self):
        @dataclass
        class MyEntity(Entity):
            id: int
            foo: str
            bar: bool

        my_entity = MyEntity(id=123, foo='abc', bar=True)

        self.assertEqual(123, my_entity.id)
        self.assertEqual('abc', my_entity.foo)
        self.assertIs(True, my_entity.bar)

    def test_str_id_entity(self):
        @dataclass
        class MyEntity(Entity):
            id: str
            foo: str
            bar: bool

        my_entity = MyEntity(id='xyz', foo='abc', bar=True,)

        self.assertEqual('xyz', my_entity.id)
        self.assertEqual('abc', my_entity.foo)
        self.assertIs(True, my_entity.bar)

    def test_uuid_id_entity(self):
        @dataclass
        class MyEntity(Entity):
            id: uuid.UUID
            foo: str
            bar: bool

        test_uuid = uuid.UUID('{12345678-1234-5678-1234-567812345678}')
        my_entity = MyEntity(id=test_uuid, foo='abc', bar=True)

        self.assertEqual(test_uuid, my_entity.id)
        self.assertEqual('abc', my_entity.foo)
        self.assertIs(True, my_entity.bar)


if __name__ == '__main__':
    unittest.main()

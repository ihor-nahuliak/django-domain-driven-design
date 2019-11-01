import unittest
import dataclasses

from app.core import types, schemas


class TestCase(unittest.TestCase):

    def setUp(self):
        @dataclasses.dataclass
        class User(types.Entity):
            id: int
            username: str
            email: str
            first_name: str = None
            last_name: str = None

        class UserSchema(schemas.Schema):
            id = schemas.fields.Integer(required=True)
            username = schemas.fields.String(required=True)
            email = schemas.fields.Email(required=True)
            first_name = schemas.fields.String(missing='', default='')
            last_name = schemas.fields.String(missing='', default='')

            class Meta:
                entity_class = User

        self.entity_class = User
        self.para_entity_class = types.ParaEntity
        self.schema_class = UserSchema

    def test_it_loads_dict_to_entity_if_not_partial(self):
        user = self.schema_class().load({
            'id': 1,
            'username': 'lennon',
            'email': 'john@beatles.com',
        })

        self.assertIsInstance(user, self.entity_class)
        self.assertEqual(1, user.id)
        self.assertEqual('lennon', user.username)
        self.assertEqual('john@beatles.com', user.email)
        self.assertEqual('', user.first_name)
        self.assertEqual('', user.last_name)

    def test_it_loads_dict_to_para_entity_if_partial(self):
        user = self.schema_class(partial=True).load({
            'id': 1,
        })

        self.assertIsInstance(user, self.para_entity_class)
        self.assertEqual(1, user.id)
        self.assertIs(dataclasses.MISSING, user.username)
        self.assertIs(dataclasses.MISSING, user.email)
        self.assertIs(dataclasses.MISSING, user.first_name)
        self.assertIs(dataclasses.MISSING, user.last_name)

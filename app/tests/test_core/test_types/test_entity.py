import unittest
import dataclasses

from app.core.types import entity


class TestCase(unittest.TestCase):

    def setUp(self):
        @dataclasses.dataclass
        class User(entity.Entity):
            id: int
            username: str
            email: str
            first_name: str = ''
            last_name: str = ''

        self.entity_class = User
        self.para_entity_class = entity.ParaEntity

    def test_it_raises_error_without_required_params(self):
        with self.assertRaises(TypeError) as err_ctx:
            self.entity_class(id=1)

        self.assertEqual("__init__() missing 2 required "
                         "positional arguments: 'username' and 'email'",
                         err_ctx.exception.args[0])

    def test_it_creates_entity_with_required_params(self):
        user = self.entity_class(id=1,
                                 username='lennon',
                                 email='john@beatles.com')

        self.assertEqual(1, user.id)
        self.assertEqual('lennon', user.username)
        self.assertEqual('john@beatles.com', user.email)
        self.assertEqual('', user.first_name)
        self.assertEqual('', user.last_name)

    def test_it_creates_entity_with_all_params(self):
        user = self.entity_class(id=1,
                                 username='lennon',
                                 email='john@beatles.com',
                                 first_name='John',
                                 last_name='Lennon')

        self.assertEqual(1, user.id)
        self.assertEqual('lennon', user.username)
        self.assertEqual('john@beatles.com', user.email)
        self.assertEqual('John', user.first_name)
        self.assertEqual('Lennon', user.last_name)

    def test_it_creates_para_entity_without_required_params(self):
        user = self.para_entity_class(id=1)

        self.assertEqual(1, user.id)
        self.assertEqual(dataclasses.MISSING, user.username)
        self.assertEqual(dataclasses.MISSING, user.email)
        self.assertEqual(dataclasses.MISSING, user.first_name)
        self.assertEqual(dataclasses.MISSING, user.last_name)

    def test_it_creates_para_entity_with_required_params(self):
        user = self.para_entity_class(id=1,
                                      username='lennon',
                                      email='john@beatles.com')

        self.assertEqual(1, user.id)
        self.assertEqual('lennon', user.username)
        self.assertEqual('john@beatles.com', user.email)
        self.assertEqual(dataclasses.MISSING, user.first_name)
        self.assertEqual(dataclasses.MISSING, user.last_name)

    def test_it_creates_para_entity_with_all_params(self):
        user = self.para_entity_class(id=1,
                                      username='lennon',
                                      email='john@beatles.com',
                                      first_name='John',
                                      last_name='Lennon')

        self.assertEqual(1, user.id)
        self.assertEqual('lennon', user.username)
        self.assertEqual('john@beatles.com', user.email)
        self.assertEqual('John', user.first_name)
        self.assertEqual('Lennon', user.last_name)


if __name__ == '__main__':
    unittest.main()

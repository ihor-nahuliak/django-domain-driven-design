import unittest
import os
import dataclasses

from django import test
from django.contrib import auth

from app.core import types
from app.core.repos import django

User = auth.get_user_model()


class TestCase(test.TestCase):
    fixtures = [
        os.path.join(os.path.pardir, os.path.dirname(__file__),
                     'fixtures', 'test_django_repo.json'),
    ]

    def setUp(self):
        @dataclasses.dataclass()
        class UserEntity:
            id: int
            username: str
            email: str
            first_name: str = ''
            last_name: str = ''

        class Repo(django.Repo):
            model_class = User
            entity_class = UserEntity

        self.repo = Repo()

    def test_get_count_no_params_returns_not_filtered_count(self):
        total_count = self.repo.get_count()

        self.assertEqual(4, total_count)

    def test_get_list_no_params_returns_not_filtered_entity_list(self):
        items_list = self.repo.get_list()

        self.assertEqual(4, len(items_list))

        self.assertEqual(1, items_list[0].id)
        self.assertEqual('jlennon', items_list[0].username)
        self.assertEqual('john.lennon@beatles.com', items_list[0].email)
        self.assertEqual('John', items_list[0].first_name)
        self.assertEqual('Lennon', items_list[0].last_name)

        self.assertEqual(2, items_list[1].id)
        self.assertEqual('pmccartney', items_list[1].username)
        self.assertEqual('paul.mccartney@beatles.com', items_list[1].email)
        self.assertEqual('Paul', items_list[1].first_name)
        self.assertEqual('McCartney', items_list[1].last_name)

        self.assertEqual(3, items_list[2].id)
        self.assertEqual('gharrison', items_list[2].username)
        self.assertEqual('george.harrison@beatles.com', items_list[2].email)
        self.assertEqual('George', items_list[2].first_name)
        self.assertEqual('Harrison', items_list[2].last_name)

        self.assertEqual(4, items_list[3].id)
        self.assertEqual('rstarkey', items_list[3].username)
        self.assertEqual('richard.starkey@beatles.com', items_list[3].email)
        self.assertEqual('Richard', items_list[3].first_name)
        self.assertEqual('Starkey', items_list[3].last_name)

    def test_get_list_filter_params_returns_filtered_entity_list(self):
        items_list = self.repo.get_list(
            filter_params=types.FilterParams(id__in=[2, 4]),
        )

        self.assertEqual(2, len(items_list))

        self.assertEqual(2, items_list[0].id)
        self.assertEqual('pmccartney', items_list[0].username)
        self.assertEqual('paul.mccartney@beatles.com', items_list[0].email)
        self.assertEqual('Paul', items_list[0].first_name)
        self.assertEqual('McCartney', items_list[0].last_name)

        self.assertEqual(4, items_list[1].id)
        self.assertEqual('rstarkey', items_list[1].username)
        self.assertEqual('richard.starkey@beatles.com', items_list[1].email)
        self.assertEqual('Richard', items_list[1].first_name)
        self.assertEqual('Starkey', items_list[1].last_name)

    def test_get_list_scoping_params_returns_filtered_entity_list(self):
        items_list = self.repo.get_list(
            scoping_params=types.ScopingParams(attrs=('id', 'username')),
        )

        self.assertEqual(4, len(items_list))

        self.assertEqual(1, items_list[0].id)
        self.assertEqual('jlennon', items_list[0].username)
        self.assertEqual(dataclasses.MISSING, items_list[0].email)
        self.assertEqual(dataclasses.MISSING, items_list[0].first_name)
        self.assertEqual(dataclasses.MISSING, items_list[0].last_name)

        self.assertEqual(2, items_list[1].id)
        self.assertEqual('pmccartney', items_list[1].username)
        self.assertEqual(dataclasses.MISSING, items_list[1].email)
        self.assertEqual(dataclasses.MISSING, items_list[1].first_name)
        self.assertEqual(dataclasses.MISSING, items_list[1].last_name)

        self.assertEqual(3, items_list[2].id)
        self.assertEqual('gharrison', items_list[2].username)
        self.assertEqual(dataclasses.MISSING, items_list[2].email)
        self.assertEqual(dataclasses.MISSING, items_list[2].first_name)
        self.assertEqual(dataclasses.MISSING, items_list[2].last_name)

        self.assertEqual(4, items_list[3].id)
        self.assertEqual('rstarkey', items_list[3].username)
        self.assertEqual(dataclasses.MISSING, items_list[3].email)
        self.assertEqual(dataclasses.MISSING, items_list[3].first_name)
        self.assertEqual(dataclasses.MISSING, items_list[3].last_name)

    def test_get_item_for_existed_id_returns_entity(self):
        item = self.repo.get_item(filter_params=types.FilterParams(id=2))

        self.assertEqual(2, item.id)
        self.assertEqual('pmccartney', item.username)
        self.assertEqual('paul.mccartney@beatles.com', item.email)
        self.assertEqual('Paul', item.first_name)
        self.assertEqual('McCartney', item.last_name)

    def test_get_item_for_unknown_id_returns_none(self):
        item = self.repo.get_item(filter_params=types.FilterParams(id=5))

        self.assertIsNone(item)

    def test_get_item_scoping_params_for_existed_id_returns_para_entity(self):
        item = self.repo.get_item(
            filter_params=types.FilterParams(id=2),
            scoping_params=types.ScopingParams(attrs=('id', 'username')),
        )

        self.assertEqual(2, item.id)
        self.assertEqual('pmccartney', item.username)
        self.assertEqual(dataclasses.MISSING, item.email)
        self.assertEqual(dataclasses.MISSING, item.first_name)
        self.assertEqual(dataclasses.MISSING, item.last_name)


if __name__ == '__main__':
    unittest.main()

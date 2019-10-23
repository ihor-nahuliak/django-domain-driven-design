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
        @dataclasses.dataclass
        class UserEntity(types.Entity):
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

    def test_get_list_scoping_params_returns_para_entity_list(self):
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

    def test_get_list_sorting_params_returns_asc_sorted_entity_list(self):
        items_list = self.repo.get_list(
            sorting_params=types.SortingParams(by=('id',)),
        )

        self.assertEqual(4, len(items_list))

        self.assertEqual(1, items_list[0].id)
        self.assertEqual(2, items_list[1].id)
        self.assertEqual(3, items_list[2].id)
        self.assertEqual(4, items_list[3].id)

    def test_get_list_sorting_params_returns_desc_sorted_entity_list(self):
        items_list = self.repo.get_list(
            sorting_params=types.SortingParams(by=('-id',)),
        )

        self.assertEqual(4, len(items_list))

        self.assertEqual(4, items_list[0].id)
        self.assertEqual(3, items_list[1].id)
        self.assertEqual(2, items_list[2].id)
        self.assertEqual(1, items_list[3].id)

    def test_get_list_slicing_params_left_part_returns_paginated_entity_list(self):
        items_list = self.repo.get_list(
            slicing_params=types.SlicingParams(offset=0, limit=2),
        )

        self.assertEqual(2, len(items_list))

        self.assertEqual(1, items_list[0].id)
        self.assertEqual(2, items_list[1].id)

    def test_get_list_slicing_params_middle_part_returns_paginated_entity_list(self):
        items_list = self.repo.get_list(
            slicing_params=types.SlicingParams(offset=1, limit=2),
        )

        self.assertEqual(2, len(items_list))

        self.assertEqual(2, items_list[0].id)
        self.assertEqual(3, items_list[1].id)

    def test_get_list_slicing_params_right_part_returns_paginated_entity_list(self):
        items_list = self.repo.get_list(
            slicing_params=types.SlicingParams(offset=2, limit=2),
        )

        self.assertEqual(2, len(items_list))

        self.assertEqual(3, items_list[0].id)
        self.assertEqual(4, items_list[1].id)

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

    def test_create_list_returns_created_entity_list(self):
        items_list = self.repo.create_list(items_list=[
            self.repo.entity_class(
                id=5,
                username='stuart',
                email='stuart.sutcliffe@beatles.com',
                first_name='Stuart',
                last_name='Sutcliffe',
            ),
            self.repo.entity_class(
                id=6,
                username='tmoore',
                email='tommy.moore@beatles.com',
                first_name='Tommy',
                last_name='Moore',
            ),
        ])

        self.assertEqual(2, len(items_list))

        self.assertEqual(5, items_list[0].id)
        self.assertEqual('stuart', items_list[0].username)
        self.assertEqual('stuart.sutcliffe@beatles.com', items_list[0].email)
        self.assertEqual('Stuart', items_list[0].first_name)
        self.assertEqual('Sutcliffe', items_list[0].last_name)

        self.assertEqual(6, items_list[1].id)
        self.assertEqual('tmoore', items_list[1].username)
        self.assertEqual('tommy.moore@beatles.com', items_list[1].email)
        self.assertEqual('Tommy', items_list[1].first_name)
        self.assertEqual('Moore', items_list[1].last_name)

    def test_create_list_stores_data_that_is_available_to_get_then(self):
        self.repo.create_list(items_list=[
            self.repo.entity_class(
                id=5,
                username='stuart',
                email='stuart.sutcliffe@beatles.com',
                first_name='Stuart',
                last_name='Sutcliffe',
            ),
            self.repo.entity_class(
                id=6,
                username='tmoore',
                email='tommy.moore@beatles.com',
                first_name='Tommy',
                last_name='Moore',
            ),
        ])
        items_list = self.repo.get_list()

        self.assertEqual(6, len(items_list))

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

        self.assertEqual(5, items_list[4].id)
        self.assertEqual('stuart', items_list[4].username)
        self.assertEqual('stuart.sutcliffe@beatles.com', items_list[4].email)
        self.assertEqual('Stuart', items_list[4].first_name)
        self.assertEqual('Sutcliffe', items_list[4].last_name)

        self.assertEqual(6, items_list[5].id)
        self.assertEqual('tmoore', items_list[5].username)
        self.assertEqual('tommy.moore@beatles.com', items_list[5].email)
        self.assertEqual('Tommy', items_list[5].first_name)
        self.assertEqual('Moore', items_list[5].last_name)


if __name__ == '__main__':
    unittest.main()

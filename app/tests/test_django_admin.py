import unittest
import django.test


class TestCase(django.test.TestCase):

    def test_django_admin_returns_200(self):
        resp = self.client.get('/admin/login/?next=/admin/')

        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()

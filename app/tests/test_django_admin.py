import unittest
import django.test
import django.urls


class TestCase(django.test.TestCase):

    def setUp(self):
        self.index_url = django.urls.reverse('admin:index')
        self.login_url = django.urls.reverse('rest_framework:login')
        self.login_url += f'?next={self.index_url}'

        self.assertEqual('/admin/', self.index_url)
        self.assertEqual('/admin/login/?next=/admin/', self.login_url)

    def test_django_admin_index_page_redirects_to_admin_login_page(self):
        resp = self.client.get(self.index_url, follow=True)

        self.assertEqual(200, resp.status_code)
        self.assertListEqual([(self.login_url, 302)], resp.redirect_chain)

    def test_django_admin_login_page_returns_200(self):
        resp = self.client.get(self.login_url)

        self.assertEqual(200, resp.status_code)


if __name__ == '__main__':
    unittest.main()

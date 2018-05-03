from django.test import TestCase


class TestErrorPages(TestCase):
    def test_404_page(self):
        url = '/quite/likely/not/a/page/'
        response = self.client.get(url)
        self.assertContains(response, url, status_code=404)

    def test_500_page(self):
        url = '/500/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)

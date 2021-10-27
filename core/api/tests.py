from django.test import SimpleTestCase
from django.urls import reverse, resolve

from core.api.views import TestAPI


class TestUrls(SimpleTestCase):
    def test_test_api_resolves(self):
        """
        To run the test: python manage.py test
        As in core/api/urls the view used is TestAPI this would be passed.
        However, if we change the view to something else this test would fail.
        """
        url = reverse('core:test')
        self.assertEquals(resolve(url).func.view_class, TestAPI)

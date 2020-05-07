from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import *


class Test(TestCase):
    def setUp(self):
        self.client = Client()

    def test_loading(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 301)

    def test_template_footer_use(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'footer.html')

    def test_template_header_use(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'header.html')

    def test_template_sidebar_use(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'left_sidebar.html')

    def test_template_index_use(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

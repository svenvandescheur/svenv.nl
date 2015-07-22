# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from mock import patch
from os.path import isfile
from unittest import skipIf


class ContactFormTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_submit_empty(self):
        response = self.c.post('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name is required')
        self.assertContains(response, 'E-mail is required')
        self.assertContains(response, 'A message is required')

    def test_submit_no_name(self):
        response = self.c.post('/contact', {'name': '', 'email': 'john@example.com', 'message': 'message'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name is required')
        self.assertNotContains(response, 'E-mail is required')
        self.assertNotContains(response, 'A message is required')

    def test_submit_no_email(self):
        response = self.c.post('/contact', {'name': 'John', 'email': '', 'message': 'message'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Name is required')
        self.assertContains(response, 'E-mail is required')
        self.assertNotContains(response, 'A message is required')

    def test_submit_no_message(self):
        response = self.c.post('/contact', {'name': 'John', 'email': 'john@example.com', 'message': ''})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Name is required')
        self.assertNotContains(response, 'E-mail is required')
        self.assertContains(response, 'A message is required')

    def test_submit_invalid_email(self):
        response = self.c.post('/contact', {'name': 'John', 'email': 'john', 'message': 'message'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')

    def test_submit_invalid_email(self):
        response = self.c.post('/contact', {'name': 'John', 'email': 'john', 'message': 'message'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')

    def test_submit_valid(self):
        response = self.c.post('/contact', {'name': 'John', 'email': 'john@example.com', 'message': 'message'})
        self.assertRedirects(response, '/thankyou', status_code=302, target_status_code=404)

    @skipIf(not isfile('/.dockerinit'), 'This test requires the docker environment')
    def test_submit_valid_unicode(self):
        response = self.c.post('/contact', {'name': 'JohnȈ', 'email': 'john@exampleȈ.com', 'message': 'messageȈ'})
        self.assertRedirects(response, '/thankyou', status_code=302, target_status_code=404)

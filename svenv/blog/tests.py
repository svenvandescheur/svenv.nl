# -*- coding: utf-8 -*-
from blog.models import BaseModel, Category, Image, Post, Page
from django.contrib.auth.models import User
from django.test import TestCase, Client, override_settings
from os.path import isfile
from unittest import skipIf
from mock import patch


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

    @skipIf(not isfile('/.dockerinit'), 'This test requires the docker environment')
    def test_submit_valid(self):
        response = self.c.post('/contact', {'name': 'John', 'email': 'john@example.com', 'message': 'message'})
        self.assertRedirects(response, '/thankyou', status_code=302, target_status_code=404)

    @skipIf(not isfile('/.dockerinit'), 'This test requires the docker environment')
    def test_submit_valid_unicode(self):
        response = self.c.post('/contact', {'name': 'JohnȈ', 'email': 'john@exampleȈ.com', 'message': 'messageȈ'})
        self.assertRedirects(response, '/thankyou', status_code=302, target_status_code=404)

    def test_permalink_not_present(self):
        response = self.c.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Permalink')


class PostTestCase(TestCase):
    def setUp(self):
        self.c = Client()

        self.author = User()
        self.author.save()
        self.category = Category(published=1, name="cat1")
        self.category.save()
        self.image = Image()
        self.image.save()

    @patch('blog.models.call')
    def test_clear_varnish_cache_on_save(self, mock_call):
        post = Post(author=self.author, category=self.category, image=self.image, published=1)
        post.save()
        self.assertEqual(mock_call.call_count, 1)


class ViewTestCase(TestCase):
    @patch('blog.models.call')
    def setUp(self, mock_call):
        self.c = Client()

        author = User()
        author.save()
        category1 = Category(published=1, name="cat1")
        category1.save()
        category2 = Category(published=1, name="cat2")
        category2.save()
        image = Image(copyright="some artist")
        image.save()
        post1 = Post(author=author, category=category1, image=image, published=1, content="Post 1", short_title="post1")
        post1.save()
        post2 = Post(author=author, category=category1, image=image, published=1, content="Post 2", short_title="post2")
        post2.save()
        post3 = Post(author=author, category=category2, image=image, published=1, content="Post 3", short_title="post3")
        post3.save()
        post4 = Post(author=author, category=category2, image=image, published=1, content="Post 4", short_title="post4")
        post4.save()
        page1 = Page(author=author, image=image, position=1, navigation=1, published=1, content="Page 1", path="page1", short_title="Page 1")
        page1.save()
        page2 = Page(author=author, image=image, position=2, navigation=1, published=1, content="Page 2", path="page2", short_title="Page 2")
        page2.save()
        page3 = Page(author=author, image=image, position=3, navigation=0, published=1, content="Page 3", path="page3", short_title="Page 2")
        page3.save()


class CategoryViewTestCase(ViewTestCase):
    def test_category(self):
        response = self.c.get('/cat2/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Post 1')
        self.assertNotContains(response, 'Post 2')
        self.assertContains(response, 'Post 3')
        self.assertContains(response, 'Post 4')

    def test_home(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 1')
        self.assertContains(response, 'Post 2')
        self.assertContains(response, 'Post 3')
        self.assertContains(response, 'Post 4')

    @override_settings(REST_FRAMEWORK={'PAGE_SIZE': 3})
    def test_pagination(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Post 1')
        self.assertContains(response, 'Post 2')
        self.assertContains(response, 'Post 3')
        self.assertContains(response, 'Post 4')

    def test_404(self):
        response = self.c.get('/404/')
        self.assertEqual(response.status_code, 404)


class PostViewTestCase(ViewTestCase):
    def test_post(self):
        response = self.c.get('/cat1/post2')
        self.assertContains(response, 'Post 2')
        self.assertNotContains(response, 'Post 4')

    def test_404(self):
        response = self.c.get('/cat1/404')
        self.assertEqual(response.status_code, 404)

    def test_permalink_present(self):
        response = self.c.get('/cat1/post1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Permalink')

    def test_image_copyright_notice(self):
        response = self.c.get('/cat1/post1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'some artist')


class PageViewTestCase(ViewTestCase):
    def test_post(self):
        response = self.c.get('/page1')
        self.assertContains(response, 'Page 1')

    def test_navigation_visibility(self):
        response = self.c.get('/')
        self.assertContains(response, 'Page 1')
        self.assertContains(response, 'Page 2')
        self.assertNotContains(response, 'Page 3')

    def test_navigation_position(self):
        response = self.c.get('/')
        content = response.content
        page1_index = content.index('Page 1')
        page2_index = content.index('Page 2')
        self.assertLess(page1_index, page2_index)

    def test_404(self):
        response = self.c.get('/404')
        self.assertEqual(response.status_code, 404)

    def test_permalink_present(self):
        response = self.c.get('/page1')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Permalink')


class PostViewSetTestCase(ViewTestCase):
    def test_api_root(self):
        response = self.c.get('/api/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{"posts":"http://testserver/api/posts/"}')

    def test_api_posts(self):
        response = self.c.get('/api/posts/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 1')
        self.assertContains(response, 'Post 2')
        self.assertContains(response, 'Post 3')
        self.assertContains(response, 'Post 4')

    @override_settings(REST_FRAMEWORK={'PAGE_SIZE': 3})
    def test_pagination(self):
        response = self.c.get('/api/posts/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Page 1')
        self.assertContains(response, 'Post 2')
        self.assertContains(response, 'Post 3')
        self.assertContains(response, 'Post 4')

    def test_html(self):
        response = self.c.get('/api/posts/?format=html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<article>')
        self.assertContains(response, 'Post 1')


class ContactViewTestCase(ViewTestCase):
    @override_settings(CONTACT_PAGE_PATH='page1')
    def test_contact_page(self):
        response = self.c.get('/contact')
        self.assertContains(response, 'Page 1')
        self.assertContains(response, '<input')


class SiteMapViewTestCase(ViewTestCase):
    def test_contains_categories(self):
        response = self.c.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '//svenv.nl/cat1/</loc>')
        self.assertContains(response, '//svenv.nl/cat2/</loc>')

    def test_contains_posts(self):
        response = self.c.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '//svenv.nl/cat1/post1</loc>')
        self.assertContains(response, '//svenv.nl/cat1/post2</loc>')
        self.assertContains(response, '//svenv.nl/cat2/post3</loc>')
        self.assertContains(response, '//svenv.nl/cat2/post4</loc>')

    def test_contains_pages(self):
        response = self.c.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '//svenv.nl/page1</loc>')
        self.assertContains(response, '//svenv.nl/page2</loc>')
        self.assertContains(response, '//svenv.nl/page3</loc>')

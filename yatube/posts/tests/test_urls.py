from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author = User.objects.create_user(
            username='author', email='author@gmail.com', password='top_secret')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post_user = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )
        cls.post_author = Post.objects.create(
            author=cls.author,
            text='Тестовый текст',
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_home_url_exists_at_desired_location(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_list_url_exists_at_desired_location(self):
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_url_exists_at_desired_location(self):
        response = self.guest_client.get('/profile/auth/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_url_exists_at_desired_location(self):
        response = self.guest_client.get(
            '/posts/' + str(self.post_author.pk) + '/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_exists_at_desired_location(self):
        response = self.author_client.get(
            '/posts/' + str(self.post_author.pk) + '/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_not_exists(self):
        response = self.authorized_client.get(
            '/posts/' + str(self.post_author.pk) + '/edit/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_post_exists_at_desired_location(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_existed_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template_guest(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test-slug/',
            'posts/profile.html': '/profile/auth/',
            'posts/post_detail.html':
                '/posts/' + str(self.post_author.pk) + '/',
        }
        for template_key, address_value in templates_url_names.items():
            with self.subTest(adress=address_value):
                response = self.guest_client.get(address_value)
                self.assertTemplateUsed(response, template_key)

    def test_urls_uses_correct_template_authorized(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test-slug/',
            'posts/profile.html': '/profile/auth/',
            'posts/post_detail.html':
                '/posts/' + str(self.post_author.pk) + '/',
            'posts/create_post.html': '/create/',
        }
        for template_key, address_value in templates_url_names.items():
            with self.subTest(adress=address_value):
                response = self.authorized_client.get(address_value)
                self.assertTemplateUsed(response, template_key)

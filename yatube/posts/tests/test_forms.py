from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, User

User = get_user_model()


class PostCreateFormTests(TestCase):
    post_text_new = 'Текст для теста test_new_post_created_in_database'
    post_text_edited = 'Отредактированный текст'
    post_author = 'auth'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def setUp(self) -> None:

        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_created_in_database(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст для теста test_new_post_created_in_database',
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        post = Post.objects.first()
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post.text,
                         self.post_text_new)
        self.assertEqual(Post.objects.get(pk=1).author.username,
                         self.post_author)
        self.assertEqual(post.group, None)

    def test_new_post_not_created_in_database(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст для теста test_new_post_not_created_in_database'
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('users:login')
                             + '?next='
                             + reverse('posts:post_create'))

        self.assertEqual(Post.objects.count(), posts_count)

    def test_post_edited_in_database(self):
        post_id = self.post.pk
        form_data_edited = {
            'text': 'Отредактированный текст',
        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post_id}),
            data=form_data_edited,
            follow=True
        )
        post = Post.objects.first()
        self.assertTrue(Post.objects.filter(
            text=form_data_edited.get('text')).exists())
        self.assertEqual(post.text,
                         self.post_text_edited)
        self.assertEqual(Post.objects.get(pk=1).author.username,
                         self.post_author)

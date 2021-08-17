from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Группа',
                             max_length=200,
                             help_text='Добавьте название группы')
    slug = models.SlugField('Слаг', unique=True, help_text='Добавьте слаг')
    description = models.TextField('Описание', help_text='Добавьте описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField('Текст поста',
                            blank=False,
                            help_text='Введите тест поста')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True,
                                    help_text='Добавьте дату публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Впишите имя автора поста')

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу')

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

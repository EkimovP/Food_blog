from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Food(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название блюда')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Информация')
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Различные блюда'
        verbose_name_plural = 'Различные блюда'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['id']

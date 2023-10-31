import unidecode
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True,)
    email = models.EmailField(max_length=150)
    post = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL', null=True)

    def __str__(self):
        return self.email


class Task(models.Model):
    users = models.ManyToManyField(User, blank=True, null=True)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    status = models.BooleanField(default=False)
    CHOICE = [
        ('1', 'Высокий'),
        ('2', 'Низкий'),
        ('0', 'Без приоритета')
    ]
    priority = models.CharField(max_length=150, null=True, choices=CHOICE)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL', null=True)
    is_fav = models.BooleanField(default=False, null=True)

    def get_status(self, *args, **kwargs):
        if self.status is True:
            status = 'Задача выполнена'
            return status
        else:
            status = 'Задача в процессе...'
            return status

    def save(self, *args, **kwargs):
        if not self.slug:
            # Используем unidecode для преобразования русского текста в ASCII
            ascii_name = unidecode(str(self.title))
            self.slug = slugify(ascii_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('task_view', kwargs={'task_slug': self.slug})



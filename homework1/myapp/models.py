from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', verbose_name='Фото профиля')


class Post(models.Model):
    Date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    img = models.ImageField(upload_to='posts', verbose_name='Фото поста')
    user = models.ForeignKey(User, on_delete=True, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    c_text = models.CharField(max_length=255, verbose_name='Текст комментария')
    user = models.ForeignKey(User, on_delete=True, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=True, verbose_name='Публикация')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follower(models.Model):
    user_1 = models.ForeignKey(User,  on_delete=True, related_name='following', verbose_name='Подписка')
    user_2 = models.ForeignKey(User,  on_delete=True, related_name='follower', verbose_name='Подписчик')

    class Meta:
        unique_together = ('user_1', 'user_2')
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class Like(models.Model):
    Date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время лайка')
    user = models.ForeignKey(User,  on_delete=True, verbose_name='Пользователь')
    post = models.ForeignKey(Post,  on_delete=True, verbose_name='Публикация')

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Отметка нравится'
        verbose_name_plural = 'Отметки нравятся'

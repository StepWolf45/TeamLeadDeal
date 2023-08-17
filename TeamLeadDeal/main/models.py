"""
Файл для моделей базы данных
"""

from .profile import *
from .tags import Tag
from PIL import Image
from django.db import models

# Create your models here.


class Worksheet (models.Model):
    """
    Модель для анкеты
    """
    IMAGE_SIZE_STANDARD = (400, 400)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='worksheets', default=r'worksheets/default_image.png')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    description = models.CharField(max_length=500)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    date = models.DateField()

    def save(self, *args, **kwargs):
        super(Worksheet, self).save(*args, **kwargs)

        filepath = self.image.path
        img = Image.open(filepath)

        img.thumbnail(self.IMAGE_SIZE_STANDARD)
        img.save(filepath)


class Chat (models.Model):
    """
    Модель для чата
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile')
    contacts = models.ManyToManyField(Profile)


class Message (models.Model):
    """
    Модель для сообщения
    """
    message = models.CharField(max_length=160)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient')
    is_checked = models.BooleanField(default=False)
    date = models.TimeField()


class SocialMedia (models.Model):
    """
    Модель для социальных сетей в профиле
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    instagram = models.CharField(max_length=100, default='')
    vk = models.CharField(max_length=100, default='')
    github = models.CharField(max_length=100, default='')
    codewars = models.CharField(max_length=100, default='')


class Like (models.Model):
    """
    Модель для лайка анкеты
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_disliked = Dislike.objects.filter(user=self.user).filter(worksheet=self.worksheet).count()

        if is_disliked != 0:
            Dislike.objects.filter(user=self.user).filter(worksheet=self.worksheet).delete()

        super(Like, self).save(*args, **kwargs)


class Dislike (models.Model):
    """
    Модель для дизлайка
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_liked = Like.objects.filter(user=self.user).filter(worksheet=self.worksheet).count()

        if is_liked != 0:
            Like.objects.filter(user=self.user).filter(worksheet=self.worksheet).delete()

        super(Dislike, self).save(*args, **kwargs)


class Comment (models.Model):
    """
    Модель для комментария к анкете
    """
    text_message = models.CharField(max_length=200)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_author')
    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE, related_name='commented_worksheet')
    date = models.DateField()

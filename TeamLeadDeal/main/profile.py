from django.contrib.auth.models import User
from django.db import models
from .tags import Tag
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Profile (models.Model):
    AVATAR_SIZE_STANDARD = (400, 300)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    tags = models.ManyToManyField(Tag)
    avatar = models.ImageField(default=r'avatars/default_avatar.png', upload_to='avatars')
    work = models.CharField(max_length=200, default='Не указано')
    bio = models.CharField(max_length=1000, default='Не указано')
    stage = models.CharField(max_length=100, default='Не указано')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        image = Image.open(self.avatar.path)

        image.thumbnail(self.AVATAR_SIZE_STANDARD)
        image.save(self.avatar.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

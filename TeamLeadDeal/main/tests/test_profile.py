from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from main.models import *
from main.tags import *
import datetime

# Create your tests here.


class ProfileTestCase (TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            username="TestUser",
            password="myPassword1234"
        )
        self.test_user.save()

        for i in range(100):
            tag = Tag(
                title=f'Test Tag {i+1}',
                description=f'Test Description {i+1}'
            )
            tag.save()

        profile = Profile.objects.get(user=self.test_user)
        profile.first_name = 'Test name'
        profile.last_name = 'Test surname'
        profile.stage = 'Test stage'
        profile.work = 'Test work'
        profile.bio = 'Test bio'

        profile.save()

        profile.tags.set(
            Tag.objects.all()
        )

    def test_profile(self):
        profile = Profile.objects.get(user=self.test_user)
        self.assertEqual(str(profile), self.test_user.username)
        self.assertEqual(profile.first_name, 'Test name')
        self.assertEqual(profile.last_name, 'Test surname')
        self.assertEqual(profile.stage, 'Test stage')
        self.assertEqual(profile.work, 'Test work')
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(
            [str(tag) for tag in profile.tags.all()],
            [f'Test Tag {i+1}' for i in range(len(profile.tags.all()))]
        )

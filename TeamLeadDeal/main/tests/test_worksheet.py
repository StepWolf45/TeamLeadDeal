from django.contrib.auth.models import User
from django.test import TestCase
from main.models import Worksheet
from main.profile import Profile
from main.tags import Tag
import datetime


class WorksheetModelTestCase (TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            username='test_user',
            password='myTestPassword1234'
        )
        self.test_user.save()

        for i in range(100):
            tag = Tag(
                title=f'Test tag title {i}',
                description=f'Test tag description {i}'
            )
            tag.save()

        worksheet = Worksheet(
            title='Test title',
            author=Profile.objects.get(user=self.test_user),
            description='Test description',
            date=datetime.datetime.now()
        )

        worksheet.save()

        worksheet.tags.set(
            Tag.objects.all()
        )

    def test_worksheet(self):
        worksheet = Worksheet.objects.get(author__user=self.test_user)
        self.assertEqual(worksheet.title, 'Test title')
        self.assertEqual(worksheet.author, Profile.objects.get(user=self.test_user))
        self.assertEqual(worksheet.description, 'Test description')
        self.assertEqual(
            [str(tag) for tag in worksheet.tags.all()],
            [f'Test tag title {i}' for i in range(len(worksheet.tags.all()))]
        )

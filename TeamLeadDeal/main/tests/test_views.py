import random

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from main.profile import Profile
from main.models import Worksheet
from main.tags import Tag

import datetime


class IndexViewTestCase(TestCase):
    def setUp(self) -> None:
        test_user = User.objects.create_user(
            username='test_user',
            password='testPassword1234'
        )
        test_user.save()

        for i in range(10):
            tag = Tag(
                title=f'Test tag title {i}',
                description=f'Test tag description {i}'
            )
            tag.save()

        for i in range(5):
            worksheet = Worksheet(
                title=f'Test title {i+1}',
                author=Profile.objects.get(user=test_user),
                description='Test description',
                date=datetime.datetime.now()
            )
            worksheet.save()

            worksheet.tags.set(
                [Tag.objects.get(pk=tag) for tag in random.sample(range(1, 10), k=3)]
            )

    def test_redirected(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main.html')


class ProfileTestCase(TestCase):
    def setUp(self) -> None:
        test_user = User.objects.create_user(
            username='test_user',
            password='testPassword1234'
        )
        test_user.save()

        self.profile_dict = {
            'first_name': 'Test name',
            'last_name': 'Test surname',
            'stage': 'Test stage',
            'work': 'Test work',
            'bio': 'Test bio',
        }

        self.profile = Profile.objects.get(user=test_user)
        self.profile.first_name = self.profile_dict['first_name']
        self.profile.last_name = self.profile_dict['last_name']
        self.profile.stage = self.profile_dict['stage']
        self.profile.work = self.profile_dict['work']
        self.profile.bio = self.profile_dict['bio']

        self.profile.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse_lazy('profile'))
        self.assertRedirects(resp, '/login/?next=/profile/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(
            username='test_user',
            password='testPassword1234'
        )
        resp = self.client.get(reverse_lazy('profile'))

        self.assertEqual(str(resp.context['user']), 'test_user')
        self.assertEqual(resp.status_code, 200)

        for item in self.profile_dict:
            self.assertTrue(item in resp.context)
            self.assertEqual(resp.context[item], self.profile_dict[item])

        self.assertTemplateUsed(resp, 'profile.html')


class ProfileViewSearchTestCase (TestCase):
    def setUp(self) -> None:
        my_test_user = User.objects.create_user(
            username=f'test_user',
            password='testPassword1234'
        )
        my_test_user.save()

        profile = Profile.objects.get(user=my_test_user)

        for i in range(5):
            tag = Tag(
                title=f'Test title {i+1}',
                color='#fff',
                description=f'Test description {i + 1}'
            )
            tag.save()

        profile.tags.set(
            Tag.objects.all()
        )

        for i in range(5):
            test_user = User.objects.create_user(
                username=f'test_user{i+1}',
                password='testPassword1234'
            )
            test_user.save()

            profile_dict = {
                'first_name': f'Test name {i}',
                'last_name': f'Test surname {i}',
                'stage': f'Test stage {i}',
                'work': f'Test work {i}',
                'bio': f'Test bio {i}',
            }

            profile = Profile.objects.get(user=test_user)
            profile.first_name = profile_dict['first_name']
            profile.last_name = profile_dict['last_name']
            profile.stage = profile_dict['stage']
            profile.work = profile_dict['work']
            profile.bio = profile_dict['bio']

            profile.save()

            profile.tags.set(
                [Tag.objects.get(pk=tag) for tag in
                 random.sample(range(1, 5), k=3)]
            )

    def test_profiles_result(self):
        resp = self.client.get('/users/')

        profiles = Profile.objects.all()

        self.assertTrue('profiles' in resp.context)
        self.assertEqual(len(resp.context['profiles']), len(profiles))

    def test_login_profiles_result(self):
        login = self.client.login(
            username='test_user',
            password='testPassword1234'
        )
        resp = self.client.get('/users/')

        profiles = Profile.objects.exclude(
            user=User.objects.get(username='test_user')
        )

        self.assertTrue('profiles' in resp.context)
        self.assertEqual(len(resp.context['profiles']), len(profiles))

    def test_search_profiles_result(self):
        checked_positions = random.sample(range(1, 10), k=2)
        url_string = f'/users/?'
        for i in range(2):
            url_string += f'tags_search_field={checked_positions[i]}&'

        resp = self.client.get(
            url_string
        )

        profiles = set(Profile.objects.filter(
            tags__in=checked_positions
        ))

        self.assertTrue('profiles' in resp.context)
        self.assertEqual(len(resp.context['profiles']), len(profiles))


class WorksheetCreationTestCase (TestCase):
    def setUp(self) -> None:
        test_user = User.objects.create_user(
            username='testUser1',
            password='testPassword1234'
        )
        test_user.save()

        for i in range(4):
            tag = Tag(
                title=f'Test title {i+1}',
                color='#fff',
                description=f'Test description {i + 1}'
            )
            tag.save()

        profile = Profile.objects.get(user=test_user)
        profile.first_name = 'Ivan'
        profile.last_name = 'Ivanov'
        profile.save()

    def test_worksheet_post_creation(self):
        login = self.client.login(
            username='testUser1',
            password='testPassword1234'
        )
        resp = self.client.post(
            '/worksheet/create/', {
                'title': 'my worksheet',
                'description': 'test',
                'tags': [1, 2],
            }, follow=True
        )

        worksheet = Worksheet.objects.get(pk=1)

        self.assertEqual(worksheet.title, 'my worksheet')
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/')

    def test_worksheet_get_creation(self):
        login = self.client.login(
            username='testUser1',
            password='testPassword1234'
        )

        resp = self.client.get(
            '/worksheet/create/'
        )

        self.assertEqual(resp.status_code, 200)


class ProfileEditViewTestCase (TestCase):
    def setUp(self) -> None:
        test_user = User.objects.create_user(
            username='testUser1',
            password='testPassword1234'
        )
        test_user.save()

        test_user = User.objects.create_user(
            username='hacker',
            password='testPassword1234'
        )
        test_user.save()

        for i in range(4):
            tag = Tag(
                title=f'Test title {i + 1}',
                description=f'Test description {i + 1}'
            )
            tag.save()

        profile = Profile.objects.get(user=test_user)
        profile.first_name = 'Ivan'
        profile.last_name = 'Ivanov'
        profile.save()

    def test_profile_edit_get(self):
        login = self.client.login(
            username='testUser1',
            password='testPassword1234'
        )

        resp = self.client.get(
            '/profile/edit/'
        )

        profile = Profile.objects.get(user__username='testUser1')

        self.assertEqual(resp.status_code, 200)


class WorksheetEditViewTestCase (TestCase):
    def setUp(self) -> None:
        test_user = User.objects.create_user(
            username='testUser1',
            password='testPassword1234'
        )
        test_user.save()

        for i in range(4):
            tag = Tag(
                title=f'Test title {i + 1}',
                description=f'Test description {i + 1}'
            )
            tag.save()

        profile = Profile.objects.get(user=test_user)
        profile.first_name = 'Ivan'
        profile.last_name = 'Ivanov'
        profile.save()

        worksheet = Worksheet(
            title='test',
            description='desc_test',
            author=profile,
            date=datetime.datetime.now()
        )
        worksheet.save()

        worksheet.tags.set(
            Tag.objects.all()
        )

    def test_worksheet_post_edit(self):
        login = self.client.login(
                username='testUser1',
                password='testPassword1234'
            )

        resp = self.client.post(
                '/worksheet1/edit/', {
                    'title': 'new_test',
                    'description': 'test',
                    'tags': [1, 3],
                }, follow=True
            )

        worksheet = Worksheet.objects.get(pk=1)

        self.assertEqual(worksheet.title, 'new_test')
        self.assertEqual(worksheet.description, 'test')
        self.assertEqual(len(worksheet.tags.all()), 2)

        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/')

    def test_worksheet_get_forbidden_edit(self):
        login = self.client.login(
            username='hacker',
            password='testPassword1234'
        )

        resp = self.client.get(
            '/worksheet1/edit/'
        )

        self.assertEqual(resp.status_code, 302)

    def test_worksheet_get_edit(self):
        login = self.client.login(
            username='testUser1',
            password='testPassword1234'
        )

        resp = self.client.get(
            '/worksheet1/edit/'
        )

        self.assertEqual(resp.status_code, 200)

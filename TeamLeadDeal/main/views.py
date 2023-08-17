"""
Основная страница, отвечающая за отрисовку всех стрианц
"""

from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import *

from .ajax_code.messages_ajax import MessagesAjax
from .ajax_code.notes_ajax import NoteAjax, CommentDelete
from .ajax_code.worksheets_ajax import WorksheetsAjax
from .user_chat_tools import *

from .forms import *
from .profile import *
import datetime
import json
import logging


# Create your views here.

logger = logging.getLogger('main')


def messages_data(request, user_pk):
    """
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :param user_pk: Первичный ключ пользователя
    :type user_pk: int
    :return: JSON ответ
    """
    messages = MessagesAjax(request, user_pk)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            context = messages.get()
            return JsonResponse(context)

        if request.method == 'POST':
            data = json.load(request)
            messages.post(data)
            return JsonResponse({'status': 'Message added!'})


def note_data_post(request, worksheet_pk):
    """
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :param worksheet_pk: Первичный ключ анкеты
    :type worksheet_pk: int
    :return: JSON ответ
    """
    notes = NoteAjax(request, worksheet_pk)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            context = notes.get()
            return JsonResponse(context)

        if request.method == 'POST':
            data = json.load(request)
            notes.post(data)
            return JsonResponse({'status': 'ok'})


def comment_data_delete(request):
    """
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :return: JSON ответ если успешно выполнилась функция
    """
    if request.method == 'POST':
        data = json.load(request)
        deleter = CommentDelete(data)
        deleter.delete()
        return JsonResponse({'status': 'OK!'})


def worksheet_index_ajax_get(request, worksheets_count):
    """
    Возвращает несколько анкет
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :param worksheets_count: количество анкет для подгрузки, константа
    :type worksheets_count: int
    :return: JSON ответ с анкетами
    """
    data = request.GET.getlist('tags_search_field', '')
    worksheets = WorksheetsAjax(worksheets_count, data)
    context = worksheets.get_context()
    return JsonResponse(context)


class MainPageView(View):
    """
    Класс для подгрузки главной страницы и взаимодействия с ней
    Шаблон страницы - main.html
    """
    template_name = 'main.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class WorksheetsView(View):
    """
    Класс для подгрузки страницы с анкетами и взаимодействия с ней
    Шаблон страницы - worksheets.html
    """
    template_name = 'worksheets.html'
    form_class = SearchForm

    def get(self, request):
        context = {}

        if request.GET.get('drop'):
            return redirect('/worksheets')

        data = request.GET.getlist('tags_search_field', '')

        context['url_get_params'] = '?'+''.join(f'tags_search_field={i}&' for i in data)[:-1]

        context['search_form'] = self.form_class(
            initial={
                'tags_search_field': data
            }
        )

        logger.info(f'{request.user} get worksheets')
        return render(request, self.template_name, context)


class UserProfile(View):
    """
    Класс для подгрузки страринцы профиля и взаимодействия с ней
    Шаблон страницы - user_page.html
    """
    template_name = 'user_page.html'

    def get(self, request, pk):
        context = {}
        user_profile = Profile.objects.get(pk=pk)
        user_worksheets = Worksheet.objects.filter(author=user_profile)
        context['profile'] = user_profile
        context['worksheets'] = user_worksheets

        try:
            profile_social_media = SocialMedia.objects.get(profile=user_profile)
            context['instagram_link'] = profile_social_media.instagram
            context['vk_link'] = profile_social_media.vk
            context['github_link'] = profile_social_media.github
            context['codewars_link'] = profile_social_media.codewars

        except:
            context['instagram_link'] = None
            context['vk_link'] = None
            context['github_link'] = None
            context['codewars_link'] = None

        return render(request, self.template_name, context)


class UserChat(TemplateView):
    """
    Класс для подгрузки страницы с чатом и взаимодействия с ней
    Шаблон страницы - chat.html
    """
    template_name = 'chat.html'
    class_form = MessageForm

    def __init__(self):
        """
        Инициализирующая функция
        """
        super().__init__()
        self.author = None
        self.text = None
        self.recipient = None
        self.correspondence = None

    def get(self, request, *args, **kwargs):
        """
        :param request: объект с деатялми запроса
        :param args: объект с системной информацией
        :param kwargs: объект с системной информацией
        :return: Возвращает страницу чата
        """
        self.call_users()
        self.get_messages()

        context = self.get_context()
        context['form'] = self.class_form()

        return render(request, self.template_name, context)

    def call_users(self):
        users = CallUsers().call(self)

        self.recipient = users['recipient']
        self.author = users['author']

    def chat_valid(self):
        validator = ChatValid()
        validator.for_author(self)
        validator.for_recipient(self)

    def get_messages(self):
        self.correspondence = GetMessages().get(self)

    def save_message(self):
        saver = SaveMessage()
        saver.save(self)

    def get_context(self):
        context = {
            'recipient': self.recipient,
            'author': self.author,
            'messages_count': [
                author.author for author in self.correspondence
            ]
        }

        return context


def chats(request):
    context = {}
    try:
        contacts = Chat.objects.get(profile__user=request.user).contacts.all()
        empty = False
    except:
        contacts = None
        empty = True

    context['contacts'] = contacts
    context['empty'] = empty

    return render(request, 'messages.html', context)


class ProfileView(View):
    """
    Класс для подгрузки страницы профиля и взаимодействия с ней
    Шаблон страницы - users.html
    """
    template_name = 'users.html'
    class_form = SearchForm

    def get(self, request):
        context = {}

        if request.GET.get('drop'):
            return redirect('/users')

        data = request.GET.getlist('tags_search_field', '')

        if data != '':
            profiles = Profile.objects.filter(
                tags__in=data
            )

        else:
            profiles = Profile.objects.all()

        if request.user.is_authenticated:
            profiles = profiles.exclude(
                user=request.user
            )

        context['profiles'] = set(profiles)
        context['form'] = self.class_form(
            initial={
                'tags_search_field': data
            }
        )

        return render(request, self.template_name, context)


def profile(request):
    context = {}
    user_profile = Profile.objects.get(user=request.user)
    user_worksheets = Worksheet.objects.filter(author=user_profile)

    context['username'] = user_profile.user.username
    context['first_name'] = user_profile.first_name
    context['last_name'] = user_profile.last_name
    context['avatar'] = user_profile.avatar
    context['tags'] = user_profile.tags.all()
    context['bio'] = user_profile.bio
    context['work'] = user_profile.work
    context['stage'] = user_profile.stage
    context['worksheets'] = user_worksheets

    try:
        profile_social_media = SocialMedia.objects.get(profile=user_profile)
        context['instagram_link'] = profile_social_media.instagram
        context['vk_link'] = profile_social_media.vk
        context['github_link'] = profile_social_media.github
        context['codewars_link'] = profile_social_media.codewars

    except:
        context['instagram_link'] = None
        context['vk_link'] = None
        context['github_link'] = None
        context['codewars_link'] = None

    return render(request, 'profile.html', context)


class ProfileEditView (View):
    """
    Класс для подгрузки страницы редактирования профиля и взаимодействия с ней
    Шаблон страницы - edit.html
    """
    template_name = 'edit.html'
    profile_edit_form_class = ProfileEditForm
    user_edit_form_class = UserEditForm
    social_media_form = SocialMediaForm

    def get_context(self, user_profile):
        bio = user_profile.bio
        work = user_profile.work

        try:
            social_media = SocialMedia.objects.get(profile=user_profile)
            social_media_form = self.social_media_form(
                initial={
                    'instagram_field': social_media.instagram,
                    'vk_field': social_media.vk,
                    'github_field': social_media.github,
                    'codewars_field': social_media.codewars
                }
            )
        except:
            social_media_form = self.social_media_form()

        if user_profile.bio == 'Не указано':
            bio = ''
        if user_profile.work == 'Не указано':
            work = ''

        forms = {
            'profile': user_profile,
            'form': self.profile_edit_form_class(
                initial={
                    'work': work,
                    'bio': bio,
                    'tags': user_profile.tags.all(),
                    'stage': user_profile.stage,
                    'username': user_profile.user.username,
                    'email': user_profile.user.email,
                }
            ),
            'user_form': self.user_edit_form_class(
                instance=user_profile.user,
                initial={
                    'username': user_profile.user.username,
                    'email': user_profile.user.email,
                    'first_name': user_profile.user.first_name,
                    'last_name': user_profile.user.last_name,
                }
            ),
            'social_media_form': social_media_form
        }
        return forms

    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        context = self.get_context(user_profile)

        return render(request, self.template_name, context)

    def post(self, request):
        user_profile = Profile.objects.get(user=request.user)
        context = self.get_context(user_profile)

        if request.POST.get('drop'):
            user_profile.avatar = 'avatars/default_avatar.png'
            user_profile.save()
            return render(request, self.template_name, context)

        user_form = self.user_edit_form_class(
                request.POST,
                instance=request.user
        )
        form = self.profile_edit_form_class(request.POST, request.FILES)

        social_media_form = self.social_media_form(request.POST)

        if social_media_form.is_valid():
            profile = Profile.objects.get(user=request.user)

            if not SocialMedia.objects.filter(profile=profile).count():
                social_media = SocialMedia(
                    profile=profile,
                    instagram=social_media_form.data['instagram_field'],
                    vk=social_media_form.data['vk_field'],
                    github=social_media_form.data['github_field'],
                    codewars=social_media_form.data['codewars_field'],
                )
                social_media.save()

            else:
                social_media = SocialMedia.objects.get(profile=profile)
                social_media.instagram = social_media_form.data['instagram_field']
                social_media.vk = social_media_form.data['vk_field']
                social_media.github = social_media_form.data['github_field']
                social_media.codewars = social_media_form.data['codewars_field']
                social_media.save()

        if form.is_valid() and user_form.is_valid():
            user_form.save()

            user_profile.first_name = user_form.data['first_name']
            user_profile.last_name = user_form.data['last_name']

            if form.data['work'] != '':
                user_profile.work = form.data['work']
            else:
                user_profile.work = 'Не указано'

            if form.data['bio'] != '':
                user_profile.bio = form.data['bio']
            else:
                user_profile.bio = 'Не указано'

            if form.data['stage'] != '':
                user_profile.stage = form.data['stage']
            else:
                user_profile.stage = 'Не указано'

            if 'avatar' in form.files:
                user_profile.avatar = form.files['avatar']

            user_profile.save()
            user_profile.tags.set(form.cleaned_data.get('tags'))

            context['form'] = form
            context['user_form'] = user_form
            context['profile'] = user_profile

            return redirect('/profile')

        return render(request, self.template_name, context)


def worksheet_creation(request):
    """
    Возвращает страницу создания анкеты
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :return: страница создания анкеты
    """
    context = {}

    if request.method == 'POST':
        form = WorksheetCreationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            worksheet = Worksheet(
                title=form.data['title'],
                author=Profile.objects.get(user=request.user),
                description=form.data['description'],
                date=datetime.datetime.now()
            )

            if 'image' in request.FILES:
                worksheet.image = form.files['image']

            worksheet.save()
            worksheet.tags.set(form.cleaned_data.get('tags'))

            return redirect(f'/worksheet{worksheet.pk}')

    else:
        form = WorksheetCreationForm()

    context['form'] = form

    return render(request, 'worksheetCreation.html', context)


def worksheet_show(request, worksheet_id):
    """
    Возвращает страницу анкеты
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :param worksheet_id: ID анкеты
    :type worksheet_id: int
    :return: страница анкеты
    """
    context = {
        'like_checked': False,
        'dislike_checked': False
    }

    worksheet = Worksheet.objects.get(id=worksheet_id)
    profile = Profile.objects.get(user=request.user)

    is_liked = Like.objects.filter(user=profile, worksheet=worksheet).count()
    is_disliked = Dislike.objects.filter(user=profile, worksheet=worksheet).count()

    if is_liked != 0:
        context['like_checked'] = True

    if is_disliked != 0:
        context['dislike_checked'] = True

    context['worksheet'] = worksheet

    return render(request, 'worksheet.html', context)


class WorksheetEditView (View):
    """
    Класс для подгрузки страницы изменения анкеты и взаимодействия с ней
    Шаблон страницы - edit_worksheet.html
    """
    template_name = 'edit_worksheet.html'
    worksheet_form_class = WorksheetCreationForm

    def get_context(self, worksheet):
        """
        Функция получает словарь данных для отображения на сайте
        :param worksheet: Объект класса, содержащий информацию об анкете
        :type worksheet: Worksheet
        :return: Форму с информацией об анкете
        """
        forms = {
            'form': self.worksheet_form_class(
                initial={
                    'title': worksheet.title,
                    'tags': worksheet.tags.all(),
                    'description': worksheet.description
                }
            )
        }
        return forms

    def get(self, request, worksheet_id):
        worksheet = Worksheet.objects.get(id=worksheet_id)

        if request.user != worksheet.author.user:
            return HttpResponseForbidden()

        context = self.get_context(worksheet)

        return render(request, self.template_name, context)

    def post(self, request, worksheet_id):
        worksheet = Worksheet.objects.get(id=worksheet_id)
        context = self.get_context(worksheet)

        if request.POST.get('delete'):
            worksheet.delete()
            return redirect('/profile')

        if request.POST.get('drop'):
            worksheet.image = 'worksheets/default_image.png'
            worksheet.save()
            return render(request, self.template_name, context)

        form = self.worksheet_form_class(request.POST, request.FILES)

        if form.is_valid():
            worksheet.title = form.cleaned_data.get('title')
            worksheet.description = form.cleaned_data.get('description')
            worksheet.date = datetime.datetime.now()

            if 'image' in form.files:
                worksheet.image = form.files['image']

            worksheet.save()
            worksheet.tags.set(
                form.cleaned_data.get('tags')
            )

            return redirect(f'/worksheet{worksheet.pk}')

        return render(request, self.template_name, context)


def create(request):
    """
    Возвращает страницу создания аккаунта
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :return: страница создания аккаунта
    """
    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

    else:
        form = RegistrationForm()

    context['form'] = form

    return render(request, 'registration/create.html', context)

"""
Файл для форм
"""

from django.core.exceptions import ValidationError

from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """
    Форма регистрационной страницы
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'text_field_input',
                'placeholder': 'Username'
            }
        )
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'text_field_input',
                'placeholder': 'First Name'
            }
        ),
        max_length=32,
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'text_field_input',
                'placeholder': 'Last Name'
            }
        ), max_length=32
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'text_field_input',
                'placeholder': 'Email'
            }
        ), max_length=64
    )

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text_field_input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text_field_input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class MessageForm(forms.Form):
    """
    Форма для отправления сообщений в чате
    """
    message = forms.CharField(
        required=True, widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Message'
            }
        )
    )


class ProfileEditForm(forms.Form):
    """
    Форма для страницы изменения профиля
    """
    CHOICES = [
        ('Меньше одного года', 'Меньше одного года'),
        ('До пяти лет', 'До пяти лет'),
        ('Больше пяти лет', 'Больше пяти лет')
    ]

    avatar = forms.ImageField(required=False)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )
    work = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Work'
            }
        )
    )
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Bio'
            }
        ),
        required=False
    )
    stage = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-input'
            }
        ),
        choices=CHOICES,
        required=True
    )


class SocialMediaForm (forms.Form):
    """
    Отдельная форма для добавления ссылок на социальные сети пользователя
    """
    instagram_field = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Instagram',
            }
        ),
        max_length=100,
        required=False
    )
    vk_field = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Vk',
            }
        ),
        max_length=100,
        required=False
    )
    github_field = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Github',
            }
        ),
        max_length=100,
        required=False
    )
    codewars_field = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Codewars',
            }
        ),
        max_length=100,
        required=False
    )


class UserEditForm(forms.ModelForm):
    """
    Форма для отображения данных профиля пользователя
    """
    class Meta:
        """
        Хранит метаданные и атрибуты html элементов
        """
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username',
                    'id': 'floatingInputUsername'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First name',
                    'id': 'floatingInputFirstName'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last name',
                    'id': 'floatingInputLastName'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email',
                    'id': 'floatingInputEmail'
                }
            )
        }


class WorksheetCreationForm(forms.Form):
    """
    Форма для создания анкеты
    """
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                'id': 'floatingInput'
            }
        )
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-check-input'
            }
        )
    )
    image = forms.ImageField(
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Leave a comment here',
                'id': 'floatingTextArea'
            }
        )
    )


class SearchForm(forms.Form):
    """
    Форма для поиска по анкетам
    """
    tags_search_field = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-check-input'
            }
        ),
    )

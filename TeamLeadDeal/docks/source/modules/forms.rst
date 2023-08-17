#######################
Используемые формы
#######################

Здесь описаны все формы, которые мы использовали в проекте.

``class RegistrationForm(UserCreationForm)`` - класс для описания формы регистрации
на сайт. Для регистрации нужны следующие поля: username, first_name, last_name, email, password1,
password2.

``class MessageForm(forms.Form)`` - Форма для отправления сообщений в чате.

``class ProfileEditForm(forms.Form)`` - Форма для страницы изменения профиля пользователя. Поля
формы: avatar, tags, work, bio, stage. Стаж можно указать, выбрав из трех вариантов: 'Меньше одного года',
'До пяти лет', 'Больше пяти лет'.

``class SocialMediaForm (forms.Form)`` - Отдельная форма для добавления ссылок на социальные сети
пользователя. Поля формы: instagram_field, vk_field, github_field, codewars_field.

``class UserEditForm(forms.ModelForm)`` - Форма для отображения данных профиля пользователя. Поля:
username, email, first_name, last_name

``class WorksheetCreationForm(forms.Form)`` - Форма для создания новой анкеты. Поля формы - title,
tags, image, description.

``class SearchForm(forms.Form)`` - Форма для поиска по анкетам. Единственное поле - tags_search_field


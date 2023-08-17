#######################
View-функции
#######################

Здесь описаны все view-функции, которые мы использовали.

``class MainPageView(View)`` - класс для подгрузки главной страницы и взаимодействия с ней. Шаблон
страницы - main.html.

``class WorksheetsView(View)`` - класс для подгрузки страницы с анкетами и взаимодействия с ней.
Шаблон страницы - worksheets.html.

``class UserProfile(View)`` - класс для подгрузки страринцы профиля и взаимодействия с ней. Шаблон
страницы - user_page.html.

``class UserChat(TemplateView)`` - класс для подгрузки страницы с чатом и взаимодействия с ней.
Шаблон страницы - chat.html.

``class ProfileView(View)`` - класс для подгрузки страницы профиля и взаимодействия с ней. Шаблон
страницы - users.html.

``class ProfileEditView (View)`` - класс для подгрузки страницы редактирования профиля и
взаимодействия с ней. Шаблон страницы - edit.html.

``class WorksheetEditView(View)`` - класс для подгрузки страницы изменения анкеты и взаимодействия с ней.
Шаблон страницы - edit_worksheet.html

``function worksheet_creation(request)`` - возвращает страницу создания анкеты
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :return: страница создания анкеты

``function worksheet_show(request, worksheet_id)`` - возвращает страницу анкеты
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :param worksheet_id: ID анкеты
    :type worksheet_id: int
    :return: страница анкеты

``function create(request)`` - возвращает страницу создания аккаунта
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :return: страница создания аккаунта

``function worksheet_index_ajax_get(request, worksheets_count)`` - Возвращает несколько анкет
    :param request: объект с деатялми запроса
    :type request: 'django.http.HttpRequest'
    :param worksheets_count: количество анкет для подгрузки, константа
    :type worksheets_count: int
    :return: JSON ответ с анкетами

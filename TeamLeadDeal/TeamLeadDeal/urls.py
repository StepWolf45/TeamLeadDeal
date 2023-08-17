"""TeamLeadDeal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import *
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainPageView.as_view()),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/', PasswordResetView.as_view(), name='password_reset'),
    path(r'reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('create/', views.create, name='create'),
    path('profile/', login_required(views.profile, login_url='/login/'), name='profile'),
    path('profile/edit/', login_required(views.ProfileEditView.as_view(), login_url='/login/'), name='edit'),

    path('worksheets/', views.WorksheetsView.as_view()),
    path('worksheet/create/', login_required(views.worksheet_creation, login_url='/login/'), name='worksheet_create'),
    path('worksheet<int:worksheet_id>/', login_required(views.worksheet_show, login_url='/login/'), name='worksheet'),
    path('worksheet<int:worksheet_id>/edit/', login_required(views.WorksheetEditView.as_view(), login_url='/login/'),
         name='worksheet_edit'),

    path('id<int:pk>/', views.UserProfile.as_view(), name='user_profile'),
    path('id<int:pk>/chat/', login_required(views.UserChat.as_view(), login_url='/login/'), name='user_chat'),
    path('messages/', login_required(views.chats, login_url='/login/'), name='messages'),

    path('users/', views.ProfileView.as_view(), name='users'),

    path('messages/data/<int:user_pk>', login_required(views.messages_data, login_url='/login/'), name='messages_data'),
    path('worksheet/data/<int:worksheet_pk>',
         login_required(views.note_data_post, login_url='/login/'), name='worksheet_data'),
    path('worksheets/data/<int:worksheets_count>', views.worksheet_index_ajax_get, name='worksheets_data'),
    path('worksheets/data/delete', views.comment_data_delete, name='worksheets_data_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

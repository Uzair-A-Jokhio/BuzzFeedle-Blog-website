from django.urls import path
from . import views
from .views import UserEditView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('edit_profile/', UserEditView.as_view() , name='edit_profile'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='authen/change_password.html')),
    path('password/', PasswordsChangeView.as_view() ),
    path("password_success/", views.password_sucess, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile' ),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page' ),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page' ),
]
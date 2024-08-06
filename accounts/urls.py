from django.urls import path
from .views import UserRegisterView, UserEditView, PasswordChangeView, password_success, ShowProfilePageView, EditProfilePageView, CreateUserProfilePageView, LoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name= 'register'),
    path('edit_profile/', UserEditView.as_view(), name= 'edit_profile'),
    path('password/', PasswordChangeView.as_view()),
    path('password_success/', password_success, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile/', CreateUserProfilePageView.as_view(), name='create_profile_page'),
    path('login/', LoginView, name='login'),
    
      
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserAuthentication.as_view(), name='auth homepage'),
    path('login/', views.UserAuthentication.login, name='auth login'),
    path('register/', views.UserAccountCRUD.Create.as_view(), name='auth register'),
    path('user_info/', views.UserInfoCRUD.Create.as_view(), name='auth register'),
]
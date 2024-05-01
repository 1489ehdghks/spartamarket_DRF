from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/', views.accounts_signup, name='signup'),
    path("token/refresh/", views.accounts_refresh_token, name="token_refresh"),
    path('login/', views.accounts_login, name='login'),
    path('<str:username>/', views.accounts_detail, name='profile'),
]

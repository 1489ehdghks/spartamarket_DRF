from django.urls import path
from .views import accounts_signup, accounts_detail, accounts_login, accounts_password
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = "accounts"
urlpatterns = [
    path('signup/', accounts_signup, name='accounts_signup'),
    path('login/', accounts_login, name='accounts_login'),
    path('<str:username>/', accounts_detail, name='profile'),
    path('<str:username>/password/', accounts_password, name='accounts_password'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

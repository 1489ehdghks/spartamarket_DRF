from django.urls import path
from .views import accounts_signup, accounts_detail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = "accounts"
urlpatterns = [
    path('signup/', accounts_signup, name='accounts_signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<str:username>/', accounts_detail, name='profile'),
]

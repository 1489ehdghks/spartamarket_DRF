from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("json-drf/", views.json_drf, name="json_drf"),
    path("", views.product_list, name="product_list"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
]

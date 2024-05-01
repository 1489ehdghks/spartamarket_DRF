from rest_framework import serializers
from accounts.views import User
from django.contrib.auth import get_user_model
from .models import Products


User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('author',)

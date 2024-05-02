from rest_framework import serializers
from .models import Accounts
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    # 비밀번호 해싱
    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_birth_date(self, value):
        if value is None:
            raise ValidationError("Birth date cannot be null.")
        return value

    class Meta:
        model = Accounts
        fields = ['username', 'email', 'name', 'nickname',
                  'birth_date', 'gender', 'features', 'password']
        # 비밀번호 표시x
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = Accounts.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            birth_date=validated_data.get('birth_date'),
            gender=validated_data.get('gender', ''),
            features=validated_data.get('features', ''),
            password=validated_data['password']
        )
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'nickname',
                  'birth_date', 'gender', 'features']
        extra_kwargs = {
            'name': {'required': True},
        }

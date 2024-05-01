from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Accounts
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        # 비밀번호 유효성 검사
        validate_password(value)
        # 비밀번호 해싱
        return make_password(value)

    def validate_birth_date(self, value):
        if value is None:
            raise ValidationError("Birth date cannot be null.")
        return value

    class Meta:
        model = Accounts
        fields = ['username', 'email', 'name', 'nickname',
                  'birth_date', 'gender', 'features', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Accounts.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            birth_date=validated_data.get('birth_date'),
            gender=validated_data.get('gender', ''),
            features=validated_data.get('features', ''),
            password=make_password(validated_data['password'])
        )
        user.save()
        return user

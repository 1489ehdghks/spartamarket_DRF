from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Accounts


class UserSerializer(serializers.ModelSerializer):
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

from django.contrib.auth.models import AbstractUser
from django.db import models


class Accounts(AbstractUser):
    email = models.EmailField(
        default='', max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(
        default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100,
                            null=False, blank=False)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=(
        ('M', 'Male'), ('F', 'Female')), blank=True)
    features = models.TextField(blank=True)


# username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능

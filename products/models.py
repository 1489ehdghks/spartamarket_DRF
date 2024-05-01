from django.db import models


class Products(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


# 로그인 상태, 제목과 내용, 상품 이미지 입력 필요.

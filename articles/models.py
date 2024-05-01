from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

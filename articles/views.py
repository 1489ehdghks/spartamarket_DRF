from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Article
from django.core import serializers


def article_list_html(request):
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, "articles/articles.html", context)


def json_01(request):
    articles = Article.objects.all()
    json_res = []

    for article in articles:
        json_res.append(
            {
                "title": article.title,
                "content": article.content,
                "created_at": article.created_at,
                "updated_at": article.updated_at,
            }
        )

    return JsonResponse(json_res, safe=False)


def json_02(request):
    articles = Article.objects.all()
    res_data = serializers.serialize("json", articles)
    return HttpResponse(res_data, content_type="application/json")

from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from products.models import Products
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def json_drf(request):
    paginator = PageNumberPagination()
    paginator.page_size = 8
    products = Products.objects.all()
    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


class ProductList(generics.ListCreateAPIView):

    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 8
        products = Products.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        self.permission_classes = [IsAuthenticated]  # 얘만 적용
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        product.delete()
        data = {"delete": f"({pk})번째 Product 삭제됨"}
        return Response(data, status=status.HTTP_200_OK)

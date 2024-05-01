from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from products.models import Products
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def json_drf(request):
    products = Products.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def product_list(request):
    if request.method == "GET":
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        data = {"delete": f"Article({pk}) is deleted."}
        return Response(data, status=status.HTTP_200_OK)

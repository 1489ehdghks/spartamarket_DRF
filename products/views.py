from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from products.models import Products
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def json_drf(request):
    products = Products.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# 상품 등록
# - **조건**: 로그인 상태, 제목과 내용, 상품 이미지 입력 필요.
# - **구현**: 새 게시글 생성 및 데이터베이스 저장.

# 상품 목록 조회
# - **조건**: 로그인 상태 불필요.
# - **구현**: 모든 상품 목록 페이지네이션으로 반환.


class ProductList(generics.ListCreateAPIView):

    def get(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.permission_classes = [IsAuthenticated]  # 편함
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# - **상품 수정**
#     - **조건**: 로그인 상태, 수정 권한 있는 사용자(게시글 작성자)만 가능.
#     - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
#     - **구현**: 입력된 정보로 기존 상품 정보를 업데이트.

# - **상품 삭제**
#     - **조건**: 로그인 상태, 삭제 권한 있는 사용자(게시글 작성자)만 가능.
#     - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
#     - **구현**: 해당 상품을 데이터베이스에서 삭제.


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

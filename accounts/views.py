from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import Accounts
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


User = get_user_model()


@api_view(["POST", "GET"])
def accounts_signup(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == "GET":
    #     if not email:
    #         raise ValueError('must have user email')
    #     if not nickname:
    #         raise ValueError('must have user nickname')
    #     if not name:
    #         raise ValueError('must have user name')
    #     user = self.model(
    #         email=self.normalize_email(email),
    #         nickname=nickname,
    #         name=name
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user


@api_view(['POST'])
def accounts_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': '리퀘'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accounts_detail(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'error': '뭔가가 없는거 같애.'}, status=status.HTTP_403_FORBIDDEN)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def accounts_detail(self, request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         if email and Accounts.objects.object.filter(email=email).exist():
#             return Response({'message': '이메일 중복'}, status=400)
#         user = serializer.save()
#         password = serializer.validated_data['password']
#         user.set_password(password)
#         user.save()
#         return Response({'message': '비밀번호 수정성공', 'userId': user.id}, status=201)
#     else:
#         return Response(serializer.errors, status=400)

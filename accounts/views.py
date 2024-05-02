from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


User = get_user_model()


@api_view(["POST"])
def accounts_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def accounts_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    print("user:", user)
    print("Username:", username)
    print("Password:", password)
    if user:
        refresh = TokenObtainPairSerializer.get_token(user=user)
        data = {
            'user_id': user.id,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'error': '11111111'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def accounts_detail(request, username):
    if request.method == "GET":
        user = get_object_or_404(User, username=username)
        if user == request.user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': "에휴 또냐"}, status=status.HTTP_403_FORBIDDEN)

    elif request.method == "PUT":
        user = get_object_or_404(User, username=username)

        if user != request.user:
            return Response({"error": "본인의 정보만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserUpdateSerializer(
            user, data=request.data, context={'request': request})

        # 변경 전 데이터
        original_data = {
            "email": user.email,
            "name": user.name,
            "nickname": user.nickname,
            "birth_date": str(user.birth_date),
            "gender": user.gender,
            "features": user.features
        }
        if serializer.is_valid():
            serializer.save()

            # 변경된 데이터 확인
            updated_data = serializer.data
            changes = {field: updated_data[field]
                       for field in original_data if original_data[field] != updated_data[field]}

            if changes:
                response_data = {
                    "message": "정보가 업데이트 되었습니다.", "original_data": original_data, "changes": changes}
            else:
                response_data = {"message": "변경된 정보가 없습니다."}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accounts_password(request, username):
    user = get_object_or_404(User, username=username)
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if not user.check_password(old_password):
        return Response({'error': '기존 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({'message': '비밀번호 변경됨', 'userId': user.id}, status=status.HTTP_200_OK)

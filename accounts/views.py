from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

User = get_user_model()


@api_view(["POST"])
def accounts_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def accounts_signup(self, email, nickname, name, password=None):
    if not email:
        raise ValueError('must have user email')
    if not nickname:
        raise ValueError('must have user nickname')
    if not name:
        raise ValueError('must have user name')
    user = self.model(
        email=self.normalize_email(email),
        nickname=nickname,
        name=name
    )
    user.set_password(password)
    user.save(using=self._db)
    return user


@api_view(['POST'])
def accounts_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accounts_detail(request, username):
    user = User.objects.get(username=username)
    if user == request.user:
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'error': 'You do not have permission to view this profile.'}, status=status.HTTP_403_FORBIDDEN)


def accounts_refresh_token():
    pass

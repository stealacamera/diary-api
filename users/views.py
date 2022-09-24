from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serialized = serializers.RegisterSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        
        account = serialized.save()
        
        refresh = RefreshToken.for_user(account)
        data = {'username': account.username,
                'email': account.email,
                'tokens': {'refresh': str(refresh),
                           'access': str(refresh.access_token)}}
        
        return Response(data, status=status.HTTP_201_CREATED)

class ChangePasswordView(APIView):
    def post(self, request):
        serialized = serializers.ChangePasswordSerializer(data=request.data, context={'request': request})
        serialized.is_valid(raise_exception=True)
        
        serialized.save()
        return Response('Password changed successfully! Please log back in.', status=status.HTTP_200_OK)

class CurrentProfileView(APIView):
    def get(self, request):
        serialized = serializers.UserSerializer(request.user)        
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serialized = serializers.ChangeUsernameSerializer(data=request.data, context={'request': request})
        serialized.is_valid(raise_exception=True)
        
        serialized.save()
        return Response('Username changed successfully!', status=status.HTTP_200_OK)

class ProfileDisplay(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
    permission_classes = [IsAdminUser]
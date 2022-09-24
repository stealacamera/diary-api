from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['current_streak', 'best_streak']

class UserSerializer(serializers.ModelSerializer):
    num_of_entries = serializers.SerializerMethodField()
    streaks = ProfileSerializer(read_only=True, source='profile')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'num_of_entries', 'streaks']
    
    def get_num_of_entries(self, obj):
        return obj.user_entries.filter(deleted=False).count()

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is taken.')
        
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is in use by another account.')

        return value
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError('Passwords do not match.')
        
        account = User(username=self.validated_data['username'],
                       email = self.validated_data['email'])
        account.set_password(password)
        account.save()
        
        return account

class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField()
    
    def validate_new_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is taken.')
        
        return value

    def save(self):
        account = self.context['request'].user
        account.username = self.validated_data['new_username']
        account.save()
        

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    refresh = serializers.CharField()
    
    def validate_current_password(self, value):
        account = self.context['request'].user
        
        if not account.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        
        return value
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self):
        try:
            account = self.context['request'].user
            new_password = self.validated_data['new_password']
            
            if new_password == self.validated_data['current_password']:
                raise serializers.ValidationError('New password has to be different from the current one.')

            account.set_password(new_password)
            account.save()
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError('Token is invalid or expired.')
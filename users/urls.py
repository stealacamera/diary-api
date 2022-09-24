from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.routers import DefaultRouter

from .views import RegisterView, CurrentProfileView, ProfileDisplay, ChangePasswordView

router = DefaultRouter()
router.register('profiles', ProfileDisplay, basename='profile')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('profile/', CurrentProfileView.as_view(), name='current-profile'),
    path('', include(router.urls)),
]

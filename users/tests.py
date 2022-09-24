from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class RegisterLoginTestCase(APITestCase):
    def setUp(self):
        data = {'username': 'example',
                'email': 'example@user.com',
                'password': 'pass123',
                'password2': 'pass123'}
               
        self.client.post(reverse('register'), data)
    
    def test_register(self):
        data = {'username': 'example2',
                'email': 'example2@user.com',
                'password': 'pass123',
                'password2': 'pass123'}
               
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login(self):
        data = {'username': 'example',
                'password': 'pass123'}
               
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='example', password='pass123')
        
        user_data = {'username': user.username,
                     'password': 'pass123'}
        token = self.client.post(reverse('login'), user_data, format='json')
        self.refresh_token = token.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.data['access']))
    
    def test_currentprofile(self):
        response = self.client.get(reverse('current-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_userprofiles_user(self):
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_userprofiles_admin(self):
        admin_user = User.objects.create_superuser(username='adminuser', password='pass123')

        data = {'username': admin_user.username,
                'password': 'pass123'}
        token_response = self.client.post(reverse('login'), data, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token_response))
        
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_changepassword(self):
        data = {'current_password': 'pass123',
                'new_password': 'password',
                'refresh': self.refresh_token}
        
        response = self.client.post(reverse('change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_changeusername(self):
        data = {'new_username': 'new_name'}
        
        response = self.client.post(reverse('current-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
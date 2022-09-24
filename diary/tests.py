from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Entry, Tag, Folder

class FolderTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='example', password='pass123')
        
        user_data = {'username': user.username,
                     'password': 'pass123'}
        token = self.client.post(reverse('login'), user_data, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
        
        user2 = User.objects.create_user(username='example2', password='pass123')
        Folder.objects.create(name='duplicate', user=user2)
        
        self.folder = Folder.objects.create(name='folder', user=user)
    
    def test_createfolder(self):
        data = {'name': 'duplicate'}
         
        response = self.client.post(reverse('folder-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def  test_getfolder(self):
        response = self.client.get(reverse('folder-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('folder-detail', args=(self.folder.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updatefolder(self):
        data = {'name': 'updated'}
        
        response = self.client.put(reverse('folder-detail', args=(self.folder.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_deletefolder(self):
        response = self.client.delete(reverse('folder-detail', args=(self.folder.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TagTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='example', password='pass123')
        
        user_data = {'username': user.username,
                     'password': 'pass123'}
        token = self.client.post(reverse('login'), user_data, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
        
        user2 = User.objects.create_user(username='example2', password='pass123')
        Tag.objects.create(name='duplicate', user=user2)
        
        self.tag = Tag.objects.create(name='tag', user=user)
    
    def test_createtag(self):
        data = {'name': 'duplicate'}
         
        response = self.client.post(reverse('tag-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def  test_gettag(self):
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('tag-detail', args=(self.tag.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updatetag(self):
        data = {'name': 'updated'}
        
        response = self.client.put(reverse('tag-detail', args=(self.tag.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_deletetag(self):
        response = self.client.delete(reverse('tag-detail', args=(self.tag.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class EntryTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='example', password='pass123')
        
        user_data = {'username': user.username,
                     'password': 'pass123'}
        token = self.client.post(reverse('login'), user_data, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
        
        user2 = User.objects.create_user(username='example2', password='pass123')
        Tag.objects.create(name='duplicate', user=user2)
        Folder.objects.create(name='duplicate', user=user2)
        
        self.entry = Entry.objects.create(text='existing entry', user=user)
        self.tag = Tag.objects.create(name='duplicate', user=user)
        self.folder = Folder.objects.create(name='duplicate', user=user)
    
    def test_createentry(self):
        data = {'text': 'example entry',
                'folder': '',
                'tags': []}
         
        response = self.client.post(reverse('entry-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def  test_getentry(self):
        response = self.client.get(reverse('entry-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('entry-detail', args=(self.entry.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updateentry(self):
        data = {'folder': self.folder,
                'tags': [self.tag]}
        
        response = self.client.patch(reverse('entry-detail', args=(self.entry.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_deleteentry(self):
        response = self.client.delete(reverse('entry-detail', args=(self.entry.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
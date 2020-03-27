from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task, Tag
import json

class TaskTests(APITestCase):
    def setUp(self):
        user = User(email='exem@qwerty.com', username='User1')
        user.set_password('qwerty')
        user.save()
        user2 = User(email='exem1@qwerty.com', username="User2")
        user2.set_password('qwerty')
        user2.save()
        Task.objects.create(title='Django', description='Django rest framework', 
        status=False, finish_date='2020-04-01T00:00', owner=user)
        Task.objects.create(title='Rest framework', description='WOW', 
        status=True, finish_date='2020-03-31T00:00', owner=user2)

    def test_list_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        result = json.loads(response.content)['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result[0]['title'], 'Django')
        self.assertEqual(result[1]['title'], 'Rest framework')

    def test_create_tasks(self):
        url = reverse('task-list')
        self.client.login(username='User1', password='qwerty')
        data = {'title': 'Test task', 'description': 'Test description',
        'status': 'False', 'finish_date': '2020-03-31T00:00'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)['title'], 'Test task')
        self.client.logout()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_task(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django')

    def test_put_task(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        self.client.login(username='User1', password='qwerty')
        data = {'title': 'Put task', 'description': 'Test description',
        'status': 'False', 'finish_date': '2020-03-31T00:00', 'owner': 'User1'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Put task')
        self.client.logout()
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username='User2', password='qwerty')
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': 2})
        self.client.login(username='User1', password='qwerty')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username='User2', password='qwerty')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TagTests(APITestCase):
    def setUp(self):
        user = User(email='exem@qwerty.com', username='User1')
        user.set_password('qwerty')
        user.save()
        user2 = User(email='exem1@qwerty.com', username="User2")
        user2.set_password('qwerty')
        user2.save()
        Tag.objects.create(title='Python', owner=user)
        Tag.objects.create(title='PHP', owner=user2)
        Task.objects.create(title='Django', description='Django rest framework', 
        status=False, finish_date='2020-04-01T00:00', owner=user)

    def test_list_tags(self):
        url = reverse('tag-list')
        response = self.client.get(url)
        result = json.loads(response.content)['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result[0]['title'], 'Python')
        self.assertEqual(result[1]['title'], 'PHP')

    def test_create_tags(self):
        url = reverse('tag-list')
        self.client.login(username='User1', password='qwerty')
        data = {'title': 'Test tag', 'tasks': [1]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test tag')
        self.client.logout()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_tag(self):
        url = reverse('tag-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Python')

    def test_put_tag(self):
        url = reverse('tag-detail', kwargs={'pk': 1})
        self.client.login(username='User1', password='qwerty')
        data = {'title': 'Put tag', 'tasks': [1]}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Put tag')
        self.client.logout()
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username='User2', password='qwerty')
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_tag(self):
        url = reverse('tag-detail', kwargs={'pk': 2})
        self.client.login(username='User1', password='qwerty')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username='User2', password='qwerty')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RegisterTests(APITestCase):
    def test_register(self):
        url = reverse('register-list')
        data = {'email': 'qwer@arw.com', 'username': 'Testuser', 'password': 'qwerty'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'username': 'Testuser'})
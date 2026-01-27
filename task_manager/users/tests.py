from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

# Create your tests here.

class UserCRUDTest(TestCase):

    def setUp(self):
        # суперпользователь для авторизации
        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='pass')
        self.client.login(username='admin', password='pass')
    
    def test_create_user_message(self):
        response = self.client.post(reverse('users:user_create'), {
            'username': 'flashuser',
            'email': 'flash@test.com',
            'password': '12345'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно создан" in str(m) for m in messages))
        self.assertRedirects(response, reverse('login'))  # проверка на редирект на логин

    def test_update_user_message(self):
        user = User.objects.create_user(username='updateuser', password='12345')
        response = self.client.post(reverse('users:user_update', args=[user.id]), {
            'username': 'updated',
            'email': 'updated@test.com'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("был изменен" in str(m) for m in messages))

    def test_delete_user_message(self):
        user = User.objects.create_user(username='deluser', password='12345')
        response = self.client.post(reverse('users:user_delete', args=[user.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно удален" in str(m) for m in messages))

    def test_create_user(self):
        response = self.client.post(reverse('users:user_create'), {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # редирект после создания
        self.assertRedirects(response, reverse('login'))  # проверка на редирект на логин
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_update_user(self):
        user = User.objects.create_user(username='updateuser', password='12345')
        response = self.client.post(reverse('users:user_update', args=[user.id]), {
            'username': 'updated',
            'email': 'updated@test.com'
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.username, 'updated')
        self.assertEqual(user.email, 'updated@test.com')

    def test_delete_user(self):
        user = User.objects.create_user(username='deluser', password='12345')
        response = self.client.post(reverse('users:user_delete', args=[user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='deluser').exists())


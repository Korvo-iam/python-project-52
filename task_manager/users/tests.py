from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.

class UserCRUDTest(TestCase):

    def setUp(self):  # суперпользователь для авторизации
        self.admin = User.objects.create_superuser(
            username='admin',
            password='pass')
        self.client.login(username='admin', password='pass')
    
    def test_create_user_message(self): #проверка flash успешного создания
        response = self.client.post(reverse('users:user_create'), {
            'username': 'flashuser',
            'first_name': 'flash',
            'last_name': 'user',
            'password1': '12345',
            'password2': '12345'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                "успешно зарегистрирован" in str(m) for m in messages))
        self.assertRedirects(response, reverse('login')) #проверка на редирект на логин  # noqa: E501

    def test_update_user_message(self): #проверка flash успешного обновления
        user = User.objects.create_user(username='updateuser', password='12345')
        response = self.client.post(
            reverse(
                'users:user_update',
                args=[user.id]),
            {
            'username': 'updated',
            'first_name': 'updated',
            'last_name': 'user',
            'password1': '12345',
            'password2': '12345'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно изменен" in str(m) for m in messages))

    def test_delete_user_message(self): #проверка flash успешного удаления
        user = User.objects.create_user(username='deluser', password='12345')
        response = self.client.post(reverse(
            'users:user_delete',
            args=[user.id]),
            follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно удален" in str(m) for m in messages))

    def test_create_user(self): #проверка создания пользователя
        response = self.client.post(reverse('users:user_create'), {
            'username': 'testuser',
            'first_name': 'test',
            'last_name': 'user',
            'password1': '12345',
            'password2': '12345'
        })
        self.assertEqual(response.status_code, 302)  # редирект после создания
        self.assertRedirects(response, reverse('login'))  # проверка на редирект на логин  # noqa: E501
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_update_user(self): #проверка обновления пользователя
        user = User.objects.create_user(username='updateuser', password='12345')
        response = self.client.post(
            reverse('users:user_update', args=[user.id]),
            {
                'username': 'updated',
                'first_name': 'updated',
                'last_name': 'user',
                'password1': '123456',
                'password2': '123456'
            }
        )
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.username, 'updated')

    def test_delete_user(self):
        user = User.objects.create_user(username='deluser', password='12345')
        response = self.client.post(
            reverse(
            'users:user_delete',
            args=[user.id]),
            follow=True)
        messages = list(get_messages(response.wsgi_request)) #проверка flash-сообщения  # noqa: E501
        self.assertTrue(any("успешно удален" in str(m) for m in messages))
        self.assertFalse(User.objects.filter(username='deluser').exists()) #проверка удаления пользователя  # noqa: E501

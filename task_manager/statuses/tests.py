from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status
from django.contrib.messages import get_messages

# Create your tests here.

class StatusCRUDTest(TestCase):

    def setUp(self):
        # создаём суперпользователя для авторизации
        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='pass')
        self.client.login(username='admin', password='pass')

    def test_create_status_message(self):
        response = self.client.post(reverse('statuses:create'), {'name': 'Flash тест'}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно создан" in str(m) for m in messages))

    def test_update_status_message(self):
        status = Status.objects.create(name='Старый')
        response = self.client.post(reverse('statuses:update', args=[status.id]), {'name': 'Новый'}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно изменен" in str(m) for m in messages))

    def test_delete_status_message(self):
        status = Status.objects.create(name='Удаляемый')
        response = self.client.post(reverse('statuses:delete', args=[status.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно удалён" in str(m) for m in messages))

    def test_list_statuses(self):
        Status.objects.create(name='Новый')
        Status.objects.create(name='В работе')
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новый')
        self.assertContains(response, 'В работе')

    def test_create_status(self):
        response = self.client.post(reverse('statuses:create'), {'name': 'Тестовый статус'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Тестовый статус').exists())

    def test_update_status(self):
        status = Status.objects.create(name='Старый статус')
        response = self.client.post(reverse('statuses:update', args=[status.id]), {'name': 'Новый статус'})
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, 'Новый статус')

    def test_delete_status(self):
        status = Status.objects.create(name='Удаляемый статус')
        response = self.client.post(reverse('statuses:delete', args=[status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(name='Удаляемый статус').exists())

    def test_access_requires_login(self):
        # выходим из аккаунта
        self.client.logout()
        response = self.client.get(reverse('statuses:list'))
        self.assertRedirects(response, '/login/?next=/statuses/')  # редирект на логин


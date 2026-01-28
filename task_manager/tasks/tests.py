from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.messages import get_messages

class TaskCRUDTest(TestCase):

    def setUp(self):
        # создаём суперпользователя и авторизуемся
        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='pass')
        self.client.login(username='admin', password='pass')

        # создаём статус для задач
        self.status = Status.objects.create(name='Новый')

    def test_create_task_message(self):
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'Flash задача',
            'description': 'Описание тестовой задачи',
            'status': self.status.id,
            'executor': self.admin.id,
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Задача успешно создана!" in str(m) for m in messages))
        self.assertRedirects(response, reverse('tasks:task_list'))

    def test_update_task_message(self):
        task = Task.objects.create(
            name='Старая задача',
            description='Описание',
            status=self.status,
            author=self.admin
        )
        response = self.client.post(reverse('tasks:task_update', args=[task.id]), {
            'name': 'Новая задача',
            'description': 'Новое описание',
            'status': self.status.id,
            'executor': self.admin.id,
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Задача успешно обновлена!" in str(m) for m in messages))

    def test_delete_task_message(self):
        task = Task.objects.create(
            name='Удаляемая задача',
            description='Описание',
            status=self.status,
            author=self.admin
        )
        response = self.client.post(reverse('tasks:task_delete', args=[task.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("была успешно удалена!" in str(m) for m in messages))

    def test_create_task(self):
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'Тестовая задача',
            'description': 'Описание',
            'status': self.status.id,
            'executor': self.admin.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Тестовая задача').exists())

    def test_update_task(self):
        task = Task.objects.create(
            name='Старая задача',
            description='Описание',
            status=self.status,
            author=self.admin
        )
        response = self.client.post(reverse('tasks:task_update', args=[task.id]), {
            'name': 'Обновленная задача',
            'description': 'Новое описание',
            'status': self.status.id,
            'executor': self.admin.id,
        })
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Обновленная задача')
        self.assertEqual(task.description, 'Новое описание')

    def test_delete_task(self):
        task = Task.objects.create(
            name='Удаляемая задача',
            description='Описание',
            status=self.status,
            author=self.admin
        )
        response = self.client.post(reverse('tasks:task_delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Удаляемая задача').exists())

    def test_access_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:task_list'))
        self.assertRedirects(response, '/login/?next=/tasks/')

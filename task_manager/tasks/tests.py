from django.test import TestCase
from django.urls import reverse
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your tests here.

class TaskCRUDTest(TestCase):

    def setUp(self): #создание суперпользователя
        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='pass')  # noqa: E501
        self.client.login(username='admin', password='pass')
        self.status = Status.objects.create(name='Новый')# создаём статус для задач

    def test_create_task_message(self): #проверка flash успешного создания
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'Flash задача',
            'description': 'Описание тестовой задачи',
            'status': self.status.id,
            'executor': self.admin.id,
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Задача успешно создана!" in str(m) for m in messages))
        self.assertRedirects(response, reverse('tasks:task_list'))

    def test_update_task_message(self): #проверка flash успешного изменения
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
        self.assertTrue(any("Задача успешно изменена!" in str(m) for m in messages))

    def test_delete_task_message(self): #проверка flash успешного удаления
        task = Task.objects.create(
            name='Удаляемая задача',
            description='Описание',
            status=self.status,
            author=self.admin
        )
        response = self.client.post(reverse('tasks:task_delete', args=[task.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Задача успешно удалена!" in str(m) for m in messages))

    def test_create_task(self): #проверка создания задачи
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'Тестовая задача',
            'description': 'Описание',
            'status': self.status.id,
            'executor': self.admin.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Тестовая задача').exists())

    def test_update_task(self): #проверка изменения задачи
        task = Task.objects.create(
            name='Старая задача',
            description='Описание',
            status=self.status,
            author=self.admin
        )
        response = self.client.post(reverse('tasks:task_update', args=[task.id]), {
            'name': 'Измененная задача',
            'description': 'Новое описание',
            'status': self.status.id,
            'executor': self.admin.id,
        })
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Измененная задача')
        self.assertEqual(task.description, 'Новое описание')

    def test_delete_task(self): #проверка удаления задачи
        task = Task.objects.create(
            name='Удаляемая задача',
            description='Описание',
            status=self.status,
            author=self.admin
        )
        response = self.client.post(reverse('tasks:task_delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Удаляемая задача').exists())

    def test_access_requires_login(self): #проверка на безуспешность просмотра списка пользователей неавторизованным пользователем
        self.client.logout()
        response = self.client.get(reverse('tasks:task_list'))
        self.assertRedirects(response, '/login/?next=/tasks/')

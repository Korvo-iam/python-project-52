from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from .models import Label
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your tests here.

class LabelCRUDTest(TestCase):

    def setUp(self): #создание суперпользователя
        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='pass')
        self.client.login(username='admin', password='pass')

    def test_create_label_message(self): #проверка flash успешного создания
        response = self.client.post(reverse('labels:create'), {'name': 'Flash метка'}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно создана" in str(m) for m in messages))

    def test_update_label_message(self): #проверка flash успешного обновления
        label = Label.objects.create(name='Старая')
        response = self.client.post(reverse('labels:update', args=[label.id]), {'name': 'Новая'}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно изменена" in str(m) for m in messages))

    def test_delete_label_message(self): #проверка flash успешного удаления
        label = Label.objects.create(name='Удаляемая')
        response = self.client.post(reverse('labels:delete', args=[label.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно удалена" in str(m) for m in messages))

    def test_list_labels(self): #проверка отображения созданных меток
        Label.objects.create(name='Метка1')
        Label.objects.create(name='Метка2')
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Метка1')
        self.assertContains(response, 'Метка2')

    def test_create_label(self): #проверка создания метки
        response = self.client.post(reverse('labels:create'), {'name': 'Тестовая метка'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Тестовая метка').exists())

    def test_update_label(self): #проверка обновления метки
        label = Label.objects.create(name='Старая метка')
        response = self.client.post(reverse('labels:update', args=[label.id]), {'name': 'Новая метка'})
        self.assertEqual(response.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, 'Новая метка')

    def test_delete_label(self): #проверка удаления метки
        label = Label.objects.create(name='Удаляемая метка')
        response = self.client.post(reverse('labels:delete', args=[label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(name='Удаляемая метка').exists())

    def test_cannot_delete_label_linked_to_task(self): #проверка невозможности удаления метки со связанной задачей
        label = Label.objects.create(name='Связанная метка')
        status = Status.objects.create(name='Новый статус')
        user = User.objects.create_user(username='user', password='pass')
        task = Task.objects.create(
            name='Задача', 
            description='Описание', 
            status=status,
            author=user
        )
        task.labels.add(label)
        response = self.client.post(reverse('labels:delete', args=[label.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("используется в задачах" in str(m) for m in messages))
        self.assertTrue(Label.objects.filter(id=label.id).exists())

    def test_access_requires_login(self): #проверка на безуспешность просмотра списка меток неавторизованным пользователем
        self.client.logout()
        response = self.client.get(reverse('labels:list'))
        self.assertRedirects(response, '/login/?next=/labels/')

class TaskFilterTest(TestCase):

    def setUp(self):
        # пользователи
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        # статусы
        self.status1 = Status.objects.create(name='Новый')
        self.status2 = Status.objects.create(name='В работе')

        # метки
        self.label1 = Label.objects.create(name='Bug')
        self.label2 = Label.objects.create(name='Feature')

        # задачи
        self.task1 = Task.objects.create(
            name='Задача 1',
            status=self.status1,
            author=self.user1,
            executor=self.user2
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Задача 2',
            status=self.status2,
            author=self.user2,
            executor=self.user1
        )
        self.task2.labels.add(self.label2)

        self.client.login(username='user1', password='pass')

    def test_filter_tasks_by_status(self):
        response = self.client.get(reverse('tasks:task_list'), {'status': self.status1.id})
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')

    def test_filter_tasks_by_executor(self):
        response = self.client.get(reverse('tasks:task_list'), {'executor': self.user2.id})
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')

    def test_filter_tasks_by_label(self):
        response = self.client.get(reverse('tasks:task_list'), {'labels': self.label1.id})
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')

    def test_filter_tasks_by_author(self):
        response = self.client.get(reverse('tasks:task_list'), {'self_tasks': 'on'})
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')
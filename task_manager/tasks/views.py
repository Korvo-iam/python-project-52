from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .filters import TaskFilter
from .models import Task

# Create your views here.

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.all()
        self.filterset = TaskFilter(
            self.request.GET,
            queryset=queryset,
            request=self.request
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'tasks'

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')
    success_message = _("Задача успешно создана!")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('tasks:task_list')
    success_message = _("Задача успешно изменена!")

    def test_func(self):
        user = self.request.user
        task = self.get_object()
        return user == task.author or user.is_superuser

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

    def test_func(self):
        user = self.request.user
        task = self.get_object()
        return user == task.author or user.is_superuser

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, _("Задача успешно удалена!"))
        return redirect(self.success_url)

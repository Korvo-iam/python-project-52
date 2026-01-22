from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Status
from .forms import StatusForm

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')
    success_message = 'Статус успешно создан!'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')
    success_message = "Статус успешно изменен!"


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses:list')

    def post(self, request, *args, **kwargs):
        #раскомментить когда появятся Task
        #if status.task_set.exists():
        #    messages.error(request, "Нельзя удалить статус, если он используется в задачах.")
        #    return redirect('statuses:list')
        self.object = self.get_object()
        name = self.object.name

        self.object.delete()
        messages.success(request, f"Статус '{name}' успешно удалён!")

        return redirect(self.success_url)
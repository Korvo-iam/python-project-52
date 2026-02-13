from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Label

# Create your views here.


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ['name']
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Метка успешно создана!')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Метка успешно изменена!')


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels:list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(request, _("Невозможно удалить метку."))
            return redirect('labels:list')
        self.object.delete()
        messages.success(request, _("Метка успешно удалена!"))
        return redirect(self.success_url)

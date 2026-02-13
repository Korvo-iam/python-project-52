from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _('Статус успешно создан!')

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _("Статус успешно изменен!")


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses:list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        try:
            self.object.delete()
            messages.success(request, _("Статус успешно удален!").format(name=name))
        except ProtectedError:
            messages.error(request,_("Невозможно удалить статус.").format(name=name))
        return redirect(self.success_url)

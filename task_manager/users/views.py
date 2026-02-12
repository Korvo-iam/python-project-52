from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserForm

User = get_user_model()

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        messages.success(self.request, _("Пользователь успешно зарегистрирован!"))
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user and not request.user.is_superuser:
            messages.error(request, _("Вы не можете редактировать чужой аккаунт."))
            return redirect('users:user_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        messages.success(self.request, _("Пользователь успешно изменен!"))
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        return form

class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, _("Пользователь успешно удален!"))
        except ProtectedError:
            messages.error(request, _("Нельзя удалить пользователя, пока у него есть задачи."))
        return redirect(self.success_url)

class LogIn(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['username'].label = 'Имя пользователя'
        form.fields['password'].label = 'Пароль'
        return form
    
    def form_valid(self, form):
        messages.success(self.request, _("Вы залогинены!"))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')

class LogOut(LogoutView):
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _("Вы разлогинены!"))
        return super().dispatch(request, *args, **kwargs)

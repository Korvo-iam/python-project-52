from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
User = get_user_model()

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'email', 'password']
    success_url = reverse_lazy('login')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['username'].label = 'Никнейм'
        form.fields['email'].label = 'E-mail адресс'
        form.fields['password'].label = 'Пароль'
        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, f"Пользователь успешно создан!")
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('users:user_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user and not request.user.is_superuser:
            messages.error(request, "Вы не можете редактировать чужой аккаунт.")
            return redirect('users:user_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Пользователь был изменен!")
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['username'].label = 'Никнейм'
        form.fields['email'].label = 'E-mail адрес'
        return form

class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        username = self.object.username
        self.object.delete()
        messages.success(request, f"Пользователь '{username}' был успешно удален!")
        return redirect(self.success_url)

class LogIn(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['username'].label = 'Никнейм'
        form.fields['password'].label = 'Пароль'
        return form
    
    def get_success_url(self):
        return reverse_lazy('home')

class LogOut(LogoutView):
    next_page = 'home'

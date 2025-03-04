from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from library.models import Reader
from django import forms


class Login(LoginView):
    template_name = 'accounts/login.html'
    next_page = '/'
    
    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.get_user().name}!')
        return super().form_valid(form)

class Logout(LogoutView):
    next_page = '/'

class ReaderCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Reader
        fields = ('username', 'email', 'name', 'phone', 'address')
        labels = {
            'username': 'Логин',
            'email': 'Электронная почта',
            'name': 'ФИО',
            'phone': 'Телефон',
            'address': 'Адрес'
        }

def register(request):
    if request.method == 'POST':
        form = ReaderCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = ReaderCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
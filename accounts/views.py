from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from library.models import Reader
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email',
            'autocomplete': 'new-email',
            'autofill': 'off'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'autocomplete': 'new-password',
            'autofill': 'off'
        }),
        label='Пароль'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = ''
        self.fields['password'].initial = ''


    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # Ищем пользователя по email
            try:
                user = Reader.objects.get(email=email)
                # Используем username пользователя для аутентификации
                self.user_cache = authenticate(username=user.username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError('Неверный email или пароль')
                else:
                    self.confirm_login_allowed(self.user_cache)
            except Reader.DoesNotExist:
                raise forms.ValidationError('Пользователь с таким email не найден')
        return self.cleaned_data

class Login(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'accounts/login.html'
    next_page = '/'
    
    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.get_user().email}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа. Проверьте введенные данные.')
        return super().form_invalid(form)

class Logout(LogoutView):
    next_page = '/'

class ReaderCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email',
            'autocomplete': 'new-email',
            'autofill': 'off'
        })
    )
    name = forms.CharField(
        label='ФИО',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ФИО',
            'autocomplete': 'off',
            'autofill': 'off'
        })
    )
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите телефон',
            'autocomplete': 'off',
            'autofill': 'off'
        })
    )
    address = forms.CharField(
        label='Адрес',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите адрес',
            'rows': 3,
            'autocomplete': 'off',
            'autofill': 'off'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'autocomplete': 'new-password',
            'autofill': 'off'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль',
            'autocomplete': 'new-password',
            'autofill': 'off'
        })
    )


    class Meta(UserCreationForm.Meta):
        model = Reader
        fields = ('email', 'name', 'phone', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.initial = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Reader.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


def register(request):
    if request.method == 'POST':
        form = ReaderCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ReaderCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

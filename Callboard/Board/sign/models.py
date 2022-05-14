from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.forms import TextInput, PasswordInput
from django.urls import reverse_lazy

"""  регистрация нового пользователя  """


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Имя юзкра")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    def get_success_url(self):
        return reverse_lazy('main')

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


""" Возможность изменения данных пользователя """


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)

        widgets = {'username': TextInput(attrs={'size': 50, 'placeholder': 'Введите логин', 'title': 'Имя пользователя'}),
                   'first_name': TextInput(attrs={'size': 50, 'placeholder': 'Введите имя'}),
                   'last_name': TextInput(attrs={'size': 50, 'placeholder': 'Введите фамилию'}),
                   'email': TextInput(attrs={'size': 50, 'placeholder': 'Введите почту'}),
                   'password1': PasswordInput(attrs={'size': 50, 'placeholder': 'Введите пароль'}),
                   'password2': PasswordInput(attrs={'size': 50, 'placeholder': 'Введите пароль ещё раз'})}


class BasicSignupForm(SignupForm):
    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, TemplateView

from .models import UserForm, BaseRegisterForm

""" Форма регистрации нового пользователя """
class BaseRegisterView(CreateView):
    model = User
    template_name = 'signup.html'
    form_class = BaseRegisterForm
    success_url = '/'

""" Редактирование профиля пользователя """
class UserProfile(UpdateView):
    template_name = 'user_profile.html'
    form_class = UserForm
    success_url = reverse_lazy('main')

    def get_object(self, **kwargs):
        user = self.request.user
        return User.objects.get(username=user)


# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'main.html'


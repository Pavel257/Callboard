from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from main.filters import AdvertFilter, ResponseFilter
from main.forms import ResponseForm, AdvertForm
from main.models import *

"""Главная страница, вывод в виде списка всех объявлений"""


class AdvertList(ListView):
    model = Advert
    template_name = 'main.html'
    context_object_name = 'Adverts'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return AdvertFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        """Добавляет filter поиска на страницу"""
        context = super().get_context_data(**kwargs)
        context['filter'] = AdvertFilter(self.request.GET, queryset=self.get_queryset())
        return context


"""Создание нового объявления"""


class AdvertCreate(CreateView):
    template_name = 'advert_create.html'
    form_class = AdvertForm
    success_url = reverse_lazy('main')
    """Автозаполнение поля user"""

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


"""Удаление объявления"""


class AdvertDelete(DeleteView):
    template_name = 'advert_delete.html'
    queryset = Advert.objects.all()
    success_url = reverse_lazy('main')


"""Вывод подробностей объявления"""


class AdvertDetail(DetailView):
    template_name = 'advert_detail.html'
    queryset = Advert.objects.all()
    form = ResponseForm
    extra_context = {'form': ResponseForm}  # простой вариант добавления переменной в шаблон

    """Функция для видимости поля откликов"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        advert_author = Advert.objects.get(id=pk).user
        current_user = self.request.user

        # проверка на то, что ты - зарегистрированный пользователь
        if current_user.is_authenticated:
            if advert_author == self.request.user:
                context['field_response'] = False
                context['message_response'] = False
                context['edit_delete'] = True  # если ты автор объявления, то скрыть поле ввода отклика

            elif Response.objects.filter(user_response=self.request.user).filter(advert=pk).exists():
                context['field_response'] = False
                context['message_response'] = True  # если ты уже ранее сделал отклик, то скрыть поле ввода отклика
                context['edit_delete'] = False

            else:
                context['field_response'] = True  # если ты не автор объявления и не сделал отклик ранее, то поле видно
                context['message_response'] = False
                context['edit_delete'] = False

        return context

    def post(self, request, *args, **kwargs):
        """form.instance - для автоматического заполнения (переопределения) полей формы instance (объект,
        вроде self, но со своими особенностями)"""
        form = ResponseForm(request.POST)
        if form.is_valid():
            form.instance.advert_id = self.kwargs.get('pk')
            form.instance.user_response = self.request.user
            form.save()

            # ссылка перехода на ту же самую страницу после выполнения POST-запроса
            # return redirect(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


"""Редактирование объявления"""


class AdvertEdit(UpdateView):
    template_name = 'advert_edit.html'
    form_class = AdvertForm
    success_url = reverse_lazy('main')

    def get_object(self, **kwargs):
        """Получает нужный объект и выводит его на страницу"""
        pk = self.kwargs.get('pk')
        return Advert.objects.get(pk=pk)


"""Фильтр и поиск объявлений"""


class AdvertSearch(ListView):
    model = Advert
    template_name = 'advert_search.html'
    context_object_name = 'advert'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """Добавляет filter поиска на страницу"""
        context = super().get_context_data(**kwargs)
        context['filter'] = AdvertFilter(self.request.GET, queryset=self.get_queryset())
        return context


"""Показывает отклики на наши объявления"""


class ResponseList(ListView):

    template_name = 'user_response.html'
    context_object_name = 'responses'
    ordering = ['-dateCreation']

    def get_queryset(self, **kwargs):
        """Создает фильтры для вывода нужных объектов.
        фильтр (advert__user) - по текущему пользователю, т.е. выводятся объявления только текущего пользователя,
        фильтры по статусу (status) - выводят еще НЕ отклоненные/принятые ранее отклики"""
        user_id = self.request.user.id
        return Response.objects.filter(advert__user=user_id).filter(status_del=False).filter(status_add=False)

    def get_context_data(self, **kwargs):
        """Для добавления новых переменных на страницу
        filter - фильтрует отклики по объявлениям
        new_response - см. выше
        del_response - выводит отклоненные отклики
        add_response - выводит принятые отклики"""
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset())
        context['new_response'] = Response.objects.filter(advert__user=user_id).filter(status_del=False). \
            filter(status_add=False)
        context['del_response'] = Response.objects.filter(advert__user=user_id).filter(status_del=True)
        context['add_response'] = Response.objects.filter(advert__user=user_id).filter(status_add=True)
        return context


"""Принятие отклика"""


class ResponseAccept(View):

    def get(self, request, *args, **kwargs):
        """Присваивает полю status_add значение = 1, (т.е. True) означает, что отклик принят, т.е. он остается в бд,
         но больше не отображается в списке новых откликов"""
        pk = self.kwargs.get('pk')
        resp = Response.objects.get(pk=pk)
        resp.status_add = 1
        resp.status_del = 0
        resp.save()

        return redirect('response')


"""Отклонение отклика (условное удаление)"""


class ResponseRemove(View):

    def get(self, request, *args, **kwargs):
        """Присваивает полю status_del значение = 1, (т.е. True) означает, что отклик принят, т.е. он остается в бд,
         но больше не отображается в списке новых откликов"""
        pk = self.kwargs.get('pk')
        respp = Response.objects.get(id=pk)
        respp.status_del = 1
        respp.status_add = 0
        respp.save()

        return redirect('response')


"""Блокировка представлений от действий незарегистрированных пользователей"""


class ProtectAdvertCreate(LoginRequiredMixin, AdvertCreate):
    permission_required = ('create',)


class ProtectAdvertDelete(LoginRequiredMixin, AdvertDelete):
    permission_required = ('delete',)


class ProtectAdvertEdit(LoginRequiredMixin, AdvertEdit):
    permission_required = ('edit',)


class ProtectResponseList(LoginRequiredMixin, ResponseList):
    permission_required = ('response',)


class ProtectResponseAccept(LoginRequiredMixin, ResponseAccept):
    permission_required = ('accept',)


class ProtectResponseRemove(LoginRequiredMixin, ResponseRemove):
    permission_required = ('remove',)



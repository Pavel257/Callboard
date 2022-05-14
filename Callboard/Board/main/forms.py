from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField, TextInput  # Импортируем true-false поле
from .models import *


"""Форма для создания/редактирования нового объявления"""


class AdvertForm(ModelForm):

    """empty_label - задает название пустого, не выбранного поля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['user'].empty_label = "Авторы не выбраны"
        self.fields['category'].empty_label = "Категории не выбраны"

    class Meta:
        """__all__ - выводит все поля, exclude - исключает указанное поле"""
        model = Advert
        fields = '__all__'
        exclude = ['user']
        """widgets - задает форматирование полей,
           size - задаёт нужный нам размер поля на странице,
           placeholder - текст в пустом поле"""
        widgets = {'title': TextInput(attrs={'size': 100, 'placeholder': 'Название объявления'})}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 120:
            raise ValidationError('Длина превышает 120 символов')

        return title


"""Форма создания отклика"""


class ResponseForm(ModelForm):

    class Meta:
        model = Response
        fields = ['text', ]
        widgets = {'text': TextInput(attrs={'size': 50, 'placeholder': 'Введите свои контакты'})}

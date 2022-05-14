from django.forms import DateInput
from django_filters import FilterSet, DateFilter, ModelChoiceFilter

from .models import *




class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = ('advert_id',)



class AdvertFilter(FilterSet):
    dateCreation = DateFilter(
        lookup_expr='gt',
        label='Позже даты',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    title = ModelChoiceFilter('title', label='Поиск по заголовкам:',
                              queryset=Advert.objects.all(), empty_label='Заголовки не выбраны',
                              )

    category = ModelChoiceFilter(queryset=Category.objects.all(), empty_label='Категории не выбраны')

    user = ModelChoiceFilter('user', label='Авторы:', queryset=User.objects.all(), empty_label='Авторы не выбраны')


    class Meta:
        model = Advert
        fields = ('user', 'category', 'title',)
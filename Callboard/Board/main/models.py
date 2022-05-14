from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

"""Модель категории"""
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название категории')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"


"""модель объявления"""

class Advert(models.Model):

    """поле content - может содержать текст, картинки, встроенные видео и другой контент"""

    title = models.CharField(max_length=128, verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name='Контент')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name="Время создания объявления")

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})


    class Meta:
        verbose_name = "Объявления"
        verbose_name_plural = "Объявления"



"""модель отклики"""

class Response(models.Model):
    """поле text содержит текст, e-mail пользователя и пр."""
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, verbose_name='Объявление')
    user_response = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отклика')
    text = models.TextField(verbose_name='Текст отклика')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата отклика')
    status_del = models.BooleanField(default=False, verbose_name='Статус отклика - отклонен')
    status_add = models.BooleanField(default=False, verbose_name='Статус отклика - принят')

    def __str__(self):
        return f'{self.user_response}'

    class Meta:
        verbose_name = "Отклики"
        verbose_name_plural = "Отклики"
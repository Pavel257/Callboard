from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response, Advert


@receiver(post_save, sender=Response)
def send_msg(instance, created, **kwargs):
    """функция-сигнал, которая срабатывает, когда в модель Response (отклики) вносятся изменения
    если создается новая запись (if created), то автору объявления отправляется письмо-уведомление,
    если автор объявления принимает отклик (elif instance.status_add), то автору отклика идет письмо"""
    user = User.objects.get(pk=instance.user_response_id)
    pk_pesponse = instance.id
    if created:
        # если создан новый отклик, то автору письма отправить письмо-уведомление

        # формирование нужный значений для письма
        pk_advert = instance.advert_id
        user = f'{user.first_name} {user.last_name}'
        user_id = Advert.objects.get(pk=pk_advert).user_id
        advert_title = Advert.objects.get(pk=pk_advert).title
        response_content = Response.objects.get(pk=pk_pesponse).text
        response_time = Response.objects.get(pk=pk_pesponse).dateCreation

        # формирование письма автору объявления
        title = f'У вас новый отклик от {str(user)[:15]}'
        msg = f'На ваше объявление "{advert_title}" пришел {str(response_time)[:19]} новый отклик\n' \
              f'от {user} следующего содержания: ' \
              f'{response_content}. Перейти в отклики http://127.0.0.1:8000/response/'
        email = 'st3p.pavel@yandex.ru'
        advert_email = User.objects.get(pk=user_id).email

        # функция отправки письма (простой вариант)
        send_mail(subject=title, message=msg, from_email=email, recipient_list=[advert_email, ])

        print("\n*************** ВЫВОД ПИСЬМА В КОНСОЛЬ (для удобства тестирования почты) *********************\n")
        print('Тема письма:', title)
        print('Контент письма:', msg)
        print('Адрес почты сервера:', email)
        print('Адрес отправления:', advert_email)
        print("\n************************************ КОНЕЦ ПИСЬМА ********************************************\n")

    elif instance.status_add:
        # если отклик принят, то автору отклика отправить письмо-уведомление

        advert_title = Advert.objects.get(pk=Response.objects.get(pk=pk_pesponse).advert_id).title
        advert_id = Advert.objects.get(pk=Response.objects.get(pk=pk_pesponse).advert_id).id
        response_time = Response.objects.get(pk=pk_pesponse).dateCreation

        title = f'У вас одобренный отклик на объявление "{str(advert_title)[:15]}"'
        msg = f'На ваш отклик от {str(response_time)[:19]} на объявление "{advert_title}" пришло положительное ' \
              f'подтверждение. Перейти на объявление http://127.0.0.1:8000/detail/{advert_id}'
        email = 'st3p.pavel@yandex.ru'
        response_email = User.objects.get(pk=Response.objects.get(pk=pk_pesponse).user_response_id).email

        send_mail(subject=title, message=msg, from_email=email, recipient_list=[response_email, ])

        print("\n*************** ВЫВОД ПИСЬМА В КОНСОЛЬ (для удобства тестирования почты) **********************\n")
        print('Тема письма:', title)
        print('Контент письма:', msg)
        print('Адрес почты сервера:', email)
        print('Адрес отправления:', response_email)
        print("\n************************************ КОНЕЦ ПИСЬМА ********************************************\n")
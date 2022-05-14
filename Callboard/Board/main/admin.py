from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Advert)
admin.site.register(Response)

admin.site.site_title = 'Админ-панель доски объявлений'
admin.site.site_header = 'Админ-панель доски объявлений'
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main.views import *

urlpatterns = [

      path('main/', AdvertList.as_view(), name='main'),
      path('', AdvertList.as_view(), name='main'),
      path('search/', AdvertSearch.as_view(), name='search'),
      path('ckeditor', include('ckeditor_uploader.urls')),
      path('detail/<int:pk>/', AdvertDetail.as_view(), name='detail'),

      # заблокированные представления (только после аутентификации)
      path('create/', ProtectAdvertCreate.as_view(), name='create'),
      path('delete/<int:pk>', ProtectAdvertDelete.as_view(), name='delete'),
      path('edit/<int:pk>', ProtectAdvertEdit.as_view(), name='edit'),
      path('response/', ProtectResponseList.as_view(), name='response'),
      path('response_accept/<int:pk>', ProtectResponseAccept.as_view(), name='accept'),
      path('response_remove/<int:pk>', ProtectResponseRemove.as_view(), name='remove'),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
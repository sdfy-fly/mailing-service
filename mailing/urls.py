from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.mail.urls')),
    path('', include('src.client.urls')),
    path('', include('src.message.urls')),
]

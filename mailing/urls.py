from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('src.mail.urls')),
    path('api/', include('src.client.urls')),
    path('api/', include('src.message.urls')),
]

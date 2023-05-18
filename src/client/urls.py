from django.urls import path, include
from rest_framework import routers

from .views import ClientView

router = routers.SimpleRouter()
router.register('client', ClientView)


urlpatterns = [
    path('', include(router.urls))
]


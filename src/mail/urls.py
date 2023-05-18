from django.urls import path, include
from rest_framework import routers
from .views import MailingView

router = routers.SimpleRouter()
router.register('mailing', MailingView)

urlpatterns = [
    path('', include(router.urls))
]
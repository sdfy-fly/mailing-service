from django.urls import path, include
from rest_framework import routers
from .views import MailingView, MailingStatsView

router = routers.SimpleRouter()
router.register('mailing/stats', MailingStatsView, basename='mailing-stats')
router.register('mailing', MailingView)

urlpatterns = [
    path('', include(router.urls))
]
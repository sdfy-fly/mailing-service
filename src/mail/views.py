from rest_framework.viewsets import ModelViewSet

from src.mail.models import Mailing
from src.mail.serializer import MailingSerializer


class MailingView(ModelViewSet):

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        # TODO: асинхронно вызывать задачу celery

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
        # TODO: асинхронно вызывать задачу celery

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

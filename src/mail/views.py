import http

from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Mailing
from .serializer import MailingSerializer
from .tasks import hello
from src.message.models import Message
from src.message.serializer import MessageSerializer


class MailingView(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        # TODO: асинхронно вызывать задачу celery

    def retrieve(self, request, *args, **kwargs):
        hello.delay()
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
        # TODO: асинхронно вызывать задачу celery

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MailingStatsView(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for item in data:
            message_stats = Message.objects.filter(mailing_id=item['id']) \
                .values('send_status').annotate(count=Count('id'))

            item['message_stats'] = message_stats

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Получаем сообщения по рассылке
        messages = Message.objects.filter(mailing=instance)
        message_serializer = MessageSerializer(messages, many=True)

        # Добавляем статистику в ответ
        data = serializer.data
        data['messages'] = message_serializer.data

        return Response(data)

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Method \"POST\" not allowed."}, http.HTTPStatus.METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method \"PUT\" not allowed."}, http.HTTPStatus.METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Method \"DELETE\" not allowed."}, http.HTTPStatus.METHOD_NOT_ALLOWED)

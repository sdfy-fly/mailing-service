import http
from datetime import datetime

from django.db.models import Count
from django.utils.timezone import make_aware
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Mailing
from .serializer import MailingSerializer
from .tasks import process_mailing

from src.message.models import Message
from src.message.serializer import MessageSerializer


class MailingView(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        mailing = Mailing.objects.get(id=response.data['id'])
        self.__mailing(mailing)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        self.__mailing(self.get_object())
        return response

    @staticmethod
    def __mailing(mailing):
        """
            Приватный метод, обертка для запуска celery задач
            Вызывается после создания или обновления рассылки
        """
        current_time = make_aware(datetime.now())
        if current_time >= mailing.finish_time:
            return

        # рассчитываю задержку перед началом задачи
        # если она отрицательная, то запускаю задачу без задержки
        delay = (mailing.start_time - current_time).total_seconds()
        if delay < 0:
            delay = 0

        process_mailing.apply_async(args=[mailing.id], countdown=delay)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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
            # Группируем сообщения, которые относятся к рассылке по статусу и считаем их количество
            message_stats = Message.objects.filter(mailing_id=item['id']) \
                .values('send_status').annotate(count=Count('id'))

            item['message_stats'] = message_stats

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        messages = Message.objects.filter(mailing=instance)
        message_serializer = MessageSerializer(messages, many=True)

        data = serializer.data
        data['messages'] = message_serializer.data

        return Response(data)

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Method \"POST\" not allowed."}, http.HTTPStatus.METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method \"PUT\" not allowed."}, http.HTTPStatus.METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Method \"DELETE\" not allowed."}, http.HTTPStatus.METHOD_NOT_ALLOWED)

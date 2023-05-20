import httpx as httpx
import logging

from asgiref.sync import async_to_sync
from celery import shared_task

from datetime import datetime
from django.db.models import Q
from django.utils.timezone import make_aware

from src.client.models import Client
from src.mail.models import Mailing
from src.message.models import Message

logger = logging.getLogger('mailing_logger')
logger.setLevel(logging.INFO)

# Создание обработчика для записи логов в файл
file_handler = logging.FileHandler('mailing.log')
file_handler.setLevel(logging.INFO)

# Форматирование сообщений логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)


def get_current_time():
    return make_aware(datetime.now())


async def send_message(data):
    url = f"https://probe.fbrq.cloud/v1/send/{data['id']}"
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU5MjczMjIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9zZGZ5bmFtZSJ9.98AOWUkw_EmRykQLfNgRwHO0awFmu6DR-MtrahIfYco',
        'Content-Type': 'application/json'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        return response


@shared_task
def process_mailing(mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)

    if not (mailing.start_time <= get_current_time() <= mailing.finish_time):
        return

    client_list = Client.objects.filter(
        Q(operator_code=mailing.client_filter_operator_code) | Q(tag=mailing.client_filter_tag)
    )

    for client in client_list:

        if get_current_time() > mailing.finish_time:
            return

        message = Message.objects.create(send_status='В работе', mailing=mailing, client=client)
        data = {
            "id": message.id,
            "phone": message.client.phone_number,
            "text": message.mailing.message_text
        }

        r = async_to_sync(send_message)(data)

        if r.status_code == 200:
            message.send_status = 'Отправлено'
            logger.info(f"Mailing №{mailing.id} - Client №{client.id}: Письмо успешно отправлено")
        else:
            message.send_status = 'Не отправлено'
            logger.error(f"Mailing №{mailing.id} - Client №{client.id}: Ошибка при отправке письма клиенту")

        message.save()


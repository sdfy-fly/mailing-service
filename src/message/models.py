from django.db import models

from src.client.models import Client
from src.mail.models import Mailing


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    send_status = models.CharField(max_length=255)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

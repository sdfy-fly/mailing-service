from rest_framework.serializers import ModelSerializer

from .models import Message
from src.mail.serializer import MailingSerializer
from src.client.serializer import ClientSerializer


class MessageSerializer(ModelSerializer):

    mailing = MailingSerializer
    client = ClientSerializer

    class Meta:
        model = Message
        fields = ('id', 'created_at', 'send_status', 'mailing', 'client')

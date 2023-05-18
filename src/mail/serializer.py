from rest_framework.serializers import ModelSerializer

from src.mail.models import Mailing


class MailingSerializer(ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'

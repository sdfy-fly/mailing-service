from django.core.exceptions import ValidationError
from django.db import models


class Client(models.Model):
    phone_number = models.CharField(max_length=11)
    operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)

    @staticmethod
    def validate_phone_number(value):
        if not value.isdigit() or len(value) != 11 or value[0] != '7':
            raise ValidationError('Incorrect phone number')

    def clean(self):
        super().clean()
        self.validate_phone_number(self.phone_number)

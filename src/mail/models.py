from django.db import models


class Mailing(models.Model):
    start_time = models.DateTimeField()
    message_text = models.TextField()
    client_filter_operator_code = models.CharField(max_length=10)
    client_filter_tag = models.CharField(max_length=255)
    finish_time = models.DateTimeField()

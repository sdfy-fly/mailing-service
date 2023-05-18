from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from .models import Client
from .serializer import ClientSerializer


class ClientView(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        if not phone_number.isdigit() or len(phone_number) != 11 or phone_number[0] != '7':
            raise ValidationError({'error': 'Incorrect phone number'})
        serializer.save()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Stamp
from .serializers import StampSerializer
from .producer_data_sent import ProducerDataSent
import json

producer_data_sent = ProducerDataSent()


class CreateStampAPIView(generics.CreateAPIView):
    queryset = Stamp.objects.all()
    serializer_class = StampSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        producer_data_sent.publish("user_created_method", json.dumps(serializer.data))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from django.urls import path
from .views import CreateStampAPIView

urlpatterns = [
    path('create_stamp/', CreateStampAPIView.as_view(), name='create_stamp'),
]

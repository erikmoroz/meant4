from django.urls import path
from faces.consumers import FaceDetectionConsumer

websocket_urlpatterns = [
    path('faces', FaceDetectionConsumer.as_asgi()),
]

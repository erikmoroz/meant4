from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings


class FaceDetectionConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(settings.NOTIFICATION_GROUP_NAME, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(settings.NOTIFICATION_GROUP_NAME, self.channel_name)

    def receive_json(self, content, **kwargs):
        pass

    def send_notification(self, event):
        message = event['message']
        self.send_json(message)

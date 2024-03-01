import pytest
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.test import override_settings
from faces.consumers import FaceDetectionConsumer


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True, reset_sequences=True)
async def test_face_detection_consumer():
    channel_layers_setting = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

    with override_settings(CHANNEL_LAYERS=channel_layers_setting):
        communicator = WebsocketCommunicator(FaceDetectionConsumer.as_asgi(), "/faces")

        connected, _ = await communicator.connect()
        assert connected

        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            settings.NOTIFICATION_GROUP_NAME,
            {
                "type": "send.notification",
                "message": {
                    "text": "Test message."
                }
            }
        )
        response = await communicator.receive_json_from()
        assert response == {"text": "Test message."}

        await communicator.disconnect()

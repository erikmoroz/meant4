from io import BytesIO
import cv2
import numpy as np
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.files.base import ContentFile

from faces.models import Image, ImageStatus
from project.celery_app import app


def detect_faces_in_image(image):
    """Detects faces within an image."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    return faces


def annotate_image_with_faces(original_image, faces):
    """Draws rectangles around detected faces in the original image."""
    for (x, y, w, h) in faces:
        cv2.rectangle(original_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    is_success, buffer = cv2.imencode(".jpg", original_image)
    return BytesIO(buffer) if is_success else None


@app.task
def process_face_recognition_task(image_id: str):
    """Celery task to process face recognition on an image."""
    image_record = Image.objects.get(id=image_id)

    if not image_record.original_image:
        image_record.status = ImageStatus.FAILED
        image_record.save()
        return

    try:
        image_np = np.fromstring(image_record.original_image.read(), np.uint8)
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        faces = detect_faces_in_image(img)
        marked_image_io = annotate_image_with_faces(img, faces)
    except Exception as e:
        image_record.status = ImageStatus.FAILED
        image_record.save()
        return

    if not marked_image_io:
        image_record.status = ImageStatus.FAILED
        image_record.save()
        return

    # If marked_image_io is not None, proceed to save and notify
    marked_image_io.seek(0)  # Rewind to the beginning
    image_record.marked_image.save(f"{image_record.tag}_marked.jpg", ContentFile(marked_image_io.read()), save=True)
    image_record.status = ImageStatus.SUCCESS
    image_record.save()

    # Send the notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.NOTIFICATION_GROUP_NAME,
        {
            "type": "send_notification",
            "message": {
                "text": f"Face recognition completed for image: http://0.0.0.0:8282/image/{image_record.tag}"
            }
        }
    )

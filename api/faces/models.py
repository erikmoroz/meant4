import uuid

from django.db import models


class ImageStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    FAILED = 'FAILED', 'Failed'
    SUCCESS = 'SUCCESS', 'Success'


class Image(models.Model):
    tag = models.CharField(default=uuid.uuid4, max_length=64)
    original_image = models.ImageField(upload_to='original_images/')
    marked_image = models.ImageField(upload_to='faces/', default=None, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=ImageStatus.choices, default=ImageStatus.PENDING)

    def __str__(self):
        return self.tag

import os
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import cv2

from faces.models import Image
from faces.tasks import detect_faces_in_image, annotate_image_with_faces, process_face_recognition_task


class CeleryFaceDetectionTasksTests(TestCase):
    def setUp(self):
        self.test_image_path = os.path.join(os.path.dirname(__file__), 'files', 'jim-carrey.jpg')

    def test_detect_faces_in_image(self):
        test_image = cv2.imread(self.test_image_path)
        faces = detect_faces_in_image(test_image)
        self.assertTrue(len(faces) > 0, "Faces should be detected in the test image")

    def test_annotate_image_with_faces(self):
        test_image = cv2.imread(self.test_image_path)
        faces = detect_faces_in_image(test_image)
        annotated_image_io = annotate_image_with_faces(test_image, faces)
        self.assertIsNotNone(annotated_image_io, "Annotated image should not be None")

    @patch('faces.tasks.get_channel_layer', return_value=None)
    def test_process_face_recognition_task(self, mocked_channel_layer):
        test_image = SimpleUploadedFile(
            name='test.jpg', content=open(self.test_image_path, 'rb').read(), content_type='image/jpeg'
        )
        image_record = Image.objects.create(tag="test", original_image=test_image)
        process_face_recognition_task.apply(args=(image_record.id,))
        image_record.refresh_from_db()
        self.assertIsNotNone(image_record.marked_image)
        mocked_channel_layer.assert_called()

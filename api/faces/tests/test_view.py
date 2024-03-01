import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from faces.models import Image


class ImageAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.upload_url = reverse('upload_image')
        self.download_url = reverse('download_image', kwargs={'tag': 'testimage'})
        self.test_image_path = os.path.join(os.path.dirname(__file__), 'files', 'jim-carrey.jpg')
        self.test_image = SimpleUploadedFile(name='test.jpg',
                                             content=open(self.test_image_path, 'rb').read(),
                                             content_type='image/jpeg')
        self.image = Image.objects.create(
            tag='testimage',
            original_image=self.test_image,
            marked_image=self.test_image
        )

    @patch('faces.tasks.process_face_recognition_task.delay')
    def test_upload_image(self, mock_task):
        with open(self.test_image_path, 'rb') as image:
            response = self.client.post(self.upload_url, {'file': image}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertTrue(Image.objects.filter(tag=response_data['tag']).exists())
        mock_task.assert_called_once_with(Image.objects.get(id=response_data['id']).id)

    def test_upload_image_bad_request(self):
        response = self.client.post(self.upload_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_download_image(self):
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'image/jpeg')

    def test_download_image_not_found(self):
        nonexistent_image_url = reverse('download_image', kwargs={'tag': 'nonexistentimage'})
        response = self.client.get(nonexistent_image_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('faces.views.FileResponse', side_effect=Exception('Error serving the image.'))
    def test_download_image_bad_request(self, *args, **kwargs):
        response = self.client.get(reverse('download_image', kwargs={'tag': self.image.tag}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Error serving the image.'})
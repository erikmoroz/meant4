from django.http import FileResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from faces.models import Image
from faces.serializers import ImageSerializer
from faces.tasks import process_face_recognition_task


class ImageAPIView(APIView):

    def get(self, request, tag, format=None):
        image = get_object_or_404(Image, tag=tag)
        if not image.marked_image:
            return Response({"error": "Marked image not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            return FileResponse(image.marked_image.open('rb'), content_type='image/jpeg')
        except Exception as e:
            return Response({"error": "Error serving the image."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        process_face_recognition_task.delay(serializer.instance.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

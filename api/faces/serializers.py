from rest_framework import serializers

from faces.models import Image


class ImageSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Image
        fields = ('id', 'tag', 'file', 'status', 'uploaded_at')
        kwargs = {
            'id': {'read_only': True},
            'tag': {'read_only': True},
            'status': {'read_only': True},
            'uploaded_at': {'read_only': True},
        }

    def create(self, validated_data):
        instance = Image.objects.create(original_image=validated_data.get('file'))
        return instance

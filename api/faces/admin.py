from django.contrib import admin

from faces.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('tag', 'status', 'uploaded_at', 'id')

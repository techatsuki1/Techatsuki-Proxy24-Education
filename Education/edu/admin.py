# admin.py
from django.contrib import admin
from .models import VideoUpload

@admin.register(VideoUpload)
class VideoUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_file', 'uploaded_at')  # Modify according to your model fields
    search_fields = ('id',)  # Modify according to the fields you want to search

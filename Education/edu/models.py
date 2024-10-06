# models.py
from django.db import models

class VideoUpload(models.Model):
    video_file = models.FileField(upload_to='videos/')  # Store video in 'media/videos/' folder
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the video was uploaded

    def __str__(self):
        return f"Video uploaded at {self.uploaded_at}"

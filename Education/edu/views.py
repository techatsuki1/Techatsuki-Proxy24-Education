from django.shortcuts import render
from .models import VideoUpload
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request,'index.html')
def auth(request):
    return render(request,'auth.html')
def about(request):
    return render(request,'about.html')
def upload(request):
    if request.method == 'POST' and request.FILES.get('videoFileInput'):
        # Get the uploaded file from the request
        video_file = request.FILES['videoFileInput']

        # Save the file to the model
        video_upload = VideoUpload(video_file=video_file)
        video_upload.save()

        # Respond with success
        return JsonResponse({'message': 'Video uploaded successfully!'})
    return render(request,'video.html')
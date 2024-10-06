from django.shortcuts import render
from .models import VideoUpload
from django.http import JsonResponse
import cv2
import mediapipe as mp
import numpy as np
from django.conf import settings
import os

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
def learning(request):
    return render(request,'learning.html')
def detect(request):
    
    # MediaPipe setup
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Define the connections explicitly for drawing
    POSE_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),  # Right Arm
        (0, 5), (5, 6), (6, 7), (7, 8),  # Left Arm
        (0, 11), (0, 12),                # Head to Shoulders
        (11, 13), (13, 15),              # Right Leg
        (12, 14), (14, 16),              # Left Leg
    ]

    def analyze_pose(video_path, pose):
        cap = cv2.VideoCapture(video_path)
        keypoints_list = []

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # Convert the BGR image to RGB for pose detection
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            # Get keypoints if detected
            frame_keypoints = []
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    x = int(landmark.x * image.shape[1])
                    y = int(landmark.y * image.shape[0])
                    frame_keypoints.append((x, y))

                # Draw custom connections for landmarks
                for connection in POSE_CONNECTIONS:
                    if results.pose_landmarks:
                        start = frame_keypoints[connection[0]]
                        end = frame_keypoints[connection[1]]
                        cv2.line(image, start, end, (0, 255, 0), 2)  # Draw green lines
                        cv2.circle(image, start, 5, (0, 0, 255), -1)  # Draw red circles for joints
                        cv2.circle(image, end, 5, (0, 0, 255), -1)

            keypoints_list.append(frame_keypoints)

            yield image, keypoints_list

        cap.release()

    def compare_videos(reference_video_path, student_video_path):
        pose = mp_pose.Pose()

        # Create a generator to yield frames and keypoints
        reference_generator = analyze_pose(reference_video_path, pose)
        student_generator = analyze_pose(student_video_path, pose)

        while True:
            try:
                # Get the next frame from both the reference and student video
                reference_frame, reference_keypoints = next(reference_generator)
                student_frame, student_keypoints = next(student_generator)

                # Resize both frames to be the same size for side-by-side comparison
                reference_frame_resized = cv2.resize(reference_frame, (640, 480))
                student_frame_resized = cv2.resize(student_frame, (640, 480))

                # Concatenate the two frames horizontally (side-by-side)
                combined_frame = np.hstack((reference_frame_resized, student_frame_resized))

                # Show the combined frame with the skeletons
                cv2.imshow('Reference (Left) vs Student (Right)', combined_frame)

                # Check if there are keypoints for both videos in the current frame
                if reference_keypoints and student_keypoints:
                    try:
                        # Convert keypoints to numpy arrays and calculate Euclidean distance
                        reference_np = np.array(reference_keypoints[-1])
                        student_np = np.array(student_keypoints[-1])

                        if reference_np.shape == student_np.shape:  # Ensure both have the same shape
                            distances = np.linalg.norm(reference_np - student_np, axis=1)
                            similarity_score = 100 - np.mean(distances)
                            print(f"Similarity Score: {similarity_score:.2f}")
                        else:
                            print("Mismatch in keypoint array shapes, skipping frame.")

                    except Exception as e:
                        print(f"Error calculating similarity: {e}")

                # Press 'ESC' to exit the video window
                if cv2.waitKey(5) & 0xFF == 27:
                    break

            except StopIteration:
                # End of video
                break

        cv2.destroyAllWindows()
    reference_video_path = os.path.join(settings.MEDIA_ROOT, 'reference_video.mp4')  # Adjust this file name
    student_video_path = os.path.join(settings.MEDIA_ROOT, 'student_video.mp4')
    compare_videos('reference_video.mp4', 'student_video.mp4')

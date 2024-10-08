import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def analyze_facial_expressions(video_path, reference_face_keypoints=None):
    cap = cv2.VideoCapture(video_path)
    face_mesh = mp_face_mesh.FaceMesh()

    student_face_keypoints = []

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and detect face landmarks
        results = face_mesh.process(image_rgb)
        
        if results.multi_face_landmarks:
            frame_keypoints = []
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    x = int(landmark.x * image.shape[1])
                    y = int(landmark.y * image.shape[0])
                    frame_keypoints.append((x, y))
                    cv2.circle(image, (x, y), 1, (0, 255, 0), -1)
            student_face_keypoints.append(frame_keypoints)

        cv2.imshow('Facial Expression Analysis', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Compare with reference if provided
    if reference_face_keypoints:
        similarity_scores = []
        for student_frame, reference_frame in zip(student_face_keypoints, reference_face_keypoints):
            distances = np.linalg.norm(np.array(student_frame) - np.array(reference_frame), axis=1)
            similarity_scores.append(100 - np.mean(distances))  # Higher score = more similarity
        return similarity_scores
    else:
        return student_face_keypoints  # Return keypoints for future comparisons

# Example usage
reference_face_keypoints = analyze_facial_expressions('reference_expression.mp4')
student_face_keypoints = analyze_facial_expressions('student_expression.mp4', reference_face_keypoints=reference_face_keypoints)
print(f"Similarity Scores: {student_face_keypoints}")

import posedetectionmodule as pd
import cv2
import mediapipe as mp
from tkinter import messagebox
mp_pose = mp.solutions.pose


def reduceResolution():
    cap.set(3, 480)
    cap.set(4, 360)


# VIDEO FEED
cap = cv2.VideoCapture('LowResExercises/situps.mp4')

# change resolution
# reduceResolution()

# Curl counter variables
counter = 0
stage = None

pose = pd.PoseDetection()

while cap.isOpened():
    ret, frame = cap.read()

    image = pose.makeDetection(frame)

    # Extract landmarks
    try:
        landmarks = pose.extractLandmarks(image)

        # Get coordinates
        # A good sit-up
        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        # Calculate angle
        angle = pose.calculateAngle(shoulder, hip, knee)
        pose.visualizeAngle(image, angle, hip)

        # Sit-up counter logic
        if angle < 40:
            stage = "up"
        if angle > 100 and stage == 'up':
            stage = "down"
            counter += 1
            print(counter)

    except:
        pass

    pose.visualizeRepCounter(image, "SIT-UPS", counter, stage)
    cv2.imshow('Mediapipe Feed', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        messagebox.showinfo("Exercise Summary",
                            "Exercise:Sit Ups\nReps:3\nRemarks: Squats not deep enough.")
        break

cap.release()
cv2.destroyAllWindows()

import posedetectionmodule as pd
import cv2
import mediapipe as mp
from tkinter import *
from tkinter import messagebox
mp_pose = mp.solutions.pose


def reduceResolution():
    cap.set(3, 480)
    cap.set(4, 360)


# VIDEO FEED
cap = cv2.VideoCapture('LowResExercises/squats.mp4')

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
        # A good squat requires a depth of around 90 degrees on the knees and a wide stance with the feet wider than shoulder width
        # Feet coordinates
        left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
        left_toe = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
        right_toe = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]

        # Knee coordinates
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        # Hip Coordinates
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

        # shoulder coordinates
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        # Calculate angle
        squat_angle = pose.calculateAngle(left_hip, left_knee, left_heel)
        pose.visualizeAngle(image, squat_angle, left_knee)

        # squat counter logic
        if squat_angle < 100:
            stage = "down"
        if squat_angle > 170 and stage == 'down':
            stage = "up"
            counter += 1
            print(counter)

    except:
        pass

    pose.visualizeRepCounter(image, "SQUATS", counter, stage)

    cv2.imshow('Mediapipe Feed', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        # top = Tk()
        # top.geometry("0x0")
        # messagebox.showinfo("Exercise Summary",
        #                     "Exercise:Squats\nReps:10\nRemarks: Satisfactory Form\nRecommendations: None")
        break

cap.release()
cv2.destroyAllWindows()

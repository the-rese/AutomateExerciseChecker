from typing import Counter
import posedetectionmodule as pd
import cv2
import mediapipe as mp
from tkinter import *
from tkinter import messagebox
mp_pose = mp.solutions.pose

# VIDEO FEED
cap = cv2.VideoCapture('LowResExercises/wide-pushups.mp4')

# Curl counter variables
counter = 0
stage = None

# Setup mediapipe instance
pose = pd.PoseDetection()

while cap.isOpened():
    ret, frame = cap.read()

    image = pose.makeDetection(frame)

    # Extract landmarks
    try:
        landmarks = pose.extractLandmarks(image)

        # Get coordinates
        # A good pushup should aim to bend the elbows at or below a 90 degree angle. Since the basis is the elbow angle, both the wide and close grip pushup variations can be accounted for

        # hand coordinates
        left_hand = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        right_hand = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        # elbow coordinates
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

        # shoulder coordinates
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        # hip coordinates
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        # Calculate angle
        elbow_angle = pose.calculateAngle(left_hand, left_elbow, left_shoulder)
        # Check Pushup Variation
        arm_angle = pose.calculateAngle(left_elbow, left_shoulder, left_hip)

        pose.visualizeAngle(image, elbow_angle, left_elbow)

        # Visualize arm angle
        # cv2.putText(image, str("{:.2f}".format(arm_angle)),
        #             tuple(np.multiply(left_shoulder,
        #                   [640, 480]).astype(int)),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
        #                                             255, 255), 2, cv2.LINE_AA
        #             )

        # pushup counter logic
        if elbow_angle < 90:
            stage = "down"
        if elbow_angle > 150 and stage == 'down':
            stage = "up"
            counter += 1
            print(counter)

    except:
        pass

    pose.visualizeRepCounter(image, "PUSHUPS", counter, stage)

    cv2.imshow('Mediapipe Feed', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        # if 90 < pushup_angle < 160 remark "Pushups not deep enough. Low muscle activation"
        # if pushup_angle < 50, remark "Pushups too deep. Risk shoulder injury in the long term"
        # if pushup_angle 80 to 100, remark "Satisfactory Form"
        messagebox.showinfo("Exercise Summary",
                            "Exercise:Pushups\nReps:10\nRemarks:Satisfactory Form")

        break

cap.release()
cv2.destroyAllWindows()

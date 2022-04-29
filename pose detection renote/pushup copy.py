# libraries used to implement pose detection
from numpy import average
import posedetectionmodule as psd
import cv2
import mediapipe as mp
import pandas as pd

from openpyxl.workbook import Workbook
from tkinter import *
from tkinter import messagebox
from typing import Counter
mp_pose = mp.solutions.pose


# VIDEO FEED
video_name = 'LowResExercises/wide-pushups.mp4'
cap = cv2.VideoCapture(video_name)
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Curl Counter variables
counter = 0
stage = None

# Angle variables
min_angle = 120
max_angle = 120
duration = 2

# Average Angle Depth variables
total_max_angle = 0
total_min_angle = 0
count_max_angle = 0
average_depth = 0
rom = ''

# Variable holder for rating
# rep_list naay max_angle, min_angle, duration
rep_list = []

# Setup mediapipe instance
pose = psd.PoseDetection()

while cap.isOpened():
    ret, frame = cap.read()

    # exits loop if video has ended
    while(ret):
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
            elbow_angle = pose.calculateAngle(
                left_hand, left_elbow, left_shoulder)
            # Check Pushup Variation
            arm_angle = pose.calculateAngle(
                left_elbow, left_shoulder, left_hip)

            pose.visualizeAngle(image, elbow_angle, left_elbow)

            # pushup counter logic
            if elbow_angle < 90:
                stage = "down"
                if elbow_angle < min_angle:
                    min_angle = elbow_angle
            if elbow_angle > 150 and elbow_angle > max_angle:
                max_angle = elbow_angle
            if elbow_angle > 150 and stage == 'down':
                # if elbow_angle > max_angle:
                #     max_angle = elbow_angle
                stage = "up"
                counter += 1
                print(counter)
                rep_list.append(
                    (round(max_angle, 2), round(min_angle, 2), duration))
                max_angle = 140
                min_angle = 90
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
        ret, frame = cap.read()

    break

# rating logic
print(rep_list)

for item in rep_list:
    if item[0]:
        total_max_angle += item[0]
        total_min_angle += item[1]
        count_max_angle += 1
average_depth_max = round(total_max_angle/count_max_angle, 2)
average_depth_min = round(total_min_angle/count_max_angle, 2)
print(average_depth_max, average_depth_min)

# remarks
# Reps that are too shallow can be defined as min_angle>90
# Reps that are too deep can be defined as min_angle<70
# If the exercise workout has limited range of motion, it can be defined as having a difference between average max depth and average min depth of less than 80
if average_depth_max-average_depth_min < 80:
    rom = 'Limited'
elif average_depth_max-average_depth_min < 100:
    rom = 'Average'
elif average_depth_max-average_depth_min >= 100:
    rom = 'Exemplary'

# outputs the type of exercise performed by a student with its rating to an excel file
columns = ["Student Name", "Exercise", "Number of Rep",
           "Range of Motion", "Average Angle Depth"]

df = pd.DataFrame(
    list(zip([video_name], ["Push ups"], [counter], [rom], [average_depth_min])), columns=columns)
print(df)

df.to_excel("sample.xlsx", sheet_name="PE Section")

cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import numpy as np


class PoseDetection():

    def __init__(self, static_img_mode=False, upper_body_only=False, smooth_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_img_mode = static_img_mode
        self.upper_body_only = upper_body_only
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.static_img_mode, self.upper_body_only,
                                      self.smooth_landmarks, self.min_detection_confidence, self.min_tracking_confidence)

    def makeDetection(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False

        self.results = self.pose.process(img)

        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        return img

    def extractLandmarks(self, frame, draw=True):
        self.mp_drawing.draw_landmarks(frame, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(
                                           color=(245, 117, 66), thickness=2, circle_radius=2),
                                       self.mp_drawing.DrawingSpec(
                                           color=(255, 255, 255), thickness=2, circle_radius=2)
                                       )
        return self.results.pose_landmarks.landmark

    def calculateAngle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
            np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360-angle

        return angle

    def visualizeAngle(self, frame, angle, location):
        cv2.putText(frame, str("{:.2f}".format(angle))+' degrees', tuple(np.multiply(location, [1080, 608]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                    0, 255), 2, cv2.LINE_AA
                    )

    def visualizeRepCounter(self, frame, title, count, stage):
        cv2.rectangle(frame, (0, 0), (320, 50), (245, 117, 16), -1)

        # Exercise performed
        cv2.putText(frame, 'EXERCISE', (15, 12),
                    cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, title, (10, 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Rep data
        cv2.putText(frame, 'REPS', (180, 12),
                    cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(count), (180, 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Stage data
        cv2.putText(frame, 'STAGE', (230, 12),
                    cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, stage, (230, 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)


# def main():
#     cap = cv2.VideoCapture('squats.mp4')
#     pd = PoseDetection()
#     counter = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         image = pd.makeDetection(frame)

#         try:
#             landmarks = pd.extractLandmarks(image)
#             left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
#                          landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
#             left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
#                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
#             left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
#                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
#             squat_angle = pd.calculateAngle(left_hip, left_knee, left_heel)

#             # squat counter logic
#             if squat_angle < 100:
#                 stage = "down"
#             if squat_angle > 170 and stage == 'down':
#                 stage = "up"
#                 counter += 1
#                 print(counter)

#         except:
#             pass

#         pd.visualizeRepCounter(image, "SQUATS", counter, stage)
#         pd.visualizeAngle(image, squat_angle, left_knee)
#         cv2.imshow('Mediapipe Feed', image)

#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()

import cv2
import mediapipe as mp
import numpy as np
mp_pose = mp.solutions.pose


class PoseDetect():

    # CONSTRUCTOR
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

    # PUBLIC METHODS
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

    def visualizeAngle(self, frame, angle, location):
        cv2.putText(frame, str("{:.2f}".format(angle))+' degrees', tuple(np.multiply(location, [1080, 608]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2, cv2.LINE_AA)

    def visualizeRepCounter(self, frame, title, count, stage):
        cv2.rectangle(frame, (0, 0), (320, 50), (245, 117, 16), -1)
        # Exercise performed
        self.__putText(frame, 'EXERCISE', (15, 12))
        self.__putText(frame, title, (10, 40), 2)
        # Rep data
        self.__putText(frame, 'REPS', (180, 12))
        self.__putText(frame, str(count), (180, 40), 2)
        # Stage data
        self.__putText(frame, 'STAGE', (230, 12))
        self.__putText(frame, stage, (230, 40), 2)

    # PRIVATE METHODS
    def __putText(self, frame, text, location, fscale=None):
        if fscale is not None:
            cv2.putText(frame, text, location, cv2.FONT_HERSHEY_PLAIN,
                        fscale, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, text, location, cv2.FONT_HERSHEY_PLAIN,
                        0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def printClass(self):
        print("Can call pose detect class")

from angles import Angle
from posedetection import PoseDetect
from standardizetest import StandardTest

import cv2
import mediapipe as mp
mp_pose = mp.solutions.pose


class SitupClass():
    # instance variables for the modules
    __pose = None
    __angle = None
    __st = None

    def __init__(self, videoname, gender) -> None:
        # variables for situps
        self.__stage = None
        self.__counter = 0
        self.__knee_angle = 0
        self.__body_angle = 0
        self.__min_angle = 70
        self.__max_angle = 80
        self.__rep_list = []
        self.__result_list = []
        # create object or instance of each module
        self.__pose = PoseDetect()
        self.__angle = Angle()
        self.__st = StandardTest()
        self.__st.setExercise('situps')
        self.__st.setGender(gender)
        # set __cap variable
        self.__cap = cv2.VideoCapture(videoname)

    def rateExercise(self):
        while self.__cap.isOpened():
            ret, frame = self.__cap.read()
            # exits loop if video has ended
            while(ret):
                image = self.__pose.makeDetection(frame)

                try:
                    landmarks = self.__pose.extractLandmarks(image)
                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    # no value
                    # foot = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT.value].x,
                    #         landmarks[mp_pose.PoseLandmark.LEFT_FOOT.value].y]
                    # print(landmarks[mp_pose.PoseLandmark.LEFT_FOOT.value])

                    # # Calculate angles (elbows, hips, and arms)
                    angle = self.__angle.calculateAngle(
                        shoulder, hip, knee)
                    # self.__knee_angle = self.__angle.calculateAngle(
                    #     hip, knee, foot)
                    # self.__body_angle = self.__angle.calculateAngle(
                    #     shoulder, hip, foot)

                    # print(angle)
                    # print(self.__knee_angle)
                    # print(self.__body_angle)

                    # self.__pose.visualizeAngle(
                    #     image, "SITUPS ANGLE", angle, "KNEE ANGLE", self.__knee_angle, "BODY ANGLE", self.__body_angle)
                    self.__SitupCounter(angle)

                except:
                    pass

                self.__pose.visualizeRepCounter(
                    image, "SITUPS", self.__counter, self.__stage)
                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                ret, frame = self.__cap.read()
            break
        self.__cap.release()
        cv2.destroyAllWindows()

    def summarizeResult(self):
        # calls the range of motion function
        # where it calculates for the ave min and max depth
        # including the total number of bad reps
        rom = self.__rangeOfMotion()
        ave_min_depth = self.__angle.getAveMinDepth()
        total_bad_reps = self.__angle.getTotalBadReps()
        correct_reps = self.__counter - total_bad_reps

        # sets number of reps to get the outcome
        # based on the standardized test for Physical Education
        self.__st.setNumReps(self.__counter)
        st = self.__st.getStandardizeTest()

        # appends the following to the list: counter, correct num of reps, st, rom, and ave. min depth
        self.__result_list.append(
            (self.__counter, correct_reps, st, rom, ave_min_depth))

    def getSummary(self):
        # returns the result list
        return self.__result_list

    # private and helper functions
    def __SitupCounter(self, angle):
        if angle < 70:
            self.__stage = "up"
            if angle < self.__min_angle:
                self.__min_angle = angle
        if angle > 80 and self.__stage == 'up':
            if angle > self.__max_angle:
                self.__max_angle = angle
            self.__stage = "down"
            self.__counter += 1
            self.__rep_list.append((round(self.__max_angle, 2), round(
                self.__min_angle, 2), self.__isBadSitup()))
            self.__max_angle = 70
            self.__min_angle = 80

    def __rangeOfMotion(self):
        self.__angle.calculateAveAngle(self.__rep_list)
        ave_min_depth = self.__angle.getAveMinDepth()
        ave_max_depth = self.__angle.getAveMaxDepth()
        if (ave_max_depth - ave_min_depth < 80):
            output = 'Limited'
        elif (ave_max_depth - ave_min_depth < 100):
            output = 'Average'
        else:
            output = 'Exemplary'

        return output

    def __isBadSitup(self):
        # too shallow range of motion (min angle > 50), bad situp
        if(self.__min_angle > 50):
            return 1
        # knees should be between 45 and 90 degrees
        elif(self.__knee_angle < 45 or self.__knee_angle > 90):
            return 1
        # shoulders should not touch the ground (body angle < 180)
        elif(self.__body_angle >= 179):
            return 1
        else:
            return 0

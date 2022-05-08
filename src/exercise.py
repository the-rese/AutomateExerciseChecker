from angles import Angle
from posedetection import PoseDetect
from standardizetest import StandardTest

import cv2
import mediapipe as mp
mp_pose = mp.solutions.pose


class PushupClass():
    # instance variables for the modules
    __pose = None
    __angle = None
    __st = None

    # variables exclusively for this class only
    __cap = None
    __stage = None
    __counter = 0
    __min_angle = 150
    __max_angle = 160
    __hip_angle = 0
    __arm_angle = 0
    __rep_list = []
    __result_list = []

    def __init__(self, videoname) -> None:
        # create object or instance of each module
        self.__pose = PoseDetect()
        self.__angle = Angle()
        self.__st = StandardTest()
        self.__st.setExercise('pushups')
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

                    # knee coordinates
                    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    # hip coordinates
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                    # Calculate angles (elbows, hips, and arms)
                    elbow_angle = self.__angle.calculateAngle(
                        left_hand, left_elbow, left_shoulder)
                    self.__hip_angle = self.__angle.calculateAngle(
                        left_knee, left_hip, left_shoulder)
                    self.__arm_angle = self.__angle.calculateAngle(
                        left_elbow, left_shoulder, left_hip)

                    self.__pose.visualizeAngle(
                        image, elbow_angle, left_elbow)
                    self.__pushupCounter(elbow_angle)

                except:
                    pass

                self.__pose.visualizeRepCounter(
                    image, "PUSHUPS", self.__counter, self.__stage)
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

        # sets the gender and number of reps to get the outcome
        # based on the standardized test for Physical Education
        self.__st.setGender('male')
        self.__st.setNumReps(self.__counter)
        st = self.__st.getStandardizeTest()

        # appends the following to the list: counter, correct num of reps, st, rom, and ave. min depth
        self.__result_list.append(
            (self.__counter, correct_reps, st, rom, ave_min_depth))

    def getSummary(self):
        # returns the result list
        return self.__result_list

    # private and helper functions

    def __pushupCounter(self, angle):
        if angle < 150:
            self.__stage = "down"
            if angle < self.__min_angle:
                self.__min_angle = angle
        if angle > 160 and angle > self.__max_angle:
            self.__max_angle = angle
        if angle > 160 and self.__stage == 'down':
            if angle > self.__max_angle:
                self.__max_angle = angle
            self.__stage = "up"
            self.__counter += 1
            # print(self.__counter)
            self.__rep_list.append(
                (round(self.__max_angle, 2), round(self.__min_angle, 2), self.__isBadPushup()))
            self.__max_angle = 160
            self.__min_angle = 150

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

    def __isBadPushup(self):
        # too shallow range of motion (min angle > 100), bad pushup
        if(self.__min_angle > 100):
            return 1
        # hips raised too high (hip angle < 150)
        elif(self.__hip_angle < 150):
            return 1
        # elbows pointed out too much (arm_angle > 85)
        elif(self.__arm_angle == 85):
            return 1
        else:
            return 0

    # def getTotalNumReps(self):
    #     return self.__counter

    # def getTotalBadRep(self):
    #     return self.__angle.getTotalBadReps()

    # def getStandardizeTest(self):
    #     self.__st.setGender('male')
    #     self.__st.setNumReps(self.__counter)
    #     st = self.__st.getStandardizeTest()
    #     return st

    # def getROM(self):
    #     rom = self.__rangeOfMotion()
    #     return rom

    # def getAveAngle(self):
    #     ave_min_depth = self.__angle.getAveMinDepth()
    #     return ave_min_depth

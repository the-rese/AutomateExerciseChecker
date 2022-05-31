from angles import Angle
from posedetection import PoseDetect
from standardizetest import StandardTest

import cv2
import mediapipe as mp
mp_pose = mp.solutions.pose


class SquatClass():
    # instance variables for the modules
    __pose = None
    __angle = None
    __st = None

    def __init__(self, videoname, gender) -> None:
        # variables for squats
        self.__stage = None
        self.__counter = 0
        self.__back_angle = 0
        self.__min_angle = 150
        self.__max_angle = 160
        self.__rep_list = []
        self.__result_list = []
        # create object or instance of each module
        self.__pose = PoseDetect()
        self.__angle = Angle()
        self.__st = StandardTest()
        self.__st.setExercise('squats')
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

                    # Calculate angles (elbows, hips, and arms)
                    squat_angle = self.__angle.calculateAngle(
                        left_hip, left_knee, left_heel)
                    self.__back_angle = self.__angle.calculateAngle(
                        left_knee, left_hip, left_shoulder)

                    self.__pose.visualizeAngle(
                        image, "SQUAT ANGLE", squat_angle, "BACK ANGLE", self.__back_angle, "NONE", 0)
                    self.__SquatCounter(squat_angle)

                except:
                    pass

                self.__pose.visualizeRepCounter(
                    image, "SQUATS", self.__counter, self.__stage)
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

        # sets the number of reps to get the outcome
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
    def __SquatCounter(self, angle):
        if angle < 150:
            self.__stage = "down"
            if angle < self.__min_angle:
                self.__min_angle = angle
        if angle > 160 and self.__stage == 'down':
            if angle > self.__max_angle:
                self.__max_angle = angle
            self.__stage = "up"
            self.__counter += 1
            self.__rep_list.append((round(self.__max_angle, 2), round(
                self.__min_angle, 2), self.__isBadSquat()))
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

    def __isBadSquat(self):
        # too shallow range of motion (min angle > 100), bad Squat
        if(self.__min_angle > 100):
            return 1
        # back bending forward too much (bend angle < 70), bad squat
        elif(self.__back_angle < 70):
            return 1
        else:
            return 0

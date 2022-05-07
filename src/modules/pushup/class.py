# from posedetection import PoseDetect
# from angles import Angle
from standardizetest import StandardTest
import cv2
import mediapipe as mp
mp_pose = mp.solutions.pose


class PushupClass():
    __instance = None

    def __init__(self) -> None:
        pass

    def connect(self):
        self.__instance = StandardTest(3)
        return self.__instance.printClass()


def main():
    test = PushupClass()
    test.connect()


if __name__ == "__main__":
    main()

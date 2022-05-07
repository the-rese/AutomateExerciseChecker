from typing import List
import numpy as np


class Angle():
    __total_bad_rep = 0
    __total_max_angle = 0
    __total_min_angle = 0
    __count_max_angle = 0

    def __init__(self) -> None:
        pass

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

    def calculateAveAngle(self, rep_list: List):
        for item in rep_list:
            if item[0]:
                self.__total_max_angle += item[0]
                self.__total_min_angle += item[1]
                self.__count_max_angle += 1
                self.__total_bad_rep += item[2]

    def getAveMinDepth(self):
        return round(self.__total_min_angle/self.__count_max_angle, 2)

    def getAveMaxDepth(self):
        return round(self.__total_max_angle/self.__count_max_angle, 2)

    def printClass(self):
        print("Can call angle class")

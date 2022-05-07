from package.female.pushups import FemalePushups
from package.female.situps import FemaleSitups
from package.female.squats import FemaleSquats
from package.male.pushups import MalePushups
from package.male.situps import MaleSitups
from package.male.squats import MaleSquats


class StandardTest():
    __gender = None
    __instance = None
    __exercise = None
    __numOfReps = None

    def __init__(self, numOfReps) -> None:
        self.__numOfReps = numOfReps

    def setGender(self, gender):
        self.__gender = gender

    def setExercise(self, exercise):
        self.__exercise = exercise

    def getStandardizeTest(self):
        result = None
        if (self.__gender == 'female'):
            if (self.__exercise == 'squats'):
                self.__instance = FemaleSquats()
            elif (self.__exercise == 'situps'):
                self.__instance = FemaleSitups()
            else:
                self.__instance = FemalePushups()
        else:
            if (self.__exercise == 'squats'):
                self.__instance = MaleSquats()
            elif (self.__exercise == 'situps'):
                self.__instance = MaleSitups()
            else:
                self.__instance = MalePushups()

        result = self.__instance.getResults(self.__numOfReps)
        return result

    def printClass(self):
        print("Can call angle class")

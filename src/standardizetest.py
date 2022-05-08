from package.pushups import FemalePushups, MalePushups
from package.situps import FemaleSitups, MaleSitups
from package.squats import FemaleSquats, MaleSquats


class StandardTest():
    __gender = None
    __instance = None
    __exercise = None
    __numOfReps = None

    def __init__(self) -> None:
        pass

    def setGender(self, gender):
        self.__gender = gender

    def setExercise(self, exercise):
        self.__exercise = exercise

    def setNumReps(self, numOfReps):
        self.__numOfReps = numOfReps

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


def main():
    exercise_result = StandardTest()
    exercise_result.setNumReps(27)
    exercise_result.setGender('female')
    exercise_result.setExercise('situps')
    print(exercise_result.getStandardizeTest())


if __name__ == "__main__":
    main()

class FemaleSquats():
    def __init__(self) -> None:
        pass

    def getResults(self, numOfReps):
        output = None
        if(numOfReps > 43):
            output = "Excellent"
        elif(numOfReps >= 37 and numOfReps <= 43):
            output = "Good"
        elif(numOfReps >= 33 and numOfReps <= 36):
            output = "Above Average"
        elif(numOfReps >= 29 and numOfReps <= 32):
            output = "Average"
        elif(numOfReps >= 25 and numOfReps <= 28):
            output = "Below Average"
        elif(numOfReps >= 18 and numOfReps <= 24):
            output = "Poor"
        else:
            output = "Very Poor"

        return output


class MaleSquats():
    def __init__(self) -> None:
        pass

    def getResults(self, numOfReps):
        output = None
        if(numOfReps > 49):
            output = "Excellent"
        elif(numOfReps >= 44 and numOfReps <= 49):
            output = "Good"
        elif(numOfReps >= 39 and numOfReps <= 43):
            output = "Above Average"
        elif(numOfReps >= 35 and numOfReps <= 38):
            output = "Average"
        elif(numOfReps >= 31 and numOfReps <= 34):
            output = "Below Average"
        elif(numOfReps >= 25 and numOfReps <= 30):
            output = "Poor"
        else:
            output = "Very Poor"

        return output

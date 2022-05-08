class FemalePushups():
    def __init__(self) -> None:
        pass

    def getResults(self, numOfReps):
        output = None
        if(numOfReps > 48):
            output = "Excellent"
        elif(numOfReps >= 34 and numOfReps <= 38):
            output = "Good"
        elif(numOfReps >= 17 and numOfReps <= 33):
            output = "Average"
        elif(numOfReps >= 6 and numOfReps <= 16):
            output = "Fair"
        else:
            output = "Poor"

        return output


class MalePushups():
    def __init__(self) -> None:
        pass

    def getResults(self, numOfReps):
        output = None
        if(numOfReps > 54):
            output = "Excellent"
        elif(numOfReps >= 45 and numOfReps <= 54):
            output = "Good"
        elif(numOfReps >= 35 and numOfReps <= 44):
            output = "Average"
        elif(numOfReps >= 20 and numOfReps <= 34):
            output = "Fair"
        else:
            output = "Poor"

        return output

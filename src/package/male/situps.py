class MaleSitups():
    def __init__(self) -> None:
        pass

    def getResults(self, numOfReps):
        output = None
        if(numOfReps > 60):
            output = "Excellent"
        elif(numOfReps >= 45 and numOfReps < 60):
            output = "Good"
        elif(numOfReps >= 30 and numOfReps < 45):
            output = "Fair"
        else:
            output = "Poor"

        return output

def makelogFile(lines, outputName):
    file = open(outputName, "w")
    for line in lines:
        for value in line:
            file.write(str(value) + "\t")
        file.write("\n")
    file.close()


def saveParetoFront(front):
    outputName = "front.gen"
    file = open(outputName, "w")
    for individual in front:
        file.write(individual[0])
        file.write("\n")

    file.close()


class Result:

    def __init__(self, logbooks, hall_of_fame, time):
        self.logbooks = logbooks
        self.hall_of_fame = hall_of_fame
        self.time = time

    def get_logbooks(self):
        return self.logbooks

    def get_hall_of_fame(self):
        return self.hall_of_fame

    def get_time(self):
        return self.time

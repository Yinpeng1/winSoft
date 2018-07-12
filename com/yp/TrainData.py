
class Train(object):

    def __init__(self, trainType, depCity, arrCity, time, duration, businessSit, firstSit, secondSit, highSoft, soft, moveSoft, hardSoft, softSit, hardSit,
                 noSit, other):
        self.trainType = trainType
        self.depCity = depCity
        self.arrCity = arrCity
        self.time = time
        self.duration = duration
        self.businessSit = businessSit
        self.firstSit = firstSit
        self.secondSit = secondSit
        self.highSoft = highSoft
        self.soft = soft
        self.moveSoft = moveSoft
        self.hardSoft = hardSoft
        self.softSit = softSit
        self.hardSit = hardSit
        self.noSit = noSit
        self.other = other
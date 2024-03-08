class PID():
    def __init__(self,kP,uAboveLimit,uUnderLimit):
        self.kP = kP
        self.uAboveLimit = uAboveLimit
        self.uUnderLimit = uUnderLimit
        
    def PidCal(self,Target,current):
        err = Target - current
        uP = self.kP * err
        u = uP
        
        if(u>self.uAboveLimit):
            u=self.uAboveLimit
        elif(u<self.uUnderLimit):
            u=self.uUnderLimit 
        else:
            u = u
        return u
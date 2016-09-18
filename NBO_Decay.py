# NBO with decay

import NBO

class NBO_Decay(NBO.NBO):
    def __init__(self, bodies=50, initType='u', G=1, decayRate=0.01, decayStartPoint=50, decayEndPoint=1000):
        NBO.NBO.__init__(self, bodies, initType, G=G)
        self.decayRate = decayRate # G decays this much every iter
        self.decayStartPoint = decayStartPoint # start on this iteration
        self.decayEndPoint = decayEndPoint # end on this iter 

    def step(self):
        NBO.NBO.step(self)
        if (self.iter > self.decayStartPoint) and (self.iter < self.decayEndPoint):
            if (self.G - self.decayRate) > 0: # G cant be below 0
                self.G -= self.decayRate
        
        

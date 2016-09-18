# Decay Hyperheurtistic

import hyperheuristic

class Particle_Decay_HH(hyperheuristic.Hyperheuristic):
    def __init__(self, optimizers, decayParams):
        hyperheuristic.Hyperheuristic.__init__(self, optimizers)
        self.optimizers = optimizers # a list of optimizer objects
        self.decayParams = decayParams # json array of length len(optimizers) -1
        # {
        #  'decayStartPoint': point at which decay starts
        #  'decayEndPoint': point at which decay end (complete transition)
        # }

    def initialize(self):
        # initially only optimizer 1 should have particles
        pass
        
        
        

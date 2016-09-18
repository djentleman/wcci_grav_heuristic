import optimizer
import hyperparameters as hy
import function
import functionutils as fu
import random

class RS(optimizer.Optimizer):
    def __init__(self, bodies=50, initType='u'):
        optimizer.Optimizer.__init__(self, bodies, initType)
        self.velocities = [(100*(random.random()-0.5), 100*(random.random()-0.5)) for x in self.positions]


    def step(self):
        self.updatePositions()
        self.velocities = [(2*50*(random.random()-0.5), 2*50*(random.random()-0.5)) for x in self.positions]
        self.getCurrMaxima()
        self.iter+=1
        
if __name__ == "__main__":
    rs = RS(20, 'r');
    exLambda = lambda args: -fu.griewank(args[0], args[1]) 
    rs.setupOptimization(function.Function(exLambda))
    print rs.optimizationFunction
    for i in range(100):
        print rs.bestMaxima
        rs.step()

import optimizer
import hyperparameters as hy
import functionutils as fu
import function
import random

class PSO(optimizer.Optimizer):
    def __init__(self, bodies=50, initType='u'):
        optimizer.Optimizer.__init__(self, bodies, initType)
        self.initialiseVelocity()
        self.bests = [(x[0], x[1], -99999999) for x in self.positions]
        #self.maxima = self.getCurrMaxima(self.positions, -9999999)
        self.maxima = (-9999999, (0, 0))
        

    def initialiseVelocity(self):
        ### the following needs to be an n dimensional list comprehention??
        self.velocities = [(2*hy.rvel*(random.random()-0.5), 2*hy.rvel*(random.random()-0.5)) for x in self.positions]

    def getBests(self):
        for i in range(len(self.positions)):
            x = optimizer.translate(self.positions[i][0], 0, hy.granularity, hy.lxb, hy.uxb)
            y = optimizer.translate(self.positions[i][1], 0, hy.granularity, hy.lyb, hy.uyb)
            curr = self.optimizationFunction.run([x, y])
            if curr > self.bests[i][2]:
                self.bests[i] = (self.positions[i][0], self.positions[i][1], curr)

    def updateVelocities(self):
        for i in range(len(self.positions)):
            #print self.positions[i]
            Fx = ((self.positions[i][0] - self.bests[i][0]) / optimizer.getMinkowskiDistance(self.positions[i], self.bests[i]) ) + \
                    ( (self.positions[i][0] - self.maxima[1][0]) / optimizer.getMinkowskiDistance(self.positions[i], self.maxima[1]))
            #print PSOmaxima[1]
            Fy = ((self.positions[i][1] - self.bests[i][1]) / optimizer.getMinkowskiDistance(self.positions[i], self.bests[i]) ) + \
                    ( (self.positions[i][1] - self.maxima[1][1]) / optimizer.getMinkowskiDistance(self.positions[i], self.maxima[1]))
            Vx = self.velocities[i][0] - Fx
            Vy = self.velocities[i][1] - Fy 
            #print (Vx, Vy)
            self.velocities[i] = (Vx, Vy)

    def updatePositions(self):
        for i in range(len(self.positions)):
            sx = self.positions[i][0]
            sy = self.positions[i][1]
            vx = self.velocities[i][0]
            vy = self.velocities[i][1]
            dsx = vx*hy.dT
            dsy = vy*hy.dT
            npx = sx + dsx
            npy = sy + dsy
            nvx = vx
            nvy = vy
            if npx > hy.granularity:
                npx = hy.granularity
                nvx = -vx*hy.cor
            if npx < 0:
                npx = 0
                nvx = -vx*hy.cor
            if npy > hy.granularity:
                npy = hy.granularity
                nvy = -vy*hy.cor
            if npy < 0:
                npy = 0
                nvy = -vy*hy.cor
            self.velocities[i] = (nvx, nvy)
            self.positions[i] = (npx, npy)  
    


    def step(self):
        #print self.iter
        self.getBests()
        self.updateVelocities()
        self.updatePositions()
        if self.getCurrMaxima(maxima=self.maxima[0])[0] > self.maxima[0]:
            self.maxima = self.getCurrMaxima(maxima=self.maxima[0], pos=self.maxima[1])
        self.iter+=1

   



if __name__ == "__main__":
    # create classifier
    pso = PSO(20, 'r');
    exLambda = lambda args: -fu.griewank(args[0], args[1]) 
    pso.setupOptimization(function.Function(exLambda))
    print pso.optimizationFunction
    for i in range(100):
        print pso.bestMaxima
        pso.step()

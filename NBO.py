import optimizer
import hyperparameters as hy
import functionutils as fu
import function
import random



class NBO(optimizer.Optimizer):
    def __init__(self, bodies=50, initType='u'):
        optimizer.Optimizer.__init__(self, bodies, initType)
        #TODO: inherit Optimizer

        # initialize NBO specific parameters
        self.defaultZeroMass = 0.0000000001 # 'zero mass' can't actually be zero, or we divide by zero
        ##### 4 configurable parameters mentioned in the paper #####
        self.k = 2 # used to force attractive forces to overpower repulsive forces
        self.G = 1 # gravitational constant
        self.cvr = 10 # centroid velocity reduction
        self.massThreshold = 0 # when the fitness of a particle is configured, this is where the boundary between
        # positive and negative masses lies

        self.repulsion = False
        self.bestStop = True # slows the current best particle


        # initialize all NBO specific vectors
        self.velocities = []
        self.masses = []

        # run initialization functions, including super.initialisePositions
        self.initialiseVelocity()

    
    def initialiseVelocity(self):
        ### the following needs to be an n dimensional list comprehention??
        self.velocities = [(2*hy.rvel*(random.random()-0.5), 2*hy.rvel*(random.random()-0.5)) for x in self.positions]

    def getMasses(self):
        masses = []
        for i in range(len(self.positions)):
            x = optimizer.translate(self.positions[i][0], 0, hy.granularity, hy.lxb, hy.uxb)
            y = optimizer.translate(self.positions[i][1], 0, hy.granularity, hy.lyb, hy.uyb)
            funcOutput = self.optimizationFunction.run([x, y])
            if (funcOutput == 0):
                masses.append(0.0000000001)
            else:
                if funcOutput > self.massThreshold:
                    masses.append((funcOutput-massThreshold)**k)
                else:
                    if self.repulsion:
                        masses.append((funcOutput-massThreshold)*k) # hmm
                    else:
                        masses.append(0.0000000001)
        self.masses = masses

        ##### TODO - refactor the below code

    def getMinkowskiDistance(x, y):
        # assume 2d
        if math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2)) != 0:
            return math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2))
        else:
            return 0.0000000001

    def getForces(self):
        Fs = []
        for i in range(len(self.masses)):
            m1 = self.masses[i]
            s1 = self.positions[i]
            Fx = 0
            Fy = 0
            for j in range(len(self.masses)):
                m2 = self.masses[j]
                s2 = self.positions[j]
                if i != j:
                    try:
                        Fx += (G*m1*m2*(s1[0]-s2[0]))/(math.pow(self.getMinkowskiDistance(s1, s2), 2))
                    except:
                        Fx = 0
                    try:
                        Fy += (G*m1*m2*(s1[1]-s2[1]))/(math.pow(self.getMinkowskiDistance(s1, s2), 2))
                    except:
                        Fy = 0
            Fs.append((Fx, Fy))
        return Fs
            
                                  
    def updateVelocities(self, forces):
        for i in range(len(self.velocities)):
            # dT * a = dT * (F/m)
            vx = self.velocities[i][0]
            vy = self.velocities[i][1]
            m = self.masses[i]
            Fx = forces[i][0]
            Fy = forces[i][1]
            dvx = hy.dT*(float(Fx)/float(m))
            dvy = hy.dT*(float(Fy)/float(m))
            self.velocities[i] = (vx - dvx, vy - dvy)

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
            self.velocities[i] = (nvy, nvy)
            self.positions[i] = (npx, npy)

    def step(self):
        self.getMasses()
        forces = self.getForces()
        self.updateVelocities(forces)
        if self.bestStop:
            if (self.getCurrMaxima()[0] - self.massThreshold > 0):
                self.velocities[getBesti(self.positions)] = \
                  (self.velocities[getBesti(positions)][0]/self.cvr, self.velocities[getBesti(self.positions)][1]/self.cvr)
        self.updatePositions()




if __name__ == "__main__":
    # create classifier
    nbo = NBO(20, 'r');
    exLambda = lambda args: -fu.griewank(args[0], args[1]) 
    nbo.setupOptimization(function.Function(exLambda))
    for i in range(100):
        print nbo.bestMaxima
        nbo.step()
    

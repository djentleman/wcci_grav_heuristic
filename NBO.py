import optimizer
import hyperparameters as hy 
import function



class NBO(optimizer.Optimizer):
	def __init__(self, bodies=50, initType='u'):
		pass
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
		self.bestStop = False # stops the current best particle
		# essentially the same as cvr tending to infinity


		# initialize all NBO specific vectors
		self.velocities = []
		self.masses = []

		# run initialization functions, including super.initialisePositions

	
	def initialiseVelocity(self):
		### the following needs to be an n dimensional list comprehention??
		self.velocities = [(2*rvel*(random.random()-0.5), 2*rvel*(random.random()-0.5)) for x in self.positions]


	def getMasses(self):
		masses = []
		for i in range(len(self.positions)):
			x = translate(self.positions[i][0], 0, granularity, lxb, uxb)
			y = translate(self.positions[i][1], 0, granularity, lyb, uyb)
			if (function(x, y)) == 0:
				masses.append(0.0000000001)
			else:
				if function(x, y) > massThreshold:
			masses.append((function(x, y)-massThreshold)**k)
			else:
				if repulsion:
					masses.append((function(x, y)-massThreshold)*k) # hmm
				else:
					masses.append(0.0000000001)
		return masses


		##### TODO - refactor the below code

def getMinkowskiDistance(x, y):
    # assume 2d
    if math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2)) != 0:
        return math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2))
    else:
        return 0.0000000001

def getForces(positions, masses):
    Fs = []
    for i in range(len(masses)):
        m1  = masses[i]
        s1 = positions[i]
        Fx = 0
        Fy = 0
        for j in range(len(masses)):
            m2 = masses[j]
            s2 = positions[j]
            if i != j:
                try:
                    Fx += (G*m1*m2*(s1[0]-s2[0]))/(math.pow(getMinkowskiDistance(s1, s2), 2))
                except:
                    Fx = 0
                try:
                    Fy += (G*m1*m2*(s1[1]-s2[1]))/(math.pow(getMinkowskiDistance(s1, s2), 2))
                except:
                    Fy = 0
        Fs.append((Fx, Fy))
    return Fs
            
                              
def updateVelocities(velocities, forces, masses):
    for i in range(len(velocities)):
        # dT * a = dT * (F/m)
        vx = velocities[i][0]
        vy = velocities[i][1]
        m = masses[i]
        Fx = forces[i][0]
        Fy = forces[i][1]
        dvx = dT*(float(Fx)/float(m))
        dvy = dT*(float(Fy)/float(m))
        velocities[i] = (vx - dvx, vy - dvy)
    return velocities

    def step(self):
		self.masses = getMasses(positions)
		forces = getForces(positions, masses)
		self.velocities = updateVelocities(self.velocities, forces, self.masses)
		if self.bestStop:
			if (getCurrMaxima(positions, -999999999)[0] - self.massThreshold > 0):
				self.velocities[getBesti(self.positions)] = \
				  (self.velocities[getBesti(positions)][0]/self.cvr, self.velocities[getBesti(self.positions)][1]/self.cvr)
		self.positions = updatePositions(self.positions, self.velocities)




if __name__ == "__main__":
	# create classifier
	nbo = NBO(20, 'r');

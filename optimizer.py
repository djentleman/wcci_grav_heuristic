# parent class, high level util functions

import hyperparameters as hy
import math
import random

class Optimizer:
	def __init__(self, bodies=50, initType='u'):
		self.positions = []
		self.bodies = bodies
		self.initType = initType
		self.initialize()
		self.optimizationFunction = None
		self.bestMaxima = -99999999999
		self.iter = 0

	def initialize(self):
		# initType - 'u'nufirm, or 'r'andom
		# update to handle n dimenstional search spaces!!!!
		if self.initType == 'u':
			perRow = int(math.sqrt(self.bodies)) # this will NOT be sqrt, but the nth root for n dimensional space
			gap = float(hp.granularity)/(perRow+1)
			for x in range(perRow):
				for y in range(perRow):
					self.positions.append(((x+1)*gap, (y+1)*gap))
		# print positions
		elif self.initType == 'r':
			for i in range(self.bodies):
				self.positions.append((random.randint(0, hy.granularity-1), random.randint(0, hy.granularity-1)))
		return self.positions

	def printout(self):
		print "	Bodies:	" + str(self.bodies)
		print "	Init Type:	" + initType

	def setupOptimization(self, function):
		self.optimizationFunction = function

        def getCurrMaxima(self, maxima=-9999999999, pos = (0, 0)):
             for i in range(len(self.positions)):
                  x = translate(self.positions[i][0], 0, hy.granularity, hy.lxb, hy.uxb)
                  y = translate(self.positions[i][1], 0, hy.granularity, hy.lyb, hy.uyb)
                  fOut = self.optimizationFunction.run([x, y])
                  if (fOut > maxima):
                      maxima = fOut
                      pos = tuple(self.positions[i])
             if (maxima > self.bestMaxima):
                 self.bestMaxima = maxima
             #print pos
             return (maxima, pos)

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

        

	## all child classes will have a 'step function', which completes one 
	## iteration of the optimization algorithm

	## the step function will be called from the main method in the event loop




def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def getMinkowskiDistance(x, y):
        # assume 2d
        if math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2)) != 0:
            return math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2))
        else:
            return 0.0000000001



if __name__ == "__main__":
	o = Optimizer()

# parent class, high level util functions

import hyperparameters as hp

class Optimizer:
	def __init__(self, bodies=50, initType='u'):
		self.positions = []
		self.bodies = bodies
		self.initType = initType
		self.initialize(bodies, initType)
		self.optimizationFunction = None

	def initialize(self):
		# initType - 'u'nufirm, or 'r'andom
		# update to handle n dimenstional search spaces!!!!
		if initType == 'u':
			perRow = int(math.sqrt(self.bodies)) # this will NOT be sqrt, but the nth root for n dimensional space
			gap = float(hp.granularity)/(perRow+1)
			for x in range(perRow):
				for y in range(perRow):
					self.positions.append(((x+1)*gap, (y+1)*gap))
		# print positions
		elif initType == 'r':
			for i in range(self.bodies):
				self.positions.append((random.randint(0, hp.granularity-1), random.randint(0, hp.granularity-1)))
		return self.positions

	def printout(self):
		print "	Bodies:	" + str(self.bodies)
		print "	Init Type:	" + initType

	def setupOptimization(self, function):
		self.optimizationFunction = function

	## all child classes will have a 'step function', which completes one 
	## iteration of the optimization algorithm

	## the step function will be called from the main method in the event loop





if __name__ == "__main__":
	o = Optimizer()
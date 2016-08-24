import functionutils as fu
import hyperparameters as hp

class Function:
	def __init__(self, func):
		# given a function, generates a search space
		self.func = func
		self.searchSpace = []
		self.setSearchSpace()

	def run(self, args):
		return self.func(args)

	def drange(self, start, stop, step):
		r = start
		while r < stop:
 			yield r
	 		r += step

	def setSearchSpace(self):
		# TODO: this needs to be extended to handle n dimensional search spaces
		i = 0
		j = 0
		for x in self.drange(hp.lxb, hp.uxb, (float(hp.uxb-hp.lxb))/(hp.granularity-1)):
			row = []
			for y in self.drange(hp.lyb, hp.uyb, (float(hp.uyb-hp.lyb))/(hp.granularity-1)):
				
				row.append(self.run([x, y])) # + 5*math.cos(3*x) +  + 5*math.cos(3*y))
			self.searchSpace.append(row)

	def getSearchSpaceMaxima(self):
		# get grid search maxima
		return max([y for row in self.searchSpace for y in row])


if __name__ == "__main__":
	# example using lambda function
	exLambda = lambda args: -fu.griewank(args[0], args[1]) 
	f = Function(exLambda)
	print f.run([1, 4])
	print f.getSearchSpaceMaxima()

	# example with function defenition

	def nDimMean(args):
		return float(sum(args)) / float(len(args))
	g = Function(nDimMean)
	print g.run([1, 4, 7, 4])
	print g.run([20, 21])
	print g.getSearchSpaceMaxima()

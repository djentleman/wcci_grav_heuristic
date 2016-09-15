import optimizer
import hyperparameters as hy
import function
import functionutils as fu
import random

class GA(optimizer.Optimizer):
    def __init__(self, bodies=50, initType='u'):
        optimizer.Optimizer.__init__(self, bodies, initType)

        self.mr = 0.2 # percent mutations
        self.cr = 0.8 # percept crossover
        self.mp = 0.1 # chance of bit being flipped
        self.tSize = 3 # tornament size


    def mutate(self, genome):
        newgenome = ''
        for ch in genome:
            if (random.random() < self.mp):
                if ch == '0':
                    newgenome += '1'
                else:
                    newgenome += '0'
            else:
                newgenome += ch
        return newgenome

    def crossover(self, parent1, parent2):
        child1 = ''
        child2 = ''
        crossoverPoint = random.randint(0, len(parent1)-1)
        for i in range(len(parent1)):
            if i < crossoverPoint:
                child1 += parent1[i]
                child2 += parent2[i]
            else:
                child1 += parent2[i]
                child2 += parent1[i]
        return (child1, child2)

    def iterateGA(self):
        newPositions = []
        while len(newPositions) < len(self.positions):
            if (random.random() < self.cr):
                p1 = tournament(self.positions, self.tSize, self.optimizationFunction)
                p2 = tournament(self.positions, self.tSize, self.optimizationFunction)
                children = self.crossover(posToGenome(p1), posToGenome(p2))
                newPositions.append(genomeToPos(children[0]))
                newPositions.append(genomeToPos(children[1]))
            else:
                newPositions.append(
                    genomeToPos(self.mutate(
                        posToGenome(tournament(self.positions, self.tSize, self.optimizationFunction))
                        ))
                    )
        self.positions = newPositions

    def step(self):
        self.iterateGA()
        self.getCurrMaxima()


def posToGenome((x, y)):
    # 2 12 bit binary numbers
    # for genetic operators
    binx = (12 - len(bin(int((x)*4)).split("b")[-1]))*"0" + bin(int((x)*4)).split("b")[-1]
    biny = (12 - len(bin(int((y)*4)).split("b")[-1]))*"0" +bin(int((y)*4)).split("b")[-1]
    return binx+biny

def genomeToPos(g):
    binx = g[:12]
    biny = g[12:]
    return ((int(binx, 2) / 4.0) % hy.granularity, (int(biny, 2) / 4.0)  % hy.granularity)

def tournament(s, k, func):
    tour = []
    for i in range(k):
        tour.append(s[random.randint(0, len(s)-1)])
        best = -1
    for i in range(len(tour)):
        if best == -1:
            best = i
        x = optimizer.translate(tour[i][0], 0, hy.granularity, hy.lxb, hy.uxb)
        y = optimizer.translate(tour[i][1], 0, hy.granularity, hy.lxb, hy.uxb)
        bx = optimizer.translate(tour[best][0], 0, hy.granularity, hy.lxb, hy.uxb)
        by = optimizer.translate(tour[best][1], 0, hy.granularity, hy.lxb, hy.uxb)
        if func.run([x, y]) > func.run([bx, by]):
            best = i
    return tour[best]


if __name__ == "__main__":
    ga = GA(20, 'r');
    exLambda = lambda args: -fu.griewank(args[0], args[1]) 
    ga.setupOptimization(function.Function(exLambda))
    print ga.optimizationFunction
    for i in range(100):
        print ga.bestMaxima
        ga.step()

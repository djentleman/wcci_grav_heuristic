# n body optimization

import pygame
import sys
import math
import random
from math import sin, cos, tan, e,pi, exp, sqrt
import time

granularity = 500
bodies = 50
lxb = -10; uxb = 10;
lyb = -10; uyb = 10;
G = 0.000001
k = 2 # mass multiplier
cvr = 10 # center mass velocity reduction
massThreshold = -1000
dT = 1
initType = 'r'
cor = 0.2 # Coefficient of restitution, needs to be less than 1
rvel = 2

bestStop = True



repulsion = False

mr = 0.2 # percent mutations
cr = 0.8 # percept crossover
mp = 0.1 # chance of bit being flipped
tSize = 3

delay = 0

imax = -1


def sphere(x, y):
    return (x**2 + y**2)

def pyramid(x, y):
    return -(abs(x + y) + abs(y - x)) + 10

def ackley(x, y):
    return (-20*exp(-0.2*sqrt(0.5*(x**2 + y**2))) - exp(0.5*(cos(2*pi*x) + cos(2*pi*y))) + e + 20)

def waves(x, y):
    return 20*(sin(3*x) + sin(3*y) + 20*sin(x)) + -(-abs(x**2 + (y+3)**2) + 2) + 10*x + 100*y

def pyramidal(x, y):
    return 10*pyramid(sin(x), sin(y))-90 + 0.1*x + 0.1*y

def npyramidal(x, y):  return pyramidal(pyramidal(x, y), pyramidal(x, y))

def spherewave(x, y):
    return 10*sphere(sin(x), sin(y)) + 0.1*x + 0.1*y

def rosenbrock(x, y):
    return (100*(y - x**2)**2 + (1-x)**2)


def beale(x, y):
    return ((1.5-x+x*y)**2+(2.25-x-x*y**2)**2+(2.625-x+x*y**3)**2)

def rastagrin(x, y):
    return -20 +  (x**2 -10*cos(2*math.pi*x)) + (y**2 -10*cos(2*math.pi*y))

def scwefel(x, y):
    return  -x*sin(math.sqrt(abs(x)))  + -y*sin(math.sqrt(abs(y)))   + 2*(418.982887)

def matyas(x, y):
    return 0.26*(x**2+y**2)-0.48*(x*y)

def griewank(x, y):
    return  1 + ((x**2/4000) + (y**2/4000)) - (cos(x/math.sqrt(2)) * cos(y/math.sqrt(2)))

function = lambda x, y: -griewank(x, y) 

    # x*1.5 + y*1.1 + 500*sphere(sin(2*x), sin(2*y)) - 40 NICE


    #-ackley(x, y) + 10


    #-griewank(x, y) + 2

    #-scwefel(x, y) +850

    #-scwefel(x, y) - 840
    #-sphere(x, y)+10

    #pyramidal(x+0.1, y+0.1*x) 


# pyramidal(x+0.1*y, y+0.1*x) - 0.01*(ackley(x+4, y-0.2) + 10) - 0.01*(sphere(x+6, y-10) + 5)
#

# pyramidal(x+0.1*y, y+0.1*x) - 0.01*(ackley(x+4, y-0.2) + 10) - 0.01*(sphere(x+6, y-10) + 5)

# ^^ fuxx shit up
# pyramidal(x+0.1*y, y+0.1*x) - 0.01*(ackley(x+4, y-0.2) + 10) - 0.01*(sphere(x+6, y-10) + 5)
# ^^ also good

# pyramidal(x*0.1*y, y) - 0.01*(ackley(x+4, y-0.2) + 10) - 0.01*(sphere(x+6, y-10) + 5)
# ^^ NICE
#x + y
#10*(-sphere((x+4), (y+7.2))+5) *sin(x) * sin(y)
# pyramidal(x, y) - 0.01*(ackley(x+4, y-0.2) + 10) - 0.01*(sphere(x+6, y-10) + 5)
# x + y**2
#30*sin((x+0.2)*2) + 30*sin((y+0.2)*2) + 0.1*x + 0.1*y
#-ackley((x+3), (y-2)) + 10
#-((y+4)**2 + (x-2.4) ** 2) + 10 + 0.2*x + 0.2*y
#pyramidal(x, y) ** 2
#30*sin(x*2) + 30*sin(y*2) + 1*x + 1*y
#pyramidal(x, y)
#100*sin(x*2) + 100*sin(y*2) + 1*x + 1*y
#-sphere(x, y)+20
#100*sin(x/20) + 100*sin(y/10) + 0.1*x + 0.1*y
#-sphere(x, y)+600
#10*((-ackley((sin(x+3)), sin(y-2)) + 5) - sin(10*x)) + 0.1*y + 0.2*x
#10*(-sphere((x+4), (y+7.2))+5)

#30*(waves(cos(x), sin(y)) - x*cos(y) - 40*y)


#10*pyramid(sin(x), sin(y))-90 + 0.1*x + 0.1*y # THE KILLER

#-sphere(pyramid(x, y), ackley(x, y)) + 1000
#20*(sin(3*x) + sin(3*y) + 20*sin(x)) + -(-abs(x**2 + (y+3)**2) + 2) + 10*x + 100*y
#20*(sin(1*-(abs(x + y) + abs(y - x)) + 10))+x+y
#pyramid(x, y)

#-ackley((x+3), (y-2)) + 10
#-sphere(x, y)+100
#-ackley((x+3), (y-2)) + 10
#60*sin(x) + 8*x + 8*y + 100*(cos(x) + cos(y))
#10*(-((x+3)**2 + (y-4)**2) + 3)
#tan(x)
#30*(-abs((x+4) + y) - abs((x+4)-(y+5)) + 7) + 50*cos(3*x) + 50*cos(3*y)
#1.2*(-((x-3)**2 + (y+4)**2)+20) + 50*cos(3*x) + 50*cos(3*y) - 20*x + 20*y
#0.2*x + 0.2*y
#if x < 4 and y < 4 and y > 3 and x > 3:
#    return 10
#return -1
#20*(sin(3*x) + sin(3*y) + 20*sin(x)) + -(-abs(x**2 + (y+3)**2) + 2) + 10*x + 100*y
#10*(-((x-2)**2 + (y+4)**2) + 5)

#5*cos(x*y) + 0.2 * x + 0.2 * y
    
#return 20*(sin(3*x) + sin(3*y) + 20*sin(x)) + -(-abs(x**2 + (y+3)**2) + 2) + 10*x + 100*y
    



#100*(-abs(x**2 + (y+3)**2) + 2)

#200*math.cos(10*x) + 200*math.cos(10*y) + 0.2*x + 0.2*y
#-((x + 4)**2 + y**2) + 50*math.cos(5*x)  + 100*math.cos(2*x)

def drange(start, stop, step):
     r = start
     while r < stop:
     	yield r
     	r += step

def rgb(r, g, b):
    try:
        if (r > 255): r = 255
        if (g > 255): g = 255
        if (b > 255): b = 255
        if (r < 0): r = 0
        if (g < 0): g = 0
        if (b < 0): b = 0
        return pygame.Color(int(r), int(g), int(b)) # makes life easier!
    except:
        print(r, g, b)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def initGraphics():
    gw = GraphWin("NBO", granularity, granularity)
    return gw

def setSearchSpace(lxb, uxb, lyb, uyb):
    grid = []
    i = 0
    j = 0
    for x in drange(lxb, uxb, (float(uxb-lxb))/(granularity-1)):
        row = []
        for y in drange(lyb, uyb, (float(uyb-lyb))/(granularity-1)):
            
            row.append(function(x, y)) # + 5*math.cos(3*x) +  + 5*math.cos(3*y))
        grid.append(row)
    return grid

def renderSearchSpace(screen, grid):
     
     minima = min([y for x in grid[:-1] for y in x])
     maxima = max([y for x in grid[:-1] for y in x])
     for x in range(granularity-1):
          for y in range(granularity-1):

               if (grid[x][y] > 0):
                    screen.set_at((x, y),rgb(translate(grid[x][y], 0, maxima, 0, 255), 0, 0) )
               else:
                    screen.set_at((x, y),rgb(0, 0, translate(grid[x][y], minima, 0, 255, 0) ))

def initializeNBO(bodies=50, initType='u'):
     # initType - 'u'nufirm, or 'r'andom
     positions = [] # array of tuples
     if initType == 'u':
          perRow = int(math.sqrt(bodies)) # this will NOT be sqrt, but the nth root for n dimensional space
          gap = float(granularity)/(perRow+1)
          for x in range(perRow):
               for y in range(perRow):
                    positions.append(((x+1)*gap, (y+1)*gap))
         # print positions
     elif initType == 'r':
         for i in range(bodies):
             positions.append((random.randint(0, granularity-1), random.randint(0, granularity-1)))
     return positions


        
        
          
          
def getMasses(positions):
     masses = []
     for i in range(len(positions)):
          x = translate(positions[i][0], 0, granularity, lxb, uxb)
          y = translate(positions[i][1], 0, granularity, lyb, uyb)
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


        
        
def updatePositions(positions, velocities):
    for i in range(len(positions)):
        sx = positions[i][0]
        sy = positions[i][1]
        vx = velocities[i][0]
        vy = velocities[i][1]
        dsx = vx*dT
        dsy = vy*dT
        npx = sx + dsx
        npy = sy + dsy
        nvx = vx
        nvy = vy
        if npx > granularity:
            npx = granularity
            nvx = -vx*cor
        if npx < 0:
            npx = 0
            nvx = -vx*cor
        if npy > granularity:
            npy = granularity
            nvy = -vy*cor
        if npy < 0:
            npy = 0
            nvy = -vy*cor
        velocities[i] = (nvx, nvy)
        positions[i] = (npx, npy)
    return positions
          
def getCurrMaxima(positions, maxima, pos = (0, 0)):
     masses = maxima
     for i in range(len(positions)):
          x = translate(positions[i][0], 0, granularity, lxb, uxb)
          y = translate(positions[i][1], 0, granularity, lyb, uyb)
          if (function(x, y) > masses):
              masses = function(x, y)
              pos = (positions[i][0], positions[i][1])
     return masses, pos

def getBests(pos, bests):
    for i in range(len(pos)):
        x = translate(pos[i][0], 0, granularity, lxb, uxb)
        y = translate(pos[i][1], 0, granularity, lyb, uyb)
        curr = function(x, y)
        if curr > bests[i][2]:
            bests[i] = (pos[i][0], pos[i][1], curr)
    return bests
        
def updatePSOVelocities(velocities, positions, bests, PSOmaxima):
    for i in range(len(positions)):
        #print positions[i]
        Fx = ((positions[i][0] - bests[i][0]) / getMinkowskiDistance(positions[i], bests[i]) ) + \
                ( (positions[i][0] - PSOmaxima[1][0]) / getMinkowskiDistance(positions[i], PSOmaxima[1]))
        #print PSOmaxima[1]
        Fy = ((positions[i][1] - bests[i][1]) / getMinkowskiDistance(positions[i], bests[i]) ) + \
                ( (positions[i][1] - PSOmaxima[1][1]) / getMinkowskiDistance(positions[i], PSOmaxima[1]))
        Vx = velocities[i][0] - Fx
        Vy = velocities[i][1] - Fy 
        #print (Vx, Vy)
        velocities[i] = (Vx, Vy)
    return velocities

def posToGenome((x, y)):
    # 2 12 bit binary numbers
    # for genetic operators
    binx = (12 - len(bin(int((x)*4)).split("b")[-1]))*"0" + bin(int((x)*4)).split("b")[-1]
    biny = (12 - len(bin(int((y)*4)).split("b")[-1]))*"0" +bin(int((y)*4)).split("b")[-1]
    return binx+biny

def genomeToPos(g):
    binx = g[:12]
    biny = g[12:]
    return ((int(binx, 2) / 4.0) % granularity, (int(biny, 2) / 4.0)  % granularity)

def mutate(genome):
    newgenome = ''
    for ch in genome:
        if (random.random() < mp):
            if ch == '0':
                newgenome += '1'
            else:
                newgenome += '0'
        else:
            newgenome += ch
    return newgenome

def crossover(parent1, parent2):
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

def tournament(s, k):
    tour = []
    for i in range(k):
        tour.append(s[random.randint(0, len(s)-1)])
        best = -1
    for i in range(len(tour)):
        if best == -1:
            best = i
        x = translate(tour[i][0], 0, granularity, lxb, uxb)
        y = translate(tour[i][1], 0, granularity, lxb, uxb)
        bx = translate(tour[best][0], 0, granularity, lxb, uxb)
        by = translate(tour[best][1], 0, granularity, lxb, uxb)
        if function(x, y) > function(bx, by):
            best = i
    return tour[best]

def runGA(positions):
    newPositions = []
    while len(newPositions) < len(positions):
        if (random.random() < cr):
            p1 = tournament(positions, tSize)
            p2 = tournament(positions, tSize)
            children = crossover(posToGenome(p1), posToGenome(p2))
            newPositions.append(genomeToPos(children[0]))
            newPositions.append(genomeToPos(children[1]))
        else:
            newPositions.append(genomeToPos(mutate(posToGenome(tournament(positions, tSize)))))
    return newPositions
            
        
        
def getBesti(positions):
    best = getCurrMaxima(positions, -999999999)[0]
    #print best
    for i in range(len(positions)):
        x = translate(positions[i][0], 0, granularity, lxb, uxb)
        y = translate(positions[i][1], 0, granularity, lyb, uyb)
        if function(x, y) == best:
            return i
    return -1


        

def compare(ui=True, itmax=-1, dump=False, dumpEachIter=False):
    # init window
    global G
    if ui:
        size = width, height = granularity+300, granularity-1
        black = 0, 0, 0
        screen = pygame.display.set_mode(size)
        background = pygame.Surface((granularity,granularity))
        pygame.display.set_caption('NBO')
    
    # set search space
    searchspace = setSearchSpace(lxb, uxb, lyb, uyb)
    gsMaxima = max([y for x in searchspace[:-1] for y in x])
    #print gsMaxima

    # render search space
    if ui:
        renderSearchSpace(background, searchspace)

    positions = initializeNBO(bodies, initType)
    velocities = [(2*rvel*(random.random()-0.5), 2*rvel*(random.random()-0.5)) for x in positions]

    PSOpositions = initializeNBO(bodies, initType)
    PSOvelocities = [(2*rvel*(random.random()-0.5), 2*rvel*(random.random()-0.5)) for x in positions]
    PSObests = getBests(PSOpositions, [(x[0], x[1], -99999999) for x in positions])
    PSOmaxima = getCurrMaxima(PSOpositions, -9999999)

    RSpositions = initializeNBO(bodies, initType)
    RSvelocities = [(100*(random.random()-0.5), 100*(random.random()-0.5)) for x in positions]

    GApositions = initializeNBO(bodies, initType)

    if ui:
        NBO = pygame.Surface((granularity,granularity))
        NBO.set_colorkey((0,0,0))
        NBO.convert_alpha()

        PSO = pygame.Surface((granularity,granularity))
        PSO.set_colorkey((0,0,0))
        PSO.convert_alpha()

        RS = pygame.Surface((granularity,granularity))
        RS.set_colorkey((0,0,0))
        RS.convert_alpha()

        GA = pygame.Surface((granularity,granularity))
        GA.set_colorkey((0,0,0))
        GA.convert_alpha()

        panel = pygame.Surface((300, granularity))

    maxima = getCurrMaxima(positions, -99999)[0]
    RSmaxima = getCurrMaxima(RSpositions, -99999)[0]
    GAmaxima = getCurrMaxima(GApositions, -99990)[0]
    #print(maxima)
    if ui:
        for body in positions:
            pygame.draw.circle(NBO, rgb(0, 255, 0), (int(body[0]), int(body[1])), 2)

        for body in PSOpositions:
            pygame.draw.circle(PSO, rgb(0, 255, 255), (int(body[0]), int(body[1])), 2)

        for body in PSOpositions:
            pygame.draw.circle(RS, rgb(255, 255, 0), (int(body[0]), int(body[1])), 2)

        for body in GApositions:
            pygame.draw.circle(GA, rgb(255, 0, 255), (int(body[0]), int(body[1])), 2)

        GSenabled = True
        NBOenabled = True
        PSOenabled = True
        RSenabled = True
        GAenabled = True

    
        

        screen.blit(background, (0,0,granularity,granularity))
        screen.blit(NBO, (0,0,granularity,granularity))
        screen.blit(PSO, (0,0,granularity,granularity))
        screen.blit(RS, (0,0,granularity,granularity))
        screen.blit(GA, (0,0,granularity,granularity))
        pygame.init()
        myfont = pygame.font.SysFont("monospace", 15)

    it = 0

    while 1:
        #print PSOmaxima[1]
        if ui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = event.pos
                    if x > 500:
                        # panel click
                        if y > 10 and y < 30:
                            GSenabled = not GSenabled
                        if y > 30 and y < 50:
                            NBOenabled = not NBOenabled
                        if y > 50 and y < 70:
                            PSOenabled = not PSOenabled
                        if y > 70 and y < 90:
                            GAenabled = not GAenabled
                        if y > 90 and y < 110:
                            RSenabled = not RSenabled
                    
                        

        
            # draw black over
            if GSenabled:
                NBO.fill(rgb(0, 0, 0))
                PSO.fill(rgb(0, 0, 0))
                GA.fill(rgb(0, 0, 0))
                RS.fill(rgb(0, 0, 0))
                     
            # trails
            else:
                for body in positions:
                     pygame.draw.circle(NBO, rgb(0, 100, 0), (int(body[0]), int(body[1])), 2)
                for body in PSOpositions:
                     pygame.draw.circle(PSO, rgb(0, 100, 100), (int(body[0]), int(body[1])), 2)
                for body in RSpositions:
                     pygame.draw.circle(RS, rgb(100, 100, 0), (int(body[0]), int(body[1])), 2)
                for body in GApositions:
                     pygame.draw.circle(GA, rgb(100, 0, 100), (int(body[0]), int(body[1])), 2)

        masses = getMasses(positions)
        forces = getForces(positions, masses)
        velocities = updateVelocities(velocities, forces, masses)
        if bestStop:
            if (getCurrMaxima(positions, -999999999)[0] - massThreshold > 0):
                velocities[getBesti(positions)] = (velocities[getBesti(positions)][0]/cvr, velocities[getBesti(positions)][1]/cvr)
        positions = updatePositions(positions, velocities)

        if ui:
            for body in positions:
                pygame.draw.circle(NBO, rgb(0, 255, 0), (int(body[0]), int(body[1])), 2)


        PSObests = getBests(PSOpositions, PSObests)
        PSOvelocities = updatePSOVelocities(PSOvelocities, PSOpositions, PSObests, PSOmaxima)
        PSOpositions = updatePositions(PSOpositions, PSOvelocities)
        if getCurrMaxima(PSOpositions, PSOmaxima)[0] > PSOmaxima[0]:
            PSOmaxima = getCurrMaxima(PSOpositions, PSOmaxima[0], PSOmaxima[1])
        if ui:
            for body in PSOpositions:
                pygame.draw.circle(PSO, rgb(0, 255, 255), (int(body[0]), int(body[1])), 2)

        RSpositions = updatePositions(RSpositions, RSvelocities)
        RSvelocities = [(2*50*(random.random()-0.5), 2*50*(random.random()-0.5)) for x in positions]

        if ui:
            for body in RSpositions:
                pygame.draw.circle(RS, rgb(255, 255, 0), (int(body[0]), int(body[1])), 2)

        GApositions = runGA(GApositions)

        if ui:
            for body in GApositions:
                pygame.draw.circle(GA, rgb(255, 0, 255), (int(body[0]), int(body[1])), 2)

            if GSenabled:
                screen.blit(background, (0,0,granularity,granularity))
            if NBOenabled:
                screen.blit(NBO, (0,0,granularity,granularity))
            if PSOenabled:
                screen.blit(PSO, (0,0,granularity,granularity))
            if RSenabled:
                screen.blit(RS, (0,0,granularity,granularity))
            if GAenabled:
                screen.blit(GA, (0,0,granularity,granularity))

            panel.fill(black)
            pygame.draw.line(panel, rgb(255, 255, 255), (0, 0), (0, granularity), 4)
            screen.blit(panel, (499, 0))

            if GSenabled:
                label = myfont.render("Grid Search Maxima:   " + str("%.4f" % gsMaxima) , 1, (255,255,255))
            else:
                label = myfont.render("Grid Search Maxima:   " + str("%.4f" % gsMaxima) , 1, (100,100,100))
            screen.blit(label, (510, 10))

            
            if getCurrMaxima(positions, maxima)[0] > maxima:
                maxima = getCurrMaxima(positions, maxima)[0]
            if NBOenabled:
                label2 = myfont.render("NBO Search Maxima:    " + str("%.4f" % maxima) , 1, (0,255,0))
            else:
                label2 = myfont.render("NBO Search Maxima:    " + str("%.4f" % maxima) , 1, (0,100,0))
            screen.blit(label2, (510, 30))

            
            if getCurrMaxima(PSOpositions, PSOmaxima)[0] > PSOmaxima[0]:
                PSOmaxima = getCurrMaxima(PSOpositions, PSOmaxima[0], PSOmaxima[1])
            if PSOenabled:
                label3 = myfont.render("PSO Search Maxima:    " + str("%.4f" % PSOmaxima[0]) , 1, (0,255,255))
            else:
                label3 = myfont.render("PSO Search Maxima:    " + str("%.4f" % PSOmaxima[0]) , 1, (0,100,100))
            screen.blit(label3, (510, 50))

            
            if getCurrMaxima(GApositions, -99990)[0] > GAmaxima:
                GAmaxima = getCurrMaxima(GApositions, -99990)[0]
            if GAenabled:
                label5 = myfont.render("GA Search Maxima:     " + str("%.4f" % GAmaxima) , 1, (255,0,255))
            else:
                label5 = myfont.render("GA Search Maxima:     " + str("%.4f" % GAmaxima) , 1, (100,0,100))
            screen.blit(label5, (510, 70))


            if getCurrMaxima(RSpositions, RSmaxima)[0] > RSmaxima:
                RSmaxima = getCurrMaxima(RSpositions, RSmaxima)[0]
            if RSenabled:
                label4 = myfont.render("Random Search Maxima: " + str("%.4f" % RSmaxima) , 1, (255,255,0))
            else:
                label4 = myfont.render("Random Search Maxima: " + str("%.4f" % RSmaxima) , 1, (100,100,0))
            screen.blit(label4, (510, 90))
            

            labelX = myfont.render("Iter:  " + str(it) , 1, (255,255,255))
            screen.blit(labelX, (510, 480))
            
            pygame.display.update() # update display

        
        
        
        if (dumpEachIter):
            print str(it+1) + ": " + str(maxima)
        it += 1
        #print str(bodies) + ": " + str(maxima) 
        if it > itmax and itmax != -1:
            print str(bodies) + ": " + str(maxima)
            #print "---------------------------------------------------"
            if dump:
                print "done"
                print "NBO: " + str(getCurrMaxima(positions, maxima)[0])
                print "PSO: " + str(getCurrMaxima(PSOpositions, PSOmaxima)[0][0])
                print "GA: " + str(getCurrMaxima(GApositions, GAmaxima)[0])
                print "GS: " + str(gsMaxima)
                print "RS: " + str(getCurrMaxima(RSpositions, RSmaxima)[0])
            pygame.quit()
            return (getCurrMaxima(positions, maxima)[0], getCurrMaxima(PSOpositions, PSOmaxima)[0][0], getCurrMaxima(GApositions, GAmaxima)[0]
                    ,gsMaxima, getCurrMaxima(RSpositions, RSmaxima)[0])

        time.sleep(delay)



def main():
    for i in range(10):
        compare(True, itmax = imax, dump=True)


if __name__ == "__main__":
    main()

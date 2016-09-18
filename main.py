## new main file

# util we abstract pygame:
import pygame

import sys

import hyperparameters as hy
import function
import functionutils as fu
import optimizer

# import heuristics...
import NBO
import PSO
import GA
import RS


# modified heuristics
import NBO_Decay

# hyperheuristics
import Particle_Decay_HH


def compare(optimizers, func, ui=True, itmax=-1, dump=False, dumpEachIter=False):
    # set up optimizers to use func
    for optimizer in optimizers:
        optimizer['optimizer'].setupOptimization(func)
    
    # init window
    if ui:
        size = width, height = hy.granularity+300, hy.granularity-1
        black = 0, 0, 0
        screen = pygame.display.set_mode(size)
        background = pygame.Surface((hy.granularity, hy.granularity))
        pygame.display.set_caption('NBO')

    # render search space (func)
    if ui:
        renderSearchSpace(background, func.searchSpace)

        GSenabled = True

    

    if ui:
        surfaces = []

        for optimizer in optimizers:
            currSurface = pygame.Surface((hy.granularity, hy.granularity))
            currSurface.set_colorkey((0,0,0))
            currSurface.convert_alpha()
            surfaces.append(currSurface)

        panel = pygame.Surface((300, hy.granularity))

    # TODO: abtract this into the respective optimizer classes
    # we can use the same util functions
    ###maxima = getCurrMaxima(positions, -99999)[0]
    ###RSmaxima = getCurrMaxima(RSpositions, -99999)[0]
    ###GAmaxima = getCurrMaxima(GApositions, -99990)[0]
    #print(maxima)
        surfaceIdx = 0
        for optimizer in optimizers:
            for body in optimizer['optimizer'].positions:
                pygame.draw.circle(surfaces[surfaceIdx], optimizer['particle_color'], (int(body[0]), int(body[1])), 2)
            surfaceIdx += 1

    
        

        screen.blit(background, (0,0,hy.granularity, hy.granularity))
        for surface in surfaces:
            screen.blit(surface, (0,0,hy.granularity, hy.granularity))
        pygame.init()
        myfont = pygame.font.SysFont("monospace", 15)

    it = 0

    paused = False

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
                        if y > 10 and y < 30:
                            GSenabled = not GSenabled
                        yPos = 30
                        for optimizer in optimizers:
                            if y > yPos and y < yPos+20:
                                optimizer['enabled'] = not optimizer['enabled']
                            yPos+=20

        
            # draw black over
            if GSenabled:
                for surface in surfaces:
                    surface.fill(rgb(0, 0, 0))
                     
            # trails
            else:
                surfaceIdx = 0

                for optimizer in optimizers:
                    for body in optimizer['optimizer'].positions:
                        pygame.draw.circle(surfaces[surfaceIdx], optimizer['trail_color'], (int(body[0]), int(body[1])), 2)
                    surfaceIdx += 1

        for optimizer in optimizers:
            # perform step (this should be genertic across all heuristics)
            optimizer['optimizer'].step()

        if ui:
            # render 
            surfaceIdx = 0
            for optimizer in optimizers:
                if optimizer['enabled']:
                    for body in optimizer['optimizer'].positions:
                        pygame.draw.circle(surfaces[surfaceIdx], optimizer['particle_color'], (int(body[0]), int(body[1])), 2)
                surfaceIdx += 1



            if GSenabled:
                screen.blit(background, (0,0,hy.granularity,hy.granularity))

            surfaceIdx = 0
            for optimizer in optimizers:
                if optimizer['enabled']:
                    screen.blit(surfaces[surfaceIdx], (0,0,hy.granularity,hy.granularity))
                surfaceIdx += 1

            # render panel

            panel.fill(black)
            pygame.draw.line(panel, rgb(255, 255, 255), (0, 0), (0, hy.granularity), 4)
            screen.blit(panel, (499, 0))


            if GSenabled:
                label = myfont.render("Grid Search Maxima:   " + str("%.4f" % func.getSearchSpaceMaxima()), 1, (255,255,255))
            else:
                label = myfont.render("Grid Search Maxima:   " + str("%.4f" % func.getSearchSpaceMaxima()), 1, (100,100,100))
            screen.blit(label, (510, 10))
            
            yPos = 30
            for optimizer in optimizers:
                if optimizer['enabled']:
                    label = myfont.render(optimizer['name'] + " Maxima:   " + str("%.4f" % optimizer['optimizer'].bestMaxima), 1, optimizer['particle_color'])
                else:
                    label = myfont.render(optimizer['name'] + " Maxima:   " + str("%.4f" % optimizer['optimizer'].bestMaxima), 1, (100,100,100))
                screen.blit(label, (510, yPos))
                yPos+= 20

            

            labelX = myfont.render("Iter:  " + str(it) , 1, (255,255,255))
            screen.blit(labelX, (510, 480))
            
            pygame.display.update() # update display

        
        it += 1
        #print str(bodies) + ": " + str(maxima) 
        if it > itmax and itmax != -1:
            pygame.quit()
            return (getCurrMaxima(positions, maxima)[0], getCurrMaxima(PSOpositions, PSOmaxima)[0][0], getCurrMaxima(GApositions, GAmaxima)[0]
                    ,gsMaxima, getCurrMaxima(RSpositions, RSmaxima)[0])


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

def renderSearchSpace(screen, grid):
     minima = min([y for x in grid[:-1] for y in x])
     maxima = max([y for x in grid[:-1] for y in x])
     for x in range(hy.granularity-1):
          for y in range(hy.granularity-1):
               if (grid[x][y] > 0):
                    screen.set_at((x, y),rgb(optimizer.translate(grid[x][y], 0, maxima, 0, 255), 0, 0) )
               else:
                    screen.set_at((x, y),rgb(0, 0, optimizer.translate(grid[x][y], minima, 0, 255, 0) ))



def main():
    # define a function
    exLambda = lambda args: -fu.griewank(args[0], args[1]) + 1
    f = function.Function(exLambda)
    # define a set of optimizers
    # each one is a dict with parameters - color, name, optimizer object
    optimizers = []
    """
    optimizers.append({
        'name': 'NBO-10',
        'particle_color': rgb(0, 255, 0),
        'trail_color': rgb(0, 100, 0),
        'optimizer': NBO.NBO(10, 'r'),
        'enabled': True
        })

    optimizers.append({
        'name': 'NBO-15',
        'particle_color': rgb(0, 125, 255),
        'trail_color': rgb(0, 50, 100),
        'optimizer': NBO.NBO(15, 'r'),
        'enabled': True
        })
    """
    optimizers.append({
        'name': 'NBO-20',
        'particle_color': rgb(255, 125, 0),
        'trail_color': rgb(100, 50, 0),
        'optimizer': NBO.NBO(20, 'r'),
        'enabled': True
        })
    optimizers.append({
        'name': 'NBO_Decay-20',
        'particle_color': rgb(0, 125, 255),
        'trail_color': rgb(0, 50, 100),
        'optimizer': NBO_Decay.NBO_Decay(20, 'r'),
        'enabled': True
        })
    optimizers.append({
        'name': 'NBO_Increase-20',
        'particle_color': rgb(0, 255, 255),
        'trail_color': rgb(0, 100, 100),
        'optimizer': NBO_Decay.NBO_Decay(20, 'r', decayRate=-0.01),
        'enabled': True
        })
    optimizers.append({
        'name': 'PSO-20',
        'particle_color': rgb(255, 255, 255),
        'trail_color': rgb(100, 100, 100),
        'optimizer': PSO.PSO(20, 'r'),
        'enabled': True
        })
    # pass into compare functionn, along with configuration params
    compare(optimizers, f)

if __name__ == "__main__":
    main()

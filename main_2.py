## new main file

# util we abstract pygame:
import pygame

import hyperparameters
import function
import functionutils as fu

# import heuristics...
import NBO
import PSO
import GA
import RS 


def compare(optimizers, func, ui=True, itmax=-1, dump=False, dumpEachIter=False):
 	# init window
    if ui:
        size = width, height = granularity+300, granularity-1
        black = 0, 0, 0
        screen = pygame.display.set_mode(size)
        background = pygame.Surface((granularity,granularity))
        pygame.display.set_caption('NBO')

    # render search space (func)
    if ui:
        renderSearchSpace(background, func.searchSpace)

        GSenabled = True

    

    if ui:
    	surfaces = []

    	for optimizer in optimizers:
    		currSurface = pygame.Surface((granularity,granularity))
    		currSurface.set_colorkey((0,0,0))
    		currSurface.convert_alpha()

        panel = pygame.Surface((300, granularity))

    # TODO: abtract this into the respective optimizer classes
    # we can use the same util functions
    ###maxima = getCurrMaxima(positions, -99999)[0]
    ###RSmaxima = getCurrMaxima(RSpositions, -99999)[0]
    ###GAmaxima = getCurrMaxima(GApositions, -99990)[0]
    #print(maxima)
    if ui:
    	surfaceIdx = 0
    	for optimizer in optimizers:
    		for body in optimizer['optimizer'].positions:
    			pygame.draw.circle(surfaces[surfaceIdx], optimizer['optimizer'].color, (int(body[0]), int(body[1])), 2)
    		surfaceIdx += 1

    
        

        screen.blit(background, (0,0,granularity,granularity))
        for surface in surfaces:
        	screen.blit(surface, (0,0,granularity,granularity))
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
                    	###### this needs to be generared procedurally!!!!
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
            	for surface in surfaces:
            		surface.fill(rgb(0, 0, 0))
                     
            # trails
            else:
            	surfaceIdx = 0

            	for optimizer in optimizers:
                	for body in optimizer['optimizer'].positions:
                		# we need to generate the trail color from the defauly color
                		## TODO
                    	pygame.draw.circle(surfaces[surfaceIdx], rgb(0, 100, 0), (int(body[0]), int(body[1])), 2)
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
	                    	pygame.draw.circle(surfaces[surfaceIdx], optimizer['color'], (int(body[0]), int(body[1])), 2)
	            surfaceIdx += 1



            if GSenabled:
                screen.blit(background, (0,0,granularity,granularity))

            surfaceIdx = 0
            for optimizer in optimizers:
            	if optimizer['enabled']:
            		screen.blit(surface['surfaceIdx'], (0,0,granularity,granularity))
                surfaceIdx += 1

            # render panel

            panel.fill(black)
            pygame.draw.line(panel, rgb(255, 255, 255), (0, 0), (0, granularity), 4)
            screen.blit(panel, (499, 0))


            # this all needs to be automated

            """

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

            """
            

            labelX = myfont.render("Iter:  " + str(it) , 1, (255,255,255))
            screen.blit(labelX, (510, 480))
            
            pygame.display.update() # update display

        
        it += 1
        #print str(bodies) + ": " + str(maxima) 
        if it > itmax and itmax != -1:
            pygame.quit()
            return (getCurrMaxima(positions, maxima)[0], getCurrMaxima(PSOpositions, PSOmaxima)[0][0], getCurrMaxima(GApositions, GAmaxima)[0]
                    ,gsMaxima, getCurrMaxima(RSpositions, RSmaxima)[0])






def main():
	# define a function
	exLambda = lambda args: -fu.griewank(args[0], args[1]) 
	f = Function(exLambda)
	# define a set of optimizers
	# each one is a dict with parameters - color, name, optimizer object
	optimizers = []
	optimizers.append({
		'name': 'NBO-20',
		'particle_color': rgb(0, 255, 0),
		'optimizer': NBO(20, 'r'),
		'enabled': True
		})

	optimizers.append({
		'name': 'NBO-50',
		'particle_color': rgb(0, 255, 0),
		'optimizer': NBO(50, 'r')
		'enabled': True
		})
	# pass into compare functionn, along with configuration params
	compare(optimizers, f)

if __name__ == "__main__":
	main()
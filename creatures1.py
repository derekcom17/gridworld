# Creatures move and eat the plants
import random
from gridworld import *

period = 0.033 # [s]
willRender = True

width = 100
height = 100
creatureSize = 1.5
plantSize = 0.6

lookRadius = 10
plantSpawnProb = 0.2

loopNum = 0

def main():
	setupGrid(width,height,render=willRender,lines=False,winWidth=600,winHeight=600) # setup
	
	# Add herbivores
	GridEntity(randCoord(),creatureSize,name='herbivore',color='red')
	GridEntity(randCoord(),creatureSize,name='herbivore',color='blue')
	GridEntity(randCoord(),creatureSize,name='herbivore',color='yellow')
	GridEntity(randCoord(),creatureSize,name='herbivore',color='orange')
	
	# add plants
	for x in range(width):
		for y in range(height):
			if random.random() < plantSpawnProb:
				GridEntity((x,y),plantSize,name='plant',color='black')
	
	runGrid(period,updateEntities) # run gridworld

def updateEntities(entities):
	global loopNum
	plantPop = 0	
	for e in entities: 
		if e.getAttr('name') == 'herbivore': # For each herbivore...
			food = e.closestInRadius(lookRadius,'name','plant') # look			
			if food: # move
				move = moveTowards(food)
				e.move(move[0],move[1])
			else:
				randMove(e) 			
			others = e.entitiesAtRelCoord() # eat
			for other in others:
				if other.getAttr('name') == 'plant':
					other.remove() 
					break # only eat once 	
		elif e.getAttr('name') == 'plant': # for each plant...
			plantPop += 1 # update plant counter
	
	if loopNum%50 == 0 :#and plantPop != 0:
		print('plant population: '+str(plantPop))
	loopNum += 1
	if plantPop == 0:
		print('plant population: 0 DONE!')
		stopGrid()

def moveTowards(coord):
	xMove = 0
	yMove = 0
	if coord[0] != 0:
		xMove = coord[0]/abs(coord[0])
	if coord[1] != 0:
		yMove = coord[1]/abs(coord[1])
	return (xMove,yMove)
	
def randMove(e):
	dir = random.randint(0,3)
	if   dir == 0: # Go East
		e.moveInDir('E')
	elif dir == 1: # Go South
		e.moveInDir('S')
	elif dir == 2: # Go West
		e.moveInDir('W')
	else:          # Go North
		e.moveInDir('N')

if __name__ == "__main__":
    main()

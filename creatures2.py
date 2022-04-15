# Creatures move and eat the plants
import random
from gridworld import *

# Window Behavior
period = 0.033 # [s]
willRender = True

# Look Behavior
width = 100
height = 100
creatureSize = 1.5
plantSize = 0.6

# Behavior vars
lookRadius = 5
plantSpawnNum = 80
plantSpawnDelay = 10
lifePerPlant = 20
movePeriod = 4

# state vars
loopNum = 0

def main():
	setupGrid(width,height,render=willRender,lines=False,winWidth=600,winHeight=600) # setup
	
	# Add herbivores
	for i in range(40):
		newHerbivore(randCoord())
	
	runGrid(period,updateEntities) # run gridworld

def updateEntities(entities):
	global loopNum
	plantPop = 0	
	for e in entities: 
		if e.getAttr('name') == 'herbivore': # For each herbivore...
			handleHerbivore(e)
		elif e.getAttr('name') == 'plant': # for each plant...
			plantPop += 1 # update plant counter
	
	if loopNum%plantSpawnDelay == 0: # Add more plants
		addPlants()
				
	# Print plant pop
	if loopNum%50 == 0:
		print('plant population: '+str(plantPop))
	loopNum += 1

def handleHerbivore(e):
	if e.getAttr('moveProg')%movePeriod == 0:
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
				e.setAttr('life', (e.getAttr('life') + lifePerPlant))
				break # only eat once 
		if e.getAttr('life') <= 0:
			e.remove() # Dead
		if e.getAttr('life') > 60: # reproduce!
			e.setAttr('life', (e.getAttr('life') - 40)) # lose life
			new = newHerbivore(e.location)
			randMove(new)
	e.setAttr('life', (e.getAttr('life')-1)) # Reduce one life always
	e.setAttr('moveProg', (e.getAttr('moveProg')+1)) # Increase moveProg

def addPlants():
	for i in range(plantSpawnNum):
		x = random.randint(0,width-1)
		y = random.randint(0,height-1)
		if entitiesEachCoord[y][x] == set():
			GridEntity((x,y),plantSize,name='plant',color='black')

def newHerbivore(coord):
	h = GridEntity(coord,creatureSize,name='herbivore',color='green')
	h.setAttr('life', 20)
	h.setAttr('moveProg', random.randint(0,movePeriod-1))
	return h
			
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

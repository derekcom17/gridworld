# Creatures move and eat the plants
import random
from gridworld import *

# Window Behavior
period = 0.030 # [s]
willRender = True
winSize = 600

# Look Behavior
width = 100
height = 100

# Plants
plantSize = 0.6
plantSpawnNum = 80
plantSpawnDelay = 10

# Herbivores
herb_size = 1.5
herb_lookRadius = 8
herb_movePeriod = 2
herb_longivity = 60
lifePerPlant = 20

# Carnivores
carn_size = 2.0
carn_lookRadius = 10
carn_movePeriod = 2
carn_longivity = 60
lifePerHerbivore = 20


# state vars
loopNum = 0
logFile = open('creatures3_log.csv', 'w') # open logFile

def main():
	setupGrid(width,height,render=willRender,lines=False,winWidth=winSize,winHeight=winSize) # setup
	
	# Add entities
	for i in range(100):
		newHerbivore(randCoord())
	for i in range(10):
		newCarnivore(randCoord())
	addPlants(8*plantSpawnNum)
	
	logPoint(['time','plants','herbivores','carnivores']) # print log headder
	runGrid(period,updateEntities) # run gridworld
	
	logFile.close() # close logFile

def updateEntities(entities):
	global loopNum
	pops = [0,0,0]
	for e in entities: 
		if e.getAttr('name') == 'herbivore': # For each herbivore...
			handleHerbivore(e)
			pops[1] += 1
		elif e.getAttr('name') == 'carnivore':
			handleCarnivore(e)
			pops[2] += 1
		elif e.getAttr('name') == 'plant': # for each plant...
			pops[0] += 1 # update plant counter
	
	if loopNum%plantSpawnDelay == 0: # Add more plants
		addPlants(plantSpawnNum)
	
	logPoint([loopNum,pops[0],pops[1],pops[2]])
	# Print pops
	if loopNum%50 == 0:
		print('plants:     '+str(pops[0]))
		print('herbivores: '+str(pops[1]))
		print('carnivores: '+str(pops[2]))
		print('')
	loopNum += 1

def handleHerbivore(e):
	if e.getAttr('moveProg')%herb_movePeriod == 0:
		food = e.closestInRadius(herb_lookRadius,'name','plant') # look 
		if food: # move toward food
			move = moveTowards(food)
			e.move(move[0],move[1])
		else: # Avoid competitors
			neighbor = e.closestInRadius(herb_lookRadius,'name','herbivore') # look 
			if neighbor and len(e.entitiesAtRelCoord()) == 1:
				move = moveTowards(neighbor)
				e.move(-move[0],-move[1]) # Move away for neighbor
			else: # Move randomly
				randMove(e) 			
		others = e.entitiesAtRelCoord() # eat
		for other in others:
			if other.getAttr('name') == 'plant':
				other.remove() 
				e.setAttr('life', (e.getAttr('life') + lifePerPlant))
				break # only eat once 
		if e.getAttr('life') <= 0:
			e.remove() # Dead
		if e.getAttr('life') > herb_longivity: # reproduce!
			e.setAttr('life', (e.getAttr('life') - (herb_longivity/2))) # lose life
			new = newHerbivore(e.location)
			randMove(new)
	e.setAttr('life', (e.getAttr('life')-1)) # Reduce one life always
	e.setAttr('moveProg', (e.getAttr('moveProg')+1)) # Increase moveProg

def handleCarnivore(e):
	if e.getAttr('moveProg')%carn_movePeriod == 0:
		food = e.closestInRadius(carn_lookRadius,'name','herbivore') # look 
		if food: # move
			move = moveTowards(food)
			e.move(move[0],move[1])
		else:
			neighbor = e.closestInRadius(carn_lookRadius,'name','carnivore') # look 
			if neighbor and len(e.entitiesAtRelCoord()) == 1:
				move = moveTowards(neighbor)
				e.move(-move[0],-move[1]) # Move away for neighbor
			else:
				randMove(e) 				
		others = e.entitiesAtRelCoord() # eat
		for other in others:
			if other.getAttr('name') == 'herbivore':
				other.remove() 
				e.setAttr('life', (e.getAttr('life') + lifePerHerbivore))
				break # only eat once 
		if e.getAttr('life') <= 0:
			e.remove() # Dead
		if e.getAttr('life') > carn_longivity: # reproduce!
			e.setAttr('life', (e.getAttr('life') - (carn_longivity/2))) # lose life
			new = newCarnivore(e.location)
			randMove(new)
	e.setAttr('life', (e.getAttr('life')-1)) # Reduce one life always
	e.setAttr('moveProg', (e.getAttr('moveProg')+1)) # Increase moveProg
	
def addPlants(spawnNum):
	for i in range(spawnNum):
		x = random.randint(0,width-1)
		y = random.randint(0,height-1)
		if entitiesEachCoord[y][x] == set():
			GridEntity((x,y),plantSize,name='plant',color='black')

def newHerbivore(coord):
	h = GridEntity(coord,herb_size,name='herbivore',color='green')
	h.setAttr('life', 20)
	h.setAttr('moveProg', random.randint(0,herb_movePeriod-1))
	return h

def newCarnivore(coord):
	h = GridEntity(coord,carn_size,name='carnivore',color='red')
	h.setAttr('life', 40)
	h.setAttr('moveProg', random.randint(0,carn_movePeriod-1))
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

def logPoint(points):
	data = str(points[0])
	for i in range(1,len(points)):
		data += (','+str(points[i]))
	logFile.write(data+'\n')
	
if __name__ == "__main__":
    main()

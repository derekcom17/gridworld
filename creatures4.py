# Evolving creatures!
import random
from gridworld import *

# Window Behavior
period = 0.05 # [s]
willRender = True
winSize = 400

# Look Behavior
width = 50
height = 50

# Plant vars
plantSize = 0.6
initialPlantSpawnNum = 30
regularPlantSpawnNum = 20
plantSpawnDelay = 5

# Creature vars
lifePerPlant = 20
lifePerCreature = 40
omnivorePenalty = 0.75
creatureLongivity = 60
mutationProbablity = 0.05

# Make multiple starting species...
defaultStats = []
defaultStats.append('herbivore') # Type
defaultStats.append(1.5)         # size
defaultStats.append(2)           # move period
defaultStats.append(8)           # look radius
defaultStats.append(['avoid_predators','persue_food','avoid_competitors']) # Priorities



# state vars
loopNum = 0
logFile = open('creatures3_log.csv', 'w') # open logFile

def main():
	setupGrid(width,height,render=willRender,lines=False,winWidth=winSize,winHeight=winSize) # setup
	
	# Add entities
	addPlants(initialPlantSpawnNum)
	for i in range(1):
		newCreature(randCoord())
	
	#logPoint(['time','plants','herbivores','carnivores']) # print log headder
	runGrid(period,updateEntities) # run gridworld
	
	logFile.close() # close logFile

def updateEntities(entities):
	global loopNum
	#pops = [0,0,0]
	for e in entities: 
		if e.getAttr('name') != 'plant':
			handleCreature(e)		
	
	if loopNum%plantSpawnDelay == 0: # Add more plants
		addPlants(regularPlantSpawnNum)
	
	#logPoint([loopNum,pops[0],pops[1],pops[2]])
	# Print pops
	#if loopNum%50 == 0:
	#	print('plants:     '+str(pops[0]))
	#	print('herbivores: '+str(pops[1]))
	#	print('carnivores: '+str(pops[2]))
	#	print('')
	loopNum += 1

def handleCreature(e):
	moveProg = e.getAttr('moveProg')
	movePeriod = e.getAttr('move_period')
	if moveProg % movePeriod == 0: # Time to move
		creatureMoves(e)
		creatureEats(e)
	creatureDies(e)
	creatureReproduces(e)
	energy = e.getAttr('energy')
	delPower = getCreaturePower(e)
	e.setAttr('energy', energy - delPower) # Reduce energy by power of creature
	e.setAttr('moveProg', moveProg + 1) # Increase moveProg

# Move functions:
def creatureMoves(e):
	priorities = e.getAttr('priorities')
	success = False
	for i in range(3):
		if   priorities[i] == 'persue_food':
			success = persueFood(e)
			#if success:
			#	print('persued food.')
		elif priorities[i] == 'avoid_predators':
			success = avoidPredator(e)
			#if success:
			#	print('avoided predator.')
		elif priorities[i] == 'avoid_competitors':
			success = avoidCompetitors(e)
			#if success:
			#	print('avoided competitor.')
		else:
			print('Something broke...')
		if success:
			break
	if not success:
		randMove(e) # Move randomly if no stimulus

def persueFood(e):
	target = False
	type = e.getAttr('name')
	radius = e.getAttr('look_radius')
	target = e.closestInRadiusFunct(radius, isEdible)
	if target:
		move = moveTowards(target)
		e.move(move[0],move[1])
		return True
	return False

def isEdible(this, other):
	type = this.getAttr('name')
	if type != 'carnivore': # eats plants
		if other.getAttr('name') == 'plant': # is a plant
			return True
	if type != 'herbivore':
		if other.getAttr('name') == 'plant':
			return False
		if this.getAttr('size') * 0.9 >= other.getAttr('size'): # Don't hardcode this?
			return True
	return False

def avoidPredator(e):
	target = False
	radius = e.getAttr('look_radius')
	target = e.closestInRadiusFunct(radius, isPreditor)
	if target:
		move = moveTowards(target)
		e.move(-move[0],-move[1]) # Move away instead
		return True
	return False

def isPreditor(this, other):
	if other.getAttr('name') == 'plant':
		return False
	return isEdible(other, this)
	'''if other.getAttr('name') == 'plant':
		return False
	if other.getAttr('name') != 'herbivore': # other eats meat
		return other.getAttr('size') * 0.9 >= this.getAttr('size'): # Don't hardcode this?'''
	
def avoidCompetitors(e):
	target = False
	radius = e.getAttr('look_radius')
	target = e.closestInRadiusFunct(radius, isCompetitor)
	if target and len(e.entitiesAtRelCoord()) == 1: # only if alone
		move = moveTowards(target)
		e.move(-move[0],-move[1]) # Move away instead
		return True
	return False

def isCompetitor(this, other):
	if other.getAttr('name') == 'plant':
		return False
	type = this.getAttr('name')
	if type == 'omnivore':
		return True # Everyone is competitor!
	if type == 'herbivore':
		return other.getAttr('name') != 'carnivore' # Other also eats plants
	if type == 'carnivore':
		return other.getAttr('name') != 'herbivore' # Other also eats meat
	return False # (Should never reach here...)


def creatureEats(e):
	others = e.entitiesAtRelCoord()
	for other in others:
		if isEdible(e, other):
			life = 0
			if other.getAttr('name') == 'plant':
				life = lifePerPlant
			else:
				life = lifePerCreature
			other.remove() 
			if e.getAttr('name') != 'omnivore':
				e.setAttr('energy', (e.getAttr('energy') + life))
			else :
				e.setAttr('energy', (e.getAttr('energy') + (life * omnivorePenalty)))
			break # only eat once 

def creatureDies(e):
	if e.getAttr('energy') <= 0:
			e.remove() # Dead

def creatureReproduces(e):
	if e.getAttr('energy') > creatureLongivity: # reproduce!
			e.setAttr('energy', (e.getAttr('energy') / 2)) # lose life
			
			childType = e.getAttr('name')
			childSize = e.getAttr('size')
			childPeriod = e.getAttr('move_period')
			childRadius = e.getAttr('look_radius')
			childPriorities = e.getAttr('priorities')
			
			if pChance(mutationProbablity): # Mutate type
				if childType == 'omnivore': # parent is omnivore
					if pChance(0.5):
						childType = 'herbivore'
					else:
						childType = 'carnivore'
				else: 
					childType = 'omnivore'
			if pChance(mutationProbablity): # Mutate size
				if pChance(0.5):
					childSize *= 1.1
				else:
					childSize /= 1.1
			if pChance(mutationProbablity): # Mutate speed
				if pChance(0.5):
					childPeriod -= 1
				else:
					childPeriod += 1
			#if childPeriod > 6: # constrain minimum speed.
			#	childPeriod = 6
			if childPeriod <= 0:
				childPeriod = 1 # constrin max speed.
			if pChance(mutationProbablity): # Mutate look radius
				if pChance(0.5):
					childRadius -= 1
				else:
					childRadius += 1
			if pChance(mutationProbablity): # Mutate priorities
				if pChance(0.5): # swap 1 and 0
					childPriorities[0],childPriorities[1] = childPriorities[1],childPriorities[0]
				else: # swap 2 and 2
					childPriorities[2],childPriorities[1] = childPriorities[1],childPriorities[2]
			newStats = [childType,childSize,childPeriod,childRadius,childPriorities]
			new = newCreature(e.location, newStats)
			randMove(new)

def getCreaturePower(e):
	size = e.getAttr('size') / 1.5
	speed = 2.0 / e.getAttr('move_period') 
	sense = e.getAttr('look_radius') / 8.0
	
	return (size * pow(speed, 2) + sense) # Equasion for power

def newCreature(location, stats=defaultStats):
	type = stats[0]
	c = 'black'
	if type == 'herbivore':
		c = 'green'
	elif type == 'omnivore':
		c = 'blue'
	else:
		c = 'red'
	e = GridEntity(location, stats[1], name=type, color=c)
	e.setAttr('size',        stats[1])
	e.setAttr('move_period', stats[2])
	e.setAttr('look_radius', stats[3])
	e.setAttr('priorities',  stats[4])
	
	e.setAttr('energy', creatureLongivity / 2)
	e.setAttr('moveProg', random.randint(0,stats[2]-1))
	return e
	
def addPlants(spawnNum):
	for i in range(spawnNum):
		x = random.randint(0,width-1)
		y = random.randint(0,height-1)
		if entitiesEachCoord[y][x] == set():
			GridEntity((x,y),plantSize,name='plant',color='black')
			
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

def pChance(p):
	return random.random() < p
		
def logPoint(points):
	data = str(points[0])
	for i in range(1,len(points)):
		data += (','+str(points[i]))
	logFile.write(data+'\n')
	
if __name__ == "__main__":
    main()

	

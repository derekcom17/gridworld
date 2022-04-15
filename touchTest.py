# Tests touching entities
import random
from gridworld import *

period = 0.05 # [s]

width = 5
height = 5
ballSize = 30

def main():
	setupGrid(width,height,render=True,lines=True)
	
	GridEntity(randCoord(),ballSize,name='red',color='red')
	GridEntity(randCoord(),ballSize,name='blue',color='blue')
	
	runGrid(period,updateEntities)

def updateEntities(entities):
	for e in entities: # Make a random move
		randMove(e) 
		#print('new location: '+str(e.location))
		
	for e in entities: # See if on same space
		atLocation = e.entitiesAtRelCoord((0,0))
		for i in atLocation:
			if not e.getAttr('name') == i.getAttr('name'):
				print(e.getAttr('name')+' met '+i.getAttr('name')+'!')
	
	#print('')

def randMove(e):
	dir = random.randint(0,3)
	if   dir == 0: # Go East
		e.move(1,0)
	elif dir == 1: # Go South
		e.move(0,1)
	elif dir == 2: # Go West
		e.move(-1,0)
	else:          # Go North
		e.move(0,-1)

if __name__ == "__main__":
    main()

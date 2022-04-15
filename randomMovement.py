# Some randomly moving grid entities. 
import random
from gridworld import *

period = 0.000 # [s]
numEntities = 50
colors = ['red','green','blue','yellow','orange']

width = 50
height = 50
ballSize = 2.0

def main():
	setupGrid(width,height,render=True,lines=False)
	
	for i in range(numEntities):
		GridEntity(randCoord(),ballSize,color=colors[random.randint(0,len(colors))-1])
	
	runGrid(period,updateEntities)

def updateEntities(entities):
	for e in entities:
		dir = random.randint(0,4)
		if   dir == 0: # Go East
			e.moveInDir('E')
		elif dir == 1: # Go South
			e.moveInDir('S')
		elif dir == 2: # Go West
			e.moveInDir('W')
		elif dir == 3: # Go North
			e.moveInDir('N')
		else: 
			pass # stay put

if __name__ == "__main__":
    main()

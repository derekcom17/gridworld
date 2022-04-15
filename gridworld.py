# gridworld.py
from graphics import *
import random, time, math

## GLOBAL VARS

window = False # Graphics window
gridPoints = []
cashedContainedPoints = {} # key: radius, value: set of points inside radius
gridWidth = 0  # Number of squares in x dimension
gridHeight = 0 # Number of squares in y dimension

allEntities = set()      # set of GridEntitys
newEntities = set()      # entities just created
deleatedEntities = set() # removed entities get added here
entitiesEachCoord = []   # all entities get added here per location

isDone = False # Default to keep running

## GRID CONTROL FUNCTIONS

def setupGrid(width, height, winWidth=400, winHeight=400, render=True, lines=True):
	global window, gridpoints, gridWidth, gridHeight, entitiesEachCoord
	gridWidth = width
	gridHeight = height
	for y in range(gridHeight): # initialize entitiesEachCoord
		row = []
		for x in range(gridWidth):
			row.append(set())
		entitiesEachCoord.append(row)	
	if render: # setup window
		window = GraphWin("GRIDWORLD", winWidth, winHeight)		
		for y in range(gridHeight): # Make gridPoints
			row = []
			yCoord = (2*y+1)*window.getHeight()/gridHeight / 2
			for x in range(gridWidth):
				xCoord = (2*x+1)*window.getWidth()/gridWidth / 2
				row.append(Point(xCoord,yCoord))
			gridPoints.append(row)
		if (lines): # add lines
			drawGridlines()	

def drawGridlines():
	global window, gridHeight, gridWidth	
	# Draw vertical lines
	for x in range(1,gridWidth+1):
		offset = x * window.getWidth() / gridWidth
		line = Line(Point(offset,0),Point(offset,window.getHeight()))
		line.draw(window)
	# Draw horizontal lines
	for y in range(1,gridHeight+1):
		offset = y * window.getHeight() / gridHeight
		line = Line(Point(0,offset),Point(window.getWidth(),offset))
		line.draw(window)

def placeDots(size):
	global window, gridPoints
	for i in range(len(gridPoints)):
		for j in range(len(gridPoints[i])):
			Circle(gridPoints[i][j],size).draw(window)

def doneGrid():
	global window
	window.getMouse() # Pause to view result
	window.close()    # Close window when done

def checkClick():
	global window
	return window.checkMouse()

def closeGrid():
	global window
	window.close()

def runGrid(period_s, updateFunct, closeOnClick=True):
	global isDone, newEntities, allEntities
	updateSets()
	isDone = False
	while (not (window and closeOnClick and checkClick())) and (not isDone):
		startTime = time.clock()
		
		callUpdateFunct(updateFunct)
		
		updateSets()
		
		if(time.clock()-startTime > period_s):
			dt = round(1000*(time.clock()-startTime),1)
			print("TIME! ("+str(dt)+" ms)")
		else:
			while (time.clock()-startTime < period_s):
				time.sleep(0.001) # wait 1 ms
	
	closeGrid()

def updateSets():
	global allEntities, newEntities, deleatedEntities
	for e in newEntities:
		allEntities.add(e)
	newEntities = set()
	
	willDestory = set()
	for e in deleatedEntities: # Remove entities
		allEntities.discard(e)
		if window:
			e.circle.undraw()
	
def callUpdateFunct(updateFunct):
	return updateFunct(allEntities)

def stopGrid():
	global isDone
	isDone = True

def randCoord():
	x = random.randint(0,gridWidth-1)
	y = random.randint(0,gridHeight-1)
	return (x,y)

def pointsInRadius(radius):
	if radius in cashedContainedPoints:
		return cashedContainedPoints[radius]
	else:
		points = set()
		for x in range(-radius,radius+1):
			for y in range(-radius,radius+1):
				if math.sqrt(pow(x,2) + pow(y,2)) <= radius:
					points.add((x,y))
		cashedContainedPoints[radius] = points
		return points
	
## GRID ENTITY CLASS

class GridEntity:
	def __init__(self,location,size,color='black',name='DEFAULT'):
		self.attr = {} # Empty dict
		self.attr['name'] = name
		newEntities.add(self)
		
		locationX = (location[0])%gridWidth
		locationY = (location[1])%gridHeight
		self.location = (locationX, locationY)
		entitiesEachCoord[locationY][locationX].add(self)
		if window:
			actualSize = size*window.getHeight()/gridHeight/2
			self.circle = Circle(gridPoints[locationY][locationX],actualSize)
			self.circle.setFill(color)
			self.circle.draw(window)
		else:
			self.circle = False
	
	def moveTo(self,location):
		entitiesEachCoord[self.location[1]][self.location[0]].discard(self)
		locationX = (location[0])%gridWidth
		locationY = (location[1])%gridHeight
		self.location = (locationX, locationY)
		entitiesEachCoord[locationY][locationX].add(self)
		if self.circle:
			nextPoint = gridPoints[locationY][locationX]
			dx = nextPoint.getX() - self.circle.getCenter().getX()
			dy = nextPoint.getY() - self.circle.getCenter().getY()
			self.circle.move(dx,dy)
	
	def move(self,dx,dy):
		self.moveTo((self.location[0]+dx, self.location[1]+dy))
	
	def moveInDir(self,dir):
		if   dir == 'N':
			self.move( 0,-1)
		elif dir == 'NE':
			self.move( 1,-1)
		elif dir == 'E':
			self.move( 1, 0)
		elif dir == 'SE':
			self.move( 1, 1)
		elif dir == 'S':
			self.move( 0, 1)
		elif dir == 'SW':
			self.move(-1, 1)
		elif dir == 'W':
			self.move(-1, 0)
		elif dir == 'NW':
			self.move(-1,-1)
		else:
			print('Direction: '+dir+' not valid!')
	
	def remove(self):
		deleatedEntities.add(self)
		entitiesEachCoord[self.location[1]][self.location[0]].discard(self)
	
	def getAttr(self,attr):
		return self.attr[attr]
	
	def setAttr(self,attr,value):
		self.attr[attr] = value
	
	def entitiesAtRelCoord(self, coord=(0,0)):
		coordX = ((self.location[0]+coord[0])%gridWidth)
		coordY = ((self.location[1]+coord[1])%gridHeight)
		#print('checking: ('+str(coordX)+','+str(coordY)+')')
		return entitiesEachCoord[coordY][coordX]
	
	def entsInRadius(self,radius):
		result = {}
		'''for x in range(-radius,radius+1):
			for y in range(-radius,radius+1):
				if math.sqrt(pow(x,2) + pow(y,2)) <= radius: # Make lookup table for this?
					result[(x,y)] = self.entitiesAtRelCoord((x,y))'''
		for point in pointsInRadius(radius):
			if point != (0,0): # Don't look at own location
				result[point] = self.entitiesAtRelCoord(point)
		return result

	def closestInRadius(self,radius,attr=False,value='DEFAULT'):
		nearby = self.entsInRadius(radius)
		closestCoord = False
		closestDist = gridHeight+gridWidth
		for space in nearby: # each space...
			inSpace = nearby[space]
			for e in inSpace: # each entity on space...
				if attr: # We are looking for a specific attr value
					if e.getAttr(attr) == value: # Has the value
						dist = self.movesToReach(space)
						if dist < closestDist: # Is closer
							closestCoord = space
							closestDist = dist
				else: # Looking for any entity
					dist = movesToReach(space)
					if dist < closestDist: # Is closer
						closestCoord = space
						closestDist = dist
		return closestCoord
	
	def closestInRadiusFunct(self,radius,qualifies):
		nearby = self.entsInRadius(radius)
		closestCoord = False
		closestDist = gridHeight+gridWidth
		for space in nearby: # each space...
			inSpace = nearby[space]
			for e in inSpace: # each entity on space...
				if qualifies(self, e): # Qualifies
					dist = self.movesToReach(space)
					if dist < closestDist: # Is closer
						closestCoord = space
						closestDist = dist
				#else: # Looking for any entity
				#	dist = self.movesToReach(space)
				#	if dist < closestDist: # Is closer
				#		closestCoord = space
				#		closestDist = dist
		return closestCoord
	
	def movesToReach(self,coord):
		result = 0
		x = coord[0]
		y = coord[1]
		while (x,y) != (0,0):
			if (x != 0):
				x -= x / abs(x)
			if (y != 0):
				y -= y / abs(y)
			result += 1
		return result
	
## MAIN

def dummy(entities):
	pass

def main():
	setupGrid(16,16)
	runGrid(0.01,dummy)

if __name__ == "__main__":
	main()

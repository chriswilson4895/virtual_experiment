import pygame
#import random
from numpy import linspace, meshgrid, column_stack, array
import math

# COLORS and SCALE
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)
grey = (128,128,128)
gold = (255,215,0)
COLOR = (1, 1, 1)
scale = 20
  
  
from peds import *
from bounds import *
from ExperimentMapConfig import *



# edit generatePeds
def generatePeds(all_pedestrians,numPeds):
    # this is run on the enter stage of the game
    playerPos = 0
    playerTarget = 0
    if len(all_pedestrians)>0:
        playerPos = all_pedestrians.sprites()[0].pos
        playerTarget = all_pedestrians.sprites()[0].target
    else:
        playerPos = outsidePoint
        playerTarget = outsidePoint
    for i in all_pedestrians:
        all_pedestrians.remove(i)
    p1 = player(black)
    p1.pos = playerPos
    p1.target = playerTarget
    all_pedestrians.add(p1)
        
    for i in range(numPeds):
        tempPed = npc(grey)
        all_pedestrians.add(tempPed)
    return all_pedestrians


def StartPositions(all_pedestrians,a,b,c,d):
    numPeds = len(all_pedestrians) - 1
    n = math.ceil(math.sqrt(numPeds))
     
    x = linspace(a, b, n)  # Generate n x-coordinates between a and b
    y = linspace(c, d, n)  # Generate n y-coordinates between c and d
    xx, yy = meshgrid(x, y)  # Create a meshgrid of x and y coordinates
    coordinates = column_stack((xx.flatten(), yy.flatten()))
    
    for i in range(numPeds):   
        all_pedestrians.sprites()[i+1].pos = coordinates[i]
    
    return all_pedestrians


def asignTargets(top_targets,bottom_targets,all_pedestrians,method="closest"):
    # all inputs are sprite groups
    if method == "closest":
        counter = 0
        for i in all_pedestrians:
            if counter != 0:
                if i.magnitude(i.wallDist(top_targets.sprites()[0])) > i.magnitude(i.wallDist(bottom_targets.sprites()[0])):
                    i.targetList = bottom_targets.sprites()
                else:
                    i.targetList = top_targets.sprites()
            counter+=1
        return all_pedestrians
    elif method == "even":
        counter = 0
        top_dist_list = []
        for i in all_pedestrians:
            if counter != 0:
                top_dist = i.magnitude(i.wallDist(top_targets.sprites()[0]))
                top_dist_list.append(top_dist)
            counter+=1   
        dist_and_index_list = sorted(enumerate(top_dist_list), key=lambda x: x[1])
        #print(len(dist_and_index_list))
        #print(len(top_dist_list))
        numPeds = len(all_pedestrians) - 1
        split = math.floor(numPeds/2)
        for i in range(numPeds):
            if i <= split:
                all_pedestrians.sprites()[dist_and_index_list[i][0] + 1].asignTargets(top_targets)
            else:
                all_pedestrians.sprites()[dist_and_index_list[i][0] + 1].asignTargets(bottom_targets)
        return all_pedestrians
    elif method == "top":
        counter = 0
        for i in all_pedestrians:
            if counter != 0:
                i.targetList = top_targets.sprites()
            counter+=1
        return all_pedestrians
    elif method == "bottom":
        counter = 0
        for i in all_pedestrians:
            if counter != 0:
                i.targetList = bottom_targets.sprites()
            counter+=1
        return all_pedestrians
        



def generateCoins(coins):
    for i in coins:
        coins.remove(i)
    numCoins = 10
    coins_y_position = insidePoint[1]
    coins_x_positions = linspace((leftWidth+wWidth+fcWidth+2*wWidth)*scale,insidePoint[0]-radius*3,numCoins)
    for i in range(numCoins):
        coin1 = coin(coins_x_positions[i],coins_y_position,gold,"circle")
        coins.add(coin1)
    return coins





boundries = pygame.sprite.Group()
innerRoomBoundries = pygame.sprite.Group()
top_targets = pygame.sprite.Group()
bottom_targets = pygame.sprite.Group()
rooms = pygame.sprite.Group()

for i in wallData:
    wall1 = wall(black, i)
    boundries.add(wall1)

counter = 0
for i in topRouteData:
    label = topRouteLabels[counter]
    target1 = target(i,label)
    top_targets.add(target1)
    counter +=1
 
counter=0
for i in bottomRouteData:
    label = bottomRouteLabels[counter]
    target1 = target(i,label)
    bottom_targets.add(target1)
    counter+=1
    
for i in roomData:
    room1 = room(i)
    rooms.add(room1)
    
for i in innerRoomBoundData:
    wall1 = wall(red,i)
    innerRoomBoundries.add(wall1)








all_pedestrians = pygame.sprite.Group()
all_pedestrians = generatePeds(all_pedestrians,numberPedestrians)
buffer = 2*wWidth
a=int(leftWidth+3*wWidth+fcWidth+buffer)*scale
b=int(leftWidth+wWidth+fcWidth+mrWidth-buffer)*scale
c=int(topWidth+3*wWidth+tcWidth+buffer)*scale
d=int(topWidth+wWidth+tcWidth+mrHeight-buffer)*scale
all_pedestrians = StartPositions(all_pedestrians,a,b,c,d)
"""
all_pedestrians.sprites()[0].pos = outsidePoint
all_pedestrians.sprites()[0].target = outsidePoint
all_pedestrians.sprites()[0].acc = array([0,0])
all_pedestrians.sprites()[0].vel = array([0,0])
"""

coin_counter = CoinCounter(coin_counter_pos)
evac_timer = Timer(timer_pos)
high_score = HighScore(high_score_pos)



radius = all_pedestrians.sprites()[0].rScaled

startExit = checkpoint(pygame.Rect(insidePoint[0]-radius,insidePoint[1]-radius,radius*2,radius*2),COLOR)
endExit = checkpoint(pygame.Rect(outsidePoint[0]-radius,outsidePoint[1]-radius,radius*2,radius*2),red)


endEnter = checkpoint(pygame.Rect(insidePoint[0]-radius,insidePoint[1]-radius,radius*2,radius*2),red)
startEnter = checkpoint(pygame.Rect(outsidePoint[0]-radius,outsidePoint[1]-radius,radius*2,radius*2),COLOR)


coins = pygame.sprite.Group()
coins = generateCoins(coins)



### TRAINING CONFIG



def generateTrainingPeds(training_pedestrians,numPeds):

    playerPos = startPoint
    playerTarget = startPoint
    for i in training_pedestrians:
        training_pedestrians.remove(i)
    p1 = player(black)
    p1.pos = playerPos
    p1.target = playerTarget
    training_pedestrians.add(p1)
        
    for i in range(numPeds):
        tempPed = npc(grey)
        tempPed.speed = 3
        training_pedestrians.add(tempPed)
    return training_pedestrians



training_pedestrians = pygame.sprite.Group()
training_pedestrians = generateTrainingPeds(training_pedestrians,5)
buffer = 2*wWidth
a = int(leftWidth+wWidth + buffer)*scale
b = int(leftWidth+wWidth+bWidth-buffer)*scale
c = int(topWidth+wWidth+buffer)*scale
d = int(topWidth+wWidth+bHeight-buffer)*scale
training_pedestrians = StartPositions(training_pedestrians,a,b,c,d)


radius = training_pedestrians.sprites()[0].rScaled
startTraining = checkpoint(pygame.Rect(startPoint[0]-radius,startPoint[1]-radius,radius*2,radius*2),COLOR)
endTraining = checkpoint(pygame.Rect(endPoint[0]-radius,endPoint[1]-radius,radius*2,radius*2),red)


trainingObjects = pygame.sprite.Group()

orange = (255, 165, 0)
blue = (0, 0, 255)
purple= (128, 0, 128)
obj1 = coin(objPositions[0][0],objPositions[0][1],orange,"triangle")
obj2 = coin(objPositions[1][0],objPositions[1][1],blue,"square")
obj3 = coin(objPositions[2][0],objPositions[2][1],purple,"circle")
trainingObjects.add(obj1)
trainingObjects.add(obj2)
trainingObjects.add(obj3)
coins = generateCoins(coins)

trainingBounds = pygame.sprite.Group()
trainingRooms = pygame.sprite.Group()

for i in trainingWallData:
    wall1 = wall(black,i)
    trainingBounds.add(wall1)
    
for i in trainingRoomData:
    room1 = room(i)
    trainingRooms.add(room1)



















"""
def StartPositions(all_pedestrians):
    numPeds = len(all_pedestrians) - 1
    center_list = [all_pedestrians.sprites()[0].pos]
    radius = all_pedestrians.sprites()[0].rScaled
    for i in range(numPeds):
        notValid = True
        while notValid:
            rand_x = random.randint(int(leftWidth+3*wWidth+fcWidth)*scale,int(leftWidth+wWidth+fcWidth+mrWidth)*scale)
            rand_y = random.randint(int(topWidth+3*wWidth+tcWidth)*scale,int(topWidth+wWidth+tcWidth+mrHeight)*scale)
            index = 0
            Valid = True
            while Valid and index < len(center_list):
                if (rand_x-center_list[index][0])**2 + (rand_y-center_list[index][1])**2 < radius**2:
                    Valid = False
                    print("overlap")
                else:
                    index +=1
            if Valid == True:
                notValid = False
                all_pedestrians.sprites()[i+1].pos = array([rand_x,rand_y])
                center_list.append([rand_x,rand_y])
    return all_pedestrians
"""

"""
center_list = [insidePoint]
numPeds = 20

for i in range(numPeds):
    notValid = True
    while notValid:
        rand_x = random.randint(int(leftWidth+3*wWidth+fcWidth)*scale,int(leftWidth+wWidth+fcWidth+mrWidth)*scale)
        rand_y = random.randint(int(topWidth+3*wWidth+tcWidth)*scale,int(topWidth+wWidth+tcWidth+mrHeight)*scale)
        index = 0
        Valid = True
        while Valid and index < len(center_list):
            if (rand_x-center_list[index][0])**2 + (rand_y-center_list[index][1])**2 < radius**2:
                Valid = False
                print("overlap")
            else:
                index +=1
        if Valid == True:
            notValid = False
            currentPedTargets = bottom_targets
            if i>= 10:
                currentPedTargets = top_targets
            ped = npc(grey,currentPedTargets)
            ped.pos = array([rand_x,rand_y])
            center_list.append([rand_x,rand_y])
            pedestrians.add(ped)
            all_pedestrians.add(ped)

"""

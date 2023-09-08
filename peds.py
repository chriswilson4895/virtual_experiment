import pygame
from numpy import array, dot, reshape
import math
import random

# COLORS and SCALE
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)
grey = (128,128,128)
gold = (255,215,0)
COLOR = (1, 1, 1)
scale = 20



class coin(pygame.sprite.Sprite):
    def __init__(self,x,y,color,shape):
        super().__init__()
        self.radius = 0.5
        self.rScaled = self.radius*scale
        
        self.color = color
        self.shape = shape
        #print("USED COIN!")
        self.image = pygame.Surface([self.rScaled*2, self.rScaled*2])
        self.image.set_colorkey(COLOR)
        self.image.fill(COLOR)
      
        if self.shape == "triangle":

            points = [(0, self.rScaled * 2), (self.rScaled * 2, self.rScaled * 2), (self.rScaled, 0)]
            pygame.draw.polygon(self.image, self.color, points)
        elif self.shape == "circle":
            pygame.draw.circle(self.image, self.color, (self.rScaled, self.rScaled), self.rScaled)
        elif self.shape == "square":
            pygame.draw.rect(self.image, self.color, (0, 0, self.rScaled * 2, self.rScaled * 2))

        
        self.rect = self.image.get_rect()
        self.rect.x = x - 10
        self.rect.y = y - 10
        self.pos = array([x,y])
        self.enabled = True
        
    def blitMe(self,surface):
        if self.enabled == False:
            return
        else:
            surface.blit(self.image,self.rect)
        
    def checkCollection(self,player):
        if self.enabled == True:
            if self.magnitude(self.pos-player.pos) < player.rScaled + self.radius:
                self.enabled = False
                return True
            else:
                return False
        else:
            return False
            
    def magnitude(self,vector):
        return math.sqrt(sum(pow(element, 2) for element in vector))  

      
class player(pygame.sprite.Sprite):
    

    def __init__(self, color):
        super().__init__()

        self.r = 0.5 #m
        self.speed = 3 #m
        
        # scale is number of pixels per m
        # radius is half a meter
        # divide pixels by scale to get m
        # times m by by scale to get pixels
        
        self.top_speed = 3

        # pos, acc, vel
        self.acc = array([0,0]) #m
        self.vel = array([0,0]) #m
    
        self.scale = scale
        self.rScaled = self.r*self.scale
         
        # image is a surface
        self.image = pygame.Surface([self.rScaled*2, self.rScaled*2])
        
        self.image.set_colorkey(COLOR)
        self.image.fill(COLOR)
  
        # you draw onto a surface
        # pygame.Rect(left,top,width,height)
        
        #pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height))
        pygame.draw.circle(self.image,color, pygame.Vector2(self.rScaled, self.rScaled), self.rScaled)
        # the coordinates for draw are relative to the surface, not the screen!!!!
        
        #print(pygame.Vector2(xStart+width, yStart+width))
        # self.rect controls the position of where the image is drawn in later updates
        self.rect = self.image.get_rect()
        # gives the left,top,width,height of the surface. all surface start at 0,0
        #print(self.rect)
        
        # by default location is 0,0 and this moves it
        self.rect.x = 0
        self.rect.y = 0
        
        
        #if these arent set then when draw and update are called the image is considered to still be in 0,0

        # these are for my own use
        self.pos = array([self.rScaled,self.rScaled]) #pixels
        self.target = array([self.rScaled,self.rScaled]) #pixels
        
        
    def updateTarget(self,target):
        self.target = target
        #self.target = target - [self.r, self.r]

    def drawTarget(self,surface):
        borderWidth = 3
        targetImage = pygame.Surface([self.rScaled*2 + 2*borderWidth,self.rScaled*2 + 2*borderWidth])
        targetImage.set_colorkey(COLOR)
        targetImage.fill(COLOR)
        pygame.draw.circle(targetImage, red, pygame.Vector2(self.rScaled+borderWidth, self.rScaled+borderWidth), self.rScaled+borderWidth)
        pygame.draw.circle(targetImage, COLOR, pygame.Vector2(self.rScaled+borderWidth, self.rScaled+borderWidth), self.rScaled)
        targetRect = targetImage.get_rect()
        targetRect.x = self.target[0] - self.rScaled - borderWidth
        targetRect.y = self.target[1] - self.rScaled - borderWidth
        surface.blit(targetImage,targetRect)
        
    def updateOld(self,dt,bounds,peds):
        
        new_pos = self.pos
        
        #print(self.target)
        #print(self.pos)
        

        diff = self.target - self.pos
        
        diff_mag = ((diff[0])**2 + (diff[1])**2)**(1/2) #magnitude of how far we need to go
        change_mag = dt*self.speed #magnitude of how much we gonna move
        
        if diff_mag > 0:
            if change_mag > diff_mag: #if we gonna move further than the distance just move to there
                change = diff_mag*diff
                new_pos = self.target
            else:
                ratio = change_mag/diff_mag
                change = ratio*diff    
                new_pos = self.pos + change
            
            
            self.rect.x = new_pos[0]
            self.rect.y = new_pos[1]
            self.pos = array([self.rect.x,self.rect.y])
    
            collide = False
            counter = 0
            bounds = bounds.sprites()
            while collide == False and counter < len(bounds):
                if self.rect.colliderect(bounds[counter]):
                    collide = True
                counter += 1
            
            if collide:
                new_pos = new_pos - change
                self.target = new_pos
            
            
            self.rect.x = new_pos[0]
            self.rect.y = new_pos[1]
            self.pos = new_pos
                 
    def update(self,dt,bounds,peds):
        if self.magnitude(self.pos-self.target)<1:
            self.acc = array([0,0])
            self.vel = array([0,0])
        boundsList = bounds.sprites()
        pedsList = peds.sprites()
        totalForce = array([0,0])
        wallDists = []
        playerDists = []
        
        A = 2e3
        B = 0.08
        k = 1.2e5
        K = 2.4e5
        
        r = self.r
        rScaled = r*self.scale
        vel = self.vel
        acc = self.acc
        speed = self.speed
        
        def g(x):
            # return zero if pedestrians do not touch
            if x<0:
                return 0
            else:
                return x
            
        index = 0
        for i in boundsList:
            loc = self.wallDist(i)
            
            dist = self.magnitude(loc)/self.scale #dist in m from ped centre to wall edge
            wallDists.append(dist)
            n_iW = -1*self.normalise(loc) #direction the force acts in
            t_iW = array([-n_iW[1],n_iW[0]])
            
            overlap = -dist
            #if index == 0:
            #    print(str(overlap))
            #index+=1
            
            normalFactor = A*math.exp((overlap)/B) + k*g((overlap))
            normalForce = normalFactor*n_iW
            
            tangFactor = K*g((overlap))*(dot(vel, t_iW))
            tangForce = tangFactor*t_iW
            
            wallForce = normalForce - tangForce
            #wallForces.append(wallForce)
            
            #print(normalFactor)
            #print(tangFactor)
           
            
            totalForce = totalForce + wallForce
        
        for i in pedsList:
            loc = self.playerDist(i)
            
            dist = self.magnitude(loc)/self.scale #dist in m from ped centre to wall edge
            playerDists.append(dist)
            n_iW = -1*self.normalise(loc) #direction the force acts in
            t_iW = array([-n_iW[1],n_iW[0]])
            
            overlap = r-dist
            #if index == 0:
            #    print(str(overlap))
            #index+=1
            
            normalFactor = A*math.exp((overlap)/B) + k*g((overlap))
            normalForce = normalFactor*n_iW
            
            tangFactor = K*g((overlap))*(dot(vel, t_iW))
            tangForce = tangFactor*t_iW
            
            playerForce = normalForce - tangForce
            
            totalForce = totalForce + playerForce
        
        desiredDirection = self.target - self.pos
        if self.magnitude(desiredDirection) > 0:
            desiredDirection = self.normalise(self.target - self.pos)
        else:
            desiredDirection = array([0,0])
        relaxTime = 0.25
        adjustmentForce = (1/relaxTime)*(speed*desiredDirection-vel)
        totalForce = totalForce + adjustmentForce
        
        self.acc = totalForce
        self.vel = self.vel + dt*self.acc

        if self.magnitude(self.vel) > self.top_speed:
            self.vel = self.top_speed*self.normalise(self.vel)
        
        self.pos = self.pos + dt*self.vel*self.scale
        
        self.rect.x = self.pos[0] - rScaled
        self.rect.y = self.pos[1] - rScaled
            
        
        
            
            
    def magnitude(self,vector):
        return math.sqrt(sum(pow(element, 2) for element in vector))
    
    def normalise(self,vector):
        mag = self.magnitude(vector)
        if mag == 0:
            return array([0,0])
        else:
            factor = 1/mag
            return factor*vector
    
    def playerDist(self,player):
        myX = self.pos[0]
        myY = self.pos[1]
        otherX = player.pos[0]
        otherY = player.pos[1]
        return array([otherX-myX,otherY-myY])
        
    def wallDist(self,wall):
        # returns pixel distance
        # input wall is a sprite
        
        # .c1 .c5 .c2
        # .c8 ... .c6
        # .c3 .c7 .c4
        c1 = array([wall.rect.left, wall.rect.top])
        c2 = array([wall.rect.left + wall.rect.width, wall.rect.top])
        c3 = array([wall.rect.left, wall.rect.top + wall.rect.height])
        c4 = array([wall.rect.left + wall.rect.width, wall.rect.top + wall.rect.height])
        x = self.pos[0]
        y = self.pos[1]
        
        dist = array([0,0])
        # if the pedestrian is outside of the wall.
        # wall - self
        if c3[1] < y and c4[1] < y:
            # wall above. neg
            if c4[0] > x and c3[0] < x:
                # direct above
                #dist = array([0,c3[1] - y + self.r])
                dist = array([0,c3[1] - y])
            elif c4[0] < x:
                # top left
                dist = c4 - self.pos
            elif c3[0] > x:
                # top right
                dist = c3 - self.pos
        elif c1[1] > y and c2[1] > y:
            # wall below. pos
            if c1[0] < x and c2[0] > x:
                # direct below
                #dist = array([0, c1[1] - y - self.r])
                dist = array([0, c1[1] - y])
            elif c1[0] > x:
                # bot right
                dist = c1 - self.pos
            elif c2[0] < x:
                # bot left
                dist = c2 - self.pos
            
        elif c2[0] < x and c4[0] < x:
            # wall to left. neg
            if c2[1] < y and c4[1] > y:
                #directly left
                #dist = array([c2[0] - x + self.r,0])
                dist = array([c2[0] - x,0])
            elif c4[1] < y:
                #top left
                dist = c4 - self.pos
            elif c2[1] > y:
                #bot left
                dist = c2 - self.pos
        elif c1[0] > x and c3[0] > x:
            # wall to right. pos
            if c1[1] < y and c3[1] > y:
                # directly right
                #dist = array([c1[0] - x - self.r,0])
                dist = array([c1[0] - x,0])
            elif c3[1] > y:
                # top right
                dist = c3 - self.pos
            elif c1[1] > y:
                # bot right
                dist = c1 - self.pos
        
        # if the pedestrian is inside of the wall
        
        
        return dist
         
    def blitMe(self,surface):
      surface.blit(self.image,self.rect)
        
      
        
      
class npc(player):
    
    def __init__(self,color):
        super().__init__(color)
        self.targetList = 0
        self.randomTargetAsigned = False
        self.speed = 1
    
    def asignTargets(self,targets):
        # input sprite group of targets
        targetList = targets.sprites()
        self.targetList = targetList
        
    def updateTarget(self):
        # checks where we are in the map and what target should be next
        bound1 = self.targetList[0]
        if bound1.rect.colliderect(self):
            #print("here")
            del self.targetList[0]
            
        if len(self.targetList) > 0:
            
            targetRect = self.targetList[0].rect
            targetX = (targetRect.left + targetRect.left + targetRect.width)/2
            targetY = (targetRect.top + targetRect.top + targetRect.height)/2
            targetPos = array([targetX,targetY])
            self.target = targetPos
            return True
        else:
            return False
        
    def wanderTarget(self):
        posVector = reshape(self.pos,(2,1))
        if self.randomTargetAsigned == True:
            targetVector = reshape(self.target,(2,1))
            
            targetDirection = self.normalise(targetVector-posVector)
            
            randomAngle = random.uniform(-1*math.pi/4, math.pi/4)
            randomMatrix = array([[math.cos(randomAngle),-1*math.sin(randomAngle)],[math.sin(randomAngle),math.cos(randomAngle)]])
            self.target = posVector + randomMatrix@(targetDirection*1000)
            
            
            self.target = reshape(self.target,(2))
        else:
            randomAngle = random.uniform(0, 2 * math.pi)
            randomMatrix = array([[math.cos(randomAngle),-1*math.sin(randomAngle)],[math.sin(randomAngle),math.cos(randomAngle)]])
            self.target = posVector + array([[0],[1000]])
            self.target = posVector + randomMatrix@(self.target-posVector)
            #self.target = self.target.T
            self.target = reshape(self.target,(2))
            self.randomTargetAsigned = True
        
        #self.target = self.target + self.normalise(self.acc) * 100
        #self.target = array([0,0])
        #print("wander target")
        
        
    
        
            
        

       

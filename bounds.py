import pygame
from numpy import array

# COLORS and SCALE
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)
grey = (128,128,128)
gold = (255,215,0)
COLOR = (1, 1, 1)
scale = 20

# Initialize pygame
#pygame.init()
# Initialize pygame font module
#pygame.font.init()

class CoinCounter(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.coin_count = 0
        self.font = pygame.font.Font(None, 24)  # Change the font size if desired
        self.color = black

    def update(self):
        self.coin_count += 1

    def blitMe(self, screen):
        coin_text = f"My Score: {self.coin_count} coins"
        text_surface = self.font.render(coin_text, True, self.color)  # Change the text color if desired
        screen.blit(text_surface, self.position)
        
    def reset(self):
        self.coin_count = 0
 
class HighScore(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.score = 12
        self.font = pygame.font.Font(None, 24)  # Change the font size if desired


    def blitMe(self, screen):
        coin_text = f"High Score: {self.score} coins"
        text_surface = self.font.render(coin_text, True, gold)  # Change the text color if desired
        screen.blit(text_surface, self.position)
    
    def update(self,newScore):
        self.score = newScore


class Timer(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.start_time = 0
        self.font = pygame.font.Font(None, 24)  # Change the font size if desired
        self.begin_time = 20000
        self.time = 25000

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.time = self.begin_time - elapsed_time
        if self.time <= 0:
            self.time = 0

    def blitMe(self, screen):
        timeSecs = self.time / 1000
        time_text = f"Time remaining: {timeSecs:.1f}"
        if timeSecs < 5:
            text_surface = self.font.render(time_text, True, red)
        else:
            text_surface = self.font.render(time_text, True, black)  # Change the text color if desired
        screen.blit(text_surface, self.position)
        
    def reset(self):
        self.time = 0

class wall(pygame.sprite.Sprite):
    def __init__(self, color, rectPassed):
        #c1 c2 are two top corners
        super().__init__()
        left = rectPassed[0]
        top = rectPassed[1]
        width = rectPassed[2]
        height = rectPassed[3]
        
        # image is a surface
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.image.set_colorkey(COLOR)
  
        # you draw onto a surface
        
        #pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height))
        #pygame.draw.circle(self.image,color, pygame.Vector2(xStart + width, yStart + width), width)
        
        #print(pygame.Vector2(xStart+width, yStart+width))
        self.rect = self.image.get_rect()
        #print(self.rect)
        
        # by default location is 0,0 and this moves it
        self.rect.x = left
        self.rect.y = top
        #print(self.rect)
        
        
        # these are for my own use
        self.pos = array([self.rect.x,self.rect.y])
        
    def checkCollision(self, objRect):
        a = range(self.rect[0],self.rect[2])
        b = range(self.rect[1],self.rect[3])
        
        
class checkpoint(pygame.sprite.Sprite):

    def __init__(self,rectPassed,color):
        super().__init__()
        left = rectPassed[0]
        top = rectPassed[1]
        width = rectPassed[2]
        height = rectPassed[3]
        
        # image is a surface
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.image.set_colorkey(COLOR)
  
        # you draw onto a surface
        
        #pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height))
        #pygame.draw.circle(self.image,color, pygame.Vector2(xStart + width, yStart + width), width)
        
        #print(pygame.Vector2(xStart+width, yStart+width))
        self.rect = self.image.get_rect()
        #print(self.rect)
        
        # by default location is 0,0 and this moves it
        self.rect.x = left
        self.rect.y = top
        #print(self.rect)
        
        
        # these are for my own use
        self.pos = array([self.rect.x,self.rect.y])
        
    def checkPlayer(self,player):
        # 1 player sprite as input
        if self.rect.colliderect(player):
            return True
        else:
            return False
        
    
    def blitMe(self,surface):
         surface.blit(self.image,self.rect)
         
         
class nce(pygame.sprite.Sprite): #non-collidable enttiy
    def __init__(self,rectPassed):
        super().__init__()
        left = rectPassed[0]
        top = rectPassed[1]
        width = rectPassed[2]
        height = rectPassed[3]
        
        # image is a surface
        self.image = pygame.Surface([width, height])
        
        self.image.set_colorkey(COLOR)
        self.image.fill(COLOR)
  
        # you draw onto a surface
        
        #pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height))
        #pygame.draw.circle(self.image,color, pygame.Vector2(xStart + width, yStart + width), width)
        
        #print(pygame.Vector2(xStart+width, yStart+width))
        self.rect = self.image.get_rect()
        #print(self.rect)
        
        # by default location is 0,0 and this moves it
        self.rect.x = left
        self.rect.y = top
        #print(self.rect)
        
        
        # these are for my own use
        self.pos = array([self.rect.x,self.rect.y])
        
    def blitMe(self,surface):
         surface.blit(self.image,self.rect)

class target(nce):
    def __init__(self,rectPassed,label):
        super().__init__(rectPassed)
        self.image.fill(grey)
        self.label = label
         
         
         
class room(nce):
    def __init__(self,rectPassed):
        super().__init__(rectPassed)
        self.image.fill(COLOR)

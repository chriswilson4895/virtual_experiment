# https://www.geeksforgeeks.org/pygame-creating-sprites/

import pygame
import random
from numpy import array
import math
import csv
#import sys
from pandas import DataFrame

from tkinter import Tk
from tkinter import messagebox

root = Tk()
root.wm_attributes("-topmost", 1)

# COLORS and SCALE
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)
grey = (128,128,128)
gold = (255,215,0)
COLOR = (1, 1, 1)
scale = 20

pygame.init()


from peds import player, npc
from bounds import wall, checkpoint, target

from ExperimentMapConfig import *
from LevelExitConfig import *

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Experiment")

### data collection
coinCollectionTimes = [0,0,0]

coinsCollected = [0,0,0]

evacTimes = [0,0,0]
enterTimes = [0,0,0]

routeChoiceExit = [[],[],[]]
routeChoiceEnter = [[],[],[]]

distanceFromExitsPeds = [0,0,0]

firstCoinCollectionTimes = [0,0,0]

numberClicksEnter = [0,0,0]
numberClicksExit = [0,0,0]


### levels

level = "training"
evacs = 0
stage = "part1"

clock = pygame.time.Clock()
lastRefresh = 0
currentTime = 0




coinFreezeTime = 1500
coinFreezeStartTime = 0


crowdDelays = [0,0,0]
coinsDisplayed = [True,True,True]
treatment = 0
random_number = random.uniform(0, 1)
if random_number < 0.5:
    crowdDelays = [0,0,0]
    coinsDisplayed = [True,True,True]
    treatment = 1
else:
    crowdDelays = [5000,5000,5000]
    coinsDisplayed = [True,True,True]
    treatment = 2
#crowdDelays = [0,0,0]
#coinsDisplayed = [True,True,True]
#treatment = 1
print(treatment)

#print(treatment)
#print(crowdDelays)

# Enter variables
prevTargetCollision = False

### TIMERS AND INDICATORS

bufferTime = 0

enterNotInstructed = True
exitNotInstructed = True
coinDropNotInstructed = True


enterLevelStartTime = 0
enterAfterNotifStartTime = 0
enterAfterNotifElapsedTime = 0

trainingPart1StartTime =  0
trainingPart1TopRoomStartTime = 0
trainingPart1NotInstructed = True
pedInfoNotInstructed = True
topRoomReached = False
objectsCollected = False

part2NotInstructed = True
part2StartTime = 0

part3NotInstructed = True
part3StartTime = 0


exit = True

exitLevelStartTime = 0
evacStartTime = 0
lastCoinCollectedTime = 0
evacInstructed = False
coinsInstructed = False
evacAlertTime = 0 
coinAlertTime = 0

alternativeMessage = False

highScoreBeat = False

# between exit and enter levels
evacFailed = False

my_data = {
    'coinsCollected': coinsCollected,
    'evacTimes': evacTimes,
    'enterTimes': enterTimes,
    'enterSequence': routeChoiceEnter,
    'exitSequence': routeChoiceExit,
    'numberOfClicksEnter': numberClicksEnter,
    'numberOfClicksExit': numberClicksExit
}

df = DataFrame(my_data, index=[1, 2, 3])

refreshRate = 24
simulationRate = 1000

while exit:
    
    dt = clock.tick(simulationRate) / 1000 - bufferTime/1000
    bufferTime = 0
    currentTime = pygame.time.get_ticks()
    
    if level == "training":
        
        
        
        ### EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(pygame.mouse.get_pos())
                #print(type(pygame.mouse.get_pos()))
                training_pedestrians.sprites()[0].updateTarget(array(pygame.mouse.get_pos()))
            if event.type == pygame.VIDEOEXPOSE:
                time=pygame.time.get_ticks()
                bufferTime = bufferTime + time-currentTime
        
        ### UPDATING NPC TARGETS
        counter = 0
        for i in training_pedestrians.sprites():
            if counter>0:
                i.wanderTarget()
            counter += 1
            
        if stage == "part1":
            if trainingPart1StartTime == 0:
                trainingPart1StartTime = pygame.time.get_ticks()
            
            trainingPart1ElapsedTime = currentTime-trainingPart1StartTime
            
            ### UPDATING PLAYER + PEDESTRIAN POSITIONS
            counter = 0
            for i in training_pedestrians:
                if counter == 0:
                    i.update(dt,trainingBounds,training_pedestrians)
                else:
                    i.update(dt,trainingBounds,training_pedestrians)
                counter+=1
            
            ### TOP ROOM REACHED?
            p1 = training_pedestrians.sprites()[0]
            if topRoomReached == False and p1.rect.colliderect(trainingRooms.sprites()[0].rect):
                topRoomReached = True
                trainingPart1TopRoomStartTime = pygame.time.get_ticks()
            
            ### PED TUTORIAL NOTIF
            if currentTime - trainingPart1TopRoomStartTime > 250 and topRoomReached == True and pedInfoNotInstructed == True:
                t1=pygame.time.get_ticks()
                root.wm_withdraw() #to hide the main window
                instruct = "Other pedestrians are shown in grey. Go to the red square!"
                messagebox.showinfo('Training',instruct)
                t2=pygame.time.get_ticks()
                bufferTime = bufferTime + t2-t1
                pedInfoNotInstructed = False
                
            ### ENTER ALERT WINDOW
            if trainingPart1NotInstructed == True and trainingPart1ElapsedTime>250:
                t1=pygame.time.get_ticks()
                root.wm_withdraw() #to hide the main window
                instruct = 'Welcome to the training level!'
                messagebox.showinfo('Training', instruct)
                root.wm_withdraw()
                instruct = 'Your pedestrian is the black circle. To navigate your pedestrian, simply point and click on the screen.'
                messagebox.showinfo('Training',instruct)
                root.wm_withdraw()          
                instruct = 'Navigate to the red square shown on the map.'
                messagebox.showinfo('Training', instruct)
                t2=pygame.time.get_ticks()
                bufferTime = bufferTime + t2-t1
                trainingPart1NotInstructed = False

            ### DRAWING TO SCREEN
            currentTime = pygame.time.get_ticks()
            if currentTime - lastRefresh > 1000/refreshRate:
                screen.fill(white)
                
                p1 = training_pedestrians.sprites()[0]
                for i in trainingRooms.sprites():
                    if p1.rect.colliderect(i.rect):
                        i.image.fill(COLOR)
                    else:
                        i.image.fill(grey)
                
                trainingBounds.draw(screen)
                trainingRooms.draw(screen)
                
                
                endTraining.blitMe(screen)
                startTraining.blitMe(screen)
                
                for i in trainingRooms:
                    if training_pedestrians.sprites()[0].rect.colliderect(i.rect):
                        for j in training_pedestrians:
                            if j.rect.colliderect(i.rect):
                                j.blitMe(screen)
                
                training_pedestrians.sprites()[0].drawTarget(screen)
                training_pedestrians.sprites()[0].blitMe(screen)
                
                pygame.display.flip()
                lastRefresh = pygame.time.get_ticks()
            
            
            if endTraining.checkPlayer(training_pedestrians.sprites()[0]):
                stage = "part2"
                
                trainingPart1LevelStartTime = 0
                currentTime = 0
                
        elif stage == "part2":
            if part2StartTime == 0:
                part2StartTime = pygame.time.get_ticks()
            part2ElapsedTime = currentTime - part2StartTime
            
            
            ### UPDATING PLAYER + PEDESTRIAN POSITIONS
            counter = 0
            for i in training_pedestrians:
                if counter == 0:
                    if currentTime - coinFreezeStartTime > coinFreezeTime:    
                        i.update(dt,trainingBounds,training_pedestrians)
                else:
                    i.update(dt,trainingBounds,training_pedestrians)
                counter+=1
            
            ### PART 2 INSTRUCTIONS        
            if part2NotInstructed == True and part2ElapsedTime > 250:
                t1=pygame.time.get_ticks()
                root.wm_withdraw() #to hide the main window
                instruct = "Collect the objects that are scattered around the room. Simply walk over them to collect them. You will be frozen briefly while collecting objects!"
                messagebox.showinfo('Training',instruct)
                t2=pygame.time.get_ticks()
                bufferTime = bufferTime + t2-t1
                part2NotInstructed = False
 
            ### COIN COLLECTION UPDATES
            for i in trainingObjects:
                if i.checkCollection(training_pedestrians.sprites()[0]):
                    coinFreezeStartTime = pygame.time.get_ticks()
                    allCollected = True
                    counter = 0
                    while allCollected == True and counter < len(trainingObjects):
                        if trainingObjects.sprites()[counter].enabled == True:
                            allCollected = False
                        counter +=1
                    if allCollected == True:
                        objectsCollected = True
  
            ### DRAWING TO SCREEN
            currentTime = pygame.time.get_ticks()
            if currentTime - lastRefresh > 1000/refreshRate:
                screen.fill(white)
                
                p1 = training_pedestrians.sprites()[0]
                
                for i in trainingRooms.sprites():
                    if p1.rect.colliderect(i.rect):
                        i.image.fill(COLOR)
                    else:
                        i.image.fill(grey)
                
                trainingBounds.draw(screen)
                trainingRooms.draw(screen)
                
                
                for i in trainingRooms:
                    if training_pedestrians.sprites()[0].rect.colliderect(i.rect):
                        
                        for j in trainingObjects:
                            if j.rect.colliderect(i.rect):
                                j.blitMe(screen)       
                                
                        for j in training_pedestrians:
                            if j.rect.colliderect(i.rect):
                                j.blitMe(screen)
    
                
                training_pedestrians.sprites()[0].drawTarget(screen)
                training_pedestrians.sprites()[0].blitMe(screen)
                
                pygame.display.flip()
                lastRefresh = pygame.time.get_ticks()
            
            if objectsCollected == True:
                stage = "part3"
                
        elif stage == "part3":
            if part3StartTime == 0:
                part3StartTime = pygame.time.get_ticks()
            part3ElapsedTime = currentTime - part3StartTime
            
            
            ### UPDATING PLAYER + PEDESTRIAN POSITIONS
            counter = 0
            for i in training_pedestrians:
                if counter == 0:
                    if currentTime - coinFreezeStartTime > coinFreezeTime:    
                        i.update(dt,trainingBounds,training_pedestrians)
                else:
                    i.update(dt,trainingBounds,training_pedestrians)
                counter+=1
            
                
            ### PART 3 INSTRUCTIONS        
            if part3NotInstructed == True and part3ElapsedTime > 250:
                t1=pygame.time.get_ticks()
                root.wm_withdraw() #to hide the main window
                instruct = "Walk to the red square."
                messagebox.showinfo('Training',instruct)
                root.wm_withdraw()
                t2=pygame.time.get_ticks()
                bufferTime = bufferTime + t2-t1
                part3NotInstructed = False
            
            
            ### DRAWING TO SCREEN
            currentTime = pygame.time.get_ticks()
            if currentTime - lastRefresh > 1000/refreshRate:
                screen.fill(white)
                
                p1 = training_pedestrians.sprites()[0]
                for i in trainingRooms.sprites():
                    if p1.rect.colliderect(i.rect):
                        i.image.fill(COLOR)
                    else:
                        i.image.fill(grey)
                
                trainingBounds.draw(screen)
                trainingRooms.draw(screen)
                
                endTraining.blitMe(screen)
                startTraining.blitMe(screen)
                
                
                for i in trainingRooms:
                    if training_pedestrians.sprites()[0].rect.colliderect(i.rect):
                        for j in training_pedestrians:
                            if j.rect.colliderect(i.rect):
                                j.blitMe(screen)       
    
                
                training_pedestrians.sprites()[0].drawTarget(screen)
                training_pedestrians.sprites()[0].blitMe(screen)
                
                pygame.display.flip()
                lastRefresh = pygame.time.get_ticks()
            
            if endTraining.checkPlayer(training_pedestrians.sprites()[0]):
                level = "enter"
                ### PART 2 INSTRUCTIONS        
                t1=pygame.time.get_ticks()
                root.wm_withdraw() #to hide the main window
                instruct = "Training level complete. The experiment will now start."
                messagebox.showinfo('Training',instruct)
                root.wm_withdraw()
                t2=pygame.time.get_ticks()
                bufferTime = bufferTime + t2-t1
            
    elif level == "enter":
        if enterLevelStartTime == 0:
            enterLevelStartTime = pygame.time.get_ticks()
        
        enterElapsedTime = currentTime - enterLevelStartTime
        enterTimes[evacs] = currentTime - enterAfterNotifStartTime
        
        ### EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(pygame.mouse.get_pos())
                #print(type(pygame.mouse.get_pos()))
                all_pedestrians.sprites()[0].updateTarget(array(pygame.mouse.get_pos()))
                numberClicksEnter[evacs] +=1
            if event.type == pygame.VIDEOEXPOSE:
                #print("screen moved?")
                time=pygame.time.get_ticks()
                bufferTime = bufferTime + time-currentTime
      
        
        ### ENTER ALERT WINDOW
        if enterNotInstructed == True and enterElapsedTime>250:
            t1=pygame.time.get_ticks()
            root.wm_withdraw() #to hide the main window
            if evacs==0:
                messagebox.showinfo('Alert!','Please enter the building and navigate to the red square.')
            elif evacs==1 or evacs==2:
                if alternativeMessage:
                    instruct = "You could have picked up coins!"
                    messagebox.showinfo('Alert!',instruct)
                    alternativeMessage = False
                else:
                    if evacFailed:
                        instruct = "False alarm! You would have lost all of your coins if that were a real evacuation!"
                        messagebox.showinfo('Alert!',instruct)
                    else:
                        instruct = "False alarm! You could have picked up more coins!"
                        messagebox.showinfo('Alert!',instruct)   
                root.wm_withdraw()
                instruct = "Please re-enter the building and navigate to the red square."
                messagebox.showinfo('Alert!',instruct)
            t2=pygame.time.get_ticks()
            bufferTime = bufferTime + t2-t1
            enterNotInstructed = False
            enterAfterNotifStartTime = pygame.time.get_ticks()
        
        
        ### PLAYER TARGET COLLISIONS
        collision = False
        numTargets = len(top_targets) + len(bottom_targets)
        counter = 0
        while counter < numTargets and collision == False:
            currentTarget = 0
            if counter < len(top_targets):
                currentTarget = top_targets.sprites()[counter]
            else:
                currentTarget = bottom_targets.sprites()[counter-4]

            if all_pedestrians.sprites()[0].rect.colliderect(currentTarget.rect):
                if prevTargetCollision == False:
                    routeChoiceEnter[evacs].append(currentTarget.label)
                collision = True
            counter+=1
        if collision == False:
            prevTargetCollision = False
        else:
            prevTargetCollision = True
        
        
        ### UPDATING NPC TARGETS
        counter = 0
        for i in all_pedestrians.sprites():
            if counter>0:
                i.wanderTarget()
            counter += 1

        
        ### UPDATING PLAYER + PEDESTRIAN POSITIONS
        counter = 0
        for i in all_pedestrians:
            if counter == 0:
                i.update(dt,boundries,all_pedestrians)
            else:
                i.update(dt,innerRoomBoundries,all_pedestrians)
            counter+=1
        
            
        ### DRAWING TO SCREEN
        currentTime = pygame.time.get_ticks()
        if currentTime - lastRefresh > 1000/refreshRate:
            screen.fill(white)
            
            #top_targets.draw(screen)
            #bottom_targets.draw(screen)
            
            p1 = all_pedestrians.sprites()[0]
            for i in rooms.sprites():
                if p1.rect.colliderect(i.rect):
                    i.image.fill(COLOR)
                else:
                    i.image.fill(grey)
            
            coin_counter.blitMe(screen)
            high_score.blitMe(screen)
            
            boundries.draw(screen)
            rooms.draw(screen)
            
            #innerRoomBoundries.draw(screen)
            
            endEnter.blitMe(screen)
            startEnter.blitMe(screen)
            
            for i in rooms:
                if all_pedestrians.sprites()[0].rect.colliderect(i.rect):
                    for j in all_pedestrians:
                        if j.rect.colliderect(i.rect):
                            j.blitMe(screen)
            
            all_pedestrians.sprites()[0].drawTarget(screen)
            all_pedestrians.sprites()[0].blitMe(screen)
            
            pygame.display.flip()
            lastRefresh = pygame.time.get_ticks()
        
        
        
        if endEnter.checkPlayer(all_pedestrians.sprites()[0]):
            level = "exit"
            #print("level change to exit")
            enterLevelStartTime = 0
            enterNotInstructed = True
            # even route split
            all_pedestrians = asignTargets(top_targets,bottom_targets,all_pedestrians,method="even")

    elif level == "exit":
        if exitLevelStartTime == 0:
            exitLevelStartTime = pygame.time.get_ticks()
        
        exitElapsedTime = currentTime - exitLevelStartTime
        evacTimes[evacs] = currentTime - evacStartTime
    
        ### EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_pedestrians.sprites()[0].updateTarget(array(pygame.mouse.get_pos()))
                numberClicksExit[evacs] += 1
            if event.type == pygame.VIDEOEXPOSE:
                #print("screen moved?")
                time=pygame.time.get_ticks()
                bufferTime = bufferTime + time-currentTime

        
        ### NPC TARGET AND SPEED UPDATING
        currentTime = pygame.time.get_ticks()
        if evacInstructed and (currentTime-evacStartTime)>crowdDelays[evacs]:
            #exit instructed and now peds evacuating
            #updating the npc targets and rmeovign npc if no target
            counter = 0
            for i in all_pedestrians.sprites():
                if counter>0:
                    newTargetAvai = i.updateTarget()
                    i.speed = 3
                    if not(newTargetAvai):
                        all_pedestrians.remove(i)
                counter += 1  
        elif evacInstructed == False:
            # exit not instructed yet
            # updating the npc targets to wander
            counter = 0
            for i in all_pedestrians.sprites():
                if counter>0:
                    i.wanderTarget()
                counter += 1
        elif evacInstructed and (currentTime-evacStartTime)<crowdDelays[evacs]:
            #exit instructed and peds not evacuating yet
            #updating the npc targets to wander
            counter = 0
            for i in all_pedestrians.sprites():
                if counter>0:
                    i.wanderTarget()
                counter += 1
                    
        
        
        ### PLAYER TARGET COLLISIONS
        collision = False
        numTargets = len(top_targets) + len(bottom_targets)
        counter = 0
        while counter < numTargets and collision == False:
            currentTarget = 0
            if counter < len(top_targets):
                currentTarget = top_targets.sprites()[counter]
            else:
                currentTarget = bottom_targets.sprites()[counter-4]

            if all_pedestrians.sprites()[0].rect.colliderect(currentTarget.rect):
                if prevTargetCollision == False:
                    routeChoiceExit[evacs].append(currentTarget.label)
                collision = True
            counter+=1
        if collision == False:
            prevTargetCollision = False
        else:
            prevTargetCollision = True
        
        
        ### COIN ALERTS
        if coinsInstructed == False and exitElapsedTime>250:
            t1=pygame.time.get_ticks()
            Tk().wm_withdraw() #to hide the main window
            if highScoreBeat == False:
                instruct = "Try and beat the high score, collect as many coins as you can!"
                messagebox.showinfo('Alert!',instruct)
            else:
                instruct = "Keep up your high score, collect as many coins as you can!"
                messagebox.showinfo('Alert!',instruct)
            t2=pygame.time.get_ticks()
            bufferTime = bufferTime + t2-t1
            
            coinsInstructed = True 
            
        
            
        ### COIN COLLECTION UPDATES
        if coinsInstructed:
            for i in coins:
                if i.checkCollection(all_pedestrians.sprites()[0]):
                    
                    
                    ### EVACUATION ALERTS
                    if evacInstructed == False:
                        t1=pygame.time.get_ticks()
                        root.wm_withdraw() #to hide the main window
                        instruct = "Evacuate! A fire has been detected in the building. You have 20 seconds to navigate to the evacuation point outside the building. You can still collect coins, but if the timer gets to 0 you might lose all your coins!"
                        
                        messagebox.showinfo('Alert!',instruct)
                        t2=pygame.time.get_ticks()
                        bufferTime = bufferTime + t2-t1
                        
                        evac_timer.start() ### START TIMER
                        evacStartTime = pygame.time.get_ticks()
                        evacInstructed = True
                    
                    coinFreezeStartTime = pygame.time.get_ticks()
                    lastCoinCollectedTime = pygame.time.get_ticks()
                    coinCollectionTimes[evacs] = coinFreezeTime + lastCoinCollectedTime - evacStartTime
                    
                    coinsCollected[evacs] += 1
                    coin_counter.update()
                    
        
        
        ### PEDESTRIAN POSITION UPDATES
        currentTime = pygame.time.get_ticks()
        counter = 0
        for i in all_pedestrians:
            if counter ==0:
                if currentTime-coinFreezeStartTime > coinFreezeTime:
                    i.update(dt,boundries,all_pedestrians)
            else:
                i.update(dt,boundries,all_pedestrians)
            counter+=1
        #all_pedestrians.update(dt,boundries,all_pedestrians)
        #lastSimulation = pygame.time.get_ticks()
        currentTime = pygame.time.get_ticks()
        
        
        ## EVAC_TIMER UPDATE
        evac_timer.update()
        
        
        ## HIGH SCORE UPDATE
        if coin_counter.coin_count>=high_score.score:
            coin_counter.color = gold
            high_score.update(coin_counter.coin_count)
            highScoreBeat = True
        
        ### DISPLAY
        if currentTime - lastRefresh > 1000/refreshRate:
            screen.fill(white)
            #top_targets.draw(screen)
            #bottom_targets.draw(screen)
            p1 = all_pedestrians.sprites()[0]
            for i in rooms.sprites():
                if p1.rect.colliderect(i.rect):
                    i.image.fill(COLOR)
                else:
                    i.image.fill(grey)
            
            boundries.draw(screen)
            rooms.draw(screen)
            

            #if evacInstructed:
            #    endExit.blitMe(screen)
            endExit.blitMe(screen)    
            
            
            startExit.blitMe(screen)

            for i in rooms:
                if all_pedestrians.sprites()[0].rect.colliderect(i.rect):
                    if coinsInstructed and coinsDisplayed[evacs] == True:
                        for j in coins:
                            if j.rect.colliderect(i.rect):
                                j.blitMe(screen)
                    for j in all_pedestrians:
                        if j.rect.colliderect(i.rect):
                            j.blitMe(screen)
                    
            all_pedestrians.sprites()[0].drawTarget(screen)
            all_pedestrians.sprites()[0].blitMe(screen)
            
            
            high_score.blitMe(screen)
            if evacInstructed:
                evac_timer.blitMe(screen)
                
            coin_counter.blitMe(screen)
            
            
            pygame.display.flip()
            lastRefresh = pygame.time.get_ticks()
          
            
          
        ### END REACHED FUNCTIONALITY
        #if endExit.checkPlayer(all_pedestrians.sprites()[0]) and evacInstructed:
        if endExit.checkPlayer(all_pedestrians.sprites()[0]):
            
            if evacStartTime == 0:
                evacTimes[evacs] = 0
                alternativeMessage = True
            
            evacs += 1
            exitLevelStartTime = 0
            evacStartTime = 0
            
  
            prevTargetCollision = False
            
            
            evacInstructed = False
            coinsInstructed = False
            #print(evac_timer.time)
            if evac_timer.time > 0:
                #print("evac successfuly!")
                evacFailed = False
            else:
                #print("evac failed")
                evacFailed = True
            evac_timer.reset()
            if evacs <3:
                level = "enter"
                all_pedestrians = generatePeds(all_pedestrians,numberPedestrians)
                buffer = 2*wWidth
                a=int(leftWidth+3*wWidth+fcWidth+buffer)*scale
                b=int(leftWidth+wWidth+fcWidth+mrWidth-buffer)*scale
                c=int(topWidth+3*wWidth+tcWidth+buffer)*scale
                d=int(topWidth+wWidth+tcWidth+mrHeight-buffer)*scale
                all_pedestrians = StartPositions(all_pedestrians,a,b,c,d)
                coins = generateCoins(coins)
                #print("level change to enter")
            else:
                level = "end"
   
    elif level == "end":
        
        #print("game over, 3 evacuations completed")
        
        
        NEWrouteChoiceEnter = [','.join(inner_list) for inner_list in routeChoiceEnter]
        NEWrouteChoiceExit = [','.join(inner_list) for inner_list in routeChoiceExit]
        
        my_data = {
            'coins': coinsCollected,
            'coinTimes': coinCollectionTimes,
            'evacTimes': evacTimes,
            'enterTimes': enterTimes,
            'enterSequence': NEWrouteChoiceEnter,
            'exitSequence': NEWrouteChoiceExit,
            'enterClicks': numberClicksEnter,
            'exitClicks': numberClicksExit
        }
        

        # Create a DataFrame
        df = DataFrame(my_data, index=[1, 2, 3])
        
        root.wm_withdraw() #to hide the main window

        if alternativeMessage:
            instruct = "You could have picked up coins!"
            messagebox.showinfo('Alert!',instruct)
            alternativeMessage = False
        else:
            if evacFailed:
                instruct = "That was a real evacuation! You lost all your coins."
                messagebox.showinfo('Alert!',instruct)
            else:
                instruct = "That was a real evacuation! Thankfully you made it out in time."
                messagebox.showinfo('Alert!',instruct)
        
        root.wm_withdraw()
        messagebox.showinfo('Game over!','Game over!')
        exit = False
        
pygame.quit()

root.destroy()

"""
if evacs == 3:
    import UI_closing
else:
    print("here")
    sys.exit()
"""

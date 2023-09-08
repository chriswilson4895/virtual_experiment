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
  

numberPedestrians = 24

wWidth = 0.5
bWidth = 20
bHeight = 15
# coridoor widths (m)
tcWidth = 2
fcWidth = 2

rdPos = 0.75 # ratio
fdPos = 0.5 # ratio

dWidth = 1 # door width (m)

leftWidth = 3 #m
topWidth = 3

# derived main room measurements
mrWidth = bWidth-(fcWidth + wWidth)
mrHeight = bHeight - (2*wWidth + 2*tcWidth)

length3 = mrWidth*rdPos-0.5*dWidth
length5 = mrWidth*(1-rdPos)-0.5*dWidth
length9 = bHeight/2-0.5*dWidth

trLength = bWidth-fcWidth-wWidth


WIDTH = (leftWidth+bWidth+leftWidth+2*wWidth)*scale
HEIGHT = (topWidth+bHeight+topWidth+2*wWidth)*scale
size = (WIDTH, HEIGHT)  


#all measurements of rooms are to do with internal space excluding the wall widths

#walls
wallData = array([[leftWidth,topWidth,bWidth + wWidth*2,wWidth],
                [leftWidth,topWidth+wWidth+bHeight,bWidth+wWidth*2,wWidth],
                [leftWidth+wWidth+fcWidth,topWidth+wWidth+tcWidth,length3+wWidth,wWidth],
                [leftWidth+wWidth+fcWidth,topWidth+2*wWidth+tcWidth+mrHeight,length3+wWidth,wWidth],
                [leftWidth+wWidth+fcWidth+wWidth+length3+dWidth,topWidth+wWidth+tcWidth,length5+wWidth,wWidth],
                [leftWidth+wWidth+fcWidth+wWidth+length3+dWidth,topWidth+2*wWidth+tcWidth+mrHeight,length5+wWidth,wWidth],
                [leftWidth+bWidth+wWidth,topWidth,wWidth,bHeight+2*wWidth],
                [leftWidth+wWidth+fcWidth,topWidth+wWidth+tcWidth,wWidth,mrHeight+2*wWidth],
                [leftWidth,topWidth,wWidth,length9],
                [leftWidth,topWidth+length9+wWidth+dWidth,wWidth,length9],
                [leftWidth+wWidth+fcWidth,topWidth+wWidth,wWidth,(tcWidth-dWidth)/2],
                [leftWidth+wWidth+fcWidth,topWidth+wWidth+(tcWidth+dWidth)/2,wWidth,(tcWidth-dWidth)/2],
                [leftWidth+wWidth+fcWidth,topWidth+wWidth*3+tcWidth+mrHeight,wWidth,(tcWidth-dWidth)/2],
                [leftWidth+wWidth+fcWidth,topWidth+wWidth*3+tcWidth+mrHeight+(tcWidth+dWidth)/2,wWidth,(tcWidth-dWidth)/2]
                ])

#inner room boundries
innerRoomBoundData = array([[leftWidth+wWidth+fcWidth,topWidth+wWidth+tcWidth,mrWidth+2*wWidth,wWidth],
                               [leftWidth+wWidth+fcWidth,topWidth+wWidth+tcWidth,wWidth,mrHeight+2*wWidth],
                               [leftWidth+wWidth+fcWidth+wWidth+mrWidth,topWidth+wWidth+tcWidth,wWidth,mrHeight+2*wWidth], 
                               [leftWidth+wWidth+fcWidth,topWidth+2*wWidth+tcWidth+mrHeight,mrWidth+2*wWidth,wWidth]
                                ])



#top route
topRouteData = array([[leftWidth+wWidth+fcWidth+wWidth+length3,topWidth+tcWidth,dWidth,wWidth],
                  [leftWidth+fcWidth+length3-2*wWidth,topWidth+wWidth,wWidth,tcWidth],
                  [leftWidth+fcWidth,topWidth+wWidth,wWidth,tcWidth],
                  [leftWidth,topWidth+wWidth+length9,wWidth,dWidth]
                  ])

topRouteLabels = ["TR","TM","TL","E"]


#bottom route
bottomRouteData = array([[leftWidth+wWidth+fcWidth+wWidth+length3,topWidth+tcWidth+mrHeight+3*wWidth,dWidth,wWidth],
                  [leftWidth+fcWidth+length3-2*wWidth,topWidth+3*wWidth+mrHeight+tcWidth,wWidth,tcWidth],
                  [leftWidth+fcWidth,topWidth+3*wWidth+mrHeight+tcWidth,wWidth,tcWidth],
                  [leftWidth,topWidth+length9,wWidth,dWidth]
                  ])

bottomRouteLabels = ["BR","BM","BL","E"]

#rooms
roomData = array([
                 [leftWidth+wWidth*1.5+fcWidth,topWidth+1.5*wWidth+tcWidth,mrWidth+0.5*wWidth,mrHeight+1*wWidth], #main room
                 [leftWidth+1.5*wWidth+fcWidth,topWidth+wWidth,trLength+0.5*wWidth,tcWidth+0.5*wWidth], #tc
                 [leftWidth+1.5*wWidth+fcWidth,topWidth+2.5*wWidth+mrHeight+tcWidth,trLength+0.5*wWidth,tcWidth+0.5*wWidth], #bc
                 [leftWidth+wWidth,topWidth+wWidth,fcWidth+0.5*wWidth,bHeight] #fr
                ])


timer_pos = ((leftWidth+3*wWidth+fcWidth)*scale,(topWidth+3*wWidth+tcWidth)*scale)
coin_counter_pos = (leftWidth*scale,25)
high_score_pos = (320,25)

wallData = wallData*scale
topRouteData = topRouteData*scale
bottomRouteData = bottomRouteData*scale
roomData = roomData*scale
innerRoomBoundData = innerRoomBoundData*scale


    
outsidePoint = array([(leftWidth/2)*scale,(topWidth+wWidth+0.5*bHeight)*scale])
insidePoint = array([(leftWidth+wWidth+0.8*bWidth)*scale,(topWidth+wWidth+0.5*bHeight)*scale])

    
#### TRAINING ROOM

trainingWallData = array([[leftWidth,topWidth,bWidth + wWidth*2,wWidth], #tw
                     [leftWidth,topWidth+wWidth+bHeight,bWidth+wWidth*2,wWidth], #bw
                     [leftWidth,topWidth,wWidth,bHeight+wWidth*2], #lw
                     [leftWidth+wWidth+bWidth,topWidth,wWidth,bHeight+wWidth*2], #rw
                     [leftWidth+wWidth, topWidth+wWidth+bHeight/2 - wWidth/2, bWidth/4 - dWidth/2, wWidth],
                     [leftWidth+wWidth+bWidth/4 + dWidth/2, topWidth+wWidth+bHeight/2 - wWidth/2, 3*bWidth/4 - dWidth/2, wWidth]
                     ])
    
trainingRoomData = array([[leftWidth+wWidth,topWidth+wWidth,bWidth,bHeight/2],
                             [leftWidth+wWidth,topWidth+wWidth+bHeight/2,bWidth,bHeight/2]
                            ])

trainingWallData *= scale
trainingRoomData *= scale

objPositions=array([[leftWidth+wWidth+1,topWidth+wWidth+3],
                       [leftWidth+bWidth-3,topWidth+wWidth+bHeight/4],
                       [leftWidth+bWidth/2,topWidth+wWidth+1]])
                      
objPositions*=scale
    
startPoint = array([leftWidth+wWidth+bWidth/2,topWidth+wWidth+bHeight*0.8])*scale 
endPoint = array([leftWidth+wWidth+bWidth/2,topWidth+wWidth+bHeight*0.2])*scale 

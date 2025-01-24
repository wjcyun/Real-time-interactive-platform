# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 16:04:17 2022

@author: wjc
"""

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import serial
from collections import deque
import time

pts = deque(maxlen=10000)
font = cv2.FONT_HERSHEY_SIMPLEX

lower_blue = np.array([50,120,140])   # Lower blue threshold,Modified according to the actual situation
higher_blue = np.array([180,200,255]) # upper blue threshold,Modified according to the actual situation


#*********************************************************
#Distance detection function
#*********************************************************
def Decision(frame):

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(img_hsv, lower_blue, higher_blue)  # Getting the blue part of the mask(robotic bait)
    mask_blue = cv2.medianBlur(mask_blue, 9)  # median filter
    contoursji, hierarchy2 = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Contour detection of robotic bait
    cv2.drawContours(frame, contoursji, -1, (0, 255, 0), 1) 
           
    for e in contoursji:
        #Calculate the perimeter of each contour
        perimeter = cv2.arcLength(e,True)
        if perimeter > 0:
            #Find a straight rectangle (won't rotate)
            p,q,m,n = cv2.boundingRect(e)
            global center
            center=(int(p+m/2),int(q+n/2))
            cv2.putText(frame, str(center), (530, 430), font, 0.6, (255, 0, 0), 2)
            pts.appendleft(center)
            for i in range(1,len(pts)):
                if pts[i-1]is None or pts[i]is None:
                    continue
                cv2.line(frame, pts[i - 1], pts[i], (255, 255, 0)) 
        else:
            center=(0,0)
    
    robotx=center[0]
    roboty=center[1]
    cv2.imshow('result', frame)
    return robotx, roboty

#*********************************************************
#Define each parameter
#*********************************************************
def Parameter(borx,bory):
    
    zhongxz=342
    zhongyz=241                    #The center pixel point of the arena

    x=borx-zhongxz
    y=bory-zhongyz
    xdis=math.pow(x, 2)
    ydis=math.pow(y, 2)
    rdistance=math.sqrt(xdis+ydis)
    distance=round(rdistance,2)
    cv2.putText(frame, str(distance), (540,470), font, 0.5, (0, 255, 255), 2)        #Display relative distance（pix）

    dis_prez=10                   #Distance from the center position (judgment distance,pix)

    dq1 = 0                       #Direction of motion of servo motors
    dq2 = 1
    dy1 = 0
    dy2 = 1
    
    v = 5                     # the velocity of robotic bait, 5 cm/s
    
    vfang=math.pow(v,2)
    ratio_yy=zhongyz-bory
    if zhongyz-bory== 0:
        ratio_y=1
    else :
        ratio_y=ratio_yy
    
    bizhichu=abs((zhongxz-borx)/ratio_y)
    if bizhichu==0:
        ratio=0.00001
    else:
        ratio=bizhichu
    speed_ratio=math.pow(ratio, 2)                      
    
    velx=math.sqrt(vfang/(speed_ratio+1))       
    vely=ratio*velx
    speedxxx=72000000/((velx/7.5)*16000)              #Setting according to the crystal frequency of the stm32 and the parameters of the motor
    speedyyy=72000000/((vely/7.5)*16000)              #Setting according to the crystal frequency of the stm32 and the parameters of the motor
    speedxx=round(speedxxx/10)
    speedyy=round(speedyyy/10)
    if speedxx>=1000:
        speedxz=999
    else:
        speedxz=speedxx
    if speedyy>=1000:
        speedyz=999
    else:
        speedyz=speedyy

    return speedxz, speedyz, zhongxz, zhongyz, distance, dis_prez, dq1, dq2, dy1, dy2


# ==============================================================================
#   ****************************Main function entry***********************************
# ==============================================================================
# Setting Serial Port Parameters
ser = serial.Serial()
ser.baudrate = 115200    # Setting the bit rate to 115200bps
ser.port = 'COM8'      # The microcontroller is connected to which serial port, write which serial port. Here the default is connected to the "COM8" port.
ser.open()             # Open the serial port

# First send a center coordinate so that the initialization is artificial prey stationary
data = 'A'+str('0')+'B'+str('0')+'C'+str('0')+'D'+str('0')+'\r\n'
ser.write(data.encode())
cap = cv2.VideoCapture(0)       #Capture video via local camera

while(cap.isOpened()):
    
    ret, frame = cap.read()
    borx,bory =Decision(frame)
    speedx,speedy,zhongx,zhongy,dist,deci_dis,q1,q2,y1,y2 = Parameter(borx,bory)

    if dist<=deci_dis:
        print('approved location')
        X=0
        Y=0
        P=0
        Q=0
        data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
        ser.write(data.encode())
        
    if dist>deci_dis:   

        if zhongx>borx and zhongy<bory:                        #The midpoint is in the first quadrant of the robot decoy.   
            print('Reset 1')
            X=speedy
            Y=y2
            P=speedx
            Q=q1
            data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
            ser.write(data.encode())
            
        elif zhongx<borx and zhongy<bory:               #The midpoint is in the second quadrant of the robot decoy.
            print('Reset 2')
            X=speedy
            Y=y2
            P=speedx
            Q=q2
            data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
            ser.write(data.encode())   
        
        elif zhongx<borx and zhongy>bory:              #The midpoint is in the third quadrant of the robot decoy.
            print('Reset 3
            Y=y1
            P=speedx
            Q=q2
            data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
            ser.write(data.encode())
        
        elif zhongx>borx and zhongy>bory:                #The midpoint is in the fourth quadrant of the robot decoy.
            print('Reset 4')
            X=speedy
            Y=y1
            P=speedx
            Q=q1
            data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
            ser.write(data.encode())

            
    if cv2.waitKey(1) & 0xFF==27:
        break

ser.close()                                     # Close the serial port
cv2.destroyAllWindows()
cap.release()


            

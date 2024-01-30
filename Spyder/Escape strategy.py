# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:54:58 2023

@author: DELL
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import serial
from collections import deque
import time
# import os



kernel = np.ones((5, 5), np.uint8) 
kernel2 = np.ones((3, 3), np.uint8) 
pts = deque(maxlen=10000000)
pts2 = deque(maxlen=10000000)
pts3 = deque(maxlen=10000000)
pts4 = deque(maxlen=10000000)
time_list = deque(maxlen=10000000)

font = cv2.FONT_HERSHEY_SIMPLEX
lower_black = np.array([40, 10, 10])     # Lower black threshold
higher_black = np.array([150, 150, 50])  # upper black threshold


lower_blue = np.array([50,120,140])   # Lower blue threshold
higher_blue = np.array([180,200,255]) # upper blue threshold


#*********************************************************
#Trajectory and distance detection functions
#*********************************************************
def Decision(frame, flag):
   

    
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_black = cv2.inRange(img_hsv, lower_black, higher_black)  # Getting a black mask

    mask_black = cv2.medianBlur(mask_black, 19)  # median filter
    contoursshu, hierarchy1 = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Contour Detection #Black
    # cv2.drawContours(frame, contoursshu, -1, (255, 0, 0), 1) 
    
    
    mask_blue = cv2.inRange(img_hsv, lower_blue, higher_blue)  # Getting a blue mask
    mask_blue = cv2.medianBlur(mask_blue,9)  # median filter
    contoursji, hierarchy2 = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Contour Detection #blue
    # cv2.drawContours(frame, contoursji, -1, (0, 255, 0), 1) 
    

    for d in contoursshu:
        # Calculate the perimeter of each contour
        perimeter = cv2.arcLength(d,True)
        if perimeter > 0:
            x,y,w,h = cv2.boundingRect(d)

            # cv2.putText(frame, 'mouse',(x, y - 5), font, 0.5, (0, 0, 0), 2)
            global center1
            
            center1=(int(x+w/2),int(y+h/2))
            
            cv2.putText(frame, str(center1), (540 , 450), font, 0.5, (0, 0, 0), 2)
            # print ("location of mouse",center1)
            fp4 = open("C:\\Users\\DELL\\Desktop\\centerx-10-26-266-2.text", "a")  
            print(center1[0], file=fp4)
            fp4.close()
            fp5 = open("C:\\Users\\DELL\\Desktop\\centery-10-26-266-2.text", "a")  
            print(center1[1], file=fp5)
            fp5.close()
            pts.appendleft(center1)
            if len(pts)>=2:
                if pts[1] is None:
                    continue
                xdif=pts[0][0]-pts[1][0]
                ydif=pts[0][1]-pts[1][1]
                a=math.pow(xdif, 2)
                b=math.pow(ydif, 2)
                c=a+b
                s=math.sqrt(c)
                vel=s/0.033/5.73
                v=round(vel,2)
                cv2.putText(frame, str(v), (540,410), font, 0.5, (0, 0, 0), 2)
                fp = open("C:\\Users\\DELL\\Desktop\\velocity-10-26-266-2.text", "a")  
                print(v, file=fp)
                fp.close()
            # draw a trajectory of mouse
            # if flag == 1:
            #     pts3.appendleft(center1)
            #     for i in range(1,len(pts3)):
            #         if pts3[i-1]is None or pts3[i]is None:
            #             continue
            #         cv2.line(frame, pts3[i - 1], pts3[i], (255, 0, 225))
                  
        else:
            center1=(0,0)
 
               
    for e in contoursji:
        perimeter2 = cv2.arcLength(e,True)
        if perimeter2 > 0:
            #Find a straight rectangle (won't rotate)
            p,q,m,n = cv2.boundingRect(e)
            #Draw this rectangle
            #cv2.rectangle(frame,(p,q),(p+m,q+n),(0,0,255),2) 
            # print(p,q,m,n)
            # cv2.putText(frame, 'prey', (p, q - 5), font, 0.5, (255, 0, 0), 2)
            global center2
            center2=(int(p+m/2),int(q+n/2))
            cv2.putText(frame, str(center2), (540, 430), font, 0.5, (255, 0, 0), 2)
            # print ("location of artificial prey",center2)  
            # with open("C:\\Users\\joych\\Desktop\\blockx-9-27-ce.text", 'a') as fp6:
            #     fp6.write(str(center2[0])+"\n")
            fp6 = open("C:\\Users\\DELL\\Desktop\\blockx-10-26-266-2.text", "a")   
            print(center2[0], file=fp6)
            fp6.close()
            fp7 = open("C:\\Users\\DELL\\Desktop\\blocky-10-26-266-2.text", "a")   
            print(center2[1], file=fp7)
            fp7.close()                                            
            # draw a trajectory of artificial prey
            # if flag == 1:
            #     pts2.appendleft(center2)
            #     for i in range(1,len(pts2)):
            #         if pts2[i-1]is None or pts2[i]is None:
            #             continue
            #         cv2.line(frame, pts2[i - 1], pts2[i], (255, 255, 0)) 
        else:
            center2=(0,0)
            
    # center2=(0,0)
    
    x=center1[0]-center2[0]
    y=center1[1]-center2[1]
    xdis=math.pow(x, 2)
    ydis=math.pow(y, 2)
    rdistance=math.sqrt(xdis+ydis)
    distance=round(rdistance,2)
    realdis=distance/5.73
    reald=round(realdis,2)
    cv2.putText(frame, str(reald), (540,470), font, 0.5, (0, 255, 255), 2)
    fp2 = open("C:\\Users\\DELL\\Desktop\\distance-10-26-266-2.text", "a")   
    print(reald, file=fp2)
    fp2.close()
    # print("distance",distance)
    
    mx=center1[0]
    my=center1[1]
    borderx=center2[0]
    bordery=center2[1]
     

    cv2.imshow('result', frame)
        
    return distance, borderx, bordery, mx, my



def Parameter(borx,bory,micex,micey):
    

    dis_prez=50                    #Capture area within 8cm
    dis_safez=143                  #Safe area 25cm away
    huanz=41                       #The size of the surrounding area is 7.5cm
    
    v = 25                         # the velocity of artificial prey
    vfang=math.pow(v,2)
    
    zhongxz=325
    zhongyz=241                    #The center pixel point of the arena
    shangz=22                      #Upper boundary of the arena
    xiaz=461                       #Lower boundary of the arena
    zuoz=106                       #Left border of the arena
    youz=544                       #Right border of the arena
    r=180                          # 
    R=221
    rfangz=math.pow(r,2)
    Rfangz=math.pow(R,2)
    
    xianxx=borx-zhongxz
    if xianxx==0:
        xianxz=0.000001
    else:
        xianxz=xianxx
    xianyz=bory-zhongyz
    
    
    pandingxz=math.pow(borx-zhongxz,2)
    pandingyz=math.pow(bory-zhongyz,2)
    
    chayy=bory-micey
    if bory-micey== 0:
        chay=1
    else :
        chay=chayy
    bizhichu=abs((micex-borx)/chay)
    if bizhichu==0:
        bizhi=0.00001
    else:
        bizhi=bizhichu
    bizhifang=math.pow(bizhi,2)
    velx=math.sqrt(vfang/(bizhifang+1))               
    vely=bizhi*velx    
    speedxxx=72000000/((velx/7.5)*16000)
    speedyyy=72000000/((vely/7.5)*16000)
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
        
        
    return speedxz, speedyz,dis_prez,dis_safez,zhongxz,zhongyz,shangz,xiaz,zuoz,youz,xianxz,xianyz,rfangz,Rfangz,pandingxz,pandingyz
    
    


# ==============================================================================
#   ****************************Main function entry***********************************
# ==============================================================================
# Setting Serial Port Parameters
ser = serial.Serial()
ser.baudrate = 115200    # Setting the bit rate to 115200bps
ser.port = 'COM3'      # The microcontroller is connected to which serial port, write which serial port. Here the default is connected to the "COM3" port.
ser.open()             # Open the serial port

# First send a center coordinate so that the initialization is artificial prey stationary
data = 'A'+str('0')+'B'+str('0')+'C'+str('0')+'D'+str('0')+'\r\n'
ser.write(data.encode())


cap = cv2.VideoCapture(0)#Capture video via local camera


flag = 0
while(cap.isOpened()):

    start = time.time()
    ret, frame = cap.read()
    dist,borx,bory,micex,micey=Decision(frame, flag)
    speedx,speedy,dis_pre,dis_safe,zhongx,zhongy,shang,xia,zuo,you,xianx,xiany,rfang,Rfang,pandingx,pandingy = Parameter(borx,bory,micex,micey)


    if dist<=dis_pre:
        print('It has been preyed upon!!!')
        X=0
        Y=0
        P=0
        Q=0
        data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
        ser.write(data.encode())
        
    if dis_pre<dist<=dis_safe:   
        flag = 1
         
        if pandingx+pandingy<=rfang  :                                          #Central area    
            if micex>=borx and micey<=bory:                                     #first quadrant 
                 
                X=speedx
                Y=0
                P=speedy
                Q=1
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            
            elif micex<borx and micey<bory:                                     #second quadrant 
                
                X=speedx
                Y=0
                P=speedy
                Q=0
                # Packages speed and direction according to protocol and sends to serial port
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())   
            
            elif micex<=borx and micey>=bory:                                   #third quadrant 
                 
                X=speedx
                Y=1
                P=speedy
                Q=0
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            
            elif micex>borx and micey>bory:                                     #fourth quadrant 
                 
                X=speedx
                Y=1
                P=speedy
                Q=1            
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
        
        if pandingx+pandingy > rfang and pandingx+pandingy < Rfang and zhongx <= borx < you and shang < bory < zhongy: #First quadrant sector, upper right      
            if ((micex-zhongx)/xianx)*xiany+zhongy > micey and micey <= bory:      #above the radius and in the second quadrant , run toward the third quadrant
                 
                X=speedy
                Y=0
                P=speedx
                Q=1

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())  
            elif ((micex-zhongx)/xianx)*xiany+zhongy >= micey and micey > bory:    #above the radius and in the third quadrant , run toward the fourth quadrant
                
                X=speedy
                Y=0
                P=speedx
                Q=0

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy <= micey and micex < borx:    #below the radius and in the third quadrant , run toward the second quadrant                                  
                 
                X=speedy
                Y=1
                P=speedx
                Q=1

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy < micey and micex >= borx:    #Below the radius and in the fourth quadrant , run toward the third quadrant                                           
                 
                X=speedy
                Y=0
                P=speedx
                Q=1

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
    
        if pandingx+pandingy > rfang and pandingx+pandingy < Rfang and zuo < borx < zhongx and shang < bory <= zhongy: #Second quadrant sector, upper left      
            if ((micex-zhongx)/xianx)*xiany+zhongy > micey and micey <= bory:      
                 
                X=speedy
                Y=0
                P=speedx
                Q=0

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())  
            elif ((micex-zhongx)/xianx)*xiany+zhongy >= micey and micey > bory:     
                 
                X=speedy
                Y=0
                P=speedx
                Q=1

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy <= micey and micex > borx:                                          
                 
                X=speedy
                Y=1
                P=speedx
                Q=0

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy < micey and micex <= borx:                                                 
                 
                X=speedy
                Y=0
                P=speedx
                Q=0

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())    
        if pandingx+pandingy > rfang and pandingx+pandingy < Rfang and zuo < borx <= zhongx and zhongy < bory < xia: #Third quadrant sector, upper left      
            if ((micex-zhongx)/xianx)*xiany+zhongy > micey and micex <= borx:      
                 
                X=speedy
                Y=1
                P=speedx
                Q=0
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())  
            elif ((micex-zhongx)/xianx)*xiany+zhongy >= micey and micex > borx:     
               
                X=speedy
                Y=0
                P=speedx
                Q=0
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy <= micey and micey < bory:                                        
                 
                X=speedy
                Y=1
                P=speedx
                Q=1
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy < micey and micey >= bory:                                                
                 
                X=speedy
                Y=1
                P=speedx
                Q=0
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode()) 
        if pandingx+pandingy > rfang and pandingx+pandingy < Rfang and zhongx < borx < you and zhongy <= bory < xia: #Fourth quadrant sector, upper left      
            if ((micex-zhongx)/xianx)*xiany+zhongy > micey and micex >= borx:       
                 
                X=speedy
                Y=1
                P=speedx
                Q=1
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())  
            elif ((micex-zhongx)/xianx)*xiany+zhongy >= micey and micex < borx:    
                 
                X=speedy
                Y=0
                P=speedx
                Q=1
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy <= micey and micey < bory:                                          
                 
                X=speedy
                Y=1
                P=speedx
                Q=0
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy < micey and micey >= bory:                                                 
                 
                X=speedy
                Y=1
                P=speedx
                Q=1
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode()) 
    

    if dist>dis_safe:
        print('Safe position!!!')
        X=0
        Y=0
        P=0
        Q=0
        data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
        ser.write(data.encode())
            
    if cv2.waitKey(1) & 0xFF==27:
        break
    
    end = time.time()
    time_list.append(end-start)
    avarge = sum(time_list) / len(time_list)
    print("detect:", end-start)
    print("avarge:",avarge)

ser.close()                                     # Close the serial port
cv2.destroyAllWindows()
cap.release()

            

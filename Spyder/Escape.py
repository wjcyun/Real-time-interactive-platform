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
lower_black = np.array([40, 10, 10])  # 黑色阈值下界
higher_black = np.array([150, 150, 50])  # 黑色阈值上界


lower_blue = np.array([50,120,140])   # 蓝色阈值下界
higher_blue = np.array([180,200,255]) # 蓝色阈值上界


#*********************************************************
#距离检测函数
#轨迹检测
#*********************************************************
def Decision(frame, flag):
   

    
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_black = cv2.inRange(img_hsv, lower_black, higher_black)  # 获得黑色的掩膜

    mask_black = cv2.medianBlur(mask_black, 19)  # 中值滤波
    contoursshu, hierarchy1 = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 轮廓检测 #黑色
    # cv2.drawContours(frame, contoursshu, -1, (255, 0, 0), 1) 
    
    
    mask_blue = cv2.inRange(img_hsv, lower_blue, higher_blue)  # 获得lan色部分掩膜
    mask_blue = cv2.medianBlur(mask_blue,9)  # 中值滤波
    contoursji, hierarchy2 = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 轮廓检测 #红色
    # cv2.drawContours(frame, contoursji, -1, (0, 255, 0), 1) 
    

    for d in contoursshu:
        #计算各轮廓的周长
        perimeter = cv2.arcLength(d,True)
        if perimeter > 0:
            x,y,w,h = cv2.boundingRect(d)

            # cv2.putText(frame, 'mouse',(x, y - 5), font, 0.5, (0, 0, 0), 2)
            global center1
            
            center1=(int(x+w/2),int(y+h/2))
            
            cv2.putText(frame, str(center1), (540 , 450), font, 0.5, (0, 0, 0), 2)
            print ("黑色物体位置",center1)
            fp4 = open("C:\\Users\\DELL\\Desktop\\centerx-06-02-1633-1.text", "a")  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加
            print(center1[0], file=fp4)
            fp4.close()
            fp5 = open("C:\\Users\\DELL\\Desktop\\centery-06-02-1633-1.text", "a")  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加
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
                fp = open("C:\\Users\\DELL\\Desktop\\velocity-06-02-1633-1.text", "a")  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加
                print(v, file=fp)
                fp.close()
            if flag == 1:
                pts3.appendleft(center1)
                for i in range(1,len(pts3)):
                    if pts3[i-1]is None or pts3[i]is None:
                        continue
                    # cv2.line(frame, pts3[i - 1], pts3[i], (255, 0, 225))
                  
        else:
            center1=(0,0)
 
               
    for e in contoursji:
        #计算各轮廓的周长
        perimeter2 = cv2.arcLength(e,True)
        if perimeter2 > 0:
            #找到一个直矩形（不会旋转）
            p,q,m,n = cv2.boundingRect(e)
            #画出这个矩形
            #cv2.rectangle(frame,(p,q),(p+m,q+n),(0,0,255),2) 
            print(p,q,m,n)
            # cv2.putText(frame, 'prey', (p, q - 5), font, 0.5, (255, 0, 0), 2)
            global center2
            center2=(int(p+m/2),int(q+n/2))
            cv2.putText(frame, str(center2), (540, 430), font, 0.5, (255, 0, 0), 2)
            print ("蓝色物体位置",center2)  
            # with open("C:\\Users\\joych\\Desktop\\blockx-9-27-ce.text", 'a') as fp6:
            #     fp6.write(str(center2[0])+"\n")
            fp6 = open("C:\\Users\\DELL\\Desktop\\blockx-06-02-1633-1.text", "a")  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加
            print(center2[0], file=fp6)
            fp6.close()
            fp7 = open("C:\\Users\\DELL\\Desktop\\blocky-06-02-1633-1.text", "a")  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加
            print(center2[1], file=fp7)
            fp7.close()                                            #
            if flag == 1:
                pts2.appendleft(center2)
                for i in range(1,len(pts2)):
                    if pts2[i-1]is None or pts2[i]is None:
                        continue
                    # cv2.line(frame, pts2[i - 1], pts2[i], (255, 255, 0)) 
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
    fp2 = open("C:\\Users\\DELL\\Desktop\\distance-06-02-1633-1.text", "a")  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加
    print(reald, file=fp2)
    fp2.close()
    print("距离",distance)
    
    mx=center1[0]
    my=center1[1]
    borderx=center2[0]
    bordery=center2[1]
     
    # out.write(frame)
    # cv2.imshow('mouse', mask_red)
    # cv2.imshow('food', mask_blue) 
    cv2.imshow('result', frame)
        
    return distance, borderx, bordery, mx, my


# ==============================================================================
#   ****************************主函数入口***********************************
# ==============================================================================
# 设置串口参数
ser = serial.Serial()
ser.baudrate = 115200    # 设置比特率为115200bps
ser.port = 'COM4'      # 单片机接在哪个串口，就写哪个串口。这里默认接在"COM3"端口
ser.open()             # 打开串口

# 先发送一个中心坐标使初始化时云台保持水平
data = 'A'+str('0')+'B'+str('0')+'C'+str('0')+'D'+str('0')+'\r\n'
ser.write(data.encode())


cap = cv2.VideoCapture(0)#通过本地摄像头捕获视频
# fourcc = cv2.VideoWriter_fourcc(*'MP4V')#指定fourcc编码
# out = cv2.VideoWriter('movie-9-27-ce.avi',fourcc, 30.0, (640,480))

flag = 0
while(cap.isOpened()):

    start = time.time()
    ret, frame = cap.read()
    dist,borx,bory,micex,micey=Decision(frame, flag)
    
    end = time.time()
    time_list.append(end-start)
    avarge = sum(time_list) / len(time_list)
    print("detect:", end-start)
    print("avarge:",avarge)
    
    speed=159                    #正分分量 
    dis_pre=54                    #捕获区域 8cm以内
    dis_safe=143                 #按全区域 25cm以外
    huan=43                   #环形区域大小为7cm
    
    v=30
    vfang=math.pow(v,2)
    
    
    shang=25
    xia=467
    zuo=103
    you=550
    
    zhongx=325
    zhongy=245
    r=180
    R=223
    rfang=math.pow(r,2)
    Rfang=math.pow(R,2)
    
    #判定，中间量
    
    xianxx=borx-zhongx
    if xianxx==0:
        xianx=0.000001
    else:
        xianx=xianxx
    xiany=bory-zhongy
    
    
    pandingx=math.pow(borx-zhongx,2)
    pandingy=math.pow(bory-zhongy,2)
    chayy=bory-micey
    if bory-micey== 0:
        chay=1
    else :
        chay=chayy
    bizhichu=abs((micex-borx)/chay)
    if bizhichu==0:
        bizhi=0.001
    else:
        bizhi=bizhichu
    bizhifang=math.pow(bizhi,2)
    velx=math.sqrt(vfang/(bizhifang+1))                #合速度 v
    vely=bizhi*velx    
    speedxxx=72000000/((velx/7.5)*16000)
    speedyyy=72000000/((vely/7.5)*16000)
    speedxx=round(speedxxx/10)
    speedyy=round(speedyyy/10)
    if speedxx>=1000:
        speedx=999
    else:
        speedx=speedxx
    if speedyy>=1000:
        speedy=999
    else:
        speedy=speedyy

    print('vx',speedx)
    print('vy',speedy)
    if pandingx+pandingy > rfang and pandingx+pandingy < Rfang:
        print('边缘')

     
    if dist<=dis_pre:
        print('已被捕食！！！')
        X=0
        Y=0
        P=0
        Q=0
        data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
        ser.write(data.encode())
        
    if dis_pre<dist<=dis_safe:   
        flag = 1
        print('逃跑')
        if pandingx+pandingy<=rfang  :               #中间区域    r方=30276
            print('在中间')
            if micex>=borx and micey<=bory:            #第一象限
                print('逃跑1')
                X=speed
                Y=0
                P=speed
                Q=1
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            
            elif micex<borx and micey<bory:               #第二象限
                print('逃跑2')
                X=speed
                Y=0
                P=speed
                Q=0
                # 按照协议将形心坐标打包并发送至串口
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())   
            
            elif micex<=borx and micey>=bory:              #第三象限
                print('逃跑3')
                X=speed
                Y=1
                P=speed
                Q=0
                # 按照协议将形心坐标打包并发送至串口
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            
            elif micex>borx and micey>bory:                #第四象限
                print('逃跑4')
                X=speed
                Y=1
                P=speed
                Q=1            
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
        
        if pandingx+pandingy > rfang and pandingx+pandingy < Rfang and zhongx <= borx < you and shang < bory < zhongy: #第一象限扇形，右上      
            if ((micex-zhongx)/xianx)*xiany+zhongy > micey and micey <= bory:      #半径上方，且在第二象限 ，向第三象限跑
                print('逃跑5')
                X=speedy
                Y=0
                P=speedx
                Q=1

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())  
            elif ((micex-zhongx)/xianx)*xiany+zhongy >= micey and micey > bory:    #半径上方，且在第三象限 ，向第四象限跑
                print('逃跑6')
                X=speedy
                Y=0
                P=speedx
                Q=0

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy <= micey and micex < borx:    #半径下方，且在第三象限 ，向第二象限跑                                    #左上角平分线上面  往下跑
                print('逃跑7')
                X=speedy
                Y=1
                P=speedx
                Q=1

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy < micey and micex >= borx:    #半径下方，且在第四象限 ，向第三象限跑                                           #左上角平分线上面  往下跑
                print('逃跑8')
                X=speedy
                Y=0
                P=speedx
                Q=1

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
    
        if pandingx+pandingy > rfang and pandingx+pandingy < Rfang and zuo < borx < zhongx and shang < bory <= zhongy: #第二象限扇形，左上      
            if ((micex-zhongx)/xianx)*xiany+zhongy > micey and micey <= bory:     #半径上方，且在第一象限 ，向第四象限跑
                print('逃跑9')
                X=speedy
                Y=0
                P=speedx
                Q=0

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())  
            elif ((micex-zhongx)/xianx)*xiany+zhongy >= micey and micey > bory:    #半径上方，且在第四象限 ，向第三象限跑
                print('逃跑10')
                X=speedy
                Y=0
                P=speedx
                Q=1

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy <= micey and micex > borx:    #半径下方，且在第四象限 ，向第一象限跑                                    #左上角平分线上面  往下跑
                print('逃跑11')
                X=speedy
                Y=1
                P=speedx
                Q=0

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy < micey and micex <= borx:    #半径下方，且在第三象限 ，向第四象限跑                                           #左上角平分线上面  往下跑
                print('逃跑12')
                X=speedy
                Y=0
                P=speedx
                Q=0

                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())    
        if pandingx+pandingy > rfang and pandingx+pandingy < Rfang and zuo < borx <= zhongx and zhongy < bory < xia: #第三象限扇形，左上      
            if ((micex-zhongx)/xianx)*xiany+zhongy > micey and micex <= borx:     #半径上方，且在第二象限 ，向第一象限跑
                print('逃跑13')
                X=speedy
                Y=1
                P=speedx
                Q=0
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())  
            elif ((micex-zhongx)/xianx)*xiany+zhongy >= micey and micex > borx:    #半径上方，且在第一象限 ，向第四象限跑
                print('逃跑14')
                X=speedy
                Y=0
                P=speedx
                Q=0
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy <= micey and micey < bory:    #半径下方，且在第一象限 ，向第二象限跑                                    #左上角平分线上面  往下跑
                print('逃跑15')
                X=speedy
                Y=1
                P=speedx
                Q=1
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy < micey and micey >= bory:    #半径下方，且在第四象限 ，向第一象限跑                                           #左上角平分线上面  往下跑
                print('逃跑16')
                X=speedy
                Y=1
                P=speedx
                Q=0
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode()) 
        if pandingx+pandingy > rfang and pandingx+pandingy < Rfang and zhongx < borx < you and zhongy <= bory < xia: #第四象限扇形，左上      
            if ((micex-zhongx)/xianx)*xiany+zhongy > micey and micex >= borx:      #半径上方，且在第一象限 ，向第二象限跑
                print('逃跑17')
                X=speedy
                Y=1
                P=speedx
                Q=1
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())  
            elif ((micex-zhongx)/xianx)*xiany+zhongy >= micey and micex < borx:    #半径上方，且在第二象限 ，向第三象限跑
                print('逃跑18')
                X=speedy
                Y=0
                P=speedx
                Q=1
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy <= micey and micey < bory:    #半径下方，且在第二象限 ，向第一象限跑                                    #左上角平分线上面  往下跑
                print('逃跑19')
                X=speedy
                Y=1
                P=speedx
                Q=0
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode())
            elif ((micex-zhongx)/xianx)*xiany+zhongy < micey and micey >= bory:    #半径下方，且在第三象限 ，向第二象限跑                                           #左上角平分线上面  往下跑
                print('逃跑20')
                X=speedy
                Y=1
                P=speedx
                Q=1
    
                data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
                ser.write(data.encode()) 
    

    if dist>dis_safe:
        print('安全位置！！！')
        X=0
        Y=0
        P=0
        Q=0
        data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
        ser.write(data.encode())
            
    if cv2.waitKey(1) & 0xFF==27:
        break

ser.close()                                     # 关闭串口
cv2.destroyAllWindows()
cap.release()

            

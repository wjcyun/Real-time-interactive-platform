# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:19:36 2022

@author: DELL
"""
# Get the pixel coordinates of the target point in the image

import cv2
import numpy as np

img=cv2.imread('D:\\WJC1049PYTHON\\pythoncode\\picture\\2023423.png')

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        cv2.imshow("image", img)
        print("coordinate",x,y)
cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)

cv2.imshow('image', img)
cv2.waitKey()
cv2.destroyAllWindows()
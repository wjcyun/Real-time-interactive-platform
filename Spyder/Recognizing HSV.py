# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 13:28:45 2022

@author: jcyt
"""


# Convert the image to HSV color gamut and get the HSV value of the clicked position

import cv2

img = cv2.imread('D:\\WJC1049PYTHON\\pythoncode\\picture\\6271.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse click
        #print('PIX:', x, y)
        #print("BGR:", img[y, x])
        #print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])


if __name__ == '__main__':
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", mouse_click)
    while True:
        cv2.imshow('img', img)
        if cv2.waitKey() == ord('q'):
            break
    cv2.destroyAllWindows()
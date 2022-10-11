#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 03:11:31 2020

@author: prabhakar
"""

import cv2

cv2.namedWindow("RTSP View", cv2.WINDOW_NORMAL)

#cap = cv2.VideoCapture("rtsp://192.168.1.64:8554/rgb")
cap = cv2.VideoCapture("rtsp://192.168.1.64:8554/depth")
#cap = cv2.VideoCapture("rtsp://192.168.1.64:8554/depth", cv2.CAP_FFMPEG)
#cap = cv2.VideoCapture("rtsp://192.168.1.64:8554/ir",cv2.CAP_FFMPEG)

#raspberry pi
#cap = cv2.VideoCapture("rtsp://192.168.1.45:8554/rgb")
#cap = cv2.VideoCapture("rtsp://192.168.1.45:8554/depth")
#cap = cv2.VideoCapture("rtsp://192.168.1.45:8554/ir")
while True:
    
    ret, frame = cap.read()
    #print(frame.shape)
    temp = frame[:,:,0]
    temp1 = frame[:,:,1]
    temp1 = temp1.astype('uint16')
    temp = temp.astype('uint16')

    temp = temp * 256 + temp1
    print(temp.shape)
    print(temp.dtype)
    if ret:
        cv2.imshow("RTSP View", temp)
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        print("unable to open RGB camera")
        break

    
cap.release()

cv2.destroyAllWindows()


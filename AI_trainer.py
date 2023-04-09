import cv2
import mediapipe as mp
import time
import pose_mode as pm
import numpy as np

#cap = cv2.VideoCapture('video/w1.mp4')
cap = cv2.VideoCapture(0)
#332 - 201
detector = pm.poseDetector()
count = 0
dir = 0

pTime = 0

while True:
    success, img = cap.read()
    #img  = cv2.resize(img, 640, 480)
    img = cv2.flip(img, 1)
    img = detector.findPose(img, False)
    lmList = detector.findPositin(img, False)
    
    #RIGHT ARM
    if lmList:
        detector.findAngle(img, 12, 14, 16)

    #LEFT ARM
    if lmList:
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (210, 300), (0, 100))
        bar = np.interp(angle, (210, 300), (100, 400))
        #print(angle, per)

        #CHECK FOR THE DUMBBELL CURLS
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)

        #DRAW BAR
        cv2.rectangle(img, (550, 400), (600, 100), color, 3)
        cv2.rectangle(img, (550, int(bar)), (600, 100), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %',  (500, 75), cv2.FONT_HERSHEY_PLAIN,
                    4, color, 4)

        #DRAW COUNT
        cv2.rectangle(img, (0, 550), (120, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)),  (25, 470), cv2.FONT_HERSHEY_PLAIN,
                    5, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 
                3, (255, 0, 0), 2)
    

    cv2.imshow('Trainer', img)

    if cv2.waitKey(1) == ord('q'):
        break

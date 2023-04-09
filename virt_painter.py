import cv2
import numpy as np
import time
import os
import Hand_track_mod as htm

folderPath = "Painter_pics"
myList = os.listdir(folderPath)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)


header = overlayList[0]

color = (255, 0, 255)
brushThickness = 15
eraserThickness = 100

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((480, 640, 3), np.uint8)

pTime = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #FIND HAND LANDMARKS
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    #CHECKING WHICH FINGERS ARE UP
        fingers = detector.fingersUp()
        #print(fingers)

    #IF TWO FINGERS ARE UP
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            #cv2.rectangle(img, (x1, y1-25), (x2, y2+25), color, cv2.FILLED)
            print('selection mode')
            if y1 < 100:
                if 40 < x1 < 100:
                    header = overlayList[0]
                    color = (255, 0, 255)
                elif 190 < x1 < 250:
                    header = overlayList[1]
                    color = (255, 0, 0)
                elif 350 < x1 < 400:
                    header = overlayList[2]
                    color = (0, 0, 255)
                elif 500 < x1 < 630:
                    color = (0, 0, 0)
                    header = overlayList[3]

        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
            print('draw mode')
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if color == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), color, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), color, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), color, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), color, brushThickness)
            
            cv2.line(img, (xp, yp), (x1, y1), color, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), color, brushThickness)

            xp, yp = x1, y1

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)    

    #SETTING THE HEADER IMAGE
    img[0:100,0:640] = header

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 460), cv2.FONT_HERSHEY_PLAIN, 
                3, (255, 0, 0), 2)
    
    cv2.imshow('Painter', img)
    #cv2.imshow('Canvas', imgCanvas)
    if cv2.waitKey(1) == ord('q'):
        break
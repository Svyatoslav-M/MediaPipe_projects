import cv2
import mediapipe as mp
import time
import Hand_track_mod as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture("video/3.mp4")
detector = htm.handDetector(0)
    
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[4])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, 
        (255,0,255), 3)

    cv2.imshow("Hand", img)

    #cv2.waitKey(1)
    if cv2.waitKey(1) == ord('q'):
        break
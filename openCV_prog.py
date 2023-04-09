
'''
import cv2


face_c = cv2.CascadeClassifier('D:\Программы\openCV_test\haarcascade_frontalface_default.xml')
img = cv2.imread('D:\Программы\openCV_test\photo.jpg')
faces = face_c.detectMultiScale(img,1.1,4)
for(x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+y,y+h),(255,0,0),2)
cv2.imwrite('photo2',img)


capture = cv2.VideoCapture(0)

while True:
    isTrue, frame = capture.read()
    cv2.imshow('Video', frame)

    if cv2.waitKey(20) and 0xFF == ord('d'):
        break

capture.release()
cv2.destroyAllWindows()



import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    #frame = cv2.Canny(frame,125,175)
    dil = cv2.dilate(frame, (10, 10), iterations=10)
    dil = cv2.erode(frame, (10,10), iterations = 10)
    cv2.imshow("Mirrored Video", frame)
    cv2.imshow("dil", dil)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


'''

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    cv2.imshow("Hand", img)
    cv2.waitKey(1)
    '''
    if cv2.waitKey(1) == ord('q'):
        break
    '''
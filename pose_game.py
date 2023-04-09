import cv2
import pose_mode as pm
import time

cap = cv2.VideoCapture("video/3.mp4")
pTime = 0
detector = pm.poseDetector()

while True:
	success, img = cap.read()
	img = cv2.flip(img,1)
	img = detector.findPose(img)
	lmList = detector.findPositin(img, draw=False)
	'''
	if lmList:
		print(lmList[12])
		cv2.circle(img, (lmList[12][1],lmList[12][2]), 15, (255,0,0), cv2.FILLED)
	'''
	cTime = time.time()
	fps = 1/(cTime-pTime)
	pTime = cTime

	cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
				(255, 0, 255), 3)

	cv2.imshow("Image", img)
	
	if cv2.waitKey(1) == ord('q'):
		break
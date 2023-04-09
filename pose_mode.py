import cv2
import mediapipe as mp
import time
import math


class poseDetector():
	
	def __init__(self, mode=False, upBody=False, smooth=True, ensegment = True, detectionCon = 0.5, trackCon= 0.5):

		self.mode = mode
		self.upBody = upBody
		self.smooth = smooth
		self.ensegment = ensegment
		self.detectionCon = detectionCon
		self.trackCon = trackCon
		
		self.mpDraw = mp.solutions.drawing_utils
		self.mpPose = mp.solutions.pose
		self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
			self.ensegment, self.detectionCon, self.trackCon)
		
	def findPose(self, img, draw=True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.pose.process(imgRGB)
		if self.results.pose_landmarks:
			if draw:
				self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
							  		self.mpPose.POSE_CONNECTIONS)
		return img

	def findPositin(self, img, draw=True):
		self.lmList = []
		if self.results.pose_landmarks:
				for id, lm in enumerate(self.results.pose_landmarks.landmark):
					h, w, c = img.shape
					cx, cy = int(lm.x*w), int(lm.y*h)
					self.lmList.append([id, cx, cy])
					if draw:
						cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
		return self.lmList
	
	def findAngle(self, img, p1, p2, p3, draw=True):
		
		#GET THE LANDMARKS
		x1, y1 = self.lmList[p1][1:]
		x2, y2 = self.lmList[p2][1:]
		x3, y3 = self.lmList[p3][1:]

		#CALCULATE THE ANGLE
		angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
		#print(angle)
		if angle < 0:
			angle += 360

		#DRAW
		if draw:
			cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
			cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
			cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
			cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
			cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
			cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
			cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
			cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
			cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
	       				cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
		return angle


def main():

	cap = cv2.VideoCapture(0)
	pTime = 0
	detector = poseDetector()

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
	


if __name__ == "__main__":
	main()


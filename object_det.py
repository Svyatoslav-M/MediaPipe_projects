import os
import cv2
import util

model_cfg_path = os.path.join('.','model', 'cfg', 'yolov3.cfg')
model_weights_path = os.path.join('.', 'model', 'weights', 'yolov3.weights')
class_names_path = os.path.join('.', 'model', 'class.names')

img_path = '.\pics\plate1.jpeg'

#LOAD CLASS NAMES
with open(class_names_path, 'r') as f:
    class_name = [j[:-1] for j in f.readlines() if len(j) > 2]
    f.close()

#LOAD MODEL
net = cv2.dnn.readNetFromDarknet(model_cfg_path, model_weights_path)

#LOAD IMAGE
img = cv2.imread(img_path)



#CONVERT IMAGE
blob = cv2.dnn.blobFromImage(img, 1 / 255, (420, 420), (0, 0, 0), True)

#GET DETECTION
net.setInput(blob)

detections = util.get_outputs(net)

#bboxes, class_ids, confidences
bbpxes = []
class_ids = []
scores = []

#for detection in detections:
#    print(detection)
 #   break

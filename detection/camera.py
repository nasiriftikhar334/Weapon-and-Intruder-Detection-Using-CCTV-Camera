import cv2, os, time
from queue import Queue
from datetime import datetime
import numpy as np
from django.conf import settings

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

# Load Yolo
# Download weight file(yolov3_training_2000.weights) from this link :- https://drive.google.com/file/d/10uJEsUpQI3EmD98iwrwzbD4e19Ps-LHZ/view?usp=sharing

weigths_file_path = os.path.join(settings.BASE_DIR,'yolov3_training_2000.weights')
config_file_path = os.path.join(settings.BASE_DIR,'yolov3-testing.cfg')

net = cv2.dnn.readNet(weigths_file_path, config_file_path)
classes = ["Weapon"]
# with open("coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]

ln = net.getLayerNames()
output_layers = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

class VideoCamera(object):
	def __init__(self, cam=0, model_object=None):
		
		# camera properties to identify object
		self.video = cv2.VideoCapture(cam)
		self.cam_name = model_object.name
		self.cam_sys_name = model_object.cam_sys_name
		self.choice = model_object.detection_choice

		# alert settings
		self.allowed_once = False
		self.allowed_an_hour = False
		self.start_after_time = 10
		self.detected = False
		self.alert_sent = False
		self.alert_sent_time = 0

		# if self.video.isOpened():
		# 	frameCount = 0
		# 	capture_duration = 10
		# 	start_time = time.time()
		# 	while( int(time.time() - start_time) < capture_duration ):
		# 		# wait for camera to grab next frame
		# 		ret, frame = self.video.read()
		# 		# count number of frames
		# 		frameCount = frameCount+1
								
		# 	self.fps = frameCount/10

		# 	self.rec_path = os.path.join(settings.BASE_DIR, f'recordings/{self.cam_name}')
		# 	if os.path.exists(self.rec_path):
		# 		pass
		# 	else:
		# 		os.mkdir(self.rec_path)



			

	def __del__(self):
		self.video.release()

	def face_detection_frame(self):

		
		# fourcc = cv2.VideoWriter_fourcc(*'XVID')
		
		while True:
			_, image = self.video.read()
			# We are using Motion JPEG, but OpenCV defaults to capture raw images,
			# so we must encode it into JPEG in order to correctly display the
			# video stream.

			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
			for (x, y, w, h) in faces_detected:
				cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
				if not self.alert_sent:
					alertlist(self)
					self.alert_sent = True
					self.alert_sent_time = time.time()
					self.allowed_once = True
				elif (self.allowed_once and time.time() - self.alert_sent_time >= 10 ):
					self.alert_sent = False
					self.allowed_once = False
				elif (self.allowed_an_hour and time.time() - self.alert_sent_time >= 3600):
					self.alert_sent = False
					self.allowed_an_hour = False


			cv2.putText(image, f'{self.cam_name}    {datetime.now().strftime("%D:%H:%M:%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,255,255), 2)

			# frame_flip = cv2.flip(image, )
			ret, jpeg = cv2.imencode('.jpg', image)
			frame = jpeg.tobytes()
			return frame
			# yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		
	
	def weapon_detection_frame(self):
		_, img = self.video.read()
		height, width, channels = img.shape
		# width = 640
		# height = 480

		# Detecting objects
		while True:
			_, img = self.video.read()
			blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

			net.setInput(blob)
			outs = net.forward(output_layers)

			# Showing information on the screen
			class_ids = []
			confidences = []
			boxes = []
			for out in outs:
				for detection in out:
					scores = detection[5:]
					class_id = np.argmax(scores)
					confidence = scores[class_id]
					if confidence > 0.5:
						# Object detected
						center_x = int(detection[0] * width)
						center_y = int(detection[1] * height)
						w = int(detection[2] * width)
						h = int(detection[3] * height)

						# Rectangle coordinates
						x = int(center_x - w / 2)
						y = int(center_y - h / 2)

						boxes.append([x, y, w, h])
						confidences.append(float(confidence))
						class_ids.append(class_id)

			indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
			# if indexes == 0: print("weapon detected in frame")
			font = cv2.FONT_HERSHEY_PLAIN
			for i in range(len(boxes)):
				if i in indexes:
					x, y, w, h = boxes[i]
					label = str(classes[class_ids[i]])
					color = colors[class_ids[i]]
					cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
					cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
					cv2.putText(img, f'{self.cam_name}    {datetime.now().strftime("%D:%H:%M:%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,255,255), 2)
					if not self.alert_sent:
						alertlist(self)
						self.alert_sent = True
						self.alert_sent_time = time.time()
						self.allowed_once = True
					elif (self.allowed_once and time.time() - self.alert_sent_time >= 10 ):
						self.alert_sent = False
						self.allowed_once = False
					elif (self.allowed_an_hour and time.time() - self.alert_sent_time >= 3600):
						self.alert_sent = False
						self.allowed_an_hour = False


			# frame = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
			ret, jpeg = cv2.imencode('.jpg', img)
			frame = jpeg.tobytes()
			return frame
			# yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


	def record(self):

		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter(f'{self.rec_path}/{datetime.now().strftime("%H_%M_%S")}.avi', fourcc, self.fps, (640,480))

		while True:
			_, frame = self.video.read()

			cv2.putText(frame, f'{self.cam_name}    {datetime.now().strftime("%D:%H:%M:%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX,
							0.6, (255,255,255), 2)

			out.write(frame)
			ret, jpeg = cv2.imencode('.jpg', frame)
			frame = jpeg.tobytes()
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
			# ret, jpeg = cv2.imencode('.jpg', frame)
			# return jpeg.tobytes()
		

# Function to create alert for detections
que = Queue(maxsize = 5)
def alertlist(object):
	msg = f'{object.choice} detected in {object.cam_name}'
	if not que.full(): que.put(msg)
	return
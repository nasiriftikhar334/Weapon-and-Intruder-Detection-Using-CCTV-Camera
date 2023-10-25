# from django.test import TestCase

# Create your tests here.
import cv2, time
from datetime import datetime
from threading import Thread
import queue

class VideoCamera(object):
    def __init__(self, que):
            self.recording_thread = Thread(target=self.record, args=(que,))
            self.recording_thread.start()
            

    def record(self, que):
        try:
            self.video = cv2.VideoCapture(1)
            print('self.video: ', self.video, 'video.isOpened(): ', self.video.isOpened())

            if self.video.isOpened():

                frameCount = 0
                capture_duration = 10
                start_time = time.time()
                while( int(time.time() - start_time) < capture_duration ):
                    # wait for camera to grab next frame
                    ret, frame = self.video.read()
                    # count number of frames
                    frameCount = frameCount+1
                                
                framerate = frameCount/10.05
                print(framerate)
                

                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(f'recordings/{datetime.now().strftime("%H_%M_%S")}.avi', fourcc, framerate, (640,480))

                while True:
                    _, frame = self.video.read()

                    cv2.putText(frame, f'{datetime.now().strftime("%D:%H:%M:%S")}', (50,50), cv2.FONT_HERSHEY_COMPLEX,
                                    0.6, (255,255,255), 2)

                    out.write(frame)
                    que.put(frame)
                    # frame = frame.tobytes()
                    # yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                    # ret, jpeg = cv2.imencode('.jpg', frame)
                    # return jpeg.tobytes()
                    cv2.imshow("esc. to stop", frame)
                    if cv2.waitKey(1) == 27:
                        break
        except Exception as e:
            print(e)
        

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()
        if not self.video.isOpened():
            print('done')

que = queue.Queue()
obj = VideoCamera(que)

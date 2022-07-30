from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
import cv2
import time
import numpy as np
import sqlite3

from function.recognize import *
from function.detectpose import *
from function.score import *
from function.database_func import *
from main import MainWindow

fullSequence = []

class captureCamera(QThread):
    camFrame = pyqtSignal(QImage) 
    def __init__(self):
        super(captureCamera, self).__init__()
        self.camActive = True

    def run(self):
        time0 = 0
        global fullSequence
        fullSequence = []
        self.cap = cv2.VideoCapture(0)
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self.camActive:
                ret, frame = self.cap.read()
                frame = cv2.flip(frame, 1)
                image, results = mediapipe_detection(frame, pose)

                # Show fps
                time1 = time.time()
                fps = 1 / (time1 - time0)
                time0 = time1

                draw_styled_landmarks(image, results)

                if results.pose_landmarks:
                    keypoint = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten()
                    keypoint = np.array_split(keypoint, 33)
                    fullSequence.append(keypoint)
                    # sequence = sequence[-100:]

                # cv2.putText(image,'FPS:' + str(int(fps)), (3, 475), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                image = convertImage(image)
                
                ## lay dau ra
                self.camFrame.emit(image)
            self.cap.release()

    def stop(self):
        self.camActive = False

class recogPose(QThread):
    bar = pyqtSignal(list)
    prob = []
    def __init__(self):
        super(recogPose, self).__init__()
        self.recogActive = True

    def run(self):
        global fullSequence
        while self.recogActive:
            if len(fullSequence) >= 100:
                sequence = fullSequence[-100:]
                self.prob = Recognize(sequence)
                self.bar.emit(self.prob)
            time.sleep(0.1)

    def stop(self):
        self.recogActive = False

def setBarValue(self, bar):
    self.ui.vongtay.setValue(bar[2])
    self.ui.squat.setValue(bar[0])
    self.ui.cheotay.setValue(bar[1])


def startBtnClicked(self):
    self.thread[1] = captureCamera()
    self.thread[2] = recogPose()
    self.thread[1].start()
    self.thread[2].start()
    self.ui.btnStart.setEnabled(False)
    self.ui.btnPause.setEnabled(True)
    self.thread[1].camFrame.connect(self.displayCamera)
    self.thread[2].bar.connect(lambda x: setBarValue(self, x))
    self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.videoPath)))
    self.videoPlayer.play()
        

def stopBtnClicked(self):
    global fullSequence
    self.thread[1].stop()
    self.thread[2].stop()
    self.ui.btnStart.setEnabled(True)
    self.ui.btnPause.setEnabled(False)

    self.videoPlayer.stop()

    calculateScore(self, fullSequence)


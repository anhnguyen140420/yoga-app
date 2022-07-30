from PyQt5.QtGui import QImage
import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_landmarks(image, results):
    global mp_drawing, mp_pose
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # Draw pose connections

def draw_styled_landmarks(image, results):
    global mp_drawing, mp_pose
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2)
                             )
def convertImage(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w, ch = image.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)
    image = convertToQtFormat
    return image
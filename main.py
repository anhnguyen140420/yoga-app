import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ.update({"QT_QPA_PLATFORM_PLUGIN_PATH": "/home/.local/lib/python3.8/site-packages/PyQt5/Qt5/plugins/xcbglintegrations/libqxcb-glx-integration.so"})

## import GUI file
from GUI.ui_main import *
  

## IMPORT FUNCTIONS
from function_GUI.function_gui import *
from function.practice import *

class MainWindow(QMainWindow):
    listJoint = pyqtSignal(list)
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## Default setting
        defaultSetting(self)

        # Button Press Event
        self.ui.toggle.pressed.connect(lambda: toggleMenu(self))
        self.ui.btnHome.pressed.connect(lambda: homepage(self))
        self.ui.btnWorkout.pressed.connect(lambda: workoutpage(self))
        self.ui.btnProfile.pressed.connect(lambda: profilepage(self))
        self.ui.left.pressed.connect(lambda: prev(self))
        self.ui.right.pressed.connect(lambda: next(self))
        self.ui.btnQuit.clicked.connect(lambda: content(self))
        self.ui.recentExercises.itemClicked.connect(self.detailExercise)
        self.ui.exercises.itemClicked.connect(self.detailExercise)
        self.ui.poses.itemClicked.connect(self.showPracticePage)

        self.ui.btnBack.clicked.connect(self.prevPose)
        self.ui.btnNext.clicked.connect(self.nextPose)

        ## Control thread for capture camera and recognize pose
        self.thread={}
        self.ui.btnStart.clicked.connect(lambda: startBtnClicked(self))
        self.ui.btnPause.clicked.connect(lambda: stopBtnClicked(self))

        ## tutorial video
        self.videoPlayer = QMediaPlayer()
        self.videoPlayer.setVideoOutput(self.ui.video)
        self.videoPlayer.mediaStatusChanged.connect(self.statusChanged)

    def detailExercise(self, exercise_name):
        try:
            content(self)
            self.exercise_path = 'exercises/{}'.format(exercise_name.text())
            description = loadFileFilters(self, self.exercise_path, ['*.txt'])
            a_file = open(description, "r").readlines()
            self.exercise_name = a_file[0]
            self.exercise_category = a_file[1]
            self.exercise_level = a_file[2]
            self.ui.exercise_name.setText(self.exercise_name)
            self.ui.exercise_level.setText('Độ khó: '+self.exercise_level)

            initialPage(self, self.exercise_path, self.ui.poses)
        except:
            pass

    def showPracticePage(self, poseName):
        self.poseName = poseName
        self.recogdatafile = loadFileFilters(self, self.exercise_path, ['*.h5'])
        self.pose_path = '{}/{}'.format(self.exercise_path, poseName.text())
        self.videoPath = loadFileFilters(self, self.pose_path, ['*.avi'])
        self.standardJoint = loadFileFilters(self, self.pose_path, ['*.txt'])
        preLoadWeight(self)
        practicepage(self)

    def displayCamera(self, image):
        bgsize = self.ui.camera.size()
        image = image.scaled(bgsize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.camera.setPixmap(QPixmap.fromImage(image))
        
    def displayAction(self, actionFrame):
        self.ui.action.setPixmap(QPixmap.fromImage(actionFrame))
        self.ui.action.setScaledContents(True)

    def statusChanged(self, status):
        if status == QMediaPlayer:
            print('playback ended!')

    def prevPose(self):
        currow = self.ui.poses.currentRow()
        if currow == 0:
            pass
        else:
            self.ui.poses.setCurrentRow(currow-1)
            name = self.ui.poses.currentItem()
            self.showPracticePage(name)

    def nextPose(self):
        currow = self.ui.poses.currentRow()
        if currow == 2:
            pass
        else:
            self.ui.poses.setCurrentRow(currow+1)
            name = self.ui.poses.currentItem()
            self.showPracticePage(name)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

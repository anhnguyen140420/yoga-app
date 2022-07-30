from PyQt5.QtWidgets import QDialog
import time
import sqlite3
from function.score_function import *
from function_GUI.function_gui import *
from function.database_func import *
from GUI.ui_score_dialog import Ui_Score_Dialog

def calculateScore(self, fullSequence):
    fullSequence = fullSequence[-200:]
    file_name = self.standardJoint

    a_file = open(file_name, "r")
    text_data = []
    for line in a_file:
      stripped_line = line.strip()
      line_list = stripped_line.split()
      text_data.append(line_list)
    a_file.close()

    skeleton_data = [text_data[i * 33:(i + 1) * 33] for i in range((len(text_data) + 33 - 1) // 33 )]

    r_arm_ang = []
    r_elbow_ang = []
    r_body_ang = []
    r_knee_ang = []
    r_ankle_ang = []

    r_arm_ang, r_elbow_ang, r_body_ang, r_knee_ang, r_ankle_ang = calculateAngle(fullSequence)
       
    c_arm_ang = []
    c_elbow_ang = []
    c_body_ang = []
    c_knee_ang = []
    c_ankle_ang = []

    c_arm_ang, c_elbow_ang, c_body_ang, c_knee_ang, c_ankle_ang = calculateAngle(skeleton_data)

    score1, distance1 = dtwDistanceScore(r_arm_ang, c_arm_ang)
    score2, distance2 = dtwDistanceScore(r_elbow_ang, c_elbow_ang)
    score3, distance3 = dtwDistanceScore(r_body_ang, c_body_ang)
    score4, distance4 = dtwDistanceScore(r_knee_ang, c_knee_ang)
    score5, distance5 = dtwDistanceScore(r_ankle_ang, c_ankle_ang)

    self.totalscore = score1+score2+score3+score4+score5
    self.detailScore = [score1,score2,score3,score4,score5]
    # self.totalscore = 8
    # self.detailScore = [1,8,2,2,2]
    localtime = time.asctime( time.localtime(time.time()) )
    data = [self.exercise_name, self.exercise_category, self.exercise_level, self.totalscore, localtime]

    saveData(self, data)
    showScoreDialog(self)

def showScoreDialog(self):
  self.dialog = QDialog()
  self.dialog.ui = Ui_Score_Dialog()
  self.dialog.ui.setupUi(self.dialog) 

  self.dialog.ui.score.setText(str(self.totalscore) + "/10")
  self.dialog.ui.name.setText('Tên động tác: {}'.format(self.poseName.text()))
  self.dialog.ui.detail.setText('''Chi tiết: 
    Vai: {}, Khuỷu tay: {}, Eo: {}, Đầu gối: {}, Cổ chân: {}'''.format(self.detailScore[0],self.detailScore[1],self.detailScore[2],self.detailScore[3],self.detailScore[4]))

  self.dialog.ui.btn_home.clicked.connect(lambda: backtohome(self))
  self.dialog.ui.btn_detail.clicked.connect(lambda: gotoProfile(self))
  self.dialog.exec_()

def backtohome(self):
  self.dialog.close()
  homepage(self)

def gotoProfile(self):
  self.dialog.close()
  profilepage(self)
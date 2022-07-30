import sqlite3
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def saveData(self, data):
  conn = sqlite3.connect('database.db')
  c = conn.cursor()

  c.execute("INSERT INTO score_data (lesson, category, level, score, time) VALUES (?,?,?,?,?)", data)
  conn.commit()

  conn.close()

def loadScore(self):
    data = []
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('select score from score_data')
    for x in c.fetchall():
        data.append(x[0])
    conn.close()
    return data

def addData(self, icon_path, name, place):
    item = QListWidgetItem(place)
    icon = QIcon()
    icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.Off)
    item.setIcon(icon)

    place.setIconSize(QSize(300, 300))
    place.setSpacing(20)
    
    item.setText(name)

def initialPage(self, item_dir, place):
    place.clear()
    subfolders = [ f.path for f in os.scandir(item_dir) if f.is_dir() ]
    for exercise_path in subfolders:
        exercise_name = os.path.basename(exercise_path)
        dir_ = QDir(exercise_path)
        filters = ['*.jpg', '*.JPG', '*.png', '*.PNG']
        dir_.setNameFilters(filters)
        icon_exercise = dir_.entryInfoList()
        icon_path = icon_exercise[0].absoluteFilePath()
        addData(self, icon_path, exercise_name, place)

def loadFileFilters(self, path, filters):
    recogfile = QDir(path)
    recogfile.setNameFilters(filters)
    recogfile = recogfile.entryInfoList()
    return recogfile[0].absoluteFilePath()

def updateHistoryTable(self):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('select * from score_data')

    tablerow=0
    self.ui.historyTable.setRowCount(50)
    for sqlrow in c:
        self.ui.historyTable.setItem(tablerow, 0, QTableWidgetItem(sqlrow[0]))
        self.ui.historyTable.setItem(tablerow, 1, QTableWidgetItem(sqlrow[1]))
        self.ui.historyTable.setItem(tablerow, 2, QTableWidgetItem(sqlrow[2]))
        self.ui.historyTable.setItem(tablerow, 3, QTableWidgetItem(str(sqlrow[3])))
        self.ui.historyTable.setItem(tablerow, 4, QTableWidgetItem(sqlrow[4]))
        tablerow=tablerow+1
    header = self.ui.historyTable.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.Stretch)
    header.setSectionResizeMode(1, QHeaderView.Stretch)
    header.setSectionResizeMode(2, QHeaderView.Stretch)
    header.setSectionResizeMode(3, QHeaderView.Stretch)
    header.setSectionResizeMode(4, QHeaderView.Stretch)

    conn.close()

def updateStatisticalTable(self):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    score = c.execute('select max(score) from score_data')
    self.ui.highestscore.setText('Điểm cao nhất: {}'.format(score.fetchall()[0][0]))
    mostfreq = c.execute(
        '''SELECT lesson,COUNT(lesson) AS most FROM score_data
        GROUP BY lesson
        ORDER BY most DESC;'''
        )

    self.ui.mostfreq.setText('Bài tập nhiều nhất: {}'.format(mostfreq.fetchall()[0][0]))
    exer = c.execute('''SELECT lesson, max(score) FROM score_data
        GROUP BY lesson; ''')
    self.ui.highestexercise.setText('Bài tập có điểm cao nhất: {}'.format(exer.fetchall()[0][0]))

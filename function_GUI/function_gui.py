from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
import os

from function.database_func import *

shadow_elements = {
    "category",
}

#########################################################
def defaultSetting(self):
    homepage(self)
    automaticSlide(self)
    # Hide scroll bar
    self.ui.scrollArea_2.verticalScrollBar().hide()
    self.ui.scrollArea_4.verticalScrollBar().hide()
    self.ui.scrollArea_2.verticalScrollBar().hide()
    self.ui.scrollArea_5.verticalScrollBar().hide()
    ## drop shadow
    for x in shadow_elements:
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(25)
        effect.setXOffset(5)
        effect.setYOffset(5)
        effect.setColor(QColor(150, 150, 150, 255))
        getattr(self.ui, x).setGraphicsEffect(effect)

    ## Run background music
    self.musicPlayer = QMediaPlayer()
    # self.musicPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("Yoga_sources/yoga_music.mp3")))
    self.musicPlayer.setVolume(50)
    # self.musicPlayer.play()
    
    score = loadScore(self)
    createLineChart(self, score)

    self.ui.btnStart.setEnabled(True)
    self.ui.btnPause.setEnabled(False)

######################################################################33
def toggleMenu(self): 
    key = self.ui.toggle.text()
    width = self.ui.leftBar.width()
    standard = 84
    maxExtended = 146
    if key == 'E-OGA':
        widthExtended = standard
        self.ui.toggle.setText('')
        self.ui.btnHome.setText('')
        self.ui.btnWorkout.setText('')
        self.ui.btnProfile.setText('')
        self.ui.toggle.setIcon(QIcon(':/icons/sources/icons/svgBlue/hamburger.svg'))
        self.ui.leftBar.setStyleSheet('text-align:center;padding:0px;')
    else:
        widthExtended = maxExtended
        self.ui.toggle.setText('E-OGA')
        self.ui.btnHome.setText('Trang chủ')
        self.ui.btnWorkout.setText('Tập luyện')
        self.ui.btnProfile.setText('Cá nhân')
        self.ui.toggle.setIcon(QIcon(':/icons/sources/icons/svgBlue/chevron-left.svg'))
        self.ui.leftBar.setStyleSheet('')

    ## Add animation of left bar
    self.target = self.ui.leftBar
    createAnimation(self,self.target,width,widthExtended,200)

###############################################################
def homepage(self):
    self.ui.contentWidget.setCurrentWidget(self.ui.home)
    self.ui.stackName.setText('Trang chủ')
    initialPage(self, 'exercises', self.ui.recentExercises)
def workoutpage(self):
    self.ui.contentWidget.setCurrentWidget(self.ui.workout)
    self.ui.stackName.setText('Tập luyện')
    initialPage(self, 'exercises', self.ui.exercises)
def profilepage(self):
    self.ui.contentWidget.setCurrentWidget(self.ui.profile)
    self.ui.stackName.setText('Cá nhân')
    score = loadScore(self)
    updateLineChart(self, score)
    updateHistoryTable(self)
    updateStatisticalTable(self)
def practicepage(self):
    self.ui.contentWidget.setCurrentWidget(self.ui.practice)
    self.ui.stackName.setText('Practice')
    self.ui.camera.clear()
    self.ui.vongtay.setValue(0)
    self.ui.squat.setValue(0)
    self.ui.cheotay.setValue(0)
    self.ui.stackName.setText(self.poseName.text())
def automaticSlide(self):
    timer = QTimer(self)
    timer.timeout.connect(lambda: next(self))
    timer.start(5000)
def next(self):
    self.start = self.ui.Img.currentIndex()
    self.end = self.start + 1
    if self.end >2:
        self.end = 0
    self.ui.Img.setCurrentIndex(self.end)
    createAnimation(self,self.ui.Img,self.start,self.end,500)
def prev(self):
    self.index = self.ui.Img.currentIndex()
    self.index -=1
    if self.index <0:
        self.index = 2
    self.ui.Img.setCurrentIndex(self.index)
def content(self):
    self.ui.contentWidget.setCurrentWidget(self.ui.courses)
    self.ui.stackName.setText('Content')

#############################################################
def createAnimation(self,target,start,end,duration):
    self.animation = QPropertyAnimation(target, b"minimumWidth")
    self.animation.setDuration(duration)
    self.animation.setStartValue(start)
    self.animation.setEndValue(end)
    self.animation.setEasingCurve(QEasingCurve.InOutQuart)
    self.animation.start()

#########################################################
def createLineChart(self, data):
    self.lineChart = QChart()
    self.lineChart.legend().hide()
    updateLineChart(self, data)
    self.lineChart.createDefaultAxes()
    self.lineChart.setTitle("")

    self.lineChartView = QChartView(self.lineChart)
    self.lineChartView.setRenderHint(QPainter.Antialiasing)
    self.lineChartView.chart().setTheme(QChart.ChartThemeBlueCerulean)

    self.ui.barChartLayout.addWidget(self.lineChartView)

def updateLineChart(self, data):
    series = QLineSeries()
    for x in range(len(data)):
        series.append(x, data[x])
    self.lineChart.removeAllSeries()
    self.lineChart.addSeries(series)

def createBarChart(self):
    self.set0 = QBarSet("Level 1")
    self.set1 = QBarSet("Level 2")
    self.set2 = QBarSet("Level 3")
    self.set3 = QBarSet("Level 4")
    # self.set4 = QBarSet("Sam")

    self.set0.append([1, 2, 3, 4, 5, 6])
    self.set1.append([5, 0, 0, 4, 0, 7])
    self.set2.append([3, 5, 8, 13, 8, 5])
    self.set3.append([5, 6, 7, 3, 4, 5])
    # self.set4.append([9, 7, 5, 3, 1, 2])

    self._bar_series = QBarSeries()
    self._bar_series.append(self.set0)
    self._bar_series.append(self.set1)
    self._bar_series.append(self.set2)
    self._bar_series.append(self.set3)

    self.chart = QChart()
    self.chart.addSeries(self._bar_series)
    # self.chart.setTitle("Experience per month")

    self.categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    self._axis_x = QBarCategoryAxis()
    self._axis_x.append(self.categories)
    self.chart.createDefaultAxes()
    self.chart.setAxisX(self._axis_x, self._bar_series)
    self._axis_x.setRange("Jan", "Jun")

    self._axis_y = QValueAxis()
    self.chart.setAxisY(self._axis_y, self._bar_series)
    self._axis_y.setRange(0, 15)

    self.chart.legend().setVisible(True)
    self.chart.legend().setAlignment(Qt.AlignLeft)

    self.chartView = QChartView(self.chart)
    self.chartView.setRenderHint(QPainter.Antialiasing)
    self.chartView.chart().setTheme(QChart.ChartThemeBlueCerulean)

    self.ui.barChartLayout.addWidget(self.chartView)

def createPieChart(self):
    self.series = QPieSeries()

    self.series.append('Level 1', 20)
    self.series.append('Level 2', 16)
    self.series.append('Level 3', 5)
    self.series.append('Level 4', 1)

    # self.slice = self.series.slices()[2]
    # self.slice.setExploded()
    # self.slice.setLabelVisible()
    # self.slice.setPen(QPen(Qt.darkGreen, 2))
    # self.slice.setBrush(Qt.green)

    self.chart = QChart()
    self.chart.addSeries(self.series)
    # self.chart.setTitle('Exercise difficulty')

    self.chart.legend().setVisible(True)
    self.chart.legend().setAlignment(Qt.AlignRight)

    self._chart_view = QChartView(self.chart)
    self._chart_view.setRenderHint(QPainter.Antialiasing)
    self._chart_view.chart().setTheme(QChart.ChartThemeLight)

    self.ui.pieChartLayout.addWidget(self._chart_view)

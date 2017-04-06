# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Try3.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#

from PyQt4 import QtCore, QtGui
import sys
from matplotlibwidget import MatplotlibWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import numpy as np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(663, 371)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.matplotlibwidget = MatplotlibWidget(self.centralwidget)
        self.matplotlibwidget.setObjectName(_fromUtf8("matplotlibwidget"))
        self.horizontalLayout.addWidget(self.matplotlibwidget)
        self.matplotlibwidget_2 = MatplotlibWidget(self.centralwidget)
        self.matplotlibwidget_2.setObjectName(_fromUtf8("matplotlibwidget_2"))
        self.horizontalLayout.addWidget(self.matplotlibwidget_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Btn1 = QtGui.QPushButton(self.centralwidget)
        self.Btn1.setObjectName(_fromUtf8("Btn1"))
        self.horizontalLayout_2.addWidget(self.Btn1)
        self.Btn2 = QtGui.QPushButton(self.centralwidget)
        self.Btn2.setObjectName(_fromUtf8("Btn2"))
        self.horizontalLayout_2.addWidget(self.Btn2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Btn1.setText(_translate("MainWindow", "Plot1", None))
        self.Btn2.setText(_translate("MainWindow", "Plot2", None))
        
        '''Data'''
        self.freq = np.linspace(40,1000000,100)
        self.results0 =['3878.132', '3504.161', '3165.592', '2860.42', '2584.324', '2334.81', '2109.729', '1906.073', '1721.859', '1555.656', '1405.443', '1269.945', '1147.354', '1036.509', '936.5627', '846.3204', '764.7718', '690.9653', '624.4225', '564.3945', '510.0611', '461.044', '416.87', '376.6079', '340.6439', '308.0496', '278.6077', '251.9953', '228.0299', '206.2746', '186.6915', '168.9653', '152.9761', '138.5422', '125.444', '113.6239', '102.9155', '93.21563', '84.43903', '76.53981', '69.34584', '62.81862', '56.94059', '51.56695', '46.76265', '42.39815', '38.44305', '34.84598', '31.61104', '28.66048', '25.97362', '23.55438', '21.39261', '19.40973', '17.60974', '15.98018', '14.51402', '13.18858', '11.97802', '10.88318', '9.909389', '9.015993', '8.225852', '7.508034', '6.863081', '6.295485', '5.786119', '5.337557', '4.941232', '4.596627', '4.29794', '4.03434', '3.815629', '3.629171', '3.469009', '3.340856', '3.240424', '3.159087', '3.101883', '3.069119', '3.050093', '3.055771', '3.079314', '3.123159', '3.187994', '3.281269', '3.394071', '3.531498', '3.699423', '3.89642', '4.126081', '4.392282', '4.698961', '5.050098', '5.444149', '5.892684', '6.396917', '6.963755', '7.594185', '8.304343']
        self.results1 = ['-89.16236', '-89.16116', '-89.14596', '-89.14394', '-89.12545', '-89.10586', '-89.09182', '-89.06624', '-89.03296', '-89.01389', '-88.97649', '-88.94079', '-88.90817', '-88.85525', '-88.79459', '-88.75808', '-88.6977', '-88.62376', '-88.5481', '-88.48488', '-88.39263', '-88.2883', '-88.19031', '-88.08826', '-87.98342', '-87.84882', '-87.71402', '-87.5624', '-87.42972', '-87.26712', '-87.06639', '-86.91833', '-86.72942', '-86.54362', '-86.36795', '-86.16737', '-85.96503', '-85.75699', '-85.50269', '-85.23225', '-85.02274', '-84.73141', '-84.44654', '-84.15973', '-83.73808', '-83.40476', '-83.0065', '-82.57482', '-82.04786', '-81.52676', '-80.96117', '-80.34847', '-79.62247', '-78.86547', '-78.02332', '-77.11742', '-76.05641', '-74.91241', '-73.68568', '-72.36077', '-70.79715', '-69.07257', '-67.2663', '-65.14868', '-62.8732', '-60.4368', '-57.69737', '-54.68653', '-51.60114', '-48.13024', '-44.55642', '-40.86077', '-36.8222', '-32.6556', '-28.45568', '-24.11695', '-19.76229', '-15.24041', '-10.69787', '-6.135849', '-1.572018', '2.983396', '7.534532', '12.072', '16.57078', '20.86565', '25.28811', '29.48729', '33.62636', '37.61086', '41.37828', '45.00201', '48.47696', '51.74102', '54.76994', '57.63074', '60.22816', '62.68788', '64.98302', '67.03873']
        '''Set plots'''
        self.matplotlibwidget.setnames('First plot','Amplitude','Freq')
        self.matplotlibwidget_2.setnames('Second plot','Phase','Freq')
       
        '''Set buttons'''
        self.Btn1.clicked.connect(self.printBtn1)
        self.Btn2.clicked.connect(self.printBtn2)
        
    def printBtn1(self):
        self.matplotlibwidget.plotDataPoints(self.freq,self.results0)  
        print ("Clicked first button")
        
    def printBtn2(self):
        self.matplotlibwidget_2.plotDataPoints(self.freq,self.results1)  
        print ("Clicked second button")
        
    
class MatplotlibWidget(Canvas):        
    def __init__(self, parent=None, title='Title', xlabel='x label', ylabel='y label', dpi=100, hold=False):
        super(MatplotlibWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure(dpi=dpi)
        self.canvas = Canvas(self.figure)
        self.theplot = self.figure.add_subplot(111) 
        
    def setnames(self,title,xlabel,ylabel):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.theplot.set_title(self.title)
        self.theplot.set_xlabel(self.xlabel)
        self.theplot.set_ylabel(self.ylabel)

    def plotDataPoints(self, x, y):
        self.theplot.plot(x,y)
        self.draw()            


def main():
            app = QtGui.QApplication(sys.argv)
            MainWindow = QtGui.QMainWindow()
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow)
            MainWindow.show()
            sys.exit(app.exec_())


if __name__ == '__main__':   
    main() 

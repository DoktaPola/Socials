from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.Qt import *
import sys

class Info(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    def initUI(self):
        self.setWindowTitle("General description of the program")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        #         self.setStyleSheet("QWidget { \
                #                    background-color: rgba(176, 224, 230,250);} \
                #                    \
                #                    \
                #                    background-color: rgba(0,100,255,0);} \
                #                     \
                #                    \
                #                    background-color: rgba(0,41,59,255);}")

        self.setGeometry(300, 300, 600, 100)
        self.setWindowIcon(QIcon('vopros.jpg'))
        self.label = QLabel('Будет описание проги, инфа про нее',
                            self,
                            alignment=Qt.AlignCenter)
        self.label.setFont(QFont("Future", 20, QFont.Bold))





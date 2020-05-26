#!/usr/bin/python3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication,QMessageBox,QPushButton,QHBoxLayout,QVBoxLayout
from PyQt5.QtGui import QIcon
from wx.lib.embeddedimage import PyEmbeddedImage

import info
class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        buttom_vk = QPushButton('search in Vkontakte',self)
        buttom_vk.move(30, 50)
        buttom_facebook = QPushButton('search in Vkontakte',self)
        buttom_vk.move(150, 50)
        self.info = info.Info() # нужно для открытия окна с инфой

        exitAction = QAction(QIcon('vopros.jpg'), '&To access information', self) #установка изображения и подписи
        exitAction.setShortcut('Ctrl+Q') #можно будет сделать данной комбинацией клавишей
        exitAction.setStatusTip('You will learn what this program does ') #статус  снизу подпись
        exitAction.triggered.connect(self.info.show)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Info')  #меню бар с данным называнием
        fileMenu.addAction(exitAction)




        self.setWindowIcon(QIcon('orig.ico')) # добавить иконку приложению

        self.setGeometry(300, 300, 300, 200) #параметры открытия окна


        self.setWindowTitle('A framework for search, analysis and visualization of social networks data') #название


        self.show() #демонстрация


    def closeEvent(self, event): # функция при нажатии закрытия задание уточнительного вопроса

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.setWindowOpacity(0.95)
    app.setWindowIcon(QIcon('orig.ico'))
    ex.show()
    sys.exit(app.exec_())
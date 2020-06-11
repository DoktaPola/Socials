import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import main_design  # Это наш конвертированный файл дизайна
from PyQt5.QtCore    import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication,QProgressBar
import new_lib_leg
class ExampleApp(QtWidgets.QMainWindow, main_design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

    def initUI(self):
        self.comboBox_facebook_search.activated[str].connect(self.function_selection_facebook)
        self.pushButton_facebook_offer_friends.clicked.connect(self.offer_friends)# подключаем к функциям кнопки
        self.buttom.clicked.connect(self.offer_friends)
        self.pushButton_facebook_find(self.find_facebook)
        self.pushButton__facebook_search(self.facebook_search)
        self.pushButton_vk_find_1(self.vk_find)

        # self.fig = functional.draw_social_groups()
        # self.mda = MyMplCanvas(self.fig)
        # vbox = QVBoxLayout()
        # vbox.addWidget(self.buttom_vk)
        # vbox.addWidget(self.buttom)
        # vbox.addWidget(self.mda)
        # self.setLayout(vbox)

    def offer_friends(self):
            new_lib_leg.find_by_info('study', self.lineEdit_facebook_search.text())
            url = 'D:/inter/facebook_net.html'
            self.frame_2.load(QUrl(url))

    def facebook_search(self):
        if self.comboBox_facebook_search.currentText()=="place of study":
            new_lib_leg.find_by_info('study', self.lineEdit_facebook_search.text())
            url = 'D:/inter/facebook_net.html'
            self.frame_2.load(QUrl(url))
            url='http://127.0.0.1:8889/'
            self.frame_legend.load(QUrl(url))


        elif self.comboBox_facebook_search.currentText() == "residence":
            new_lib_leg.find_by_info('live in', self.lineEdit_facebook_search.text())
            url = 'D:/inter/facebook_net.html'
            self.frame_2.load(QUrl(url))
            url = 'http://127.0.0.1:8889/'
            self.frame_legend.load(QUrl(url))
        else:
            new_lib_leg.find_by_info('b-day', self.lineEdit_facebook_search.text())
            url = 'D:/inter/facebook_net.html'
            self.frame_2.load(QUrl(url))
            url = 'http://127.0.0.1:8889/'
            self.frame_legend.load(QUrl(url))

    # def Activated(self):
    #         self.fig.clf()
    #         self.mda = MyMplCanvas(self.fig)
    # #
    # def offer_friends(self):

    # # self.fullScreenButton.clicked.connect(self.swichFullScreen)
    # # def swichFullScreen(self):
    # #     #        self.setLayout(self.findLayout("full"))           # ---
    # #     #        self.show()                                       # ---
    # #     # +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # #     if self.sender().text() == "Full":
    # #         self.topLeftBox.hide()
    # #         self.topRightBox.hide()
    # #         self.bottomLeftBox.hide()
    # #         self.bottomRightBox.hide()
    # #         self.mainLayout.addWidget(self.bottomRightBox, 0, 0, 1, 2)
    # #         self.bottomRightBox.show()
    # #         self.fullScreenButton.setText("NoFull")
    #
    #     else:
    #         self.bottomRightBox.hide()
    #         self.topLeftBox.show()
    #         self.topRightBox.show()
    #         self.bottomLeftBox.show()
    #         self.mainLayout.addWidget(self.bottomRightBox, 2, 1)
    #         self.bottomRightBox.show()
    #         self.fullScreenButton.setText("Full")
    # def initUI(self):
    #     self.browser = QWebEngineView()
    #
    #     # Загрузка локальной страницы
    #     # Полный путь к index.html
    #     url = 'D:/inter/facebook_net.html'
    #     self.browser.load(QUrl(url))
    #     self.widget(self.browser)
    # def startFunction(self, event):
    #
    #     progressbar = QMessageBox.question(self, '',
    #                                  "Information is being collected, please wait.")
    #     progressbar.pbar = QProgressBar(self)
    #     progressbar.pbar.setGeometry(30, 40, 200, 25)
    #     self.btn = QtWidgets.QPushButton('Cancel', self)
    #     self.btn.move(40, 80)
    #     self.btn.clicked.connect(self.doAction)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    # window.setWindowOpacity(0.95)
    window.setWindowIcon(QIcon('orig.ico'))
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()цию main()
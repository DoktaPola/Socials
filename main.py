import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design_final  # Это наш конвертированный файл дизайна
from PyQt5.QtCore    import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication,QProgressBar
import graph_new_lib
import vk
import functional
class Windowed_application(QtWidgets.QMainWindow, design_final.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

    def facebook_group_search(self):
        graph_new_lib.draw_groups(graph_new_lib.find_groups())
        url = 'D:/inter/facebook_net.html'
        self.frame_2.load(QUrl(url))
        url1 = 'http://127.0.0.1:8889/'
        self.frame_legend.load(QUrl(url1))

    def facebook_offers_friends(self):
        graph_new_lib.draw_common_friends_between_friends(graph_new_lib.find_common_friends_between_friends())
        url = 'D:/inter/facebook_net.html'
        self.frame_2.load(QUrl(url))
        url1 = 'http://127.0.0.1:8889/'
        self.frame_legend.load(QUrl(url1))

    def facebook_search(self):
        if self.comboBox_facebook_search.currentText() == "place of study":
            graph_new_lib.find_by_info('study', self.lineEdit_2.text())
            url = 'D:/inter/facebook_net.html'
            self.frame_2.load(QUrl(url))
            url = 'http://127.0.0.1:8889/'
            self.frame_legend.load(QUrl(url))


        elif self.comboBox_facebook_search.currentText() == "residence":
            graph_new_lib.find_by_info('live in', self.lineEdit_facebook_search.text())
            url = 'D:/inter/facebook_net.html'
            self.frame_2.load(QUrl(url))
            url = 'http://127.0.0.1:8889/'
            self.frame_legend.load(QUrl(url))
        else:
            graph_new_lib.find_by_info('b-day', self.lineEdit_facebook_search.text())
            url = 'D:/inter/facebook_net.html'
            self.frame_2.load(QUrl(url))
            url = 'http://127.0.0.1:8889/'
            self.frame_legend.load(QUrl(url))

    def facebook_find_path(self):
        friends_queue = graph_new_lib.deque()
        FB = graph_new_lib.create_graph()
        path = graph_new_lib.find_connection(FB, self.lineEdit_facebook_find_1.text(),
                                             self.lineEdit_facebook_find_2.text(), friends_queue)
        url = 'D:/inter/facebook_net.html'
        self.frame_2.load(QUrl(url))
        url = 'http://127.0.0.1:8889/'
        self.frame_legend.load(QUrl(url))

    def vk_search_social_circle(self):
        vk.main(1, self.lineEdit_11.text(), self.lineEdit_2.text(), self.lineEdit_work_time.text(), 0, 0, 0)
        functional.main(1)
        url = 'friends.html'
        self.frame_3.load(QUrl(url))

    def vk_grouping_func(self):
        vk.main(3, 0, 0, self.lineEdit_work_time.text(), 0, 0, self.lineEdit_2.text())
        functional.main(3)
        url = 'groups.html'
        self.frame_3.load(QUrl(url))

    def vk_find_path(self):
        vk.main(2, 0, 0, self.lineEdit_work_time_2.text(), self.lineEdit_vk_find_1.text(),
                self.lineEdit_vk_find_2.text(), 0)
        functional.main(3)
        url = 'way.html'
        self.frame_3.load(QUrl(url))
 

def main():
    graph_new_lib.create_graph()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Windowed_application()  # Создаём объект класса ExampleApp
    window.setWindowIcon(QIcon('orig.ico'))
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()цию main()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design1.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
from wx.lib.embeddedimage import PyEmbeddedImage

from PyQt5 import QtCore, QtGui, QtWidgets
hse = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABHNCSVQICAgIfAhkiAAAEqhJ'
    b'REFUaIGdmnt8VOWZx7/vucw9yeTK5GogCQkBRCAoiOIF1MLaar1td/2srm2t1tZ2192P26Vu'
    b'd7fa1rb2rp9qtVvv10qtrYooilxFCCIQSAK5E3KdySSZzPWc8+4fZzIQSRT7JPP5zJzzznue'
    b'3/vcn2eElFLyGchKL1eEACAcTdJ0PEzHUISxmIElJU5Nwe3QUBV7TcqwiCYNTAmqEOT5HNTM'
    b'ymJeaQ4uXZ123zMlcaYApASJRBECKSUHj4dp7AhhmpKKAg9zinyU5HrwOLSZ9wDGYimOBydo'
    b'G4jQPxoj26OzvKqAykJfBogQgjOFcUYALCkRCISAxo4gO48OUez3sGZBAL/HgQSktMHt6wyh'
    b'KoJFFbmkTAtdVRiNJtlyZICrlpYjJUwespSSo/3j7GgdImGYXLGwhNlFvs8mDfkpZJiWlFLK'
    b'vnBUPvRWs3xhV4cciyWllFIe6A7J7uGIlFLKpGFKKaV85O1WeccfPpBSSpky7O++vr9XXv6D'
    b't6Vlf5SmZUnDNKVlWTJ9SQ6OxeQjm1vl09vbZTSRsteZk3dnJuWTwJmWRFUEW5sHeGZHB59f'
    b'XMYNyyvJculs2NPNiXCMB14/Qk8oiq4qGKaF36NTPcvHi+93oqmCobE4R06Mcl51PjtbBwHo'
    b'DUX5x4d2kTItBLCvM0gokuRrl9YwrzSHBze10NI3iqIITOuTFWRahbVVAlRF8PSOdpBw19p5'
    b'iLRIQ5EETZ0j/Nf1i0jGTT5sG6Y8r4Kh8QQup8Ktl1bTemIss9cXG8qQEtoGxgHI9zm59/qF'
    b'6Kp9finTYmvzALGkwZLKPKpnZfH41mP0hmJcOj+QOcjpaFobmNTThze3MrvIxxULS2jsCBLI'
    b'cVGa5wXg12+2kDItSvxOLj+7lHyfM8PMwGiMSMKkPxzDpav4PQ5yvTqzctxTnmNYkoPdIXJ9'
    b'Dn7+12ZW1RVx3fKzMEwLTVV4Yls7OR6Nq5dWzAjiNABW2hgf3txKXUk2F88L8Oq+HrqHJ7jp'
    b'wiqy3XqG0Z5glLMKPIzFUry67wSv7e9jb0eYE+EYiZhhnwSAquBx61QWuDm/Jp+rlpRwSX0R'
    b'XqfOK409TCRS9ARjfOOyuWS5dCwpiSUNvE6dZ3Z2kOXU+MLS8mlBTAEwyfzTO9rJ8zlZt6gU'
    b'gM1Nfdy3oYlrzyvH41S5amkZ+T4XwUiC+//SzGNbOggHowgEUldBUxAKTDpDS0qwJBgWImUi'
    b'FUFleTbfuqyKb1xWg2nZEp+MCRMJg/teOcCtl9QwpyiLx949xtziLFbVzcrweBqAyRtbjgzQ'
    b'NRzh5gur0kYm0FTB7945xolwlDsvn0u+z8lDbx9l/fOHGAvFER4dRVcQaT4lkvT/yQcJG5Ci'
    b'pNckTGTCYHZlDo9+ZSmr5weQEkZjSe58vJEsl8bF8ws5v6aQsjwvP3v9MNcsq2B2oW+KKxYy'
    b'jUAA/eEYz+zs4K519ezrCFJf5sedPpXRaJJYysTvcfClh3bx5/e6ULwOhK4grdNUc6qYhf2y'
    b'LMmkU1GEsL1MPIU0LO6+rp4f//0i9rQHeWVPDxfMLWDt4jISKROnrtIXjvHczg7+Ze28KRLQ'
    b'wA4oQgg27O3hysVlCKClb5QNe4/ztUuqKctzk+NxkBiPc/5/v82HzUF0vxvDsmzmEwbStJgx'
    b'fErAlAiXhupQMS2JJSWWKVGcGqoTfvLcIY4HYzxzx3K8To0jJ8K2+agKlpQU+93ML/PzamMP'
    b'VzdUZDRGm3zT2BHC41CpLc7m/7Ycw+fWuX11Nd/fcJAf3nAOPrfG2h+9x4ctIXS/C8O0kKbE'
    b'79V4df0FlOV5SRq2XzdO8d1Jw6JreILd7SGe3tZFT18ExevASq+xLIkE9Fw3z25qQ1cFj992'
    b'HuX5HgBShsnutiBzCn1ccXYJv3jjCEPjcQqzXEhAWJaUQsCvNjZzy0VVHDo+gmFKUqbkzQN9'
    b'rFkwi8sXlnDdL7fz8tZudL+LlGFlVEOmLL66ejY1AR/RhImuKvg9evq+YFGFnxU1+ShCMB5P'
    b'ceuje3hhazeKV8+AmCRdVUiFY/zolsV85wv1APzPhoOU5nrI9WpctrCY9sEIh3tHufH82ZiW'
    b'RBMCmo6H8XscZLt1/B4HL7zfTX1pDqV5blbPL+axd4/x8tYutBx3hvlTFfyvu3u5ZmUZQgiG'
    b'R+O88E4nSFBUgQWsWhLgT99eSZ7PyXN3rmB4PMHm/QOoHn1KpDUsC5Hl5J7nD3LZ2QFqinz4'
    b'nSq3XlLFxv297DgyyLolZWw5PMBoLEWOW0cBaOwMsbymAIC6khz+99qziSUNVtYUEk0arH/u'
    b'ILgdmNZU5hUhIGVSW+nnoZsbePCmpdx3/UKcfheq34V02Dq/9d0u7nhsj40Xwfqr6kERfDxL'
    b'kBLbsA3JXU98SLbHwfwKP79+s5lNTf2cO9fmsb40h73tQduIJxIGE3GD2uJsAMZjSbxOB/90'
    b'wRxURbD++Y8YGo6h5dh6Px1N0XlTkjQtJIKV9QX4XBopUxKTMB5PkuVysHR2HsWFHvqCMduL'
    b'nQLEtCSqR2froUFe2XucqxvKqA5kE8hx43bYHnFJZR5/auxh9fwAWvOJUQI5LgBiSYMv/243'
    b'v765gdJcD6FIgie3d4FbP+30p2jRKe81VaSlAz/50gJqi7OJJU2EAIdqM+BzqeR4dPqG0sGP'
    b'07IZEIKH3zrG1Q1lnFXgYzIAW1JSmO1CRTA8nkBrHxinriQn/XCF3355GTluBwBvH+qnt38C'
    b'1ef41KxwkiaDjCVh1X1bIe3/c5wqR376OQJ+O/UITSRBnZ55y5Lg0ni3eZijfWPUFGcTiiQY'
    b'jaXY3TbMtcsqKM/30DYwjjISSVKa58kAKMp2o6azxI0f9YOc2b3PTAIhBBKBoijI8RQrq/MJ'
    b'+O3n7GgZZnAoiqKrnJ5K2mFDUwXJ8STbWoYwLJNfbGzmwbdakVKiqwoluR56QxMoKdMiz+fk'
    b'2Z0dPLW9g5f3dHOkdwSAD9pHQFdOM7ZPJSmRMQPiBqlQjOJiLw/ctBiASDzF9/7YdDIXmHEP'
    b'QAi2tQyjKSrf+Xw9l84rIp40aekbpSTXzUgkiTZ52mOxFHvaR4gmDO69/mzCE0m6QzHQlOl1'
    b'9BOeq6kKC+ty0VXB+TX5/MeVdRRluxiLJfnSb3bx4dHglGA20z5ogqZeu654ansHw5Ek5Xke'
    b'FCHIcuskTAttsqi4qG4WiyryONwbRlME4WiS8VgKFIXPwD+WJXHpCk/c1sBZ+V4My6JzKMoD'
    b'b7TwyBtHGRtNoue6To8nHwcgAUVhOJIkZZp85aJqNFXJCM6w7KivaZp9ZW5xNqoimFeajdeh'
    b'cqh3HCwQKtPq6UykKoJI3GDZ995BVxViSYNUJMnF5wRYf/0Cfv9OO0e7xlB9+ic6Bpk2vljK'
    b'IpGS+FyqXSli526aooAAZfJ0TUuSMi2y3Tq6pmLJT0jOPo0ExBIm4zEDUwpwaORlObl7XS0f'
    b'/vByrlxegjmRnLFM/NhW6RRcsulgH7uPDadbO/Z9xTDTLQxFoKsKb+zv5XDvKIFsF0K1F/5N'
    b'OBQBpoWVMFAVwYa32vnW4414nRrP37mCpXPzMOMGyky1LgIkeBwqHofGy3u6aTkxxr7OEB+0'
    b'DSPs7VGShglA13CE2//wAbuOBZlXko3XqZLndYD52RAI0imBgGfuPJe991/OH/91BY4iL8/s'
    b'6KYvHMXr1Pn+9Qsmu2XT7yMA06Is1w6y0ViKOy+v5dpl5ZwITdgRW4AyqYeDo3ECOS5m5Th5'
    b'93Affq+TOQUeuwz8LO0+kfaASM6dncfSylzOm5OHS1cYCSc42D0KwOr5Aead5cdKGNM2sCYB'
    b'1JfYKU5dmZ/vvPAhP33tCEurCghGErh1Fc2lq/SHY6yoKWRFTSETCYOh8TgAK+fms+fwEIrQ'
    b'+JSia1oy0opqTArRtOgcjgLg1FWWV+dxpG0ExcW0iR1CsKquEICG2fnMDWQhJeT5nOxtC1KQ'
    b'7UIpzHbRE5wAIGFYuB0qFenWyd+dUwza3xDI0qSmT1YVpHXLrnknqTrgYzojEwJMwyI318VF'
    b'9UWZa7leJzkeO805HpqgPN+LUlOcRdtgBABdtfsIT+1o542PelmzsJj6ihys+PRi/lvo1KTQ'
    b'73FMa1+KIiBusG5RgGK/mz9+0EXT8XAGCMDgWIKqWT6U2uIcguMJAHa2DvHdlz6iIMvFsQEb'
    b'1J1XVEPSnNFbTEeqImwXmflK+rMiphxExo1+TMKWBegK31o7F5AEIwnueekA333xIxQh6A5O'
    b'oGsKPpeOoiqCwhwXB3vCzCny8YUlpZiWpGt4gsaOILevqWF+lR8jljojEJYlMSdSGBOpTKog'
    b'pX2NSBIjaWbWThcgNVVBRpLceEEF51bl0zYQ4Wj/OOuvms8tF80BoLEjRH2pnUErAMurCtje'
    b'OkhJrofGjhB+r4NrlpXz4u4uAH5202KQEjGdR5Wgn8KJz6WxpqGENQ0leF1269XlUFm9tJjl'
    b'K8upKsnKrNUVbOtNS0VRBEbSpKjAxY/+YREg2dzUj6IoPLmtg+pZvnSTIMKS2XkACNOypCIE'
    b'j7xzlDULApT4XfxyYwtuh8a6c0qYU+RDUxTueekAP3j2ILrfTSpdmamKwJxI8tvbG7h9dQ2G'
    b'ZaEpkxabRmc/ZqqU0p2QntAEi9a/xch4KtMYM2NJNtx9IV9sKCNpWOiqXXoeOh5mXkk221qG'
    b'iCUNrlxchmnJk12J9sEImw6e4JaLqmgbiFBfmpMWsSSWMvE4NG56+H2e2tiGnpvuCaX5qyv2'
    b'oSoiM5iYtFPllOb95LXJJpeU4NQU2oeijMcNNCEwxhP87Nal3LW2loHRGLNy3Bim3Q8VAqJJ'
    b'k4ffbuGOy2ozbUjNrp4kc4p8ZLl09rQFuaC2KDNdSaRMntzWzoW1RTx5+3KEEDz5xjG0HBdS'
    b'sXOo5q7R05X5TEiC6tJQLImRSPHArUu4a20tAN998QBXN5Rx5eLSDC+v7O1mWVUBLl3NSFGB'
    b'k6Oca8+tYNfRYYbHE+iqwoHuEIYF/7yqilf39SKBJ247j3tvOQczaWBGU6iqQHdrNiPOM3up'
    b'Lg2HR0fz6JiRJFkulZfuvoB/W1vHtpYB/rC1jevOK2PLkQGe3dmBrirs7woxGktxYW3RlAZv'
    b'RshSSly6yueXlPLU9nYAmnpH2d8VYl9nyC7Msdvq91w1n533rmZJXT7meDLjcRQFTnrGk38g'
    b'EbYXtYOUKUmOJTBiKa5eVc6hn1zBdcvs9vmyOfkkDYuntnbwzcvmsqKmkPF4ijcP9HHj+bPT'
    b'ajhNd9rWU4miCDY39dMdnOCWVVVsPtRH+9AEX2wopyDLiZSS95oHOa+qALdD5eU9Pfxi41He'
    b'bw3arlIRoCknubVPx+6NGhYSiSvHydpFAf59XS3n1xTQHZzAsiSVhb7M6T6/q5PlNQVUFvh4'
    b'4LXDXL20nOpA1szt9UmaHCL8ubGHSNzgxpWzp4xYT4Rj/Ofz+7m4vpC5gWxW1BSiCEHT8TCb'
    b'Dg2wvXWYY/0RhsaTxNO9Uo9DJeB3Mq8km4vrCvncomJK/G6ShsmO1iHeax7EtODe687GtCRS'
    b'2kV9yrR4cFMLF8+bxeLKvNOYnxbAqSBe3XecgdEYX724GtJj1vv/0sSsbBf9ozHC0RT/fc1C'
    b'3Lo2pUaXSKIJk3jKVjuPU8WlaxlhRBIpfE6daNLgQE+YEyNRHnyzle9du4BL5gUAu53/6JZj'
    b'rK4PsLgyb+Y52aeNV7c2D8ifv94kRyYSMp405Au7OqWUUn7ziQ/k+8eGM+u3tQzIH/+lSb60'
    b'uzMzSpVSZsaoI5G4/N07rbJtYEze9uj7U9Z0Do3L37x5RL55oFdKKWXzibC8/9VD8mj/2BRe'
    b'pqMZx+pqesR5YW0R5fkefr/lGOdWFXDD8rMIR5M0zM7j3Dn5mYHciZEYPcMTLK7w26JFMDgW'
    b'x+NQ8bl0/F4n4XF74O3UVXpHopTmeuzRgSW5YXklRdkuXt7TzeBonK+vqSHb7cCSM08o4RQv'
    b'NBMIS0oqC3x8+4o6guMJfrWxmf5wjJsvrAJx0iNYUtI9GMl0+YSAH/65ibeb+jP75XodDIbj'
    b'rFtcwvtHh+zvWZI5RVl0DkV44LXDzMpx8fU1c8lyOabV+Y/TGf3U4FQjHhqLs+lgH6OxJIsq'
    b'8lhUkYvPpRFJpGhsD9IwpwCv0xZsPGWiKQIt3boZHItjWva0RUpJaCLJ3vYgLf1jVBb4WLMg'
    b'gMehYVnp30ucQQJ8xj/2gKm/mRiZSLKnfZjuYBSHplBZ4KUmkI3boeJ1apkh9iTFUyaxpMHA'
    b'WILOoQj94RiWhNriLJbOzsOla1MO6kzpMwEAWxof18u+cIzWvjF6QlEmEkam3yMy1bFNuirw'
    b'exxUFHiZG8gi12sPxyW2Kp1Jm+Xj9P+8ZNC/YXj7uwAAAABJRU5ErkJggg==')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.setWindowIcon(QtGui.QIcon('orig.ico'))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(717, 519)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Input_2 = QtWidgets.QFrame(self.centralwidget)
        self.Input_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.Input_2.setFrameShape(QtWidgets.QFrame.Box)
        self.Input_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Input_2.setLineWidth(2)
        self.Input_2.setMidLineWidth(5)
        self.Input_2.setObjectName("Input_2")
        self.gridLayout = QtWidgets.QGridLayout(self.Input_2)
        self.gridLayout.setObjectName("gridLayout")
        self.table_of_contents_3 = QtWidgets.QLabel(self.Input_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.table_of_contents_3.setFont(font)
        self.table_of_contents_3.setObjectName("table_of_contents_3")
        self.gridLayout.addWidget(self.table_of_contents_3, 0, 0, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.Input_2)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout.addWidget(self.radioButton_3, 2, 0, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.Input_2)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout.addWidget(self.radioButton_4, 3, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.Input_2)
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCheckable(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.Input_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setTabletTracking(False)
        self.label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.progressBar_3 = QtWidgets.QProgressBar(self.Input_2)
        self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_3.setObjectName("progressBar_3")
        self.gridLayout.addWidget(self.progressBar_3, 3, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.Input_2)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.Input_2, 0, 0, 1, 1)
        self.func = QtWidgets.QFrame(self.centralwidget)
        self.func.setFrameShape(QtWidgets.QFrame.Box)
        self.func.setFrameShadow(QtWidgets.QFrame.Raised)
        self.func.setLineWidth(2)
        self.func.setMidLineWidth(5)
        self.func.setObjectName("func")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.func)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.func)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_2.addWidget(self.doubleSpinBox, 1, 1, 1, 2)
        self.table_of_contents_2 = QtWidgets.QLabel(self.func)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.table_of_contents_2.setFont(font)
        self.table_of_contents_2.setObjectName("table_of_contents_2")
        self.gridLayout_2.addWidget(self.table_of_contents_2, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.func)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_2.setTabletTracking(False)
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.func)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_2.addWidget(self.spinBox, 2, 4, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.func)
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 0, 3, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.func)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.progressBar_2 = QtWidgets.QProgressBar(self.func)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_2.setObjectName("progressBar_2")
        self.gridLayout_2.addWidget(self.progressBar_2, 4, 0, 1, 5)
        self.label_6 = QtWidgets.QLabel(self.func)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(self.func)
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 3, 2, 1, 3)
        self.label_5 = QtWidgets.QLabel(self.func)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 4)
        self.gridLayout_3.addWidget(self.func, 0, 1, 1, 1)
        self.Visual = QtWidgets.QTabWidget(self.centralwidget)
        self.Visual.setTabPosition(QtWidgets.QTabWidget.North)
        self.Visual.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.Visual.setIconSize(QtCore.QSize(20, 20))
        self.Visual.setElideMode(QtCore.Qt.ElideNone)
        self.Visual.setUsesScrollButtons(True)
        self.Visual.setTabBarAutoHide(True)
        self.Visual.setObjectName("Visual")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setGeometry(QtCore.QRect(10, 10, 341, 251))
        self.widget_4.setObjectName("widget_4")
        self.Visual.addTab(self.widget, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.tab_2)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout.addWidget(self.widget_2)
        self.Visual.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.Visual, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.Visual.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("A framework for search, analysis and visualization of social networks data", "A framework for search, analysis and visualization of social networks data"))
        self.table_of_contents_3.setText(_translate("MainWindow", "Блок ввода"))
        self.radioButton_3.setText(_translate("MainWindow", "Vk"))
        self.radioButton_4.setText(_translate("MainWindow", "Facebook"))
        self.pushButton_3.setText(_translate("MainWindow", "Кнопка когда выберут соц сеть "))
        self.label.setText(_translate("MainWindow", "Ввод данных->"))
        self.table_of_contents_2.setText(_translate("MainWindow", "Блок фишек"))
        self.label_2.setText(_translate("MainWindow", "выберите->"))
        self.comboBox.setItemText(0, _translate("MainWindow", "поиски всякие"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Новый элемент"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Новый элемент"))
        self.label_3.setText(_translate("MainWindow", "search time:"))
        self.label_6.setText(_translate("MainWindow", "что то еще?"))
        self.pushButton_2.setText(_translate("MainWindow", "click to make something happen"))
        self.label_5.setText(_translate("MainWindow", "number of something to search for something"))
        self.Visual.setTabText(self.Visual.indexOf(self.widget), _translate("MainWindow", "Граф"))
        self.Visual.setTabText(self.Visual.indexOf(self.tab_2), _translate("MainWindow", "Таблица"))

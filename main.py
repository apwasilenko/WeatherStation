#!/usr/bin/python3
import math
import sys
from drawWidget import myDrawWidget
from config import mysql_py
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRect, Qt, QSize, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox


class MainWindow(QWidget):
    f = None

    bd = {
        'posSensor': 't_home',
        'typeGrapch': 'sensor',
        'dateBD': mysql_py('1'),
    }


    def __init__(self, parent=None):
        """Инициализация макета окна"""
        QWidget.__init__(self, parent)
        self.setGeometry(QRect(50, 50, 400, 300))
        self.setMinimumSize(QSize(320, 340))
        self.setWindowTitle("Погодная станция")
        self.mainBox = QVBoxLayout()
        self.headerBox = QHBoxLayout()
        self.f = mysql_py('1')
        if self.f is not None:
            self.headerLb = QLabel("Показания датчиков по состоянию на  " +
                                   self.f[0]['mydatetime'].strftime("%H:%M   %d.%m.%Y г."))
        else:
            self.headerLb = QLabel("Нет данных с сервера")

        self.headerLb.setAlignment(Qt.AlignTop)
        self.headerBox.addWidget(self.headerLb, stretch=0, alignment=Qt.AlignCenter)
        self.drawBox = QHBoxLayout()
        self.drawView = QWidget()
        self.drawBox.addWidget(self.drawView)
        self.elem = QHBoxLayout()
        self.btUpdate = QPushButton("Обновить")
        self.btUpdate.clicked.connect(self.drawupdate)
        self.cbComboGrapch = QComboBox()
        self.cbComboGrapch.addItem('Дом', 't_home')
        self.cbComboGrapch.addItem('Улица', 't_street')
        self.cbComboGrapch.addItem('Котел', 't_boller')
        self.elem.addWidget(self.cbComboGrapch)
        self.cbGrapchType = QComboBox()
        self.cbGrapchType.addItem('Датчик', 'sensor')
        self.cbGrapchType.addItem('График', 'chart')
        self.elem.addWidget(self.cbGrapchType)


        self.elem.addWidget(self.btUpdate)
        self.elem.setAlignment(Qt.AlignRight)
        self.mainBox.addLayout(self.headerBox, stretch=1)
        self.mainBox.addLayout(self.drawBox, stretch=100)
        self.mainBox.addLayout(self.elem, stretch=1)
        self.setLayout(self.mainBox)

    def drawupdate(self):
        """Функция обновления данных"""
        print("Обновление")


    def paintEvent(self, event):
        """Переопределение функции отрисовки"""
        self.bd['posSensor'] = self.cbComboGrapch.currentData()
        self.bd['typeGrapch'] = self.cbGrapchType.currentData()
        print(self.cbGrapchType.currentData())
        qp = QPainter()
        qp.begin(self)
        poligon = self.drawView.geometry().getRect()
        myDrawWidget(qp, poligon, self.bd)
        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

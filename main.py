#!/usr/bin/python3

import sys

from mysql.connector import connect, Error
from datetime import datetime
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout


class MainWindow(QWidget):
    def __init__(self, parent=None):
        f = mysql_py("4")
        QWidget.__init__(self, parent)
        self.setGeometry(QRect(50, 50, 690, 530))
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Погодная станция")
        self.mainBox = QVBoxLayout()
        self.headerBox = QHBoxLayout()
        cur_date_time = datetime.now().strftime("%H:%M   %d.%m.%Y г.")
        print(type(f[0][2]))
        hometemp = f[0][2]

        self.headerLb = QLabel("Проказания датчиков по состоянию на  " + cur_date_time + "\n" + str(hometemp))
        self.headerLb.setAlignment(Qt.AlignTop)
        self.headerBox.addWidget(self.headerLb, stretch=0, alignment=Qt.AlignCenter)
        self.drawBox = QHBoxLayout()
        self.drawView = QWidget()
        self.drawBox.addWidget(self.drawView)
        self.elem = QHBoxLayout()
        self.btUpdate = QPushButton("Обновить")
        self.btUpdate.clicked.connect(self.drawupdate)
        self.elem.addWidget(self.btUpdate)
        self.elem.setAlignment(Qt.AlignRight)
        self.mainBox.addLayout(self.headerBox, stretch=1)
        self.mainBox.addLayout(self.drawBox, stretch=100)
        self.mainBox.addLayout(self.elem, stretch=1)
        self.setLayout(self.mainBox)

    def drawupdate(self):
        print("Обновление")


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()


    def drawWidget(self, qp):
        poligon = self.drawView.geometry().getRect()
        x1, y1, x2, y2 = poligon[0], poligon[1], poligon[2], poligon[3]  # координаты области рисования
        qp.setBrush(QColor(255, 255, 255))
        qp.setPen(QColor(0, 0, 255))
        qp.drawRect(x1, y1, x2, y2)
        qp.drawLine(x1, y1, x2 + x1, y2 + y1)
        for i in range(0, 350):
            myColor = QColor(i, 0, 0)
            qp.setPen(QPen(myColor, 70, cap=Qt.FlatCap))
            qp.drawArc(x1 + 50, x1 + 50, int(x2 / 2), int(x2 / 2), i * 8, (i + 1) * 8)


def mysql_py(col):
    try:
        with connect(
                host="141.8.193.236",
                user="f0659051_apwasilenko",
                password="apwasilenko",
                database="f0659051_apwasilenko",
        ) as connection:
            select_movies_query = "SELECT * FROM temperatura ORDER BY temperatura.id DESC LIMIT " + col
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query)
                result = cursor.fetchall()

            return result

    except Error as e:
        print(e)
        print("Соединение не уставновлено")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

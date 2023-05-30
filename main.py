#!/usr/bin/python3

import sys

from datetime import datetime
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(QRect(50, 50, 690, 530))
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Погодная станция")
        self.mainBox = QVBoxLayout()
        self.headerBox = QHBoxLayout()
        cur_date_time = datetime.now().strftime("%H:%M   %d.%m.%Y г.")
        self.headerLb = QLabel("Проказания датчиков по состоянию на  " + cur_date_time)
        self.headerLb.setAlignment(Qt.AlignTop)
        self.headerBox.addWidget(self.headerLb, stretch=0, alignment=Qt.AlignCenter)
        self.drawBox = QHBoxLayout()
        self.drawView = QWidget()
        self.drawBox.addWidget(self.drawView)
        self.elem = QHBoxLayout()
        self.btUpdate = QPushButton("Обновить")
        self.btUpdate.clicked.connect(self.drawUpdate)
        self.elem.addWidget(self.btUpdate)
        self.elem.setAlignment(Qt.AlignRight)
        self.mainBox.addLayout(self.headerBox, stretch=1)
        self.mainBox.addLayout(self.drawBox, stretch=100)
        self.mainBox.addLayout(self.elem, stretch=1)
        self.setLayout(self.mainBox)

    def drawUpdate(self):
        pass

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        poligon = self.drawView.geometry().getRect()
        x1, y1, x2, y2 = poligon[0], poligon[1], poligon[2], poligon[3] # координаты области рисования
        qp.setBrush(QColor(255, 255, 255))
        qp.setPen(QColor(0, 0, 255))
        qp.drawRect(x1, y1, x2, y2)
        qp.drawLine(x1, y1, x2 + x1, y2 + y1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
#!/usr/bin/python3

import sys

from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle("Погодная станция")
        self.mainBox = QVBoxLayout()
        self.drawBox = QHBoxLayout()
        self.drawView = QWidget()
        self.drawBox.addWidget(self.drawView)
        self.elem = QHBoxLayout()
        self.btUpdate = QPushButton("Обновить")
        self.btUpdate.clicked.connect(self.drawUpdate)
        self.elem.addWidget(self.btUpdate)
        self.mainBox.addLayout(self.drawBox)
        self.mainBox.addLayout(self.elem)
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
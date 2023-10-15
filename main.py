#!/usr/bin/python3
import math
import sys
import pymysql
from config import host, user, password, database
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QFont, QFontMetrics
from PyQt5.QtCore import QRect, Qt, QSize, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout


class MainWindow(QWidget):
    f = None

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(QRect(50, 50, 320, 340))
        self.setMinimumSize(QSize(320, 340))
        self.setWindowTitle("Погодная станция")
        self.mainBox = QVBoxLayout()
        self.headerBox = QHBoxLayout()
        self.f = mysql_py("1")
        if self.f is not None:
            self.headerLb = QLabel("Проказания датчиков по состоянию на  " + self.f[0]['mydatetime'].strftime("%H:%M   %d.%m.%Y г.") + "\n" + str(self.f[0]['t_home']))
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
        poligon = self.drawView.geometry().getRect()
        x1, y1, x2, y2 = poligon[0], poligon[1], poligon[2], poligon[3]  # координаты области рисования
        self.drawWidget(qp, x1, y1, x2, y2, -50, 50, self.f[0]['t_home'])
        qp.end()


    def drawWidget(self, qp, x1, y1, x2, y2, min_val, max_val, cur_val):

        center_x = int((x1 + x2) / 2)  # Центр сектора датчика по горизонтали
        center_y = int((y1 + y2) / 2)  # Центр сектора датчика по вертикали
        if center_x > center_y:  # Определяем радиус датчик по наименьшему размеру
            radius_circle = int(center_y * 0.6)
        else:
            radius_circle = int(center_x * 0.6)
        sec_thick = int(radius_circle / 5)  # Толщина сектора

        # Рисуем шкалу датчика
        for i in range(0, 255):  # переход света от синего к зеленому
            myColor = QColor(0, i, 255 - i)
            qp.setPen(QPen(myColor, sec_thick, cap=Qt.FlatCap))
            qp.drawArc(center_x - radius_circle, center_y - radius_circle, radius_circle * 2, radius_circle * 2, int(3600 - i * 135 / 255 * 16), int(135 / 255 + 1) * 16)
        for i in range(0, 255):  # переход света от зеленого к красному
            myColor = QColor(i, 255 - i, 0)
            qp.setPen(QPen(myColor, sec_thick, cap=Qt.FlatCap))
            qp.drawArc(center_x - radius_circle, center_y - radius_circle, radius_circle * 2, radius_circle * 2, int(1440 - i * 135 / 255 * 16), int(135 / 255 + 1) * 16)

        for i in range(0, int((max_val - min_val)/10)+1):  # рисуем метки на шкале
            myColor = QColor(0, 0, 0)
            qp.setPen(QPen(myColor, sec_thick * 1.1, cap=Qt.FlatCap))
            qp.drawArc(center_x - radius_circle, center_y - radius_circle, radius_circle * 2, radius_circle * 2, int(3584 - i * 270 / int((max_val - min_val)/10) * 16), 2 * 16)

        for i in range(0, int((max_val - min_val)/ 10) +1):
            myColor = QColor(0, 0, 0)
            qp.setPen(QPen(myColor, sec_thick * 1.1, cap=Qt.FlatCap))
            qp.setFont(QFont("Tahoma", int(radius_circle/10)))
            size_label = qp.boundingRect(QRect(), 0, str(min_val + i*10))
            delta_x = int(size_label.width()/2)
            delta_y = int(size_label.height()/2)
            position_label = QPoint(int(center_x + math.cos(math.pi*3/4 + ((min_val + i*10) - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle*1.3 - delta_x),
                        int(center_y + math.sin(math.pi*3/4 + ((min_val + i*10) - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle*1.3 + delta_y)
                                  )
            qp.drawText(position_label, str(min_val + i*10))



        # Рисуем стрелку
        points = QPolygon([
            QPoint(int(center_x + math.cos(math.pi*1/4 + (cur_val - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle/10),
                   int(center_y + math.sin(math.pi*1/4 + (cur_val - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle/10)),

            QPoint(int(center_x + math.cos(math.pi*3/4 + (cur_val - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle),
                   int(center_y + math.sin(math.pi*3/4 + (cur_val - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle)),

            QPoint(int(center_x + math.cos(math.pi*5/4 + (cur_val - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle/10),
                   int(center_y + math.sin(math.pi*5/4 + (cur_val - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle/10)),

            QPoint(int(center_x + math.cos(math.pi*1/4 + (cur_val - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle/10),
                   int(center_y + math.sin(math.pi*1/4 + (cur_val - min_val)/(max_val-min_val)*6/4*math.pi)*radius_circle/10)),
        ])

        qp.setBrush(QColor(255, 0, 0))
        myColor = QColor(255, 0, 0)
        qp.setPen(QPen(myColor, 1, cap=Qt.FlatCap))
        qp.drawPolygon(points)

        qp.setBrush(QColor(0, 0, 0))
        myColor = QColor(0, 0, 0)
        qp.setPen(QPen(myColor, 1, cap=Qt.FlatCap))
        qp.drawEllipse(center_x - int(radius_circle/8), center_y - int(radius_circle/8), int(radius_circle/4), int(radius_circle/4))

        #Выводим текущее значение
        myColor = QColor(0, 0, 0)
        qp.setPen(QPen(myColor, sec_thick * 1.1, cap=Qt.FlatCap))
        qp.setFont(QFont("Tahoma", int(radius_circle / 10)))
        size_label = qp.boundingRect(QRect(), 0, str(cur_val))
        delta_x = int(size_label.width() / 2)
        position_label = QPoint(int(center_x - delta_x), int(center_y + radius_circle/2 - delta_y))
        qp.drawText(position_label, str(cur_val))

def mysql_py(col):
    resultat = None
    #print("Соединение устанавливается")
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
        )
        # print("Соединение установлено")
        # print('-' * 20, '#' * 20, '-' * 20)

        try:
            with connection.cursor() as cursor:
                selectqyery = "SELECT * FROM temperatura ORDER BY temperatura.id DESC LIMIT " + str(col)
                cursor.execute(selectqyery)
                rows = cursor.fetchall()

                #print(rows)
                resultat = rows
                #print('#' * 20)
                #for row in rows:
                #    print(row)
        finally:
            connection.close()
    except Exception as ex:
        print("Соединение не уставновлено")
        print(ex)
    print(resultat)
    return resultat


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

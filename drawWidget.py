import math
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QFont
from PyQt5.QtCore import QRect, Qt, QPoint


def myDrawWidget(qp, poligon, bd):
    """Функция отрицовки """
    if bd['typeGrapch'] == 'sensor':
        drawSensor(qp, poligon, bd)
    else:
        drawChart(qp, poligon, bd)


def drawSensor(qp: QPainter, poligon : QRect, bd):
    """Функция отрисовывает датчик температуры"""
    if bd['posSensor'] == 't_home':
        min_val = 16
        max_val = 32
        cur_val = bd['dateBD'][0]['t_home']
    if bd['posSensor'] == 't_street':
        min_val = -50
        max_val = 50
        cur_val = bd['dateBD'][0]['t_street']
    if bd['posSensor'] == 't_boller':
        min_val = 0
        max_val = 100
        cur_val = bd['dateBD'][0]['t_boller']
    x1, y1, x2, y2 = poligon[0], poligon[1], poligon[2], poligon[3]  # координаты области рисования
    center_x = int(x1 + x2 / 2)  # Центр сектора датчика по горизонтали
    center_y = int(y1 + y2 / 2)  # Центр сектора датчика по вертикали
    if center_x > center_y:  # Определяем радиус датчик по наименьшему размеру
        radius_circle = int(center_y * 0.6)
    else:
        radius_circle = int(center_x * 0.6)
    sec_thick = int(radius_circle / 5)  # Толщина сектора
    # Рисуем шкалу датчика
    for i in range(0, 255):  # переход света от синего к зеленому
        myColor = QColor(0, i, 255 - i)
        qp.setPen(QPen(myColor, sec_thick, cap=Qt.FlatCap))
        qp.drawArc(center_x - radius_circle, center_y - radius_circle, radius_circle * 2, radius_circle * 2,
                   int(3600 - i * 135 / 255 * 16), int(135 / 255 + 1) * 16)
    for i in range(0, 255):  # переход света от зеленого к красному
        myColor = QColor(i, 255 - i, 0)
        qp.setPen(QPen(myColor, sec_thick, cap=Qt.FlatCap))
        qp.drawArc(center_x - radius_circle, center_y - radius_circle, radius_circle * 2, radius_circle * 2,
                   int(1440 - i * 135 / 255 * 16), int(135 / 255 + 1) * 16)
    for i in range(min_val, max_val):  # Выводим подписи
        if (i % 5 == 0) or (i % 10 == 0) or (i == min_val) or (i == max_val):
            myColor = QColor(0, 0, 0)
            if (i % 10 == 0) or (i == min_val) or (i == max_val):
                qp.setPen(QPen(myColor, sec_thick * 0.2, cap=Qt.FlatCap))
                qp.setFont(QFont("Tahoma", int(radius_circle / 10)))
            else:
                qp.setPen(QPen(myColor, sec_thick * 0.1, cap=Qt.FlatCap))
                qp.setFont(QFont("Tahoma", int(radius_circle / 15)))
            size_signature = qp.boundingRect(QRect(), 0, str(i))
            delta_x = int(size_signature.width() / 2)
            delta_y = int(size_signature.height() / 2)
            position_signature = QPoint(int(center_x + math.cos(math.pi * 3 / 4 + ((i) - min_val) / (
                    max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 1.3 - delta_x),
                                        int(center_y + math.sin(math.pi * 3 / 4 + ((i) - min_val) / (
                                                max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 1.3 + delta_y)
                                        )
            position1_label = QPoint(int(center_x + math.cos(
                math.pi * 3 / 4 + ((i) - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 1.1),
                                     int(center_y + math.sin(math.pi * 3 / 4 + ((i) - min_val) / (
                                             max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 1.1)
                                     )
            position2_label = QPoint(int(center_x + math.cos(
                math.pi * 3 / 4 + ((i) - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 0.9),
                                     int(center_y + math.sin(math.pi * 3 / 4 + ((i) - min_val) / (
                                             max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 0.9)
                                     )
            qp.drawLine(position1_label, position2_label)
            qp.drawText(position_signature, str(i))

        if (i % 5 != 0) and (i % 10 != 0) and (max_val - min_val < 20):
            myColor = QColor(0, 0, 0)
            qp.setPen(QPen(myColor, sec_thick * 0.05, cap=Qt.FlatCap))
            position1_label = QPoint(int(center_x + math.cos(
                math.pi * 3 / 4 + ((i) - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 1.1),
                                     int(center_y + math.sin(math.pi * 3 / 4 + ((i) - min_val) / (
                                             max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 1.1)
                                     )
            position2_label = QPoint(int(center_x + math.cos(
                math.pi * 3 / 4 + ((i) - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 0.9),
                                     int(center_y + math.sin(math.pi * 3 / 4 + ((i) - min_val) / (
                                             max_val - min_val) * 6 / 4 * math.pi) * radius_circle * 0.9)
                                     )
            qp.drawLine(position1_label, position2_label)
    # Рисуем стрелку
    points = QPolygon([
        QPoint(int(center_x + math.cos(
            math.pi * 1 / 4 + (cur_val - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle / 10),
               int(center_y + math.sin(math.pi * 1 / 4 + (cur_val - min_val) / (
                       max_val - min_val) * 6 / 4 * math.pi) * radius_circle / 10)),
        QPoint(int(center_x + math.cos(
            math.pi * 3 / 4 + (cur_val - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle),
               int(center_y + math.sin(
                   math.pi * 3 / 4 + (cur_val - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle)),
        QPoint(int(center_x + math.cos(
            math.pi * 5 / 4 + (cur_val - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle / 10),
               int(center_y + math.sin(math.pi * 5 / 4 + (cur_val - min_val) / (
                       max_val - min_val) * 6 / 4 * math.pi) * radius_circle / 10)),
        QPoint(int(center_x + math.cos(
            math.pi * 1 / 4 + (cur_val - min_val) / (max_val - min_val) * 6 / 4 * math.pi) * radius_circle / 10),
               int(center_y + math.sin(math.pi * 1 / 4 + (cur_val - min_val) / (
                       max_val - min_val) * 6 / 4 * math.pi) * radius_circle / 10)),
    ])
    qp.setBrush(QColor(255, 0, 0))
    myColor = QColor(255, 0, 0)
    qp.setPen(QPen(myColor, 1, cap=Qt.FlatCap))
    qp.drawPolygon(points)
    qp.setBrush(QColor(0, 0, 0))
    myColor = QColor(0, 0, 0)
    qp.setPen(QPen(myColor, 1, cap=Qt.FlatCap))
    qp.drawEllipse(center_x - int(radius_circle / 8), center_y - int(radius_circle / 8), int(radius_circle / 4),
                   int(radius_circle / 4))
    # Выводим текущее значение
    myColor = QColor(0, 0, 0)
    qp.setPen(QPen(myColor, sec_thick * 1.1, cap=Qt.FlatCap))
    qp.setFont(QFont("Tahoma", int(radius_circle / 10)))
    size_signature = qp.boundingRect(QRect(), 0, str(cur_val))
    delta_x = int(size_signature.width() / 2)
    delta_y = int(size_signature.height() / 2)
    position_signature = QPoint(int(center_x - delta_x), int(center_y + radius_circle / 2 - delta_y))
    qp.drawText(position_signature, str(cur_val))


def drawChart(qp: QPainter, poligon : QRect, bd):
    x1, y1, x2, y2 = poligon[0], poligon[1], poligon[2], poligon[3]
    myColor = QColor(225, 225, 225)
    qp.setPen(QPen(myColor, 1, cap=Qt.FlatCap))
    qp.setBrush(myColor)
    qp.drawRect(x1, y1, x2, y2)
    qp.setFont(QFont("Tahoma", int(y2 / 30)))
    size_signature = qp.boundingRect(QRect(), 0, str('-50'))
    delta_x = int(size_signature.width())
    delta_y = int(size_signature.height())
    myColor = QColor(0, 0, 0)
    qp.setPen(QPen(myColor, 3, cap=Qt.FlatCap))
    qp.drawLine(int(x1 + delta_x * 1.75), y1 + y2 - delta_y*2, x2 + x1, y1 + y2 - delta_y*2)
    position_signature = QPoint(int(x1 + delta_x/2), int(y1 + y2 - delta_y * 1.75))
    qp.drawText(position_signature, str('-50'))
    size_signature = qp.boundingRect(QRect(), 0, str(bd['dateBD'][0]['mydatetime'].strftime("%H:%M")))
    delta_x = int(size_signature.width())
    delta_y = int(size_signature.height())
    position_signature = QPoint(int(x1 + delta_x/2), int(y1 + y2 - delta_y))
    qp.drawText(position_signature, str(bd['dateBD'][0]['mydatetime'].strftime("%H:%M")))
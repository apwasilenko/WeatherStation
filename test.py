# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

arcreading = 0
adder = .1


# creating a Gauge class
class Gauge(QMainWindow):

    # constructor
    def __init__(self):
        super().__init__()

        timer = QTimer(self)  # create a timer object
        timer.timeout.connect(self.update)  # add action to the timer, update the whole code
        timer.start(0)  # update cycle in milliseconds

        self.setGeometry(200, 200, 600, 600)  # window location and size
        self.setStyleSheet("background : yellow;")  # background color

    # -----------------------
    # method for paint event
    # -----------------------
    def paintEvent(self, event):
        global arcreading
        global adder
        # print('x')
        kanvasx = 50  # binding box origin: x
        kanvasy = 50  # binding box origin: y
        kanvasheight = 150  # binding box height
        kanvaswidth = 150  # binding box width
        arcsize = 270  # arc angle between start and end.
        arcwidth = 70  # arc width

        painter = QPainter(self)  # create a painter object
        painter.setRenderHint(QPainter.Antialiasing)  # tune up painter
        painter.setPen(QPen(Qt.green, arcwidth, cap=Qt.FlatCap))  # set color and width

        # ---------- the following lines simulate sensor reading. -----------
        if arcreading > arcsize or arcreading < 0:  # variable to make arc move
            adder = -adder  # arcreading corresponds to the
            # value to be indicated by the arc.
        arcreading = arcreading + adder
        # --------------------- end simulation ------------------------------
        # print(arcreading)

        # drawArc syntax:
        #       drawArc(x_axis, y_axis, width, length, startAngle, spanAngle)
        painter.drawArc(kanvasx, kanvasy,  # binding box: x0, y0, pixels
                        kanvasheight + arcwidth,  # binding box: height
                        kanvaswidth + arcwidth,  # binding box: width
                        int((arcsize + (180 - arcsize) / 2) * 16),  # arc start point, degrees (?)
                        int(-arcreading * 16))  # arc span

        painter.end()  # end painter

    # Driver code


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # creating a Gauge object
    win = Gauge()
    # show
    win.show()
    exit(app.exec_())

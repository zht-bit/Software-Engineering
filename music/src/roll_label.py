from PyQt5.QtGui import QPainter,QColor,QFont
from PyQt5.QtCore import QTimer,QRect,Qt
from PyQt5.QtWidgets import QLabel


class nameLabel(QLabel):
    def __init__(self, parent=None):
        super(nameLabel, self).__init__(parent)
        self.txt = ""
        self.newX = 0
        self.t = QTimer()
        self.font = QFont("华文新魏")
        self.t.timeout.connect(self.changeTxtPosition)

    def changeTxtPosition(self):
        if not self.parent().isVisible():
            self.t.stop()
            self.newX = 0
            return
        if self.textRect.width() + self.newX > 0:
            self.newX -= 5
        else:
            self.newX = self.width()
        self.update()

    def setText(self, s):
        self.txt = s
        self.newX = 0
        self.update()

    def enterEvent(self, event):
        self.t.start(150)

    def leaveEvent(self, event):
        # 鼠标离开则停止滚动并复位
        self.t.stop()
        self.newX = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)
        painter.setPen(QColor('transparent'))
        self.textRect = painter.drawText(
            QRect(0, 0, self.width(), self.height()), Qt.AlignHCenter | Qt.AlignVCenter, self.txt)

        if self.textRect.width() > self.width():
            painter.setPen(QColor(255, 255, 255, 255))  # 白色
            painter.drawText(QRect(self.newX, 0, self.textRect.width(),
                             self.height()), Qt.AlignLeft | Qt.AlignVCenter, self.txt)
        else:
            painter.setPen(QColor(255, 255, 255, 255))  # 白色
            self.textRect = painter.drawText(
                QRect(0, 0, self.width(), self.height()), Qt.AlignLeft | Qt.AlignVCenter, self.txt)
            self.t.stop()

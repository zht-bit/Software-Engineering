from PyQt5.QtGui import QPainter,QColor,QFont
from PyQt5.QtCore import QTimer,QRect,Qt
from PyQt5.QtWidgets import QLabel

class nameLabel_auto(QLabel):
    def __init__(self, parent=None):
        super(nameLabel_auto, self).__init__(parent)
        self.txt = ""
        self.newX = 10
        self.t = QTimer()
        self.font = QFont("华文新魏")
        self.t.timeout.connect(self.changeTxtPosition)

    def changeTxtPosition(self):
        # 如果parent不可见，则停止滚动，复位
        if not self.parent().isVisible():
            self.t.stop()
            self.newX = 10
            return
        if self.textRect.width() + self.newX > 0:
            # 每次向前滚动5像素
            self.newX -= 5
        else:
            self.newX = self.width()
        self.update()

    def setText(self, s):
        self.txt = s
        # 滚动起始位置设置为10,留下视觉缓冲
        # 以免出现 “没注意到第一个字是什么” 的情况
        self.newX = 10
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)
        painter.setPen(QColor('transparent'))
        # 以透明色绘制文字，来取得绘制后的文字宽度
        self.textRect = painter.drawText(
            QRect(0, 0, self.width(), self.height()), Qt.AlignHCenter | Qt.AlignVCenter, self.txt)

        if self.textRect.width() > self.width():
            # 如果绘制文本宽度大于控件显示宽度，准备滚动：
            painter.setPen(QColor(255, 255, 255, 255))  # 白色
            painter.drawText(QRect(self.newX, 0, self.textRect.width(
            ), self.height()), Qt.AlignLeft | Qt.AlignVCenter, self.txt)
            # 每150ms毫秒滚动一次
            self.t.start(100)
        else:
            # 如果绘制文本宽度小于控件宽度，不需要滚动，文本居中对齐
            painter.setPen(QColor(255, 255, 255, 255))  # 白色
            self.textRect = painter.drawText(
                QRect(0, 0, self.width(), self.height()), Qt.AlignHCenter | Qt.AlignVCenter, self.txt)
            self.t.stop()

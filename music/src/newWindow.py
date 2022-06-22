import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import qtawesome
from roll_label import nameLabel
from down_load import song_download

# class Main(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("主窗口")
#         button = QtWidgets.QPushButton("弹出子窗", self)
#         button.clicked.connect(self.show_child)
#         self.child_window = ChildWindow()

#     def show_child(self):
#         self.child_window.show()


class ChildWindow(QtWidgets.QWidget):
    def __init__(self,text):
        super().__init__()
        self.init_ui(text)

    def init_ui(self,text):
        self.setFixedSize(600, 400)
        self.selectSong = ""
        self.finish_down = False
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.top_widget = QtWidgets.QWidget()  # 创建上侧部件
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QGridLayout()  # 设置上侧部件布局为网格
        self.top_widget.setLayout(self.top_layout)  # 创建上侧部件的网格布局层

        self.body_widget = QtWidgets.QWidget()  # 创建主体部件
        self.body_widget.setObjectName('body_widget')
        self.body_layout = QtWidgets.QGridLayout()
        self.body_widget.setLayout(self.body_layout)  # 设置主体部件布局为网格

        self.main_layout.addWidget(
            self.top_widget, 0, 0, 1, 10)  # 上侧部件在第0行第0列，占1行10列
        self.main_layout.addWidget(
            self.body_widget, 1, 0, 12, 10)  # 下侧部件在第1行第0列，占12行10列

        # self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.top_close = QtWidgets.QPushButton(
            qtawesome.icon('msc.chrome-close', color='white'), "")

        self.top_close.clicked.connect(self.close_window)  # 关联
        self.top_layout.addWidget(self.top_close, 0, 9, 1, 1)
        self.top_close.setFixedSize(20, 20)  # 设置关闭按钮的大小
        self.top_close.setStyleSheet(
            '''QPushButton{background:#15375a;border-radius:5px;}QPushButton:hover{background:#436ba9;}''')

        # 软件名字
        self.top_label_1 = QtWidgets.QLabel("'{} '搜索结果...".format(text))
        self.top_label_1.setFont(QtGui.QFont("华文新魏", 14))
        self.top_label_1.setStyleSheet("color:white")
        self.top_label_1.setObjectName('top_label')
        self.top_layout.addWidget(self.top_label_1, 0, 1, 1, 1)
        # 本地歌曲列表部件,滚动条
        self.left_localsong_table_widget = QtWidgets.QWidget()
        self.left_localsong_table_widget.setObjectName(
            "left_localsong_table_widget")
        self.left_localsong_table_layout = QtWidgets.QGridLayout()
        self.left_localsong_table_widget.setLayout(
            self.left_localsong_table_layout)

        self.body_layout.addWidget(
            self.left_localsong_table_widget, 0, 0)

        # 创建滚动区域,显示音乐列表
        self.music_list = QtWidgets.QListWidget()
        self.music_list.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.left_localsong_table_layout.addWidget(self.music_list)
        self.songList = []
        self.music_list.itemDoubleClicked.connect(self.down_fun)
        self.left_localsong_table_widget.setStyleSheet(
            '''
                background-color:transparent
            '''
        )
        self.music_list.setStyleSheet(
            '''
            QListWidget:item
            {
                color:white;
                height:40px;
                padding-left:20px;
            }
            QListWidget:item:hover
            {
                color:#78d4fc;
            }
            QListWidget:item:selected:active
            {
                color:#4583b4;
            }
            '''
        )

        self.top_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#top_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#top_widget{
            background:#15375a;
            border-top:0px solid white;
            border-bottom:0px solid white;
            border-left:0px solid white;
            border-top-left-radius:10px;
            border-top-right-radius:10px;
            }
        ''')

        self.body_widget.setStyleSheet('''
            QWidget#body_widget{
                color:#232C51;
                border-image:url(./image/b01.jpg);
                border-top:0px solid darkGray;
                border-bottom:0px solid darkGray;
                border-right:0px solid darkGray;
                border-bottom-left-radius:10px;
                border-bottom-right-radius:10px;
            }
        ''')

        self.setWindowOpacity(1.0)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)
    # 关闭按钮动作函数

    def close_window(self):
        self.close()

    # 搜索数据，显示音乐列表
    def showMusic_List(self):
        for song in self.songList:
            item_wight = QtWidgets.QWidget()
            item_wight.setStyleSheet("color:white")
            layout_item = QtWidgets.QGridLayout()
            name_t = song[1] + " - " + song[0]
            qlabelname = nameLabel()
            qlabelname.setText(name_t)
            layout_item.addWidget(qlabelname, 0, 0, 1, 9)  # 歌名
            # down_load_btn = QtWidgets.QPushButton(
            #     qtawesome.icon('fa.cloud-download', color='white'), "")
            # down_load_btn.setStyleSheet(
            #     '''QPushButton{background:transparent;}QPushButton:hover{background:transparent;}''')
            # layout_item.addWidget(down_load_btn, 0, 9, 1, 1)
            item_wight.setLayout(layout_item)
            item = QtWidgets.QListWidgetItem()
            self.music_list.addItem(item)
            self.music_list.setItemWidget(item, item_wight)
        self.music_list.setCurrentRow(0)

    def down_fun(self):
        TheSong_index = self.music_list.currentRow()
        self.selectSong = song_download(TheSong_index, self.songList)
        self.close_window()

    def setsongList(self, songList):
        self.songList = songList

# # 运行主窗口
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = Main()
#     window.show()
#     sys.exit(app.exec_())

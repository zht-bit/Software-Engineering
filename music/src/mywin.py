# -*- coding: utf-8 -*-
import random
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import qtawesome
import time
import os
import sys
from mutagen.mp3 import MP3
from roll_label import nameLabel
from roll_label_auto import nameLabel_auto
from down_load import get_Search_Music_name
from newWindow import ChildWindow


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.TheLocalList = []
        self.TheSongName = "未选中歌曲"
        self.cur_path = './data/'
        self.song_formats = ['mp3', 'm4a', 'flac', 'wav', 'ogg']
        self.old_volume_value = 50
        self.player = QtMultimedia.QMediaPlayer()

        self.setFixedSize(1024, 600)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.is_pause = True
        self.is_switching = False

        self.top_widget = QtWidgets.QWidget()  # 创建上侧部件
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QGridLayout()  # 设置上侧部件布局为网格
        self.top_widget.setLayout(self.top_layout)  # 创建上侧部件的网格布局层

        self.body_widget = QtWidgets.QWidget()  # 创建主体部件
        self.body_widget.setObjectName('body_widget')
        self.body_layout = QtWidgets.QGridLayout()
        self.body_widget.setLayout(self.body_layout)  # 设置主体部件布局为网格

        self.left_localsong_widget = QtWidgets.QWidget()  # 创建左侧音乐列表部件
        self.left_localsong_widget.setObjectName('left_localsong_widget')
        self.left_localsong_layout = QtWidgets.QGridLayout()
        self.left_localsong_widget.setLayout(self.left_localsong_layout)

        self.right_play_widget = QtWidgets.QWidget()  # 创建右侧音乐播放部件
        self.right_play_widget.setObjectName('right_play_widget')
        self.right_play_layout = QtWidgets.QGridLayout()
        self.right_play_widget.setLayout(self.right_play_layout)

        self.right_lyrics_widget = QtWidgets.QWidget()  # 创建右上侧歌词播放部件
        self.right_lyrics_widget.setObjectName('right_lyrics_widget')
        self.right_lyrics_layout = QtWidgets.QGridLayout()
        self.right_lyrics_widget.setLayout(self.right_lyrics_layout)

        self.right_control_widget = QtWidgets.QWidget()  # 创建右下侧播放控制部件
        self.right_control_widget.setObjectName('right_control_widget')
        self.right_control_layout = QtWidgets.QGridLayout()
        self.right_control_widget.setLayout(self.right_control_layout)

        self.main_layout.addWidget(
            self.top_widget, 0, 0, 1, 10)  # 上侧部件在第0行第0列，占1行10列
        self.main_layout.addWidget(
            self.body_widget, 1, 0, 12, 10)  # 下侧部件在第1行第0列，占12行10列

        self.body_layout.addWidget(
            self.left_localsong_widget, 0, 0, 12, 5)    # 左侧部件在第0行第0列，占12行4列
        self.body_layout.addWidget(
            self.right_play_widget, 0, 5, 12, 5)

        self.right_play_layout.addWidget(
            self.right_lyrics_widget, 0, 0, 10, 6)
        self.right_play_layout.addWidget(
            self.right_control_widget, 10, 0, 2, 6)

        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # self.top_close = QtWidgets.QPushButton("") # 关闭按钮
        self.top_close = QtWidgets.QPushButton(
            qtawesome.icon('msc.chrome-close', color='white'), "")
        # self.top_max = QtWidgets.QPushButton("") # 最大化按钮
        self.top_max = QtWidgets.QPushButton(
            qtawesome.icon('msc.chrome-maximize', color='white'), "")
        # self.top_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.top_mini = QtWidgets.QPushButton(
            qtawesome.icon('msc.chrome-minimize', color='white'), "")
        self.top_close.clicked.connect(self.close_window)  # 关联
        self.top_mini.clicked.connect(self.mini_window)  # 关联
        self.top_max.clicked.connect(self.max_window)  # 关联
        self.top_layout.addWidget(self.top_mini, 0, 7, 1, 1)
        self.top_layout.addWidget(self.top_max, 0, 8, 1, 1)
        self.top_layout.addWidget(self.top_close, 0, 9, 1, 1)
        self.top_close.setFixedSize(20, 20)  # 设置关闭按钮的大小
        self.top_max.setFixedSize(20, 20)  # 设置按钮大小
        self.top_mini.setFixedSize(20, 20)  # 设置最小化按钮大小
        self.top_close.setStyleSheet(
            '''QPushButton{background:#4583b4;border-radius:5px;}QPushButton:hover{background:#436ba9;}''')
        self.top_max.setStyleSheet(
            '''QPushButton{background:#4583b4;border-radius:5px;}QPushButton:hover{background:#436ba9;}''')
        self.top_mini.setStyleSheet(
            '''QPushButton{background:#4583b4;border-radius:5px;}QPushButton:hover{background:#436ba9;}''')

        # 软件名字
        self.top_label_1 = QtWidgets.QLabel("鸣")
        self.top_label_1.setFont(QtGui.QFont("方正藏体简体", 16))
        self.top_label_1.setStyleSheet("color:white")
        self.top_label_1.setObjectName('top_label')
        self.top_layout.addWidget(self.top_label_1, 0, 1, 1, 1)

        self.search_btn = QtWidgets.QPushButton(qtawesome.icon(
                'fa.search', color='#dc8576'),"搜索")
        self.search_btn.setFlat(True)
        self.search_btn.clicked.connect(self.getMessage)

        self.left_bar_widget_search_input = QtWidgets.QLineEdit()
        self.left_bar_widget_search_input.setPlaceholderText(
            "输入歌手或歌曲，点击搜索按钮进行搜索")

        self.left_localsong_lable = QtWidgets.QLabel("本地歌曲")
        self.left_localsong_lable.setStyleSheet("color:#f5e5f8")
        self.left_localsong_lable.setFont(QtGui.QFont("华文新魏", 14))
        self.left_localsong_lable.setObjectName('right_lable')

        # 本地歌曲列表部件,滚动条
        self.left_localsong_table_widget = QtWidgets.QWidget()
        self.left_localsong_table_widget.setObjectName(
            "left_localsong_table_widget")
        self.left_localsong_table_layout = QtWidgets.QGridLayout()
        self.left_localsong_table_widget.setLayout(
            self.left_localsong_table_layout)

        self.left_localsong_layout.addWidget(self.search_btn, 0,8,1,2)
        self.left_localsong_layout.addWidget(
            self.left_bar_widget_search_input, 0, 0, 1, 8)
        self.left_localsong_layout.addWidget(self.left_localsong_lable, 1, 0,1,10)
        self.left_localsong_layout.addWidget(
            self.left_localsong_table_widget, 2, 0, 10, 10)

        # 创建滚动区域,显示音乐列表
        self.music_list = QtWidgets.QListWidget()
        self.music_list.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.music_list.itemDoubleClicked.connect(self.doubleClicked)
        self.showMusic_List()
        self.left_localsong_table_layout.addWidget(self.music_list)
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

        self.cur_song_name_lable = nameLabel_auto()
        self.cur_song_name_lable.setText(self.TheSongName)
        self.cur_song_name_lable.setStyleSheet("color:white")
        self.cur_song_name_lable.setFont(QtGui.QFont("华文新魏", 14))
        self.cur_song_name_lable.setObjectName('right_lable')
        # 设置Label大小
        # self.cur_song_name_lable.setFixedWidth(350)
        self.cur_song_name_lable.setFixedHeight(50)

        # gif图片
        self.play_label_gif = QtWidgets.QLabel()
        self.play_label_gif.setFixedWidth(300)
        self.play_label_gif.setFixedHeight(300)
        # self.play_movie = QtGui.QMovie('./image/p{}.jpg'.format(random.randint(1, 6)))
        self.play_movie = QtGui.QMovie('./image/010.gif')
        # self.play_movie = QtGui.QMovie('./image/p6.jpg')
        self.play_movie.setSpeed(150)
        self.play_label_gif.setMovie(self.play_movie)
        self.play_label_gif.setAlignment(QtCore.Qt.AlignCenter)
        self.play_movie.start()
        self.play_movie.setPaused(True)

        self.right_process_bar = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.right_process_bar.sliderMoved[int].connect(
            lambda: self.player.setPosition(self.right_process_bar.value()))
        self.timeLabel1 = QtWidgets.QLabel('00:00')
        self.timeLabel2 = QtWidgets.QLabel('00:00')
        self.timeLabel1.setStyleSheet("color:white")
        self.timeLabel2.setStyleSheet("color:white")
        self.right_process_bar.setStyleSheet(
            '''
            QSlider
            {
                border-style:outset;
                border-radius:10px;
                height:10px;
                width:50px;
            }
            QSlider:groove:horizontal
            {
                height:5px;
                background:rgb(142,139,130);
                border-radius:3px;
            }
            QSlider:handle:horizontal
            {
                background-color:rgb(158,158,158);
                width:6px;
                height:6px;
                border-radius:1px;
                border:2px solid rgb(255,255,255);
            }
            QSlider:sub-page:horizontal
            {
                background-color:#4583b4;
                border-radius:3px;
            }
            QSlider:handle:horizontal:!enabled
            {
                width:5px;
                height:5px;
                border-radius:5px;
            }
            '''
        )

        # --播放模式
        self.console_button_4 = QtWidgets.QComboBox()
        self.console_button_4.setStyleSheet('''
            QComboBox{
                color:white;
                outline: 0px;
                font-family: "华文新魏";
                font-size:14px;
                background-color:transparent;
            }
            /* 点击QComboBox后的已选中项的样式 */
            QComboBox:on {
                background-color: transparent;
            }
            /* 下拉展开后，整个下拉窗体样式 */
            QComboBox QAbstractItemView {
                color: white;
                outline: 0px;
                background-color:#191a3b;
                selection-color: #3377FF;/*下拉框选中项字体颜色*/
                selection-background-color:rgba(140, 101, 146,50);/* 下拉框选中项的背景色 */
            }
            /* 下拉框箭头样式 */
            QComboBox::drop-down {
                border-style: none;
            }


        ''')

        self.Playmode = [
            {"Icon": "ph.repeat-bold", "name": "顺序播放"},
            {"Icon": "ph.repeat-once-bold", "name": "单曲循环"},
            {"Icon": "ei.random", "name": "随机播放"},
        ]
        for mode in self.Playmode:
            self.console_button_4.addItem(qtawesome.icon(
                mode["Icon"], color='#4583b4'), mode["name"])

        self.timer = QtCore.QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.playByMode)

        self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

        self.console_button_1 = QtWidgets.QPushButton(
            qtawesome.icon('fa5s.step-backward', color='#4583b4'), "")
        self.console_button_2 = QtWidgets.QPushButton(
            qtawesome.icon('fa5s.step-forward', color='#4583b4'), "")
        self.console_button_3 = QtWidgets.QPushButton(
            qtawesome.icon('fa5s.play-circle', color='#4583b4', font=18), "")
        self.console_button_5 = QtWidgets.QPushButton(
            qtawesome.icon('fa5s.volume-down', color='#4583b4'), "")  # fa5s.volume-mute
        self.console_button_3.setIconSize(QtCore.QSize(30, 30))
        self.console_button_3.clicked.connect(self.playMusic)  # 关联
        self.console_button_1.clicked.connect(self.previewMusic)    # 关联
        self.console_button_2.clicked.connect(self.nextMusic)  # 关联
        self.console_button_5.clicked.connect(self.on_btnSound_clicked)  # 关联
        self.right_playconsole_widget.setStyleSheet('''
            QPushButton{
                border:none;
                color:gray;
                font-size:12px;
                height:40px;
                padding-left:5px;
                padding-right:5px;
                text-align:left;
            }
            QPushButton:hover{
                border-radius:10px;
                background-color:rgba(130, 117, 160, 100);
            }
        ''')

        self.volume_bar = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volume_bar.setValue(50)
        self.volume_bar.sliderMoved[int].connect(
            lambda: self.on_sliderVolumn_valueChanged(self.volume_bar.value()))  # 关联
        self.volume_bar.setStyleSheet(
            '''
            QSlider
            {
                border-style:outset;
                border-radius:10px;
                height:10px;
            }
            QSlider:groove:horizontal
            {
                height:5px;
                background:rgb(142,139,130);
                border-radius:3px;
            }
            QSlider:handle:horizontal
            {
                background-color:rgb(158,158,158);
                width:6px;
                height:6px;
                border-radius:1px;
                border:2px solid rgb(255,255,255);
            }
            QSlider:sub-page:horizontal
            {
                background-color:#4583b4;
                border-radius:3px;
            }
            QSlider:handle:horizontal:!enabled
            {
                width:5px;
                height:5px;
                border-radius:5px;
            }
            '''
        )

        self.right_playconsole_layout.addWidget(
            self.console_button_1, 0, 1, 1, 1)
        self.right_playconsole_layout.addWidget(
            self.console_button_2, 0, 3, 1, 1)
        self.right_playconsole_layout.addWidget(
            self.console_button_3, 0, 2, 1, 1)
        self.right_playconsole_layout.addWidget(
            self.console_button_4, 0, 0, 1, 1)
        self.right_playconsole_layout.addWidget(
            self.console_button_5, 0, 4, 1, 1)
        self.right_playconsole_layout.addWidget(self.volume_bar, 0, 5, 1, 2)
        self.right_playconsole_layout.setAlignment(
            QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示

        # 右侧部件添加
        self.right_lyrics_layout.addWidget(
            self.cur_song_name_lable, 0, 0)
        self.right_lyrics_layout.addWidget(self.play_label_gif, 1, 0)
        self.right_control_layout.addWidget(self.timeLabel1, 0, 0, 1, 1)
        self.right_control_layout.addWidget(self.right_process_bar, 0, 1, 1, 9)
        self.right_control_layout.addWidget(self.timeLabel2, 0, 10, 1, 1)
        self.right_control_layout.addWidget(
            self.right_playconsole_widget, 1, 0, 1, 11)

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
            background:#4774ac;
            border-top:0px solid white;
            border-bottom:0px solid white;
            border-left:0px solid white;
            border-top-left-radius:10px;
            border-top-right-radius:10px;
            }
        ''')

        self.search_btn.setStyleSheet(
            '''
            QPushButton{
                border:none;
                color:white;
                font-size:14px;
                font-family:"华文新魏";
                height:25px;
                padding-left:5px;
                padding-right:5px;
                text-align:left;
            }
            QPushButton:hover{
                border-radius:10px;
                background-color:rgba(255, 255, 255,50)
            }
            '''
        )

        self.left_bar_widget_search_input.setStyleSheet(
            '''QLineEdit{
                    color:white;
                    font-family: "华文新魏";
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 2px;
                    selection-background-color: #dd867f;
                    background-color:rgba(255, 255, 255,50)
            }''')

        self.body_widget.setStyleSheet('''
            QWidget#body_widget{
                color:#232C51;
                border-image:url(./image/b00.jpg);
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

    # 无边框的拖动

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):  # 重写移动事件
        if e.x() <= self.top_widget.width() and e.y() <= self.top_widget.height():
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = True
            self._startPos = QtCore.QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    # 关闭按钮动作函数
    def close_window(self):
        self.close()

    # 最小化按钮动作函数
    def mini_window(self):
        self.showMinimized()

    # 最大化按钮动作函数
    def max_window(self):
        if self.isMaximized():
            self.top_max.setIcon(qtawesome.icon(
                'msc.chrome-maximize', color='white'))
            self.showNormal()
        else:
            self.top_max.setIcon(qtawesome.icon(
                'msc.chrome-restore', color='white'))
            self.showMaximized()

    # 播放暂停按钮切换,播放音乐

    def playMusic(self):
        if not self.player.isAudioAvailable():
            self.setCurPlaying()
        if self.is_pause or self.is_switching:
            self.player.play()
            self.play_movie.setPaused(False)
            self.is_pause = False
            self.console_button_3.setIcon(qtawesome.icon(
                'fa5s.pause-circle', color='#4583b4', font=18))
        elif (not self.is_pause) and (not self.is_switching):
            self.player.pause()
            self.play_movie.setPaused(True)
            self.is_pause = True
            self.console_button_3.setIcon(qtawesome.icon(
                'fa5s.play-circle', color='#4583b4', font=18))

    # 根据播放模式播放音乐
    def playByMode(self):
        if (not self.is_pause) and (not self.is_switching):
            self.right_process_bar.setMinimum(0)
            self.right_process_bar.setMaximum(self.player.duration())
            self.right_process_bar.setValue(
                self.right_process_bar.value()+1000)
        self.timeLabel1.setText(time.strftime(
            '%M:%S', time.localtime(self.player.position()/1000)))
        self.timeLabel2.setText(time.strftime(
            '%M:%S', time.localtime(self.player.duration()/1000)))
        # 顺序播放
        if (self.console_button_4.currentIndex() == 0) and (not self.is_pause) and (not self.is_switching):
            if self.music_list.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.nextMusic()
        # 单曲循环
        elif (self.console_button_4.currentIndex() == 1) and (not self.is_pause) and (not self.is_switching):
            if self.music_list.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.is_switching = True
                self.setCurPlaying()
                self.right_process_bar.setValue(0)
                self.playMusic()
                self.is_switching = False
        # 随机播放
        elif (self.console_button_4.currentIndex() == 2) and (not self.is_pause) and (not self.is_switching):
            if self.music_list.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.is_switching = True
                self.music_list.setCurrentRow(
                    random.randint(0, self.music_list.count()-1))
                self.setCurPlaying()
                self.right_process_bar.setValue(0)
                self.playMusic()
                self.is_switching = False

    '''设置当前播放的音乐'''

    def setCurPlaying(self):
        self.TheSongName = self.TheLocalList[self.music_list.currentRow()][-1]
        self.cur_song_name_lable.setText(
            self.TheSongName.split('/')[-1].split('.')[0])
        self.right_process_bar.setValue(0)

        self.player.setMedia(QtMultimedia.QMediaContent(
            QtCore.QUrl(self.TheSongName)))

    # 读取本地数据，显示音乐列表
    def showMusic_List(self):
        for song in os.listdir(self.cur_path):
            if song.split('.')[-1] in self.song_formats:
                path_t = os.path.join(self.cur_path, song).replace('\\', '/')
                time_t = time.strftime('%M:%S', time.localtime(
                    int(MP3(path_t).info.length)))
                self.TheLocalList.append([song, path_t])
                item_wight = QtWidgets.QWidget()
                item_wight.setStyleSheet("color:white")
                layout_item = QtWidgets.QGridLayout()
                name_t = song.split('.')[0]
                qlabelname = nameLabel()
                qlabelname.setText(name_t)
                # if len(name_t)>18:
                #     name_t = name_t[:18]
                layout_item.addWidget(qlabelname, 0, 0, 1, 7)  # 歌名
                # layout_item.addWidget(QtWidgets.QLabel(name_t),0,0,1,8) #歌名
                layout_item.addWidget(
                    QtWidgets.QLabel("    "), 0, 7, 1, 1)  # 空格
                layout_item.addWidget(
                    QtWidgets.QLabel(time_t), 0, 8, 1, 2)  # 时间
                item_wight.setLayout(layout_item)
                item = QtWidgets.QListWidgetItem()
                self.music_list.addItem(item)
                self.music_list.setItemWidget(item, item_wight)
        self.music_list.setCurrentRow(1)
        if self.TheLocalList:
            self.cur_playing_song = self.TheLocalList[self.music_list.currentRow(
            )][-1]

    # 双击播放
    def doubleClicked(self):
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False
        self.play_movie.setPaused(False)
        self.console_button_3.setIcon(qtawesome.icon(
            'fa5s.pause-circle', color='#4583b4', font=18))

    # 上一首

    def previewMusic(self):
        self.right_process_bar.setValue(0)
        pre_row = self.music_list.currentRow()-1 \
            if self.music_list.currentRow() != 0 else self.music_list.count() - 1
        self.music_list.setCurrentRow(pre_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    # 下一首
    def nextMusic(self):
        self.right_process_bar.setValue(0)
        next_row = self.music_list.currentRow()+1 \
            if self.music_list.currentRow() != self.music_list.count()-1 else 0
        self.music_list.setCurrentRow(next_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False
    # 静音控制

    def on_btnSound_clicked(self):
        mute = self.player.isMuted()
        self.player.setMuted(not mute)
        if mute:
            self.volume_bar.setValue(self.old_volume_value)
            self.console_button_5.setIcon(
                qtawesome.icon('fa5s.volume-down', color='#4583b4'))
        else:
            self.volume_bar.setValue(0)
            self.console_button_5.setIcon(
                qtawesome.icon('fa5s.volume-mute', color='#4583b4'))
    # 调节音量

    def on_sliderVolumn_valueChanged(self, value):
        self.old_volume_value = value
        if value <= 1:
            self.console_button_5.setIcon(
                qtawesome.icon('fa5s.volume-mute', color='#4583b4'))
        elif value > 0 and value <= 60:
            self.console_button_5.setIcon(
                qtawesome.icon('fa5s.volume-down', color='#4583b4'))
        elif value > 60 and value < 100:
            self.console_button_5.setIcon(
                qtawesome.icon('fa5s.volume-up', color='#4583b4'))
        self.player.setVolume(value)

    def getMessage(self):
        TheText = self.left_bar_widget_search_input.text()
        if len(TheText):
            self.search_btn.setText("搜索中...")
            self.search_btn.repaint()

            songList = get_Search_Music_name(TheText, 5)
            if len(songList)>0:
                self.newwin = ChildWindow(TheText)
                self.newwin.setsongList(songList)
                self.newwin.showMusic_List()
                self.newwin.show()
                # if not self.newwin.isVisible() and self.newwin.selectSong != "":
                self.add_New_Song(self.newwin.selectSong)
            else:
                print("无结果")
            self.search_btn.setText("搜索")
            self.search_btn.repaint()
            self.left_bar_widget_search_input.setText("")

    def add_New_Song(self, filename):
        if filename.split('.')[-1] in self.song_formats:
            path_t = os.path.join(self.cur_path, filename).replace('\\', '/')
            time_t = time.strftime('%M:%S', time.localtime(
                int(MP3(path_t).info.length)))
            self.TheLocalList.append([filename, path_t])
            item_wight = QtWidgets.QWidget()
            item_wight.setStyleSheet("color:white")
            layout_item = QtWidgets.QGridLayout()
            name_t = filename.split('.')[0]
            print(name_t,time_t)
            qlabelname = nameLabel()
            qlabelname.setText(name_t)
            layout_item.addWidget(qlabelname, 0, 0, 1, 7)  # 歌名
            layout_item.addWidget(
                QtWidgets.QLabel("    "), 0, 7, 1, 1)  # 空格
            layout_item.addWidget(
                QtWidgets.QLabel(time_t), 0, 8, 1, 2)  # 时间
            item_wight.setLayout(layout_item)
            item = QtWidgets.QListWidgetItem()
            self.music_list.addItem(item)
            self.music_list.setItemWidget(item, item_wight)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('1.png'))
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

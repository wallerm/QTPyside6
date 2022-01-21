import sys
sys.path.append('./qt_for_python/rcc')
sys.path.append('./qt_for_python/uic')

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow

from PySide6.QtWebEngineWidgets import *
from PySide6.QtCore import QUrl
from PySide6.QtCore import QBasicTimer , Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt
import cv2

import testqtside1
from testqtside1 import Ui_MainWindow


class Communicate(QtCore.QObject):
    speakLoadNumber = Signal()
    def printLoad(self,stuff):
        print(stuff)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.browser = QWebEngineView(self)
        # 加载外部页面
        self.browser.load(QUrl('https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimg2.niutuku.com%2Fdesk%2F1208%2F1524%2Fntk-1524-42502.jpg&refer=http%3A%2F%2Fimg2.niutuku.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1645087795&t=0c4989536e666499fa0c8aa4bc60b6a7'))
        #self.setCentralWidget(self.browser)
        self.browser.setGeometry(250,50,500,300)
        self.browser.showMaximized()
        self.browser.loadProgress.connect(self.loadProgressHandler)
        self.someone = Communicate()
        self.someone.speakLoadNumber.connect(self.someone.printLoad)
        self.timeRun()
        self.browser.setZoomFactor(0.4)
    def loadProgressHandler(self, prog):
        #print("load progress:", prog)
        self.browerprop = prog
        #进度条逻辑
    def timeRun(self):
        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(10,self)  # 设置10超时时间 并开始计时
        #self.timer.timeout.connect(self.timerEvent("hello"))

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            print("current progress:" + str(self.browerprop))
            if self.browerprop >= 100:
                self.timer.stop()
                return
        else:
            print("timerid =" +str(event.timerId()) )

class picturezoom(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(picturezoom, self).__init__(parent)
        self.setupUi(self)
        # img=cv2.imread("F:\\test\\achv_new\main\\lbl_cloth_live2d.png")                                      #读取图像
        # img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)                #转换图像通道
        # x = img.shape[1]                                                        #获取图像大小
        # y = img.shape[0]
        self.zoomscale=1                                                       #图片放缩尺度
        # frame = QImage(img, x, y, QImage.Format_RGB888)
        # pix = QPixmap.fromImage(frame)
        ######方法二
        # pix = QPixmap("F:\\test\\achv_new\main\\bg_cloth.png")
        # pix.scaled(self.picshow.width(),self.picshow.height())
        # self.item=QGraphicsPixmapItem(pix)                              #创建像素图元
        # #self.item.setScale(self.zoomscale)
        # self.scene=QGraphicsScene()                                       #创建场景
        # self.scene.addItem(self.item)
        # self.picshow.setScene(self.scene)                                 #将场景添加至视图
        ######图片生成三
        self.scene = QGraphicsScene()
        self.imgShow = QPixmap()
        self.imgShow.load(":ui_qjnn/achv_new/main/bg_cloth_clothes.png")
        self.imgShowItem = QGraphicsPixmapItem()
        self.imgShowItem.setPixmap(QPixmap(self.imgShow))
        #self.imgShowItem.setPixmap(QPixmap(self.imgShow).scaled(96, 91))  
        self.scene.addItem(self.imgShowItem)
        self.picshow.setScene(self.scene)
        scaleWidth = self.picshow.width()
        scaleHeight = self.picshow.height()
        self.picshow.fitInView(0, 0, scaleWidth, scaleHeight, Qt.KeepAspectRatio)    #图像自适应大小

        self.zoomout.clicked.connect(self.on_zoomout_clicked)
        self.zoommin.clicked.connect(self.on_zoomin_clicked)

    def on_zoomin_clicked(self):
        """
        点击缩小图像
        """
        # TODO: not implemented yet
        self.zoomscale=self.zoomscale-0.05
        if self.zoomscale<=0:
           self.zoomscale=0.2
        self.imgShowItem.setScale(self.zoomscale)                                #缩小图像

    def on_zoomout_clicked(self):
        """
        点击方法图像
        """
        # TODO: not implemented yet
        self.zoomscale=self.zoomscale+0.05
        if self.zoomscale>=1.2:
            self.zoomscale=1.2
        self.imgShowItem.setScale(self.zoomscale)                             #放大图像\

if __name__ == '__main__':

    app = QApplication(sys.argv)

    piczoom = picturezoom()
    piczoom.show()
    # webwindow = MainWindow()
    # webwindow.show()
    sys.exit(app.exec_())

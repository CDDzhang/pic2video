############################################
#CDD-2020-12-11
#这个程序用于帮助不会使用OPENCV的人在Linux上合成视频
############################################

from PyQt5.Qt import QWidget, QFileDialog, QApplication, QMessageBox, QCloseEvent, QProgressBar
import PyQt5.QtCore as QtCore
import PyQt5.sip
import cv2
import sys
from UI.VideofusionUI import Ui_Form
import os
import numpy as np


class VideofusionWidget(QWidget):
    # 继承设置的图形界面
    def __init__(self, parent=None):
        super(VideofusionWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # LineEdit 设置
        self.ui.picpath.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.outputpath.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.savename.setPlaceholderText("output.avi")
        self.ui.fps.setPlaceholderText("30")
        self.ui.picpath.setPlaceholderText("/home/")
        self.ui.outputpath.setPlaceholderText("/home/")
        self.ui.progressBar.setValue(0)

        # Slot函数
        self.ui.stopButton.clicked.connect(self.close)
        self.ui.picpathButton.clicked.connect(self.choose_picpath)
        self.ui.outputpathButton.clicked.connect(self.choose_outputpath)
        self.ui.startButton.clicked.connect(self.startfusion)

    # 选择图片文件夹
    def choose_picpath(self):
        pic_dir = QFileDialog.getExistingDirectory(self, "Choose your pic dir", "/home/")
        self.ui.picpath.setText(pic_dir)

    # 选择输出文件夹
    def choose_outputpath(self):
        output_dir = QFileDialog.getExistingDirectory(self, "Choose your output dir", "/home/")
        self.ui.outputpath.setText(output_dir)

    # 开始生成视频
    def startfusion(self):
        fps = self.ui.fps.text()
        picpath = self.ui.picpath.text()
        output = self.ui.outputpath.text()
        savename = self.ui.savename.text()
        if (fps != '') & (picpath != '') & (output != '') & (savename != ''):
            self.fusion_video(picpath=picpath, output=output, savename=savename, fps=fps)
        else:
            QMessageBox.warning(self, 'Warning!', 'Make sure all the message correctly!', QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.Yes)

    # 关闭时提示消息设置
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        if reply == QMessageBox.No:
            event.ignore()

    # 利用cv2生成视频
    def fusion_video(self, picpath, output, savename, fps):
        self.ui.progressBar.setValue(0)
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')  # e.g. XVID, DIVX, MJPG, X264, mp4v, I420
        path = picpath
        fps = int(fps)
        list = sorted(os.listdir(path))
        frame = cv2.imread(path + "/" + list[0])
        size = np.shape(frame)[:2]
        size0 = size[0]
        size1 = size[1]
        size = (size1, size0)

        videowriter = cv2.VideoWriter(output + '/' + savename, fourcc, fps, size)
        for i in range(len(list)):
            frame = cv2.imread(path + '/' + list[i])
            videowriter.write(frame)
            cv2.imshow("frame", frame)
            cv2.waitKey(20)
            progressValue = int((i+1)/len(list) * 100)
            self.ui.progressBar.setValue(progressValue)
        pass
        videowriter.release()
        QMessageBox.information(self, 'information', 'already fusion video', QMessageBox.Ok, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Vwidget = VideofusionWidget()
    Vwidget.show()
    sys.exit(app.exec_())

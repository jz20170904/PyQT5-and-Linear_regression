import sys
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy  as np
import pandas as pd
import linear#调用创造的linear库

#创造绘图类
class MyMplCanvas(FigureCanvas):


    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


        self.fig = plt.figure(figsize=(width,height),dpi=dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes1 = self.fig.add_subplot(111)
        self.axes.hold(False)
        self.axes1.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def Drawing_node(self):#绘制散点图
        data=linear.ToData()
        x=data.x.values
        y=data.y.values

        self.axes.set_xticklabels(np.linspace(min(x),max(x),5))
        self.axes.set_yticklabels(np.linspace(min(y),max(y),5))
        self.axes.scatter(x,y)#散点图
        self.axes.set_xlabel('x轴')
        self.axes.set_ylabel('y轴')
        self.axes.grid(False)#不显示网格


    def Drawing_close(self):#绘制拟合图
        alpha=0.001
        N=200#迭代次数
        data=linear.ToData()
        X,y,theta=linear.data_taking(data)
        g,cost=linear.gradientDescent(X,y,theta,alpha,N)
        # print (g)
        # print (cost)

        x=np.linspace(data.x.min(),data.x.max(),100)
        f=g[0,0]+(g[0,1]*x)


        self.axes1.plot(x,f,'r',label='拟合曲线')

        self.axes1.set_xlabel('X')
        self.axes1.set_ylabel('y')
        self.axes1.set_title('单变量线性回归')
        self.axes1.grid(False)
        self.axes2=self.axes1.twinx()
        self.axes2.scatter(data.x,data.y,label='散点图')


class MainWindow(QWidget):#主窗口
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.resize(1200,600)
        self.setWindowTitle("线性回归")

        #定义全局布局
        H_layout=QHBoxLayout()

        #定义两个局部布局
        V1_layout=QVBoxLayout()
        V2_layout=QVBoxLayout()

        #定义两个布局控件
        V1_W=QWidget()
        V2_W=QWidget()

        #V1_layout布局
        self.Button1=QPushButton('读取数据',self)
        self.Button1.clicked.connect(self.ReadData)#
        V1_layout.addWidget(self.Button1)
        self.textEdit=QTextEdit()

        V1_layout.addWidget(self.textEdit)
        self.Button2=QPushButton('显示散点图',self)
        V1_layout.addWidget(self.Button2)
        self.Button2.clicked.connect(self.On_node)

        self.mpl_1 = MyMplCanvas(self, width=4, height=5, dpi=100)
        self.mpl_1.Drawing_node()
        V1_layout.addWidget(self.mpl_1)
        self.mpl_1.setVisible(False)

        V1_layout.addStretch(0.5)
        V1_W.setLayout(V1_layout)
        H_layout.addWidget(V1_W)


        #V2_layout布局
        self.Button3=QPushButton('绘制拟合曲线',self)
        self.Button3.move(800,50)
        self.Button3.clicked.connect(self.On_close)

        self.mpl_2 = MyMplCanvas(self, width=4, height=4, dpi=100)
        self.mpl_2.Drawing_close()
        self.mpl_2.setVisible(False)
        V2_layout.addWidget(self.mpl_2)
        V2_W.setLayout(V2_layout)
        H_layout.addWidget(V2_W,Qt.AlignRight,Qt.AlignBottom)


        H_layout.addStretch(0.5)
        self.setLayout(H_layout)

#定义所关联的函数
    def ReadData(self):
        filename=QFileDialog()
        filename.setFileMode(QFileDialog.AnyFile)
        filename.setFilter(QDir.Files)

        if filename.exec_():
            filenames=filename.selectedFiles()
            f=open(filenames[0],'r')#打开文件

            with f:
                data=f.read()#读取数据
                self.textEdit.setPlainText(data)#显示数据
        return data

    def On_node(self):#显示散点图函数
        self.mpl_1.setVisible(True)

    def On_close(self):#显示拟合曲线函数
        self.mpl_2.setVisible(True)

if __name__=='__main__':
    app=QApplication(sys.argv)
    form=MainWindow()
    form.show()
    sys.exit(app.exec_())

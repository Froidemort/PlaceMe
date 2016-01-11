# coding=utf-8
# IMPORTS ----------------------------------------------------------------------
import random
import sys

from PyQt4 import QtGui


# CONSTANTS (preceded with 'C_') -----------------------------------------------

# FUNCTIONS --------------------------------------------------------------------
def showMessage(self, parent, title, text):
    QtGui.QMessageBox.information(parent, title, text)
# CLASSES ----------------------------------------------------------------------

class StackBar(QtGui.QWidget):
    def __init__(self, parent=None):
        super(StackBar, self).__init__(parent)
        self.parent = parent
        self.btnList = []
        self.actList = []
        self.fctList = []
        self.nBtn = len(self.btnList)
        self.hBorder = 5
        self.btnGap = 5
        self.height = 35
        self.initGrpButton(self.height,self.height)
        self.setMinimumSize(0,self.height+self.hBorder*2)
    def initGrpButton(self, width, height, text=''):
        self.menu = QtGui.QMenu(None)
        self.menu.ToolButtonPopupMode = 2
        self.groupBtn = QtGui.QPushButton(self)
        self.groupBtn.setText(text)
        self.groupBtn.setGeometry(0,0,width, self.height)
        self.groupBtn.hide()
        self.groupBtn.setMenu(self.menu)
        for action in self.actList:
            self.menu.addAction(action)
            action.setVisible(False)
    def addItem(self, width, text, icon, txtOnIcon=False, tooltip=''):
        self.currentItem = len(self.btnList)
        self.currentx = self.currentItem*self.btnGap + sum([i.size().width()
            for i in self.btnList])
        if txtOnIcon:
            txt = text
        else:
            txt = ''#on ne met que l'icone.
        self.btnList.append(QtGui.QPushButton(txt,  self))
        self.fctList.append(lambda x: None)
        self.actList.append(QtGui.QAction(QtGui.QIcon(icon),text, self.menu))
        self.btnList[self.currentItem].move(self.currentx, self.hBorder)
        self.btnList[self.currentItem].setIcon(QtGui.QIcon(icon))
        self.btnList[self.currentItem].setFixedSize(width, self.height)
        self.btnList[self.currentItem].setToolTip(tooltip)
        self.menu.addAction(self.actList[self.currentItem])
        self.actList[self.currentItem].setVisible(False)
        self.nBtn = len(self.btnList)
        self.currentx += width
    def resizeEvent(self, e):
        if self.parent == None:
            S = self.size().width()
        else:
            S = self.parent.size().width()
        self.groupBtn.move(S-self.btnGap-self.groupBtn.size().width(),
                                                                 self.hBorder)
        if S < self.currentx:
            self.groupBtn.show()
            self.btnList[self.nBtn-1].hide()
            self.actList[self.nBtn-1].setVisible(True)
        else:
            self.groupBtn.hide()
            self.btnList[self.nBtn-1].show()
            self.actList[self.nBtn-1].setVisible(False)
        for i in range(self.nBtn-1):
            xI = self.btnGap * (i+1) + sum([j.size().width()
                                for j in self.btnList[:i+1]]) \
                                + self.groupBtn.size().width()
            if S < xI:
                self.btnList[i].hide()
                self.actList[i].setVisible(True)
            else:
                self.btnList[i].show()
                self.actList[i].setVisible(False)
    def setHeight(self, height):
        self.setMinimumSize(0,height+self.hBorder*2)
        for i in range(self.nBtn):
            self.btnList[i].setFixedHeight(height)
        self.groupBtn.setFixedHeight(height)
        
    def setFunction(self, i, function):
        if len(self.fctList) <i:
            self.fctList.append(function)
        else:
            self.fctList[i] = function
        self.btnList[i].clicked.connect(self.fctList[i])
        self.actList[i].triggered.connect(self.fctList[i])


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.widget = StackBar()

        table = QtGui.QTableWidget()
        for i in range(10):
            width = random.randrange(25, 100, 1)
            c = random.choice([True, False])
            self.widget.addItem(width,str(i), 'images/plus.png', c)
        vbox = QtGui.QVBoxLayout()
        self.widget.setHeight(45)
        vbox.addWidget(self.widget)
        vbox.addWidget(table)
        self.setLayout(vbox)
        self.show()


# MAIN -------------------------------------------------------------------------
def main():
    app = QtGui.QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()

# MAIN--------------------------------------------------------------------------
if __name__ == '__main__':
    print type(main)
    main()

# coding=utf-8
# IMPORTS ----------------------------------------------------------------------
import sys

from PyQt4 import QtGui

# CONSTANTS (preceded with 'C_') --------------------------------------
C_MODEL_EXAMPLE = QtGui.QStringListModel()


# FUNCTIONS --------------------------------------------------------------------

# CLASSES ----------------------------------------------------------------------
class TagWindow(QtGui.QWidget):
    def __init__(self, parent=None, model=C_MODEL_EXAMPLE):
        QtGui.QWidget.__init__(self, parent)
        # Declaration of the layouts
        vLayout = QtGui.QVBoxLayout()
        hBotLayout = QtGui.QHBoxLayout()
        hTopLayout = QtGui.QHBoxLayout()
        # Declaration of the widgets
        self.tagAdder = QtGui.QLineEdit()
        addButton = QtGui.QPushButton('Add tag')
        self.tagList = QtGui.QListView()
        okButton = QtGui.QPushButton('OK')
        cancelButton = QtGui.QPushButton('Cancel')
        # Designing the UI
        hTopLayout.addWidget(self.tagAdder)
        hTopLayout.addWidget(addButton)
        # Putting ok and cancel buttons to the left
        hBotLayout.addStretch(1)
        hBotLayout.addWidget(okButton)
        hBotLayout.addWidget(cancelButton)
        vLayout.addItem(hTopLayout)
        vLayout.addWidget(self.tagList)
        vLayout.addItem(hBotLayout)
        # Settings
        self.setLayout(vLayout)
        self.tagList.setModel(model)
        # Linking actions
        addButton.clicked.connect(self.addAction)
        okButton.clicked.connect(self.okAction)
        cancelButton.clicked.connect(self.cancelAction)

    def okAction(self):
        print 'okButton pressed'
        self.emit(SIGNAL("closingTagWindow(PyQt_PyObject)"))
        self.close()

    def cancelAction(self):
        print 'cancelButton pressed'
        self.emit(SIGNAL("closingTagWindow(PyQt_PyObject)"))
        self.close()

    def addAction(self):
        print 'addButton pressed'


def main():
    app = QtGui.QApplication(sys.argv)
    myWindow = TagWindow()
    myWindow.show()
    app.exec_()


# MAIN--------------------------------------------------------------------------
if __name__ == '__main__':
    main()

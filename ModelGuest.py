# IMPORT MODULES ---------------------------------------------------------------
from PyQt4 import QtGui, QtCore
import sys, os
# CONSTANTES (toutes precedees avec 'C_') --------------------------------------
C_MAN, C_WOMAN, C_CHILDREN = tuple(range(3))
# FONCTIONS --------------------------------------------------------------------

# CLASSES ----------------------------------------------------------------------
class GuestsModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(GuestsModel,self).__init__(parent)
        self.parent = parent
        self.guestList = []

    def columnCount(self, parent=QtCore.QModelIndex()):
        #Fixed to 4 (surname, name, gender, tags)
        return 4
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.guestList)
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column() != 3:
                return self.guestList[index.row()][index.column()]
            else:
                return None
        if role == QtCore.Qt.EditRole:
            pass
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid(): return False
        if role == QtCore.Qt.EditRole:
            if index.column() != 3:
                self.guestList[index.row()][index.column()]=value
            else:
                self.guestList[index.row()][index.column()]=None #ignore tags for the moment
            return True
        else:
            return False
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row + count - 1)
        self.guestList.append(['Surname_%s'%(row), 'Name_%s'%(row), C_MAN, None])

        self.endInsertRows()
        


class GuestsView(QtGui.QTableView):
    def __init__(self, parent=None):
        super(GuestsView,self).__init__(parent)
##        self.setItemDelegateForColumn(2, ComboDelegate(self))
##        self.setShowGrid(False)

class Widget(QtGui.QWidget):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.model= GuestsModel()
            self.view = GuestsView()
            self.view.setModel(self.model)
##            for row in range(0, self.model.rowCount()):
##                self.view.openPersistentEditor(self.model.index(row, 2))
            btn=QtGui.QPushButton('Add guest')
            btn.clicked.connect(self.addGuest)
            layout=QtGui.QVBoxLayout()
            layout.addWidget(self.view)
            layout.addWidget(btn)
            self.setLayout(layout)
            self.setGeometry(300,300,500,500)
        def addGuest(self):
            print "Creating a row..."
            self.model.insertRows(self.model.rowCount(), 1)

# MAIN -------------------------------------------------------------------------
def main():
    app = QtGui.QApplication(sys.argv)
    myWindow = Widget()
    myWindow.show()
    app.exec_()

# MAIN--------------------------------------------------------------------------
if __name__ == '__main__':
    main()

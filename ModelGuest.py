# coding=utf-8
# IMPORT MODULES ---------------------------------------------------------------
import sys

from PyQt4 import QtGui, QtCore

from StackBar import StackBar
from UITagList import TagWindow
# CONSTANTS (preceded with 'C_') --------------------------------------
C_MAN, C_WOMAN, C_CHILDREN = tuple(range(3))


# FUNCTIONS --------------------------------------------------------------------
def skip_duplicates(iterable, key=lambda x: x):
    fingerprints = set()
    for x in iterable:
        fingerprint = key(x)
        if fingerprint not in fingerprints:
            yield x
            fingerprints.add(fingerprint)


def _toPyObject(elem):
    try:
        return elem.toPyObject()
    except AttributeError:
        return elem


# CLASSES ----------------------------------------------------------------------
class GuestsModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(GuestsModel, self).__init__(parent)
        self.parent = parent
        self.guestList = []
        self.headerLabels = ['Name', 'Surname', 'Gender', 'Tags...']
        # In english for the moment,
        # need to implement QtLinguist functionality

    def columnCount(self, parent=QtCore.QModelIndex()):
        # Fixed to 4 (surname, name, gender, tags)
        return 4

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.guestList)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column() != 3:
                return self.guestList[index.row()][index.column()]
            else:
                # ignore tags for the moment, will be implemented later
                return None
        if role == QtCore.Qt.EditRole:
            if index.column() != 3:
                return self.guestList[index.row()][index.column()]
            else:
                # ignore tags for the moment, will be implemented later
                return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        print "Calling setData"
        if not index.isValid(): return False
        if role == QtCore.Qt.EditRole:
            if index.column() != 3:
                oldValue = self.guestList[index.row()][index.column()]
                self.guestList[index.row()][index.column()] = value
                if not self._checkDatas():
                    QtGui.QMessageBox.warning(None, 'Error : two identical guests',
                                              'Two guest cannot be identical')
                    self.guestList[index.row()][index.column()] = oldValue
                else:
                    return True

            else:
                # ignore tags for the moment, will be implemented later
                self.guestList[index.row()][index.column()] = None
            return True
        else:
            return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | \
               QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        print 'adding row n', row
        self.beginInsertRows(parent, row, row + count - 1)
        self.guestList.append([None, None, 0, None])
        # assuming count=1
        self.endInsertRows()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        print 'deleting row n', row
        self.beginRemoveRows(parent, row, row + count - 1)
        if len(self.guestList) != 0: self.guestList.pop(row)
        self.endRemoveRows()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and \
                        orientation == QtCore.Qt.Horizontal:
            return self.headerLabels[section]
        return QtCore.QAbstractTableModel.headerData(self, section,
                                                     orientation, role)

    def _checkDatas(self):
        partialGuestList = [elem[:-1] for elem in self.guestList[:]
                            if elem not in [[None, None, i, None] for i in range(3)]]
        partialGuestList = [tuple([_toPyObject(elem)
                                   for elem in x])
                            for x in partialGuestList]
        skippedGuestList = list(skip_duplicates(partialGuestList,
                                                lambda x: tuple([_toPyObject(elem)
                                                                 for elem in x])))
        return len(partialGuestList) == len(skippedGuestList)


class ComboDelegateColumn2(QtGui.QItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.pathIcons = map(lambda path: QtGui.QIcon(path),
                             ['images/male.png', 'images/female.png', 'images/baby.png'])


    def createEditor(self, parent, option, index):
        combo = QtGui.QComboBox(parent)
        comboModel = combo.model()
        for icon in self.pathIcons:
            item = QtGui.QStandardItem(icon, '')
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            comboModel.appendRow(item)
        self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self, QtCore.SLOT("currentIndexChanged()"))
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex())

    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class ButtonDelegateColumn3(QtGui.QItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.tagList = ['']

    def createEditor(self, parent, option, index):
        button = QtGui.QPushButton(parent)
        button.setText(QtCore.QString(u"Tags..."))

        # self.connect(button, QtCore.SIGNAL("currentIndexChanged(int)"),
        #             self, QtCore.SLOT("currentIndexChanged()"))
        button.clicked.connect(self.raiseUI)
        return button

    def raiseUI(self):
        print "Raise the UI !"




class GuestsView(QtGui.QTableView):
    def __init__(self, parent=None):
        super(GuestsView, self).__init__(parent)
        # Delegate for gender
        self.setItemDelegateForColumn(2, ComboDelegateColumn2(self))
        self.setItemDelegateForColumn(3, ButtonDelegateColumn3(self))


class Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        # Setting the model/view and linking the two.
        self.model = GuestsModel()
        self.tagModel = QtGui.QStringListModel()
        self.view = GuestsView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(
                QtGui.QAbstractItemView.ExtendedSelection)
        # Creation of the stackbar, adding button to it.
        self.gStackBar = StackBar()
        self.gStackBar.addItem(35, 'Add guest', 'images/plus.png', False,
                               'Add a guest at the end of the list')
        self.gStackBar.addItem(35, 'Del guest', 'images/minus.png', False,
                               '''Delete a selected guest.
            If any are selected, delete the last row''')
        self.gStackBar.addItem(55, 'Import\nguests',
                               'images/import.png', False,
                               'Import a list of guest from file')
        self.gStackBar.addItem(55, 'Export\nguests',
                               'images/export.png', False,
                               'Export a list of guest to a file')
        self.gStackBar.addItem(55, 'Manage tags', 'images/iconTags', False,
                               'Manage tags')
        # Setting function ton the stackbar buttons
        self.gStackBar.setFunction(0, self.addGuest)
        self.gStackBar.setFunction(1, self.delGuest)
        self.gStackBar.setFunction(4, self.manageTags)
        # Creating the vertical layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.gStackBar)
        layout.addWidget(self.view)
        self.setLayout(layout)
        # Temporary dimension of the widget.
        self.setGeometry(300, 300, 500, 500)

    def addGuest(self):
        print "Creating a row..."
        self.model.insertRows(self.model.rowCount(), 1)
        self.view.openPersistentEditor(
                self.model.index(self.model.rowCount() - 1, 2))
        self.view.openPersistentEditor(
                self.model.index(self.model.rowCount() - 1, 3))

    def delGuest(self):
        print "Deleting a list of selected rows"
        selection = self.view.selectionModel()
        l = reversed(list(skip_duplicates([item.row()
                                           for item in selection.selectedIndexes()])))
        for row in l:
            self.model.removeRows(row, 1)

    def manageTags(self):
        tagWindow = TagWindow()
        self.connect(tagWindow, QtCore.SIGNAL("closingTagWindow(PyQt_PyObject)"))
        tagWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        tagWindow.show()


# MAIN -------------------------------------------------------------------------
def main():
    app = QtGui.QApplication(sys.argv)
    myWindow = Widget()
    myWindow.show()
    app.exec_()


# MAIN--------------------------------------------------------------------------
if __name__ == '__main__':
    main()

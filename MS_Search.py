import nuke
import os


def nk_version():
    #Return QtCore, QtWidgets, and QtGui modules compatible with the current Nuke version.
    import nuke as _nuke
    if _nuke.NUKE_VERSION_MAJOR < 11:
        from PySide import QtCore, QtGui
        QtWidgets = QtGui
    elif _nuke.NUKE_VERSION_MAJOR < 16:
        from PySide2 import QtCore, QtWidgets
        from PySide2 import QtGui
    else:
        from PySide6 import QtCore, QtWidgets
        from PySide6 import QtGui
    return QtCore, QtWidgets, QtGui

#Qt modules and QT classes
QtCore, QtWidgets, QtGui = nk_version()

QDialog = QtWidgets.QDialog
QLineEdit = QtWidgets.QLineEdit
QTableView = QtWidgets.QTableView
QHeaderView = QtWidgets.QHeaderView
QVBoxLayout = QtWidgets.QVBoxLayout
QSettings = QtCore.QSettings
QTimer = QtCore.QTimer
QIcon = QtGui.QIcon

class Table_List(QtCore.QAbstractTableModel):
    #Table model for node search results, and also colums
    COLUMNS = ["Node/Type", "Read name", "Label"]

    def __init__(self, parent=None):
        super(Table_List, self).__init__(parent)
        self._nodes = []

    def rowCount(self, parent=None):
        return len(self._nodes)

    def columnCount(self, parent=None):
        return len(self.COLUMNS)

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return None
        node = self._nodes[index.row()]
        col = index.column()
        if col == 0:
            return "{0} ({1})".format(node.name(), node.Class())
        elif col == 1 and node.Class() == "Read":
            try:
                return os.path.basename(node['file'].value())
            except:
                return ""
        elif col == 2:
            try:
                return node['label'].value().strip()
            except:
                return ""
        return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.COLUMNS[section]
        return None

    def setNodes(self, nodes):
        self.beginResetModel()
        self._nodes = nodes
        self.endResetModel()

class NodeSearchTool(QDialog):
    #searching and focusing nodes in the Nuke Node Graph
    def __init__(self):
        super(NodeSearchTool, self).__init__()
        self.setWindowTitle("MS - Search")
        self.setWindowIcon(QIcon())

        # Restore window size
        self.settings = QSettings("MS", "MS-Search")
        size = self.settings.value("window/size")
        try:
            if isinstance(size, QtCore.QSize):
                self.resize(size)
            else:
                self.resize(500, 400)
        except:
            self.resize(500, 400)

        # Layout
        layout = QVBoxLayout(self)

        # Search field
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Enter node name or type...")
        layout.addWidget(self.search_field)

        #List
        self.table = QTableView()
        self.model = Table_List(self)
        self.table.setModel(self.model)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(self.table.SelectRows)
        layout.addWidget(self.table)

        # small delay for search bar
        self._timer = QTimer(self, singleShot=True)
        self._timer.setInterval(200)
        self.search_field.textChanged.connect(self._timer.start)
        self._timer.timeout.connect(self._on_search)

        #zoooom
        self.table.clicked.connect(self._on_focus)
        self.search_field.setFocus()

    def _on_search(self):
        term = self.search_field.text().strip().lower()
        if not term:
            self.model.setNodes([])
            return
        matched = []
        for node in nuke.allNodes():
            try:
                if term in node.name().lower() or term in node.Class().lower():
                    matched.append(node)
            except:
                pass
        self.model.setNodes(matched)

    def _on_focus(self, index):
        try:
            node = self.model._nodes[index.row()]
            nuke.centerOnNode(node)
        except:
            try:
                nuke.zoom(2, [node.xpos(), node.ypos()])
            except:
                nuke.message("Cannot focus on node.")

    def closeEvent(self, event):
        try:
            self.settings.setValue("window/size", self.size())
        except:
            pass
        super(NodeSearchTool, self).closeEvent(event)


def show_search_tool():
    global _search_tool
    try:
        _search_tool.close()
    except:
        pass
    _search_tool = NodeSearchTool()
    _search_tool.show()

show_search_tool()

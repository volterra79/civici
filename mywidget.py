from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *







"""

    CUSTOM FORM EDITING FORM


"""

MYSTYLE="""
QPushButton::checked {

    background-color: rgb(255, 0, 0);

}

QPushButton {

    min-width: 20px;
    max-width: 20px;
    min-height: 12px;
    max-height: 12px;
    font-size: 8px;
}

QLabel {

     font-size: 10px;
     font-weight: lighter;

}

"""

HEADER_STYLE_LABEL = """

QLabel {

     font-size: 12px;
     font-weight:bold;
     margin-bottom:0;
     margin-top:0;
     padding:0;

}

"""

GROUP_BOX_STYLE = """

QGroupBox {

        margin-top:0;
        margin-bottom:0;

        });


"""




POINTERCURSOR = QtGui.QCursor(QtCore.Qt.PointingHandCursor)

class QLabelClickable(QtGui.QLabel):

    def __init(self, parent):
        QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))



class MyTable(QTableWidget):
    def __init__(self, tcolumn, trows, *args):
        QTableWidget.__init__(self, *args)
        self.tcolumn = tcolumn
        self.trows = trows
        self.setmydata()
        self.name = 'Zoom To Select'
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
        self.setSelectionBehavior(1)
        self.setSelectionMode(1)
        self.currentCellChanged.connect(self.rowSelected)
        self.selectedcivico = None

    def rowSelected(self,cr,pr,cc,pc):


        self.selectedcivico = self.item(cr,4).text()

    def setmydata(self):

        horHeaders = []

        i=0
        for n, col in enumerate(self.tcolumn):
            horHeaders.append(col)
            print(col)
            for m, item in enumerate(self.trows[i]):
                if item is None:
                    newitem = QTableWidgetItem('')
                else:
                    newitem = QTableWidgetItem(str(item))
                self.setItem(m, n, newitem)
            i+=1
        self.setHorizontalHeaderLabels(horHeaders)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)

        Action = menu.addAction("I am a " + self.name + " Action")
        Action.triggered.connect(self.printName)

        menu.exec_(event.globalPos())

    def printName(self):
        print "Action triggered from " + self.name
class CustomCiviciEditDockWidget(QDockWidget):

    def __init__(self, action=None, text="Civici Editor", parent=None):
        super(CustomCiviciEditDockWidget, self).__init__(text, parent)
        self.action=action
        self.setObjectName("CustomCiviciEditDockWidget")
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setMinimumHeight(200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(palette)
    def closeEvent(self,event):
        self.action.toggle()
        super(CustomCiviciEditDockWidget,self).closeEvent(event)


class MyStackedWidget(QtGui.QStackedWidget):

    def __init__(self,parent=None,mapcanvas=None, widgetTable=None):

        super(MyStackedWidget,self).__init__(parent=None)
        self.mapcanvas = mapcanvas
        self.widgetTable = widgetTable




    def addMyWidget(self,):

        self.addWidget(self.widgetTable)
        self.setCurrentWidget(self.widgetTable)
        self.adjustSize()

        return self.widgetTable




    def removeMyWidget(self):

        self.removeWidget(self.widgetTable)
        self.adjustSize()

        return self.widgetTable





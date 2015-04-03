from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import QgsRectangle

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

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
    def __init__(self, mapcanvas, tcolumn, trows, *args):
        QTableWidget.__init__(self, *args)
        self.mapcanvas =  mapcanvas
        self.tcolumn = tcolumn
        self.trows = trows
        self.setmydata()
        self.currentSelectdRow = None
        self.setSelectionBehavior(1)
        self.setSelectionMode(1)
        self.setSortingEnabled(True)
        self.currentCellChanged.connect(self.rowSelected)
        self.selectedcivico = None


    def rowSelected(self,cr,pr,cc,pc):
        try:
            self.currentSelectdRow = cr
            self.selectedcivico = self.item(cr,0).text()
        except:
            pass

    def setmydata(self):

        horHeaders = []


        for n, col in enumerate(self.tcolumn):
            horHeaders.append(col)
            for m, item in enumerate(self.trows[n]):

                if item is None:

                    newitem = QTableWidgetItem('')

                else:

                    newitem = QTableWidgetItem(str(item))

                self.setItem(m, n, newitem)
                ##check the geometry ###
                if self.trows[-1][m] is not None:

                    self.item(m,n).setBackgroundColor(QColor('#f0f0f0'))

        self.setHorizontalHeaderLabels(horHeaders)


    def contextMenuEvent(self, event):
        index = self.trows[0].index(int(self.selectedcivico))
        self.geom = self.trows[-1][index]

        if self.geom is not None :
            xy = self.geom.split('POINT(')[1].split(' ')
            self.x = float(xy[0])
            self.y = float(xy[1].split(')')[0])
            menu = QtGui.QMenu(self)

            Action = menu.addAction("Pan to feature")
            Action.triggered.connect(self.panToRowSelected)

            menu.exec_(event.globalPos())

    def panToRowSelected(self):
        self.mapcanvas.zoomIn()
        extent = self.mapcanvas.extent()
        xmin = self.x - extent.width()

        xmax = self.x + extent.width()

        ymin = self.y - extent.height()

        ymax = self.y + extent.height()

        rect = QgsRectangle( xmin, ymin, xmax, ymax )
        self.mapcanvas.setExtent(rect)
        self.mapcanvas.refresh()

        print "Pan to feature " + self.geom


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


class WhatSaveFeatureDialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName(_fromUtf8("salvailcivico"))
        dialog.resize(200, 100)
        layout = QVBoxLayout()
        self.label = QtGui.QLabel('Vuoi salvare il civico inserito?')
        self.button_box = QtGui.QDialogButtonBox(dialog)
        #self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        layout.addWidget(self.label)
        layout.addWidget(self.button_box)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), dialog.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        dialog.setLayout(layout)

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(_translate("Save Feature", "Civici Editor", None))




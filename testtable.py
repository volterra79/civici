__author__ = 'boccafr'
from PyQt4 import QtGui, QtCore
from databaseConnection import build_table_from_database_table
from PyQt4.QtGui import *
import sys
tcolumn, trows, col_num, row_num =build_table_from_database_table()
print(tcolumn)
print(trows)
class MyTable(QTableWidget):
    def __init__(self, tcolumn, trows, *args):
        QTableWidget.__init__(self, *args)
        self.tcolumn = tcolumn
        self.trows = trows
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

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




def main(args):
    app = QApplication(args)
    table = MyTable(tcolumn, trows, row_num, col_num)
    table.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)



#
# data = {'col1':['1','2','3'], 'col2':['4','5','6'], 'col3':['7','8','9']}
#
# class MyTable(QTableWidget):
#     def __init__(self, data, *args):
#         QTableWidget.__init__(self, *args)
#         self.data = data
#         self.setmydata()
#         self.resizeColumnsToContents()
#         self.resizeRowsToContents()
#
#     def setmydata(self):
#
#         horHeaders = []
#         for n, key in enumerate(sorted(self.data.keys())):
#             horHeaders.append(key)
#             for m, item in enumerate(self.data[key]):
#                 newitem = QTableWidgetItem(item)
#                 self.setItem(m, n, newitem)
#         self.setHorizontalHeaderLabels(horHeaders)
#
# def main(args):
#     app = QApplication(args)
#     table = MyTable(data, 5, 3)
#     table.show()
#     sys.exit(app.exec_())
#
# if __name__=="__main__":
#     main(sys.argv)
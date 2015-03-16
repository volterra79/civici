# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CiviciEditor
                                 A QGIS plugin
 Custo Editor for Arcadia
                              -------------------
        begin                : 2015-02-04
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Arcadia
        email                : arcadia@arcadia.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os.path
from mywidget import *
import resources_rc
from qgis.core import QgsMapLayerRegistry
from qgis.gui import QgsMessageBar
from databaseConnection import build_table_from_database_table
from utils import get_layer_name_from_metadata
PATH = os.path.dirname(__file__)
tcolumn, trows, col_num, row_num = build_table_from_database_table()


class CiviciEditor:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface

        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.mapcanvas = iface.mapCanvas()
        self.activeLayer = None
        self.selectedcivico = None
        self.projectMainWindow = self.iface.mainWindow()
        self.mapregistry = QgsMapLayerRegistry.instance()
        self.mapregistry.layersAdded.connect(self.added_Layer)
        self.myTable = MyTable(tcolumn, trows, row_num,  col_num)
        self.customEditorDock = None
        self.scrollArea = QtGui.QScrollArea()
        palette = self.scrollArea.palette()
        palette.setColor(self.scrollArea.backgroundRole(), Qt.white)
        self.scrollArea.setPalette(palette)
        self.createRing = False
        self.stackedWidget = MyStackedWidget(mapcanvas=self.mapcanvas, widgetTable=self.myTable)

        self.scrollArea.setWidget(self.stackedWidget)
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CiviciEditor_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&CiviciEditor')
        # TODO: We are    going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CiviciEditor')
        self.toolbar.setObjectName(u'CiviciEditor')


    def added_Layer(self,layer):
        layer = layer[0]
        layer_name = get_layer_name_from_metadata(layer)
        if layer_name == 'civici':
            self.civicilayer = layer
            self.civicoindex = self.civicilayer.fieldNameIndex('codcivico')
            layer.featureAdded.connect(self.setFeatureId)
            layer.undoStack().indexChanged.connect(self.undoStackChanged)

    def tr(self, message):

        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CiviciEditor', message)


    def add_action(self, icon_path, text, callback, enabled_flag=True,
                         add_to_menu=True, add_to_toolbar=True, status_tip=None,
                         whats_this=None, parent=None ):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':icons/civ_t.png'

        self.action = self.add_action(
            icon_path,
            text=self.tr(u'Civici Editor'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.trigger()



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&CiviciEditor'),
                action)
            self.iface.removeToolBarIcon(action)
        self.iface.removeDockWidget(self.customEditorDock)




    def openMyWidget(self):

        self.stackedWidget.addMyWidget()




    def setFeatureId(self,feat_id):
        print(feat_id)

        self.feat_id = feat_id


    def before_rollback(self):

        self.stackedWidget.removeMyWidget(get_layer_name_from_metadata(self.activeLayer))




    def undoStackChanged(self,id):

        command = self.civicilayer.undoStack().command(id-1)
        if command and command.actionText() == 'add feature':
            if self.myTable.selectedcivico:
                self.civicilayer.changeAttributeValue(self.feat_id, self.civicoindex, self.myTable.selectedcivico)
            else:

                self.iface.messageBar().pushMessage("Warning", "Ooops, please select a table row before you add a new feature", level=QgsMessageBar.WARNING)

                self.civicilayer.undoStack().undo()



    def run(self):
        """Run method that performs all the real work"""
        #self.iface.TEST = self.stackedWidget


        if not self.customEditorDock:



            self.customEditorDock = CustomCiviciEditDockWidget(action=self.action, parent=self.projectMainWindow)

            self.customEditorDock.setWidget(self.stackedWidget)




        if self.action.isChecked():

                self.action.setIcon(QIcon(':icons/civ.png'))
                self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.customEditorDock)
                self.openMyWidget()



        else:
                self.action.setIcon(QIcon(':icons/civ_t.png'))
                self.iface.removeDockWidget(self.customEditorDock)







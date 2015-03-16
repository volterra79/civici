__author__ = 'francesco'

from qgis.core import QgsProject

""" EVENTS ON LAYER """
# layer.layerModified.connect(self.logLayerModified)
# layer.attributeAdded.connect(self.logAttributeAdded)
# layer.attributeDeleted.connect(self.logAttributeDeleted)
# layer.featureAdded.connect(self.logFeatureAdded)
# layer.featureDeleted.connect(self.logFeatureDeleted)
# layer.featureDeleted.connect(self.logGeometryChanged)
# layer.beforeCommitChanges.connect(self.logBeforeLayerCommitChange)
# layer.AttributeValueChanged.connect(self.logAttributeValueChanged)
# layer.editingStarted.connec(funzione) – viene atticato quando si clicca su start editing layer

def get_all_Layers_in_the_project():

        #to be filterd only the layer that we want
        root = QgsProject.instance().layerTreeRoot()
        for lyr in root.children():
            # print('Start Loop')
            # print(lyr.layerName())
            lyr.layer().editingStarted.connect(bind_start_editing_on_layer(lyr))
            lyr.layer().editingStopped.connect(bind_end_editing_on_layer(lyr))


##START END END EDITING SLOT FUNCTIONS

def bind_start_editing_on_layer(self,layer):
        def print_name(name=layer.layerName()):
            print('Start Editing '+str(name))
        return print_name

def bind_end_editing_on_layer(self,layer):

        def print_name(name=layer.layerName()):
            print('Stop Editing '+str(name))

        return print_name

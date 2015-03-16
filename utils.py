def get_layer_name_from_metadata(layer):
        layerNamefromMetadata = layer.metadata().split('table="base_geo".')[1].split(' (geom)')[0].replace('"','')
        return layerNamefromMetadata
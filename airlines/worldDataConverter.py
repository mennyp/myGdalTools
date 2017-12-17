from osgeo import gdal, osr, ogr
import numpy as np
import os
import csv
import json



def runPolitic(shpfilepath):
    datasource = ogr.Open(shpfilepath, 1)

    layer = datasource.GetLayer()
    print(layer.GetFeatureCount())
    dict = {}
    for ids, feature in enumerate(layer):
        poly = feature.GetGeometryRef()
        name = feature.GetField("NAME")

        area = poly.GetArea()
        id = feature.GetFID()
        if(dict.__contains__(name)):
            if(dict[name]['area'] > area):
                continue
        dict[name] = {'area': area, 'id': id}

    for politic in dict:
        f = layer.GetFeature(dict[politic]['id'])
        f.SetField("Name2", politic)
        layer.SetFeature(f)
        print politic

    print 's'

runPolitic("/home/menny/World_data/politic.shp")
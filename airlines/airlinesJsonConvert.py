from osgeo import gdal, osr, ogr
import numpy as np
import os
import csv
import json



def convertAirlines(jsonfilepath, pointShpFilePath, lineShpFilePath):
    # d = {}
    with open(jsonfilepath) as json_data:
        d = json.load(json_data)
        print(d)
    airlines = d["response"]["points"]
    # for point in airlines:
    #     print('{} {}'.format(point, airlines[point][0]))

    # Save extent to a new Shapefile
    outShapefile = pointShpFilePath
    outDriver = ogr.GetDriverByName("ESRI Shapefile")

    # Remove output shapefile if it already exists
    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)

    # Create the output shapefile
    outDataSource = outDriver.CreateDataSource(outShapefile)
    outLayer = outDataSource.CreateLayer("airlinesPoint", geom_type=ogr.wkbPoint)

    # create a field
    idField = ogr.FieldDefn("id", ogr.OFTInteger)
    nameField = ogr.FieldDefn('Name', ogr.OFTString)
    outLayer.CreateField(idField)
    outLayer.CreateField(nameField)

    index = 0
    for airLineName in airlines:
        # create point geometry
        try:
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(airlines[airLineName][0], airlines[airLineName][1])

            # Create the feature and set values
            featureDefn = outLayer.GetLayerDefn()
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(point)
            outFeature.SetField('id', index)
            outFeature.SetField('Name', airLineName)
            outLayer.CreateFeature(outFeature)
            print ('create {}'.format(airLineName))
            index = index + 1

        except ValueError:
            print "error"
    print ('shp {} created with success'.format(pointShpFilePath))

    airlineConnections = d["response"]["connections"]
    # for connection in airlineConnections:
    #     print connection   #{u'point_two': u'GITLA', u'point_one': u'VELOX', u'id': u'r290', u'name': u'UW13A'}


    # Save extent to a new Shapefile
    outShapefile = lineShpFilePath
    outDriver = ogr.GetDriverByName("ESRI Shapefile")

    # Remove output shapefile if it already exists
    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)

    # Create the output shapefile
    outDataSource = outDriver.CreateDataSource(outShapefile)
    outLayer = outDataSource.CreateLayer("airlinesLine", geom_type=ogr.wkbLineString)

    # create a field
    idField = ogr.FieldDefn("id", ogr.OFTInteger)
    airIdField = ogr.FieldDefn('AirId', ogr.OFTString)
    nameField = ogr.FieldDefn('Name', ogr.OFTString)
    outLayer.CreateField(idField)
    outLayer.CreateField(airIdField)
    outLayer.CreateField(nameField)

    index = 0
    for connection in airlineConnections:
        # create point geometry
        try:
            line = ogr.Geometry(ogr.wkbLineString)
            airLineName = connection['point_one']
            line.AddPoint(airlines[airLineName][0], airlines[airLineName][1])
            airLineName = connection['point_two']
            line.AddPoint(airlines[airLineName][0], airlines[airLineName][1])

            # Create the feature and set values
            featureDefn = outLayer.GetLayerDefn()
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(line)
            outFeature.SetField('id', index)
            outFeature.SetField('AirId', connection['id'])
            outFeature.SetField('Name', connection['name'])
            outLayer.CreateFeature(outFeature)
            print ('create {}'.format(connection))
            index = index + 1

        except ValueError:
            print "error"
    print ('shp {} created with success'.format(lineShpFilePath))

    outFeature = None
    outLayer = None
    outDataSource = None


convertAirlines(r"C:\Users\mennypi\PycharmProjects\gdalTools\Routes_Dec_2017.json", r"C:\Users\mennypi\PycharmProjects\gdalTools\airlinesPoint.shp", r"C:\Users\mennypi\PycharmProjects\gdalTools\airlinesPolyline.shp")
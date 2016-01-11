# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpatialDecisionDockWidget
                                 A QGIS plugin
 This is a SDSS template for the GEO1005 course
                             -------------------
        begin                : 2015-11-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Jorge Gil, TU Delft
        email                : j.a.lopesgil@tudelft.nl
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

from PyQt4 import QtGui, QtCore, uic
from qgis.core import *
from qgis.gui import *
from qgis.networkanalysis import *
import processing

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Initialize Qt resources from file resources.py
import resources
import os
import os.path
import random
import csv

from . import utility_functions as uf


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fire_interface_updated.ui'))


class SpatialDecisionDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = QtCore.pyqtSignal()
    #custom signals
    updateAttribute = QtCore.pyqtSignal(str)

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(SpatialDecisionDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # define globals
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # set up GUI operation signals
        # general tab
        self.firelocationbutton.clicked.connect(self.locatefire)
        self.policebutton.clicked.connect(self.locatepolicestation)
        self.firetruckbutton.clicked.connect(self.locatefirestation)
        self.ambulancebutton.clicked.connect(self.locatehospital)

        # data tab
        self.iface.projectRead.connect(self.updateLayers)
        self.iface.newProjectCreated.connect(self.updateLayers)
        self.iface.legendInterface().itemRemoved.connect(self.updateLayers)
        self.iface.legendInterface().itemAdded.connect(self.updateLayers)
        self.clearlayercombo.activated.connect(self.clearselectedlayer)
        self.selectlayercombo.activated.connect(self.setSelectedLayer)

        # analysis tab
        self.graph = QgsGraph()
        self.tied_points = []
        self.shortestroutebutton.clicked.connect(self.shortestroad)
        self.cheanroutebutton.clicked.connect(self.deleteRoutes)
        self.hydrantsbutton.clicked.connect(self.gethydrants)
        self.cleanwatersourcebutton.clicked.connect(self.cleanhydrants)
        self.smokebufferbutton.clicked.connect(self.smokebuffer)
        self.buildingbutton.clicked.connect(self.getintersectingbuildings)
        self.buildingupdate.clicked.connect(self.updatebuilding)

        # reporting tab
        self.showinfo.clicked.connect(self.showinfooffire)

        # save tab
        self.savemapbutton.clicked.connect(self.saveMap)

        # set current UI restrictions
        # add button icons
        self.firelocationbutton.setIcon(QtGui.QIcon(':icons/FIRE.png'))
        self.policebutton.setIcon(QtGui.QIcon(':icons/police-car2.png'))
        self.firetruckbutton.setIcon(QtGui.QIcon(':icons/1.png'))
        self.ambulancebutton.setIcon(QtGui.QIcon(':icons/ambulance2.png'))
        self.hydrantsbutton.setIcon(QtGui.QIcon(':icons/hydrantsicon.png'))
        self.cleanwatersourcebutton.setIcon(QtGui.QIcon(':icons/hydrantsicon2.png'))
        self.smokebufferbutton.setIcon(QtGui.QIcon(':icons/Transparent_Smoke_Clipart_PNG_Image.png'))
        self.buildingbutton.setIcon(QtGui.QIcon(':icons/building-20clip-20art-12065771771975582164reporter_flat.svg.med.png'))

#######
#   General functions
#######

    # load the scenario
    def locatefire(self,layer,filename=""):
        scenario_open = False
        scenario_file = os.path.join('C:\\GEO1005-Fire\\Scenario','Scenario.qgs')
        # check if file exists
        if os.path.isfile(scenario_file):
            self.iface.addProject(scenario_file)
            aLayer = uf.getLegendLayerByName(self.iface,"Event")
            blayer = uf.getLegendLayerByName(self.iface,"Building")
            clayer = uf.getLegendLayerByName(self.iface,"Obstacles")
            dlayer = uf.getLegendLayerByName(self.iface, "Road")
            layerriver = uf.getLegendLayerByName(self.iface, "River")
            layerlist = [aLayer,blayer,clayer, dlayer,layerriver]
            legend = self.iface.legendInterface()  # access the legend
            layers = uf.getLegendLayers(self.iface, 'all', 'all')
            # do something else
            for layer1 in layerlist:
                legend.setLayerVisible(layer1, True)  # show the layer
            scenario_open = True
        else:
            last_dir = uf.getLastDir("SDSS")
            new_file = QtGui.QFileDialog.getOpenFileName(self, "", last_dir, "(*.qgs)")
            if new_file:
                self.iface.addProject(new_file)
                scenario_open = True
        if scenario_open:
            self.updateLayers()

    # load the fire station
    def locatefirestation(self):
        firestation = uf.getLegendLayerByName(self.iface,"Fire_Station")
        legend = self.iface.legendInterface()
        legend.setLayerVisible(firestation, True)

    # load the police station
    def locatepolicestation(self):
        firestation = uf.getLegendLayerByName(self.iface,"Police_Station")
        legend = self.iface.legendInterface()
        legend.setLayerVisible(firestation, True)

    # load the hospital
    def locatehospital(self):
        firestation = uf.getLegendLayerByName(self.iface,"Hospital")
        legend = self.iface.legendInterface()
        legend.setLayerVisible(firestation, True)

#######
#   Data functions
#######

    # update layer
    def updateLayers(self):
        layers = uf.getLegendLayers(self.iface, 'all', 'all')
        self.selectlayercombo.clear()
        self.clearlayercombo.clear()
        if layers:
            layer_names = uf.getLayersListNames(layers)
            self.selectlayercombo.addItems(layer_names)
            self.clearlayercombo.addItems(layer_names)
            self.setSelectedLayer()
            self.clearselectedlayer()
        else:
            self.selectattributecombo.clear()
            #self.clearChart()

    # set a layer
    def setSelectedLayer(self):
        layer_name = self.selectlayercombo.currentText()
        layer = uf.getLegendLayerByName(self.iface,layer_name)
        legend = self.iface.legendInterface()  # access the legend
        legend.setLayerVisible(layer, True)
        self.updateAttributes(layer)

    # get the selected layer
    def getSelectedLayer(self):
        layer_name = self.selectlayercombo.currentText()
        layer = uf.getLegendLayerByName(self.iface,layer_name)
        return layer

    # clear the selected layer
    def clearselectedlayer(self):
        layer_name = self.selectlayercombo.currentText()
        namelist = ["Fire_Station","Hospital","Police_Station","Building","Road","Origin_Destination","Pedestrian",
                    "River","Fire_Hydrant","Obstacles","Smoke","Event","Water_Buffers"]
        if layer_name in namelist:
            layer = uf.getLegendLayerByName(self.iface,layer_name)
            legend = self.iface.legendInterface()
            legend.setLayerVisible(layer, False)
            self.refreshCanvas(layer)

    # update the attributes
    def updateAttributes(self, layer):
        self.selectattributecombo.clear()
        if layer:
            fields = uf.getFieldNames(layer)
            if fields:
                self.selectattributecombo.addItems(fields)
                self.setSelectedAttribute()

    # set the selected attributes
    def setSelectedAttribute(self):
        field_name = self.selectattributecombo.currentText()
        self.updateAttribute.emit(field_name)

#######
#    Analysis functions
#######

    # route functions
    # take origin and destination into consideration
    def tiepoints(self):
        tiepointslayer= QgsMapLayerRegistry.instance().mapLayersByName("Origin_Destination")[0]
        tiedpoints=[]
        for f in tiepointslayer.getFeatures():
            tiedpoints.append(f.geometry().asPoint())
        return tiedpoints

    # get the road network (including obstacles)
    def getNetwork(self):
        roads_layer = QgsMapLayerRegistry.instance().mapLayersByName("Road")[0]
        path = "%s/styles/" % QgsProject.instance().homePath()
        roads_layer.loadNamedStyle("%sroad.qml" % path)
        roads_layer.triggerRepaint()
        self.iface.legendInterface().refreshLayerSymbology(roads_layer)
        self.canvas.refresh()

        if roads_layer:
            # see if there is an obstacles layer to subtract roads from the network
            obstacles_layer = QgsMapLayerRegistry.instance().mapLayersByName("Obstacles")[0]
            f = obstacles_layer.getFeatures()
            lf = []
            for i in f:
                lf.append(i.geometry())

            if obstacles_layer:
                # retrieve roads outside obstacles (inside = False)
                features = uf.getFeaturesByIntersection(roads_layer, obstacles_layer, False)
                # add these roads to a new temporary layer
                road_network = uf.createTempLayer('Temp_Network','LINESTRING',roads_layer.crs().postgisSrid(),[],[])
                road_network.dataProvider().addFeatures(features)
                text = "%s obstacles were taken into consideration." % len(lf)
                self.insertReport1(text)
            else:
                road_network = roads_layer
            return road_network
        else:
            return

    # calculate the shortest path
    def shortestroad(self):
        graph = None
        roads_layer =self.getNetwork()
        points = self.tiepoints()
        if roads_layer:
            director = QgsLineVectorLayerDirector( roads_layer, -1, '', '', '', 3 )
            properter = QgsDistanceArcProperter()
            director.addProperter( properter )
            builder = QgsGraphBuilder(roads_layer.crs())
            pstart=points[0]
            pend=points[1]
            tiedPoints = director.makeGraph( builder, [ pstart, pend ] )
            graph = builder.graph()
            tstart = tiedPoints[ 0 ]
            tend = tiedPoints[ 1 ]
            idStart = graph.findVertex( tstart )
            idStop = graph.findVertex( tend )
            ( tree, cost ) = QgsGraphAnalyzer.dijkstra( graph, idStart, 0 )
            if tree[ idStop ] == -1:
                text= "Path not found."
                self.insertReport1(text)
            else:
                p = []
                curPos = idStop
                while curPos != idStart:
                    p.append( graph.vertex( graph.arc( tree[ curPos ] ).inVertex() ).point() )
                    curPos = graph.arc( tree[ curPos ] ).outVertex()
                p.append( tstart )
                text= "Path found."
                self.insertReport1(text)
                routes_layer = uf.getLegendLayerByName(self.iface,"Shortest_Route")
                # create one if it doesn't exist
                if not routes_layer:
                    attribs = ['ID']
                    types = [QtCore.QVariant.String]
                    routes_layer = uf.createTempLayer('Shortest_Route','LINESTRING',roads_layer.crs().postgisSrid(), attribs, types)
                    path = "%s/styles/" % QgsProject.instance().homePath()
                    routes_layer.loadNamedStyle("%sshortest_route.qml" % path)
                    routes_layer.triggerRepaint()
                    self.iface.legendInterface().refreshLayerSymbology(routes_layer)
                    self.canvas.refresh()
                    uf.loadTempLayer(routes_layer)
                    routes_layer.setLayerName('Shortest_Route')

                    legend = self.iface.legendInterface()
                    legend.setLayerVisible(routes_layer, True)
                    # insert route line

                    uf.insertTempFeatures(routes_layer, [p], [['1',100.00]])

                else:
                    legend = self.iface.legendInterface()
                    legend.setLayerVisible(routes_layer, True)
                    uf.loadTempLayer(routes_layer)

                    uf.insertTempFeatures(routes_layer, [p], [['1',100.00]])
                    self.refreshCanvas(routes_layer)

        rl = uf.getLegendLayerByName(self.iface,"Shortest_Route")
        feature = rl.getFeatures()
        list= []
        for f in feature:
            list.append(f.geometry())
        text1 = "Route length is %s km. " % round((list[0].length())/1000.0,3)
        self.insertReport1(text1)

    # delete the calculated route
    def deleteRoutes(self):
        text3="Route deleted."
        self.insertReport1(text3)
        routes_layer = uf.getLegendLayerByName(self.iface,"Shortest_Route")
        if routes_layer:
            ids = uf.getAllFeatureIds(routes_layer)
            routes_layer.startEditing()
            for id in ids:
                routes_layer.deleteFeature(id)
            routes_layer.commitChanges()

    # report window functions
    def insertReport1(self,item):
        self.reportList1.insertItem(0, item)

    # fire hydrants functions
    # read the buffer distance
    def getBufferCutoff(self):
        cutoff = self.bufferCutoffEdit.text()
        if uf.isNumeric(cutoff):
            return uf.convertNumeric(cutoff)
        else:
            return 0

    # calculate the buffer of the fire hydrants
    def calculateBuffer(self):
        layer = uf.getLegendLayerByName(self.iface, "Event")
        origins = layer.getFeatures()
        if origins > 0:
            cutoff_distance = self.getBufferCutoff()
            buffers = {}
            for point in origins:
                geom = point.geometry()
                buffers[point.id()] = geom.buffer(cutoff_distance,12).asPolygon()
            # store the buffer results in temporary layer called "Buffers"
            buffer_layer = uf.getLegendLayerByName(self.iface, "Water_Buffers")
            # create one if it doesn't exist
            if not buffer_layer:
                attribs = ['ID', 'DISTANCE']
                types = [QtCore.QVariant.String, QtCore.QVariant.Double]
                buffer_layer = uf.createTempLayer('Water_Buffers','POLYGON',layer.crs().postgisSrid(), attribs, types)
                buffer_layer.setLayerName('Water_Buffers')
                uf.loadTempLayer(buffer_layer)
                legend = self.iface.legendInterface()
                legend.setLayerVisible(buffer_layer, False)

            # insert buffer polygons
            geoms = []
            values = []
            for buffer in buffers.iteritems():
                # each buffer has an id and a geometry
                geoms.append(buffer[1])
                # in the case of values, it expects a list of multiple values in each item - list of lists
                values.append([buffer[0], cutoff_distance])
            uf.insertTempFeatures(buffer_layer, geoms, values)
            self.refreshCanvas(buffer_layer)

    # show fire hydrants due to a buffer
    def gethydrants(self):
        hydrants_layer=uf.getLegendLayerByName(self.iface, "Fire_Hydrant")
        self.calculateBuffer()
        event_buffer = uf.getLegendLayerByName(self.iface,"Water_Buffers")

        features=uf.getFeaturesByIntersection(hydrants_layer,event_buffer,True)
        available_hydrant = uf.getLegendLayerByName(self.iface,"Available_Hydrants")

        if not available_hydrant:
            attribs=['ID']
            types=[QtCore.QVariant.Point]
            available_hydrant=uf.createTempLayer('Available_Hydrants','Point',hydrants_layer.crs().postgisSrid(), attribs, types)

            path = "%s/styles/" % QgsProject.instance().homePath()
            available_hydrant.loadNamedStyle("%shydrants.qml" % path)
            available_hydrant.triggerRepaint()
            self.iface.legendInterface().refreshLayerSymbology(available_hydrant)
            self.canvas.refresh()

            uf.loadTempLayer(available_hydrant)
            available_hydrant.setLayerName('Available_Hydrants')
            legend = self.iface.legendInterface()
            legend.setLayerVisible(available_hydrant, True)
            available_hydrant.dataProvider().addFeatures(features)
            available_hydrant = uf.getLegendLayerByName(self.iface,"Available_Hydrants")
        else:
            uf.loadTempLayer(available_hydrant)
            available_hydrant.dataProvider().addFeatures(features)
            self.refreshCanvas(available_hydrant)

    # delete fire hydrants
    def cleanhydrants(self):
        ah = uf.getLegendLayerByName(self.iface,"Available_Hydrants")
        event_buffer = uf.getLegendLayerByName(self.iface,"Water_Buffers")

        if ah:
            QgsMapLayerRegistry.instance().removeMapLayers( [ah.id()] )
        if event_buffer:
            QgsMapLayerRegistry.instance().removeMapLayers( [event_buffer.id()])

    # smoke functions
    # show the smoke layer
    def smokebuffer(self):
        smoke_buffer=uf.getLegendLayerByName(self.iface, "Smoke")
        legend = self.iface.legendInterface()  # access the legend
        legend.setLayerVisible(smoke_buffer, True)
        self.updateAttributes(smoke_buffer)

    # threatened area functions
    # intersection of building layer with smoke layer
    def getintersectingbuildings(self):
        building_layer=uf.getLegendLayerByName(self.iface, "Building")
        smoke_buffer = uf.getLegendLayerByName(self.iface,"Smoke")
        features=uf.getFeaturesByIntersection(building_layer,smoke_buffer,True)
        threat_build = uf.getLegendLayerByName(self.iface, "Threatened_Buildings")
        if not threat_build:
            attribs=['TYPE_BUILD','NUM_DAY','NUM_NIGHT']
            types=[QtCore.QVariant.String, QtCore.QVariant.Double, QtCore.QVariant.Double]
            threat_build = uf.createTempLayer("Threatened_Buildings","POLYGON",building_layer.crs().postgisSrid(), attribs, types)
            threat_build.setLayerName("Threatened_Buildings")
            uf.loadTempLayer(threat_build)
            legend = self.iface.legendInterface()
            legend.setLayerVisible(threat_build, True)
            threat_build.dataProvider().addFeatures(features)
            self.refreshCanvas(threat_build)

        else:
            threat_build.setLayerName("Threatened_Buildings")
            uf.loadTempLayer(threat_build)
            threat_build.dataProvider().addFeatures(features)
            self.refreshCanvas(threat_build)

    # update the building layer
    def updatebuilding(self):
        tb = uf.getLegendLayerByName(self.iface, "Threatened_Buildings")
        if tb:
            ids = uf.getAllFeatureIds(tb)
            tb.startEditing()
            for id in ids:
                tb.deleteFeature(id)
            tb.commitChanges()

        if tb:
            building_layer=uf.getLegendLayerByName(self.iface, "Building")
            smoke_buffer = uf.getLegendLayerByName(self.iface,"Smoke")
            features=uf.getFeaturesByIntersection(building_layer,smoke_buffer,True)
            uf.loadTempLayer(tb)
            tb.dataProvider().addFeatures(features)
            self.refreshCanvas(threat_build)

    # after adding features to layers needs a refresh (sometimes)
    def refreshCanvas(self, layer):
        if self.canvas.isCachingEnabled():
            layer.setCacheImage(None)
        else:
            self.canvas.refresh()

#######
#    Reporting functions
#######

    # connect the report lists with functions
    def insertAfBui(self,item):
        self.reportList_3.insertItem(0, item)

    def insertTyBui(self,item):
        self.reportList_11.insertItem(0, item)

    def insertAfPop(self,item):
        self.reportList_4.insertItem(0, item)

    def insertTrBui(self,item):
        self.reportList_5.insertItem(0, item)

    def insertTrPopD(self,item):
        self.reportList_6.insertItem(0, item)

    def insertTrPopN(self,item):
        self.reportList_7.insertItem(0, item)

    def insertStartFire(self,item):
        self.reportList_8.insertItem(0, item)

    def insertEndFire(self,item):
        self.reportList_10.insertItem(0, item)

    # select information from the attribute tables
    def showinfooffire(self):
        self.reportList_3.clear()
        layer_3=uf.getLegendLayerByName(self.iface, "Event")
        lextext_3=uf.getFieldNames(layer_3)
        fieldname_3=lextext_3[0]
        extext_3=uf.getFieldValues(layer_3, fieldname_3, null=True, selection=False)
        lextext_3=extext_3[0]
        text_3=len(lextext_3)
        self.insertAfBui(str(text_3))
        #----------------------
        self.reportList_11.clear()
        layer_11=uf.getLegendLayerByName(self.iface, "Event")
        lextext_11=uf.getFieldNames(layer_11)
        fieldname_11=lextext_11[0]
        extext_11=uf.getFieldValues(layer_11, fieldname_11, null=True, selection=False)
        text_11=str(extext_11[0][0])
        self.insertTyBui(text_11)
        #-----------------------
        self.reportList_4.clear()
        layer_4=uf.getLegendLayerByName(self.iface, "Event")
        lextext_4=uf.getFieldNames(layer_4)
        fieldname_4=lextext_4[1]
        extext_4=uf.getFieldValues(layer_4, fieldname_4, null=True, selection=False)
        text_4=str(extext_4[0][0])
        self.insertAfPop(text_4)
        #------------------------
        self.reportList_5.clear()
        layer_5=uf.getLegendLayerByName(self.iface, "Threatened_Buildings")
        lextext_5=uf.getFieldNames(layer_5)
        fieldname_5=lextext_5[0]
        extext_5=uf.getFieldValues(layer_5, fieldname_5, null=True, selection=False)
        lextext_5=len(extext_5[0])
        text_5= str(lextext_5)
        self.insertTrBui(text_5)
        #------------------------
        self.reportList_6.clear()
        layer_6=uf.getLegendLayerByName(self.iface, "Threatened_Buildings")
        lextext_6=uf.getFieldNames(layer_6)
        fieldname_6=lextext_6[1]
        extext_6=uf.getFieldValues(layer_6, fieldname_6, null=True, selection=False)
        numday2=0
        for i in extext_6[0]:
            numday2=(numday2)+int(i)
        text_6= str(numday2)
        self.insertTrPopD(text_6)
        #----------------------------
        self.reportList_7.clear()
        layer_7=uf.getLegendLayerByName(self.iface, "Threatened_Buildings")
        lextext_7=uf.getFieldNames(layer_7)
        fieldname_7=lextext_7[2]
        extext_7=uf.getFieldValues(layer_7, fieldname_7, null=True, selection=False)
        numnight3=0
        for i in extext_7[0]:
            numnight3=numnight3+int(i)
        text_7=str(numnight3)
        self.insertTrPopN(text_7)
        #---------------------
        self.reportList_8.clear()
        layer_8=uf.getLegendLayerByName(self.iface, "Event")
        lextext_8=uf.getFieldNames(layer_8)
        fieldname_8=lextext_8[2]
        extext_8=uf.getFieldValues(layer_8, fieldname_8, null=True, selection=False)
        text_8=str(extext_8[0][0])
        self.insertStartFire(text_8)
        #-------------------------------
        self.reportList_10.clear()
        layer_10=uf.getLegendLayerByName(self.iface, "Event")
        lextext_10=uf.getFieldNames(layer_10)
        fieldname_10=lextext_10[3]
        extext_10=uf.getFieldValues(layer_10, fieldname_10, null=True, selection=False)
        text_10=str(extext_10[0][0])
        self.insertEndFire(text_10)

#######
#    Saving functions
#######

    # saving the current screen
    def saveMap(self):
        path = "%s/Map.png" % QgsProject.instance().homePath()
        self.canvas.saveAsImage(path,None,"PNG")


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
        # general
        self.firelocationbutton.clicked.connect(self.locatefire)
        self.policebutton.clicked.connect(self.locatepolicestation)
        self.firetruckbutton.clicked.connect(self.locatefirestation)
        self.ambulancebutton.clicked.connect(self.locatehospital)

        # data
        self.iface.projectRead.connect(self.updateLayers)
        self.iface.newProjectCreated.connect(self.updateLayers)
        self.iface.legendInterface().itemRemoved.connect(self.updateLayers)
        self.iface.legendInterface().itemAdded.connect(self.updateLayers)
        self.clearlayercombo.activated.connect(self.clearselectedlayer)
        self.selectlayercombo.activated.connect(self.setSelectedLayer)

        # analysis
        self.graph = QgsGraph()
        self.tied_points = []
        self.networkbutton.clicked.connect(self.getNetwork)
        self.shortestroutebutton.clicked.connect(self.shortestroad)
        self.cheanroutebutton.clicked.connect(self.deleteRoutes)
        self.hydrantsbutton.clicked.connect(self.gethydrants)
        self.cleanwatersourcebutton.clicked.connect(self.cleanhydrants)
        self.smokebufferbutton.clicked.connect(self.smokebuffer)
        self.buildingbutton.clicked.connect(self.getintersectingbuildings)
        self.buildingupdate.clicked.connect(self.updatebuilding)

        # visualisation
        # MAYA ----------------------------------------------
        self.showinfo.clicked.connect(self.showinfooffire)
        # ---------------------------------------------------

        # reporting
        self.savemapbutton.clicked.connect(self.saveMap)
        #self.updateAttribute.connect(self.extractAttributeSummary)
        #self.saveStatisticsButton.clicked.connect(self.saveTable)

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



    def closeEvent(self, event):
        # disconnect interface signals
        try:
            self.iface.projectRead.disconnect(self.updateLayers)
            self.iface.newProjectCreated.disconnect(self.updateLayers)
            self.iface.legendInterface().itemRemoved.disconnect(self.updateLayers)
            self.iface.legendInterface().itemAdded.disconnect(self.updateLayers)
        except:
            pass

        self.closingPlugin.emit()
        event.accept()

#######
#   General functions
#######
    def locatefire(self,layer,filename=""):
        scenario_open = False
        scenario_file = os.path.join('I:\\academic\\geo1005\\LAST\\GEO1005-Fire\\Project_data_new','Data.qgs')
        # check if file exists
        if os.path.isfile(scenario_file):
            self.iface.addProject(scenario_file)
            aLayer = uf.getLegendLayerByName(self.iface,"EVENT")
            blayer = uf.getLegendLayerByName(self.iface,"BUILDING")
            clayer = uf.getLegendLayerByName(self.iface,"OBSTACLES")
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

    def locatefirestation(self):
        firestation = uf.getLegendLayerByName(self.iface,"Fire_Station")
        legend = self.iface.legendInterface()
        legend.setLayerVisible(firestation, True)

    def locatepolicestation(self):
        firestation = uf.getLegendLayerByName(self.iface,"police_station")
        legend = self.iface.legendInterface()
        legend.setLayerVisible(firestation, True)

    def locatehospital(self):
        firestation = uf.getLegendLayerByName(self.iface,"hospital")
        legend = self.iface.legendInterface()
        legend.setLayerVisible(firestation, True)


#######
#   Data functions
#######

    def saveScenario(self):
        self.iface.actionSaveProject()

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


    def setSelectedLayer(self):
        layer_name = self.selectlayercombo.currentText()
        layer = uf.getLegendLayerByName(self.iface,layer_name)
        legend = self.iface.legendInterface()  # access the legend
        legend.setLayerVisible(layer, True)
        self.updateAttributes(layer)

    def getSelectedLayer(self):
        layer_name = self.selectlayercombo.currentText()
        layer = uf.getLegendLayerByName(self.iface,layer_name)
        return layer

    def clearselectedlayer(self):
        layer_name = self.selectlayercombo.currentText()
        namelist = ["Fire_Station","hospital","police_station","BUILDING","Road","Origin_Destination","Pedestrian",
                    "River","FIRE_HYDRANT","OBSTACLES","SMOKE","EVENT","Water_Buffers"]
        if layer_name in namelist:
            layer = uf.getLegendLayerByName(self.iface,layer_name)
            legend = self.iface.legendInterface()
            legend.setLayerVisible(layer, False)
            self.refreshCanvas(layer)


    def updateAttributes(self, layer):
        self.selectattributecombo.clear()
        if layer:
            #self.clearReport()
            #self.clearChart()
            fields = uf.getFieldNames(layer)
            if fields:
                self.selectattributecombo.addItems(fields)
                self.setSelectedAttribute()
                # send list to the report list window
                #self.updateReport(fields)


    def setSelectedAttribute(self):
        field_name = self.selectattributecombo.currentText()
        self.updateAttribute.emit(field_name)

    def getSelectedAttribute(self):
        field_name = self.selectattributecombo.currentText()
        return field_name

#######
#    Analysis functions
#######
    # route functions
    def tiepoints(self):

        tiepointslayer= QgsMapLayerRegistry.instance().mapLayersByName("Origin_Destination")[0]
        tiedpoints=[]
        for f in tiepointslayer.getFeatures():
            tiedpoints.append(f.geometry().asPoint())
        return tiedpoints

    def getNetwork(self):

        roads_layer = QgsMapLayerRegistry.instance().mapLayersByName("Road")[0]
        path = "%s/styles/" % QgsProject.instance().homePath()
        roads_layer.loadNamedStyle("%sroads.qml" % path)
        roads_layer.triggerRepaint()
        self.iface.legendInterface().refreshLayerSymbology(roads_layer)
        self.canvas.refresh()

        if roads_layer:
            # see if there is an obstacles layer to subtract roads from the network
            obstacles_layer = QgsMapLayerRegistry.instance().mapLayersByName("OBSTACLES")[0]
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
                text = "%s obstacles found" % len(lf)
                self.insertReport1(text)
            else:
                road_network = roads_layer
            return road_network
        else:
            return

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
                text= "Path not found"
                self.insertReport1(text)
            else:
                p = []
                curPos = idStop
                while curPos != idStart:
                    p.append( graph.vertex( graph.arc( tree[ curPos ] ).inVertex() ).point() )
                    curPos = graph.arc( tree[ curPos ] ).outVertex()
                p.append( tstart )
                text= "Path found"
                self.insertReport1(text)
                routes_layer = uf.getLegendLayerByName(self.iface,"Shortest_Route")
                # create one if it doesn't exist
                if not routes_layer:
                    attribs = ['id']
                    types = [QtCore.QVariant.String]
                    routes_layer = uf.createTempLayer('Shortest_Route','LINESTRING',roads_layer.crs().postgisSrid(), attribs, types)
                    path = "%s/styles/" % QgsProject.instance().homePath()
                    routes_layer.loadNamedStyle("%ssr.qml" % path)
                    routes_layer.triggerRepaint()
                    self.iface.legendInterface().refreshLayerSymbology(routes_layer)
                    self.canvas.refresh()
                    uf.loadTempLayer(routes_layer)
                    routes_layer.setLayerName('Shortest_Route')

                    legend = self.iface.legendInterface()
                    legend.setLayerVisible(routes_layer, True)
                    # insert route line

                    uf.insertTempFeatures(routes_layer, [p], [['testing',100.00]])

                else:
                    legend = self.iface.legendInterface()
                    legend.setLayerVisible(routes_layer, True)
                    uf.loadTempLayer(routes_layer)

                    uf.insertTempFeatures(routes_layer, [p], [['testing',100.00]])
                    self.refreshCanvas(routes_layer)

        rl = uf.getLegendLayerByName(self.iface,"Shortest_Route")
        feature = rl.getFeatures()
        list= []
        for f in feature:
            list.append(f.geometry())
        text1 = "Route length is %s km " % round((list[0].length())*100.0,3)
        self.insertReport1(text1)


    def deleteRoutes(self):
        text3="route deleted"
        self.insertReport1(text3)
        routes_layer = uf.getLegendLayerByName(self.iface,"Shortest_Route")
        if routes_layer:
            ids = uf.getAllFeatureIds(routes_layer)
            routes_layer.startEditing()
            for id in ids:
                routes_layer.deleteFeature(id)
            routes_layer.commitChanges()



    def getServiceAreaCutoff(self):
        cutoff = self.serviceAreaCutoffEdit.text()
        if uf.isNumeric(cutoff):
            return uf.convertNumeric(cutoff)
        else:
            return 0

    def calculateServiceArea(self):
        options = len(self.tied_points)
        if options > 0:
            # origin is given as an index in the tied_points list
            origin = random.randint(1,options-1)
            cutoff_distance = self.getServiceAreaCutoff()
            if cutoff_distance == 0:
                return
            service_area = uf.calculateServiceArea(self.graph, self.tied_points, origin, cutoff_distance)
            # store the service area results in temporary layer called "Service_Area"
            area_layer = uf.getLegendLayerByName(self.iface, "Service_Area")
            # create one if it doesn't exist
            if not area_layer:
                attribs = ['cost']
                types = [QtCore.QVariant.Double]
                area_layer = uf.createTempLayer('Service_Area','POINT',self.network_layer.crs().postgisSrid(), attribs, types)
                uf.loadTempLayer(area_layer)
            # insert service area points
            geoms = []
            values = []
            for point in service_area.itervalues():
                # each point is a tuple with geometry and cost
                geoms.append(point[0])
                # in the case of values, it expects a list of multiple values in each item - list of lists
                values.append([cutoff_distance])
            uf.insertTempFeatures(area_layer, geoms, values)
            self.refreshCanvas(area_layer)

# buffer functions
    def getBufferCutoff(self):
        cutoff = self.bufferCutoffEdit.text()
        if uf.isNumeric(cutoff):
            return uf.convertNumeric(cutoff)
        else:
            return 0

    def calculateBuffer(self):
        layer = uf.getLegendLayerByName(self.iface, "EVENT")
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
                attribs = ['id', 'distance']
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

# VAGOS
    def gethydrants(self):
        hydrants_layer=uf.getLegendLayerByName(self.iface, "FIRE_HYDRANT")
        self.calculateBuffer()
        event_buffer = uf.getLegendLayerByName(self.iface,"Water_Buffers")

        features=uf.getFeaturesByIntersection(hydrants_layer,event_buffer,True)
        available_hydrant = uf.getLegendLayerByName(self.iface,"available_hydrants")

        if not available_hydrant:
            attribs=['id']
            types=[QtCore.QVariant.Point]
            available_hydrant=uf.createTempLayer('available_hydrants','Point',hydrants_layer.crs().postgisSrid(), attribs, types)

            path = "%s/styles/" % QgsProject.instance().homePath()
            available_hydrant.loadNamedStyle("%shydrants.qml" % path)
            available_hydrant.triggerRepaint()
            self.iface.legendInterface().refreshLayerSymbology(available_hydrant)
            self.canvas.refresh()

            uf.loadTempLayer(available_hydrant)
            available_hydrant.setLayerName('available_hydrants')
            legend = self.iface.legendInterface()
            legend.setLayerVisible(available_hydrant, True)
            available_hydrant.dataProvider().addFeatures(features)
            available_hydrant = uf.getLegendLayerByName(self.iface,"available_hydrants")
        else:
            uf.loadTempLayer(available_hydrant)
            available_hydrant.dataProvider().addFeatures(features)
            self.refreshCanvas(available_hydrant)


    def cleanhydrants(self):
        ah = uf.getLegendLayerByName(self.iface,"available_hydrants")
        event_buffer = uf.getLegendLayerByName(self.iface,"Water_Buffers")

        if ah:
            QgsMapLayerRegistry.instance().removeMapLayers( [ah.id()] )
        if event_buffer:
            QgsMapLayerRegistry.instance().removeMapLayers( [event_buffer.id()])
    # -----------------

# MAYA
    def getintersectingbuildings(self):
        building_layer=uf.getLegendLayerByName(self.iface, "BUILDING")
        smoke_buffer = uf.getLegendLayerByName(self.iface,"SMOKE")
        features=uf.getFeaturesByIntersection(building_layer,smoke_buffer,True)

        threat_build = uf.getLegendLayerByName(self.iface, "THREATENED_BUILD")
        if not threat_build:
            attribs=['TYPE_BUILD','NUM_DAY','NUM_NIGHT']
            types=[QtCore.QVariant.String, QtCore.QVariant.Double, QtCore.QVariant.Double]
            threat_build = uf.createTempLayer("THREATENED_BUILD","POLYGON",building_layer.crs().postgisSrid(), attribs, types)
            threat_build.setLayerName("THREATENED_BUILD")

            uf.loadTempLayer(threat_build)
            legend = self.iface.legendInterface()
            legend.setLayerVisible(threat_build, True)
            threat_build.dataProvider().addFeatures(features)
            self.refreshCanvas(threat_build)

        else:
            threat_build.setLayerName("THREATENED_BUILD")
            uf.loadTempLayer(threat_build)
            threat_build.dataProvider().addFeatures(features)
            self.refreshCanvas(threat_build)


    def updatebuilding(self):
        tb = uf.getLegendLayerByName(self.iface, "THREATENED_BUILD")
        if tb:
            ids = uf.getAllFeatureIds(tb)
            tb.startEditing()
            for id in ids:
                tb.deleteFeature(id)
            tb.commitChanges()

        if tb:
            building_layer=uf.getLegendLayerByName(self.iface, "BUILDING")
            smoke_buffer = uf.getLegendLayerByName(self.iface,"SMOKE")
            features=uf.getFeaturesByIntersection(building_layer,smoke_buffer,True)
            uf.loadTempLayer(tb)
            tb.dataProvider().addFeatures(features)
            self.refreshCanvas(threat_build)


    # SHOW THE SMOKE, NEED CORRECTION WITH TIME MANAGER
    def smokebuffer(self):
        smoke_buffer=uf.getLegendLayerByName(self.iface, "SMOKE")
        legend = self.iface.legendInterface()  # access the legend
        legend.setLayerVisible(smoke_buffer, True)
        self.updateAttributes(smoke_buffer)

    # NEED CORRECTIONS
    def updatesmoke(self):
        self.smokebuffer()

    # CHANGE IT WITH THIS ONE??
    def removesmoke(self):
        ah = uf.getLegendLayerByName(self.iface, "SMOKE")
        if ah:
            ids = uf.getAllFeatureIds(ah)
            ah.startEditing()
            for id in ids:
                ah.deleteFeature(id)
            ah.commitChanges()
            uf.loadTempLayer(ah)
    # --------------------------------------------------------------------------

    # after adding features to layers needs a refresh (sometimes)
    def refreshCanvas(self, layer):
        if self.canvas.isCachingEnabled():
            layer.setCacheImage(None)
        else:
            self.canvas.refresh()

    # feature selection
    def selectFeaturesBuffer(self):
        layer = self.getSelectedLayer()
        buffer_layer = uf.getLegendLayerByName(self.iface, "Buffers")
        if buffer_layer and layer:
            uf.selectFeaturesByIntersection(layer, buffer_layer, True)

    def selectFeaturesRange(self):
        layer = self.getSelectedLayer()
        # for the range takes values from the service area (max) and buffer (min) text edits
        max = self.getServiceAreaCutoff()
        min = self.getBufferCutoff()
        if layer and max and min:
            # gets list of numeric fields in layer
            fields = uf.getNumericFields(layer)
            if fields:
                # selects features with values in the range
                uf.selectFeaturesByRangeValues(layer, fields[0].name(), min, max)

    def selectFeaturesExpression(self):
        layer = self.getSelectedLayer()
        uf.selectFeaturesByExpression(layer, self.expressionEdit.text())

    def filterFeaturesExpression(self):
        layer = self.getSelectedLayer()
        uf.filterFeaturesByExpression(layer, self.expressionEdit.text())


#######
#    Visualisation functions
#######
    # MAYA ----------------------------------------------
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

    def showinfooffire(self):

        #----------------------
        self.reportList_3.clear()
        layer_3=uf.getLegendLayerByName(self.iface, "EVENT")
        lextext_3=uf.getFieldNames(layer_3)
        fieldname_3=lextext_3[0]
        extext_3=uf.getFieldValues(layer_3, fieldname_3, null=True, selection=False)
        lextext_3=extext_3[0]
        text_3=len(lextext_3)
        self.insertAfBui(str(text_3))

        #----------------------
        self.reportList_11.clear()
        layer_11=uf.getLegendLayerByName(self.iface, "EVENT")
        lextext_11=uf.getFieldNames(layer_11)
        fieldname_11=lextext_11[0]
        extext_11=uf.getFieldValues(layer_11, fieldname_11, null=True, selection=False)
        text_11=str(extext_11[0][0])
        self.insertTyBui(text_11)

        #-----------------------
        self.reportList_4.clear()
        layer_4=uf.getLegendLayerByName(self.iface, "EVENT")
        lextext_4=uf.getFieldNames(layer_4)
        fieldname_4=lextext_4[1]
        extext_4=uf.getFieldValues(layer_4, fieldname_4, null=True, selection=False)
        text_4=str(extext_4[0][0])
        self.insertAfPop(text_4)

        #------------------------
        self.reportList_5.clear()
        layer_5=uf.getLegendLayerByName(self.iface, "THREATENED_BUILD")
        lextext_5=uf.getFieldNames(layer_5)
        fieldname_5=lextext_5[0]
        extext_5=uf.getFieldValues(layer_5, fieldname_5, null=True, selection=False)
        lextext_5=len(extext_5[0])
        text_5= str(lextext_5)

        self.insertTrBui(text_5)

        #------------------------
        self.reportList_6.clear()
        layer_6=uf.getLegendLayerByName(self.iface, "THREATENED_BUILD")
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
        layer_7=uf.getLegendLayerByName(self.iface, "THREATENED_BUILD")
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
        layer_8=uf.getLegendLayerByName(self.iface, "EVENT")
        lextext_8=uf.getFieldNames(layer_8)
        fieldname_8=lextext_8[2]
        extext_8=uf.getFieldValues(layer_8, fieldname_8, null=True, selection=False)
        text_8=str(extext_8[0][0])
        self.insertStartFire(text_8)

        #-------------------------------
        self.reportList_10.clear()
        layer_10=uf.getLegendLayerByName(self.iface, "EVENT")
        lextext_10=uf.getFieldNames(layer_10)
        fieldname_10=lextext_10[3]
        extext_10=uf.getFieldValues(layer_10, fieldname_10, null=True, selection=False)
        text_10=str(extext_10[0][0])
        self.insertEndFire(text_10)

    # ---------------------------------------------------------------------------
    def displayBenchmarkStyle(self):
        # loads a predefined style on a layer.
        # Best for simple, rule based styles, and categorical variables
        # attributes and values classes are hard coded in the style
        layer = uf.getLegendLayerByName(self.iface, "Obstacles")
        path = "%s/styles/" % QgsProject.instance().homePath()
        # load a categorical style
        layer.loadNamedStyle("%sobstacle_danger.qml" % path)
        layer.triggerRepaint()
        self.iface.legendInterface().refreshLayerSymbology(layer)

        # load a simple style
        layer = uf.getLegendLayerByName(self.iface, "Buffers")
        layer.loadNamedStyle("%sbuffer.qml" % path)
        layer.triggerRepaint()
        self.iface.legendInterface().refreshLayerSymbology(layer)
        self.canvas.refresh()

    def displayContinuousStyle(self):
        # produces a new symbology renderer for graduated style
        layer = self.getSelectedLayer()
        attribute = self.getSelectedAttribute()
        # define several display parameters
        display_settings = {}
        # define the interval type and number of intervals
        # EqualInterval = 0; Quantile  = 1; Jenks = 2; StdDev = 3; Pretty = 4;
        display_settings['interval_type'] = 1
        display_settings['intervals'] = 10
        # define the line width
        display_settings['line_width'] = 0.5
        # define the colour ramp
        # the ramp's bottom and top colour. These are RGB tuples that can be edited
        ramp = QgsVectorGradientColorRampV2(QtGui.QColor(0, 0, 255, 255), QtGui.QColor(255, 0, 0, 255), False)
        # any other stops for intermediate colours for greater control. can be edited or skipped
        ramp.setStops([QgsGradientStop(0.25, QtGui.QColor(0, 255, 255, 255)),
                       QgsGradientStop(0.5, QtGui.QColor(0,255,0,255)),
                       QgsGradientStop(0.75, QtGui.QColor(255, 255, 0, 255))])
        display_settings['ramp'] = ramp
        # call the update renderer function
        renderer = uf.updateRenderer(layer, attribute, display_settings)
        # update the canvas
        if renderer:
            layer.setRendererV2(renderer)
            layer.triggerRepaint()
            self.iface.legendInterface().refreshLayerSymbology(layer)
            self.canvas.refresh()

    def plotChart(self):
        plot_layer = self.getSelectedLayer()
        if plot_layer:
            attribute = self.getSelectedAttribute()
            if attribute:
                numeric_fields = uf.getNumericFieldNames(plot_layer)

                # draw a histogram from numeric values
                if attribute in numeric_fields:
                    values = uf.getAllFeatureValues(plot_layer, attribute)
                    n, bins, patches = self.chart_subplot_hist.hist(values, 50, normed=False)
                else:
                    self.chart_subplot_hist.cla()

                # draw a simple line plot
                self.chart_subplot_line.cla()
                x1 = range(20)
                y1 = random.sample(range(1, 100), 20)
                self.chart_subplot_line.plot(x1 , y1 , 'r.-')

                # draw a simple bar plot
                labels = ('Critical', 'Risk', 'Safe')
                self.chart_subplot_bar.cla()
                self.chart_subplot_bar.bar(1.2, y1[0], width=0.7, alpha=1, color='red', label=labels[0])
                self.chart_subplot_bar.bar(2.2, y1[5], width=0.7, alpha=1, color='yellow', label=labels[1])
                self.chart_subplot_bar.bar(3.2, y1[10], width=0.7, alpha=1, color='green', label=labels[2])
                self.chart_subplot_bar.set_xticks((1.5,2.5,3.5))
                self.chart_subplot_bar.set_xticklabels(labels)

                # draw a simple pie chart
                self.chart_subplot_pie.cla()
                total = float(y1[0]+y1[5]+y1[10])
                sizes = [
                    (y1[0]/total)*100.0,
                    (y1[5]/total)*100.0,
                    (y1[10]/total)*100.0,
                ]
                colours = ('lightcoral', 'gold', 'yellowgreen')
                self.chart_subplot_pie.pie(sizes, labels=labels, colors=colours, autopct='%1.1f%%', shadow=True, startangle=90)
                self.chart_subplot_pie.axis('equal')

                # draw all the plots
                self.chart_canvas.draw()
            else:
                self.clearChart()

    #def clearChart(self):
        #self.chart_subplot_hist.cla()
        #self.chart_subplot_line.cla()
        #self.chart_subplot_bar.cla()
        #self.chart_subplot_pie.cla()
        #self.chart_canvas.draw()


#######
#    Reporting functions
#######
    # update a text edit field
    def updateNumberFeatures(self):
        layer = self.getSelectedLayer()
        if layer:
            count = layer.featureCount()
            self.featureCounterEdit.setText(str(count))

    # selecting a file for saving
    def selectFile(self):
        last_dir = uf.getLastDir("SDSS")
        path = QtGui.QFileDialog.getSaveFileName(self, "Save map file", last_dir, "PNG (*.png)")
        if path.strip()!="":
            path = unicode(path)
            uf.setLastDir(path,"SDSS")
            self.saveMapPathEdit.setText(path)

    # saving the current screen
    def saveMap(self):
        path = "%s/map.png" % QgsProject.instance().homePath()
        self.canvas.saveAsImage(path,None,"PNG")

    def extractAttributeSummary(self, attribute):
        # get summary of the attribute
        layer = self.getSelectedLayer()
        summary = []
        # only use the first attribute in the list
        for feature in layer.getFeatures():
            summary.append((feature.id(), feature.attribute(attribute)))
        # send this to the table
        self.clearTable()
        self.updateTable(summary)

    # report window functions
    def updateReport(self,report):
        self.reportList.clear()
        self.reportList.addItems(report)

    def insertReport1(self,item):
        self.reportList1.insertItem(0, item)

    def insertReport(self,item):
        self.reportList.insertItem(0, item)

    def clearReport(self):
        self.reportList.clear()

    # table window functions
    def updateTable(self, values):
        # takes a list of label / value pairs, can be tuples or lists. not dictionaries to control order
        self.statisticsTable.setColumnCount(2)
        self.statisticsTable.setHorizontalHeaderLabels(["Item","Value"])
        self.statisticsTable.setRowCount(len(values))
        for i, item in enumerate(values):
            # i is the table row, items mus tbe added as QTableWidgetItems
            self.statisticsTable.setItem(i,0,QtGui.QTableWidgetItem(str(item[0])))
            self.statisticsTable.setItem(i,1,QtGui.QTableWidgetItem(str(item[1])))
        self.statisticsTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.statisticsTable.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.statisticsTable.resizeRowsToContents()

    def clearTable(self):
        self.statisticsTable.clear()

    def saveTable(self):
        path = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
        if path:
            with open(unicode(path), 'wb') as stream:
                # open csv file for writing
                writer = csv.writer(stream)
                # write header
                header = []
                for column in range(self.statisticsTable.columnCount()):
                    item = self.statisticsTable.horizontalHeaderItem(column)
                    header.append(unicode(item.text()).encode('utf8'))
                writer.writerow(header)
                # write data
                for row in range(self.statisticsTable.rowCount()):
                    rowdata = []
                    for column in range(self.statisticsTable.columnCount()):
                        item = self.statisticsTable.item(row, column)
                        if item is not None:
                            rowdata.append(
                                unicode(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fire_interface_updated.ui'
#
# Created: Thu Dec 17 13:42:16 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(515, 741)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.Visualisation = QtGui.QTabWidget(self.dockWidgetContents)
        self.Visualisation.setGeometry(QtCore.QRect(10, 10, 491, 681))
        self.Visualisation.setObjectName(_fromUtf8("Visualisation"))
        self.generaltab = QtGui.QWidget()
        self.generaltab.setWhatsThis(_fromUtf8(""))
        self.generaltab.setAccessibleName(_fromUtf8(""))
        self.generaltab.setObjectName(_fromUtf8("generaltab"))
        self.ccslabel = QtGui.QLabel(self.generaltab)
        self.ccslabel.setGeometry(QtCore.QRect(80, 10, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.ccslabel.setFont(font)
        self.ccslabel.setObjectName(_fromUtf8("ccslabel"))
        self.firelabel = QtGui.QLabel(self.generaltab)
        self.firelabel.setGeometry(QtCore.QRect(190, 50, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.firelabel.setFont(font)
        self.firelabel.setObjectName(_fromUtf8("firelabel"))
        self.firelocationbutton = QtGui.QPushButton(self.generaltab)
        self.firelocationbutton.setGeometry(QtCore.QRect(120, 110, 211, 111))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.firelocationbutton.setFont(font)
        self.firelocationbutton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.firelocationbutton.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("FIRE.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.firelocationbutton.setIcon(icon)
        self.firelocationbutton.setIconSize(QtCore.QSize(100, 100))
        self.firelocationbutton.setObjectName(_fromUtf8("firelocationbutton"))
        self.chooseservicelabel = QtGui.QLabel(self.generaltab)
        self.chooseservicelabel.setGeometry(QtCore.QRect(20, 280, 251, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.chooseservicelabel.setFont(font)
        self.chooseservicelabel.setObjectName(_fromUtf8("chooseservicelabel"))
        self.policebutton = QtGui.QPushButton(self.generaltab)
        self.policebutton.setGeometry(QtCore.QRect(20, 340, 121, 101))
        self.policebutton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("police-car2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.policebutton.setIcon(icon1)
        self.policebutton.setIconSize(QtCore.QSize(130, 130))
        self.policebutton.setObjectName(_fromUtf8("policebutton"))
        self.firetruckbutton = QtGui.QPushButton(self.generaltab)
        self.firetruckbutton.setGeometry(QtCore.QRect(160, 340, 131, 101))
        self.firetruckbutton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.firetruckbutton.setIcon(icon2)
        self.firetruckbutton.setIconSize(QtCore.QSize(100, 120))
        self.firetruckbutton.setObjectName(_fromUtf8("firetruckbutton"))
        self.ambulancebutton = QtGui.QPushButton(self.generaltab)
        self.ambulancebutton.setGeometry(QtCore.QRect(320, 340, 131, 101))
        self.ambulancebutton.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("ambulance2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ambulancebutton.setIcon(icon3)
        self.ambulancebutton.setIconSize(QtCore.QSize(110, 110))
        self.ambulancebutton.setObjectName(_fromUtf8("ambulancebutton"))
        self.generalline = QtGui.QFrame(self.generaltab)
        self.generalline.setGeometry(QtCore.QRect(10, 250, 471, 16))
        self.generalline.setFrameShape(QtGui.QFrame.HLine)
        self.generalline.setFrameShadow(QtGui.QFrame.Sunken)
        self.generalline.setObjectName(_fromUtf8("generalline"))
        self.Visualisation.addTab(self.generaltab, _fromUtf8(""))
        self.datatab = QtGui.QWidget()
        self.datatab.setObjectName(_fromUtf8("datatab"))
        self.openscenariobutton = QtGui.QPushButton(self.datatab)
        self.openscenariobutton.setGeometry(QtCore.QRect(20, 20, 141, 51))
        self.openscenariobutton.setObjectName(_fromUtf8("openscenariobutton"))
        self.savescenariobutton = QtGui.QPushButton(self.datatab)
        self.savescenariobutton.setGeometry(QtCore.QRect(170, 20, 241, 51))
        self.savescenariobutton.setObjectName(_fromUtf8("savescenariobutton"))
        self.selectlayerlabel = QtGui.QLabel(self.datatab)
        self.selectlayerlabel.setGeometry(QtCore.QRect(10, 120, 111, 41))
        self.selectlayerlabel.setObjectName(_fromUtf8("selectlayerlabel"))
        self.selectlayercombo = QtGui.QComboBox(self.datatab)
        self.selectlayercombo.setGeometry(QtCore.QRect(150, 120, 271, 31))
        self.selectlayercombo.setObjectName(_fromUtf8("selectlayercombo"))
        self.locatefireline = QtGui.QFrame(self.datatab)
        self.locatefireline.setGeometry(QtCore.QRect(10, 90, 411, 20))
        self.locatefireline.setFrameShape(QtGui.QFrame.HLine)
        self.locatefireline.setFrameShadow(QtGui.QFrame.Sunken)
        self.locatefireline.setObjectName(_fromUtf8("locatefireline"))
        self.datatime = QtGui.QTimeEdit(self.datatab)
        self.datatime.setGeometry(QtCore.QRect(250, 490, 151, 41))
        self.datatime.setWrapping(False)
        self.datatime.setCurrentSection(QtGui.QDateTimeEdit.SecondSection)
        self.datatime.setObjectName(_fromUtf8("datatime"))
        self.selectattributelabel = QtGui.QLabel(self.datatab)
        self.selectattributelabel.setGeometry(QtCore.QRect(10, 160, 151, 41))
        self.selectattributelabel.setObjectName(_fromUtf8("selectattributelabel"))
        self.selectattributecombo = QtGui.QComboBox(self.datatab)
        self.selectattributecombo.setGeometry(QtCore.QRect(150, 170, 271, 31))
        self.selectattributecombo.setObjectName(_fromUtf8("selectattributecombo"))
        self.Visualisation.addTab(self.datatab, _fromUtf8(""))
        self.analysistab = QtGui.QWidget()
        self.analysistab.setStyleSheet(_fromUtf8(""))
        self.analysistab.setObjectName(_fromUtf8("analysistab"))
        self.hydrantsbutton = QtGui.QPushButton(self.analysistab)
        self.hydrantsbutton.setGeometry(QtCore.QRect(20, 180, 141, 121))
        self.hydrantsbutton.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("hydrantsicon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hydrantsbutton.setIcon(icon4)
        self.hydrantsbutton.setIconSize(QtCore.QSize(120, 120))
        self.hydrantsbutton.setObjectName(_fromUtf8("hydrantsbutton"))
        self.shortestroutebutton = QtGui.QPushButton(self.analysistab)
        self.shortestroutebutton.setGeometry(QtCore.QRect(10, 100, 181, 51))
        self.shortestroutebutton.setObjectName(_fromUtf8("shortestroutebutton"))
        self.cheanroutebutton = QtGui.QPushButton(self.analysistab)
        self.cheanroutebutton.setGeometry(QtCore.QRect(210, 100, 191, 51))
        self.cheanroutebutton.setObjectName(_fromUtf8("cheanroutebutton"))
        self.smokebufferbutton = QtGui.QPushButton(self.analysistab)
        self.smokebufferbutton.setGeometry(QtCore.QRect(20, 340, 141, 111))
        self.smokebufferbutton.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8("Transparent_Smoke_Clipart_PNG_Image.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.smokebufferbutton.setIcon(icon5)
        self.smokebufferbutton.setIconSize(QtCore.QSize(120, 120))
        self.smokebufferbutton.setObjectName(_fromUtf8("smokebufferbutton"))
        self.buildingbutton = QtGui.QPushButton(self.analysistab)
        self.buildingbutton.setGeometry(QtCore.QRect(20, 480, 141, 111))
        self.buildingbutton.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8("building-20clip-20art-12065771771975582164reporter_flat.svg.med.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buildingbutton.setIcon(icon6)
        self.buildingbutton.setIconSize(QtCore.QSize(150, 100))
        self.buildingbutton.setObjectName(_fromUtf8("buildingbutton"))
        self.updatesmokebutton = QtGui.QPushButton(self.analysistab)
        self.updatesmokebutton.setGeometry(QtCore.QRect(210, 370, 171, 41))
        self.updatesmokebutton.setObjectName(_fromUtf8("updatesmokebutton"))
        self.networkbutton = QtGui.QPushButton(self.analysistab)
        self.networkbutton.setGeometry(QtCore.QRect(10, 30, 181, 51))
        self.networkbutton.setObjectName(_fromUtf8("networkbutton"))
        self.buildingupdate = QtGui.QPushButton(self.analysistab)
        self.buildingupdate.setGeometry(QtCore.QRect(210, 520, 171, 41))
        self.buildingupdate.setObjectName(_fromUtf8("buildingupdate"))
        self.analysisline1 = QtGui.QFrame(self.analysistab)
        self.analysisline1.setGeometry(QtCore.QRect(0, 160, 481, 16))
        self.analysisline1.setFrameShape(QtGui.QFrame.HLine)
        self.analysisline1.setFrameShadow(QtGui.QFrame.Sunken)
        self.analysisline1.setObjectName(_fromUtf8("analysisline1"))
        self.getwatersourcelabel = QtGui.QLabel(self.analysistab)
        self.getwatersourcelabel.setGeometry(QtCore.QRect(20, 310, 141, 16))
        self.getwatersourcelabel.setObjectName(_fromUtf8("getwatersourcelabel"))
        self.buildingindangerlable = QtGui.QLabel(self.analysistab)
        self.buildingindangerlable.setGeometry(QtCore.QRect(20, 600, 181, 21))
        self.buildingindangerlable.setObjectName(_fromUtf8("buildingindangerlable"))
        self.cleanwatersourcebutton = QtGui.QPushButton(self.analysistab)
        self.cleanwatersourcebutton.setGeometry(QtCore.QRect(210, 180, 141, 121))
        self.cleanwatersourcebutton.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8("hydrantsicon2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cleanwatersourcebutton.setIcon(icon7)
        self.cleanwatersourcebutton.setIconSize(QtCore.QSize(100, 100))
        self.cleanwatersourcebutton.setObjectName(_fromUtf8("cleanwatersourcebutton"))
        self.addobstaclesbutton = QtGui.QPushButton(self.analysistab)
        self.addobstaclesbutton.setGeometry(QtCore.QRect(210, 30, 191, 51))
        self.addobstaclesbutton.setObjectName(_fromUtf8("addobstaclesbutton"))
        self.analysisline2 = QtGui.QFrame(self.analysistab)
        self.analysisline2.setGeometry(QtCore.QRect(-10, 320, 511, 16))
        self.analysisline2.setFrameShape(QtGui.QFrame.HLine)
        self.analysisline2.setFrameShadow(QtGui.QFrame.Sunken)
        self.analysisline2.setObjectName(_fromUtf8("analysisline2"))
        self.analysitime = QtGui.QTimeEdit(self.analysistab)
        self.analysitime.setGeometry(QtCore.QRect(320, 600, 141, 22))
        self.analysitime.setObjectName(_fromUtf8("analysitime"))
        self.label_4 = QtGui.QLabel(self.analysistab)
        self.label_4.setGeometry(QtCore.QRect(200, 310, 151, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.analysistab)
        self.label_5.setGeometry(QtCore.QRect(40, 450, 171, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.Visualisation.addTab(self.analysistab, _fromUtf8(""))
        self.visualizationtab = QtGui.QWidget()
        self.visualizationtab.setObjectName(_fromUtf8("visualizationtab"))
        self.timeEdit = QtGui.QTimeEdit(self.visualizationtab)
        self.timeEdit.setGeometry(QtCore.QRect(327, 571, 141, 31))
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.label = QtGui.QLabel(self.visualizationtab)
        self.label.setGeometry(QtCore.QRect(60, 150, 451, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.visualizationtab)
        self.label_2.setGeometry(QtCore.QRect(60, 270, 221, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.visualizationtab)
        self.label_3.setGeometry(QtCore.QRect(50, 390, 241, 51))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.Visualisation.addTab(self.visualizationtab, _fromUtf8(""))
        self.reporting = QtGui.QWidget()
        self.reporting.setObjectName(_fromUtf8("reporting"))
        self.featurecounterlabel = QtGui.QLabel(self.reporting)
        self.featurecounterlabel.setGeometry(QtCore.QRect(0, 20, 151, 41))
        self.featurecounterlabel.setObjectName(_fromUtf8("featurecounterlabel"))
        self.featuretext = QtGui.QTextEdit(self.reporting)
        self.featuretext.setGeometry(QtCore.QRect(130, 20, 191, 31))
        self.featuretext.setObjectName(_fromUtf8("featuretext"))
        self.updatefeaturebutton = QtGui.QPushButton(self.reporting)
        self.updatefeaturebutton.setGeometry(QtCore.QRect(330, 20, 91, 31))
        self.updatefeaturebutton.setObjectName(_fromUtf8("updatefeaturebutton"))
        self.savepathtest = QtGui.QTextEdit(self.reporting)
        self.savepathtest.setGeometry(QtCore.QRect(0, 60, 321, 31))
        self.savepathtest.setObjectName(_fromUtf8("savepathtest"))
        self.savepathbuton = QtGui.QPushButton(self.reporting)
        self.savepathbuton.setGeometry(QtCore.QRect(332, 57, 91, 31))
        self.savepathbuton.setObjectName(_fromUtf8("savepathbuton"))
        self.savemapbutton = QtGui.QPushButton(self.reporting)
        self.savemapbutton.setGeometry(QtCore.QRect(110, 100, 141, 41))
        self.savemapbutton.setObjectName(_fromUtf8("savemapbutton"))
        self.reportingtext1 = QtGui.QTextEdit(self.reporting)
        self.reportingtext1.setGeometry(QtCore.QRect(0, 150, 431, 141))
        self.reportingtext1.setObjectName(_fromUtf8("reportingtext1"))
        self.reportingtext2 = QtGui.QTextEdit(self.reporting)
        self.reportingtext2.setGeometry(QtCore.QRect(0, 300, 431, 141))
        self.reportingtext2.setObjectName(_fromUtf8("reportingtext2"))
        self.reportingtime = QtGui.QTimeEdit(self.reporting)
        self.reportingtime.setGeometry(QtCore.QRect(280, 470, 151, 41))
        self.reportingtime.setWrapping(False)
        self.reportingtime.setCurrentSection(QtGui.QDateTimeEdit.SecondSection)
        self.reportingtime.setObjectName(_fromUtf8("reportingtime"))
        self.Visualisation.addTab(self.reporting, _fromUtf8(""))
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        self.Visualisation.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget", None))
        self.ccslabel.setText(_translate("DockWidget", "Command and Control System", None))
        self.firelabel.setText(_translate("DockWidget", "FIRE", None))
        self.firelocationbutton.setText(_translate("DockWidget", "Fire Location", None))
        self.chooseservicelabel.setText(_translate("DockWidget", "Choose Service:", None))
        self.Visualisation.setTabText(self.Visualisation.indexOf(self.generaltab), _translate("DockWidget", "General", None))
        self.openscenariobutton.setText(_translate("DockWidget", "Open Scenario", None))
        self.savescenariobutton.setText(_translate("DockWidget", "Save Scenario", None))
        self.selectlayerlabel.setText(_translate("DockWidget", "Select Layer:", None))
        self.selectattributelabel.setText(_translate("DockWidget", "Select attribute:", None))
        self.Visualisation.setTabText(self.Visualisation.indexOf(self.datatab), _translate("DockWidget", "Data", None))
        self.analysistab.setToolTip(_translate("DockWidget", "<html><head/><body><p><br/></p></body></html>", None))
        self.shortestroutebutton.setText(_translate("DockWidget", "Shortest Route", None))
        self.cheanroutebutton.setText(_translate("DockWidget", "Clean Route", None))
        self.updatesmokebutton.setText(_translate("DockWidget", "Update Smoke ", None))
        self.networkbutton.setText(_translate("DockWidget", "Road Network", None))
        self.buildingupdate.setText(_translate("DockWidget", "Update Buildings", None))
        self.getwatersourcelabel.setText(_translate("DockWidget", "Get Water sources", None))
        self.buildingindangerlable.setText(_translate("DockWidget", "Get Buildings in Danger", None))
        self.addobstaclesbutton.setText(_translate("DockWidget", "Add Obstacles", None))
        self.label_4.setText(_translate("DockWidget", "Clean water sources", None))
        self.label_5.setText(_translate("DockWidget", "Get Smoke Area", None))
        self.Visualisation.setTabText(self.Visualisation.indexOf(self.analysistab), _translate("DockWidget", "Analysis", None))
        self.label.setText(_translate("DockWidget", "Population needed evacuation", None))
        self.label_2.setText(_translate("DockWidget", "Fire Duration", None))
        self.label_3.setText(_translate("DockWidget", "Affected Buildings", None))
        self.Visualisation.setTabText(self.Visualisation.indexOf(self.visualizationtab), _translate("DockWidget", "Visualisation", None))
        self.featurecounterlabel.setText(_translate("DockWidget", "Feature counter:", None))
        self.updatefeaturebutton.setText(_translate("DockWidget", "Update", None))
        self.savepathbuton.setText(_translate("DockWidget", "...", None))
        self.savemapbutton.setText(_translate("DockWidget", "Save map", None))
        self.Visualisation.setTabText(self.Visualisation.indexOf(self.reporting), _translate("DockWidget", "Reporting", None))

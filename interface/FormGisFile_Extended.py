from interface.FormGisFile import Ui_FormGisFile
from PyQt5 import QtCore, QtGui, QtWidgets
from file_io import FileReadWrite
from application import ApplicationProperty
from parameter import GisParameter

class FormGisFile(Ui_FormGisFile):

    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.addSocket()
        self.addValidatior()

        self.siteList = []
        self.initialSetting()
        self.isModified = False

        #this boolean variable was used in order to access this form from "Model Run" module
        self.editMode = False

    def addSocket(self):
        self.btnSaveAs.clicked.connect(self.btnSaveAs_clicked)
        self.btnSave.clicked.connect(self.btnSave_clicked)
        self.btnClose.clicked.connect(self.btnClose_clicked)
        self.rbtNewGisFile.toggled.connect(self.rbtNewGisFile_toggled)
        self.btnGisFileBrowse.clicked.connect(self.btnGisFileBrowse_clicked)
        self.tableWidget.itemSelectionChanged.connect(self.tableWidget_itemSelectionChanged)
        self.tableWidget.itemPressed.connect(self.tableWidget_itemSelectionChanged)
        self.btnAddRow.clicked.connect(self.btnAddRow_clicked)
        self.btnEditRow.clicked.connect(self.btnEditRow_clicked)
        self.btnEditAndAdd.clicked.connect(self.btnEditAndAdd_clicked)
        self.btnDelete.clicked.connect(self.btnDelete_clicked)
        self.btnInitDirChoose.clicked.connect(self.btnInitDirChoose_clicked)
        self.btnSoilProfileFile.clicked.connect(self.btnSoilProfileFile_clicked)
        self.btnSoilHorizonFile.clicked.connect(self.btnSoilHorizonFile_clicked)
        self.btnMetFileBrowse.clicked.connect(self.btnMetFileBrowse_clicked)
        self.btnNdepFile.clicked.connect(self.btnNdepFile_clicked)

    def initialSetting(self):
        self.btnGisFileBrowse.setEnabled(False)
        self.txtInitialDirectory.setEnabled(False)
        # self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(27)
        columnHeaderText = ["Site Index", "No. of Veg Types", "Soil Profile Filename", "Soil Horizon Filename", "Profile Name", "Groundwater Depth (m)",
                            "Groundwater Model", "HSC Reduction Factor", "Dehumidification Parameter", "Dehumidification Depth",
                            "Soil Temp: Year Day of T0", "Soil Temp: Time Lag", "Soil Temp: Amplitude", "Soil Temp: Increase by Depth", "Site Elevation (m)",
                            "Site Latitude (decimal degree)", "Meteorological File", "No. Of Met. Years", "NDEP File", "N-Deposition Rate (kg/(m²*a))", "Industrial N-Deposition Rate (kg/(m²*a))",
                            "Water in Snow (mm)", "Fast microbial recycling pool (fraction)", "Medium microbial recycling pool (fraction)", "Slow microbial recycling pool (fraction)",
                            "Recalcitrant SOM (fraction)", "Soil N-min (kg/m²)"]
        self.tableWidget.setHorizontalHeaderLabels(columnHeaderText)

        for i in range(0, self.tableWidget.columnCount()):
            l = len(self.tableWidget.horizontalHeaderItem(i).text())
            self.tableWidget.setColumnWidth(i, int(l * 6 + 20))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.groundWaterOptionList = ['0. Dynamic', '1. Static']
        self.cmbGroundWaterFlag.addItems(self.groundWaterOptionList)
        self.cmbGroundWaterFlag.setCurrentIndex(-1)

        self.lockFields(True)
        self.btnEditRow.setEnabled(False)
        self.btnEditAndAdd.setEnabled(False)
        self.btnDelete.setEnabled(False)
        self.btnSave.setEnabled(False)
        self.btnSaveAs.setEnabled(False)
        # print(self.tableWidget.getColumnWidth(1))
        self.lblInitialDirectory.setVisible(False)
        self.label_67.setVisible(False)
        self.txtInitialDirectory.setVisible(False)
        self.btnInitDirChoose.setVisible(False)

    def addValidatior(self):
        rx = QtCore.QRegExp("^(19|20)\d{2}$")
        yearValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("^[0-9]*$")
        integerValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("^[\w\-.]+$")
        fileNameValidator= QtGui.QRegExpValidator(rx)

        self.txtGisFileName.setValidator(fileNameValidator)
        self.txtNoOfVegType.setValidator(integerValidator)
        self.txtSoilProfileFile.setValidator(fileNameValidator)
        self.txtSoilHorizonFile.setValidator(fileNameValidator)
        self.txtGroundWaterDepth.setValidator(decimalValidator)
        self.txtReductionFactor.setValidator(decimalValidator)
        self.txtDehumidificationParam.setValidator(decimalValidator)
        self.txtlDepthOfDehumidification.setValidator(decimalValidator)
        self.txtYearDay.setValidator(integerValidator)
        self.txtTemperaturTimeLag.setValidator(decimalValidator)
        self.txtAmplitudeofsoilTemperature.setValidator(decimalValidator)
        self.txtIncreaseOfTemperature.setValidator(decimalValidator)
        self.txtSiteElevation.setValidator(decimalValidator)
        self.txtSiteLatitude.setValidator(decimalValidator)
        self.txtNumberOfMeteorologicalYear.setValidator(integerValidator)
        self.txtNigrogenDepositionRate.setValidator(decimalValidator)
        self.txtIndustrialNitrogenDepTate.setValidator(decimalValidator)
        self.txtWaterInSnowPool.setValidator(decimalValidator)
        self.txtFastMicrobe.setValidator(decimalValidator)
        self.txtMediumMicrobe.setValidator(decimalValidator)
        self.txtSlowMicrobe.setValidator(decimalValidator)
        self.txtRecaltinationSOM.setValidator(decimalValidator)
        self.txtSoilMeneralNitrogetPool.setValidator(decimalValidator)

    def findSite(self, siteIndex):
        for site in self.siteList:
            if site.siteIndex == siteIndex:
                return site
        return None

    def addSite(self, site):
        for item in self.siteList:
            if item.siteIndex == site.siteIndex:
                QtGui.QMessageBox.about(self.form, 'Message', "This site is already added in the list.")
                break
        else:
            self.siteList.append(site)
            return True

        return False

    def editSite(self, site):
        for item in self.siteList:
            if item.siteIndex == site.siteIndex:
                item.noOfVegetation = site.noOfVegetation
                item.soilProfileFileName = site.soilProfileFileName
                item.soilHorizonFileName = site.soilHorizonFileName
                item.profileName = site.profileName
                item.groundWaterDepth = site.groundWaterDepth
                item.groundWaterFlag = site.groundWaterFlag
                item.reductionFactor = site.reductionFactor
                item.zetaParameter = site.zetaParameter
                item.depthOfDehumidification = site.depthOfDehumidification
                item.yearDay = site.yearDay
                item.temperatureTimeLag = site.temperatureTimeLag
                item.amplitudeOfSoilTemperature = site.amplitudeOfSoilTemperature
                item.increaseOfTemperature = site.increaseOfTemperature
                item.siteElevation = site.siteElevation
                item.siteLatitude = site.siteLatitude
                item.meteorologicalFileName = site.meteorologicalFileName
                item.noOfMeteorologicalYear = site.noOfMeteorologicalYear
                item.ndepFileName = site.ndepFileName
                item.ndepRate = site.ndepRate
                item.industrialNdepRate = site.industrialNdepRate
                item.snowWaterPool = site.snowWaterPool
                item.fastMicrobialFraction = site.fastMicrobialFraction
                item.mediumMicrobialFraction = site.mediumMicrobialFraction
                item.slowMicrobialFraction = site.slowMicrobialFraction
                item.recalcitrantSom = site.recalcitrantSom
                item.soilMineralNitrogenPool = site.soilMineralNitrogenPool
                break
        else:
            QtGui.QMessageBox.about(self.form, 'Message', "This site is not in the list.")
            return False
        return True

    def deleteSite(self, siteIndex):
        for site in self.siteList:
            if site.siteIndex == siteIndex:
                self.siteList.remove(site)
                break
        else:
            QtGui.QMessageBox.about(self.form, "Message", "There is no site found with same site index.")
            return False
        return True

    def createSiteWithInputValues(self):
        site = GisParameter()
        site.siteIndex = self.txtSiteIndex.text().strip()
        site.noOfVegetation = int(self.txtNoOfVegType.text().strip())
        site.soilProfileFileName = self.txtSoilProfileFile.text().strip()
        site.soilHorizonFileName = self.txtSoilHorizonFile.text().strip()
        site.profileName = self.txtProfileName.text().strip()
        site.groundWaterDepth = float(self.txtGroundWaterDepth.text().strip())
        site.groundWaterFlag = int(str(self.cmbGroundWaterFlag.currentIndex()))
        site.reductionFactor = float(self.txtReductionFactor.text().strip())
        site.zetaParameter = float(self.txtDehumidificationParam.text().strip())
        site.depthOfDehumidification = float(self.txtlDepthOfDehumidification.text().strip())
        site.yearDay = int(self.txtYearDay.text().strip())
        site.temperatureTimeLag = float(self.txtTemperaturTimeLag.text().strip())
        site.amplitudeOfSoilTemperature = float(self.txtAmplitudeofsoilTemperature.text().strip())
        site.increaseOfTemperature = float(self.txtIncreaseOfTemperature.text().strip())
        site.siteElevation = float(self.txtSiteElevation.text().strip())
        site.siteLatitude = float(self.txtSiteLatitude.text().strip())
        site.meteorologicalFileName = self.txtMeteorologicalFileName.text().strip()
        site.noOfMeteorologicalYear = int(self.txtNumberOfMeteorologicalYear.text().strip())
        site.ndepFileName = self.txtNdepFileName.text().strip()
        site.ndepRate = float(self.txtNigrogenDepositionRate.text().strip())
        site.industrialNdepRate = float(self.txtIndustrialNitrogenDepTate.text().strip())
        site.snowWaterPool = float(self.txtWaterInSnowPool.text().strip())
        site.fastMicrobialFraction = float(self.txtFastMicrobe.text().strip())
        site.mediumMicrobialFraction = float(self.txtMediumMicrobe.text().strip())
        site.slowMicrobialFraction = float(self.txtSlowMicrobe.text().strip())
        site.recalcitrantSom = float(self.txtRecaltinationSOM.text().strip())
        site.soilMineralNitrogenPool = float(self.txtSoilMeneralNitrogetPool.text().strip())
        return site

    def checkCompleteness(self):
        if len(self.txtSiteIndex.text().strip()) == 0:
            message = "Site index is missing. Please insert site index"
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSiteIndex.setFocus(True)
            return False
        elif len(self.txtNoOfVegType.text().strip()) == 0:
            message = "Please enter no. of vegetation types in current site."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtNoOfVegType.setFocus(True)
            return False
        elif len(self.txtSoilProfileFile.text().strip()) == 0:
            message = "Please enter Soil Profile File name."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSoilProfileFile.setFocus(True)
            return False
        elif len(self.txtSoilHorizonFile.text().strip()) == 0:
            message = "Please enter Soil Horizon File name."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSoilHorizonFile.setFocus(True)
            return False
        elif len(self.txtProfileName.text().strip()) == 0:
            message = "Please enter profile name."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtProfileName.setFocus(True)
            return False
        elif len(self.txtGroundWaterDepth.text().strip()) == 0:
            message = "Please enter ground water depth."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtGroundWaterDepth.setFocus(True)
            return False
        elif self.cmbGroundWaterFlag.currentIndex() == -1:
            message = "Please select ground water option."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.cmbGroundWaterFlag.setFocus(True)
            return False
        elif len(self.txtReductionFactor.text().strip()) == 0:
            message = "Please enter reduction factor for saturated hydraulic conductivity for infiltration."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtReductionFactor.setFocus(True)
            return False
        elif len(self.txtDehumidificationParam.text().strip()) == 0:
            message = "Please enter zeta parameter."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtDehumidificationParam.setFocus(True)
            return False
        elif len(self.txtlDepthOfDehumidification.text().strip()) == 0:
            message = "Please enter depth of dehumidification of bare soil."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtlDepthOfDehumidification.setFocus(True)
            return False
        elif len(self.txtYearDay.text().strip()) == 0:
            message = "Please enter day of a year for air temperature."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtYearDay.setFocus(True)
            return False
        elif len(self.txtTemperaturTimeLag.text().strip()) == 0:
            message = "Please enter factor describing temperature time lag with depth."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtTemperaturTimeLag.setFocus(True)
            return False
        elif len(self.txtAmplitudeofsoilTemperature.text().strip()) == 0:
            message = "Please enter amplitude of soil temperature in 250cm depth."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtAmplitudeofsoilTemperature.setFocus(True)
            return False
        elif len(self.txtIncreaseOfTemperature.text().strip()) == 0:
            message = "Please enter increase rate of temperature with depth."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtIncreaseOfTemperature.setFocus(True)
            return False
        elif len(self.txtSiteElevation.text().strip()) == 0:
            message = "Please enter site elevation above mean sea level."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSiteElevation.setFocus(True)
            return False
        elif len(self.txtSiteLatitude.text().strip()) == 0:
            message = "Please enter site latitude (decimal degrees)."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSiteLatitude.setFocus(True)
            return False
        elif len( self.txtMeteorologicalFileName.text().strip()) == 0:
            message = "Please enter Meteorological File name."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtMeteorologicalFileName.setFocus(True)
            return False
        elif len(self.txtNumberOfMeteorologicalYear.text().strip()) == 0:
            message = "Please enter number of meteorological years in meteorological file."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtNumberOfMeteorologicalYear.setFocus(True)
            return False
        elif len(self.txtNdepFileName.text().strip()) == 0:
            message = "Please enter Nitrogen Deposition File name."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtNdepFileName.setFocus(True)
            return False
        elif len(self.txtNigrogenDepositionRate.text().strip()) == 0:
            message = "Please enter annual rate of atmospheric nitrogen deposition."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtNigrogenDepositionRate.setFocus(True)
            return False
        elif len(self.txtIndustrialNitrogenDepTate.text().strip()) == 0:
            message = "Please enter industrial value of atmospheric nitrogen deposition rate."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtIndustrialNitrogenDepTate.setFocus(True)
            return False
        elif len(self.txtWaterInSnowPool.text().strip()) == 0:
            message = "Please enter amount of water in snow pool."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtWaterInSnowPool.setFocus(True)
            return False
        elif len(self.txtFastMicrobe.text().strip()) == 0:
            message = "Please enter the value for fraction of fast microbial recycling pool (soil carbon)."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtFastMicrobe.setFocus(True)
            return False
        elif len(self.txtMediumMicrobe.text().strip())== 0:
            message = "Please enter the value for fraction of medium microbial recycling pool (soil carbon)."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtMediumMicrobe.setFocus(True)
            return False
        elif len(self.txtSlowMicrobe.text().strip()) == 0:
            message = "Please enter the value for fraction of slow microbial recycling pool (soil carbon)."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSlowMicrobe.setFocus(True)
            return False
        elif len(self.txtRecaltinationSOM.text().strip()) == 0:
            message = "Please enter the value for fraction of recalcitrant SOM (slowest) (soil carbon)."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtRecaltinationSOM.setFocus(True)
            return False
        elif len(self.txtSoilMeneralNitrogetPool.text().strip()) == 0:
            message = "Please enter the amount of nitrogen in soil mineral nitrogen pool."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSoilMeneralNitrogetPool.setFocus(True)
            return False
        elif (float(self.txtFastMicrobe.text()) + float(self.txtMediumMicrobe.text()) + float(self.txtSlowMicrobe.text()) +
              float(self.txtRecaltinationSOM.text()) != 1):
            message = "The sum of all microbial recycling pools must be 1.0. Please check the values."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtFastMicrobe.setFocus(True)
            return False
        else: return True

    def findRowIndexInTable(self, siteIndex):
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 0).text() == siteIndex:
                return i
        return -1

    def deleteRowFromTable(self, siteIndex):
        ndx = self.findRowIndexInTable(siteIndex)
        if ndx > -1:
            self.tableWidget.removeRow(ndx)

    def addRowInTable(self, site):
        ndx = self.findRowIndexInTable(site.siteIndex)

        if ndx == -1:
            ndx = self.tableWidget.rowCount()
            self.tableWidget.insertRow(ndx)
            self.tableWidget.setRowHeight(ndx, 20)
            self.setItemInRow(ndx, site)

    def editRowInTable(self, site):
        ndx = self.findRowIndexInTable(site.siteIndex)
        if ndx > -1:
            self.setItemInRow(ndx, site)

    def clearTableRows(self):
        for i in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)
        self.siteList.clear()

    def setItemInRow(self, rowIndex, site):
        cell = QtWidgets.QTableWidgetItem(site.siteIndex)
        self.tableWidget.setItem(rowIndex, 0, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.noOfVegetation))
        self.tableWidget.setItem(rowIndex, 1, cell)
        cell = QtWidgets.QTableWidgetItem(site.soilProfileFileName)
        self.tableWidget.setItem(rowIndex, 2, cell)
        cell = QtWidgets.QTableWidgetItem(site.soilHorizonFileName)
        self.tableWidget.setItem(rowIndex, 3, cell)
        cell = QtWidgets.QTableWidgetItem(site.profileName)
        self.tableWidget.setItem(rowIndex, 4, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.groundWaterDepth))
        self.tableWidget.setItem(rowIndex, 5, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.groundWaterFlag))
        self.tableWidget.setItem(rowIndex, 6, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.reductionFactor))
        self.tableWidget.setItem(rowIndex, 7, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.zetaParameter))
        self.tableWidget.setItem(rowIndex, 8, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.depthOfDehumidification))
        self.tableWidget.setItem(rowIndex, 9, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.yearDay))
        self.tableWidget.setItem(rowIndex, 10, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.temperatureTimeLag))
        self.tableWidget.setItem(rowIndex, 11, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.amplitudeOfSoilTemperature))
        self.tableWidget.setItem(rowIndex, 12, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.increaseOfTemperature))
        self.tableWidget.setItem(rowIndex, 13, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.siteElevation))
        self.tableWidget.setItem(rowIndex, 14, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.siteLatitude))
        self.tableWidget.setItem(rowIndex, 15, cell)
        cell = QtWidgets.QTableWidgetItem(site.meteorologicalFileName)
        self.tableWidget.setItem(rowIndex, 16, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.noOfMeteorologicalYear))
        self.tableWidget.setItem(rowIndex, 17, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.ndepFileName))
        self.tableWidget.setItem(rowIndex, 18, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.ndepRate))
        self.tableWidget.setItem(rowIndex, 19, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.industrialNdepRate))
        self.tableWidget.setItem(rowIndex, 20, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.snowWaterPool))
        self.tableWidget.setItem(rowIndex, 21, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.fastMicrobialFraction))
        self.tableWidget.setItem(rowIndex, 22, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.mediumMicrobialFraction))
        self.tableWidget.setItem(rowIndex, 23, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.slowMicrobialFraction))
        self.tableWidget.setItem(rowIndex, 24, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.recalcitrantSom))
        self.tableWidget.setItem(rowIndex, 25, cell)
        cell = QtWidgets.QTableWidgetItem(str(site.soilMineralNitrogenPool))
        self.tableWidget.setItem(rowIndex, 26, cell)

    def showSiteListInTable(self):
        for i in range(len(self.siteList)):
            self.tableWidget.insertRow(i)
            self.tableWidget.setRowHeight(i, 20)

            item = self.siteList[i]
            self.setItemInRow(i, item)

    def btnGisFileBrowse_clicked(self):
        startingDir = ""
        if ApplicationProperty.currentModelDirectory != "": startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath ()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Text File (*.txt)")

        if len(filename.strip())>0:
            self.clearTableRows()
            self.siteList = FileReadWrite.readGisFile(filename)
            if self.siteList is not None:
                temp = filename.split("/")[-1]
                self.txtGisFileName.setText(temp)
                self.txtInitialDirectory.setText(filename.replace("/" + temp, "").replace("/ini",""))
                ApplicationProperty.currentModelDirectory = self.txtInitialDirectory.text()
                self.showSiteListInTable()

                if self.tableWidget.rowCount() > 0:
                    self.btnEditRow.setEnabled(True)
                    self.btnEditAndAdd.setEnabled(True)
                    self.btnDelete.setEnabled(True)
                    self.btnSaveAs.setEnabled(True)
                    # self.btnSave.setEnabled(False)

    def tableWidget_itemSelectionChanged(self):
        if len(self.siteList) > 0:
            rowIndex = self.tableWidget.currentRow()
            if rowIndex > -1:
                self.txtSiteIndex.setText(self.tableWidget.item(rowIndex, 0).text())
                self.txtNoOfVegType.setText(self.tableWidget.item(rowIndex, 1).text())
                self.txtSoilProfileFile.setText(self.tableWidget.item(rowIndex, 2).text())
                self.txtSoilHorizonFile.setText(self.tableWidget.item(rowIndex, 3).text())
                self.txtProfileName.setText(self.tableWidget.item(rowIndex, 4).text())
                self.txtGroundWaterDepth.setText(self.tableWidget.item(rowIndex, 5).text())
                self.cmbGroundWaterFlag.setCurrentIndex(int(self.tableWidget.item(rowIndex, 6).text()))
                self.txtReductionFactor.setText(self.tableWidget.item(rowIndex, 7).text())
                self.txtDehumidificationParam.setText(self.tableWidget.item(rowIndex, 8).text())
                self.txtlDepthOfDehumidification.setText(self.tableWidget.item(rowIndex, 9).text())
                self.txtYearDay.setText(self.tableWidget.item(rowIndex, 10).text())
                self.txtTemperaturTimeLag.setText(self.tableWidget.item(rowIndex, 11).text())
                self.txtAmplitudeofsoilTemperature.setText(self.tableWidget.item(rowIndex, 12).text())
                self.txtIncreaseOfTemperature.setText(self.tableWidget.item(rowIndex, 13).text())
                self.txtSiteElevation.setText(self.tableWidget.item(rowIndex, 14).text())
                self.txtSiteLatitude.setText(self.tableWidget.item(rowIndex, 15).text())
                self.txtMeteorologicalFileName.setText(self.tableWidget.item(rowIndex, 16).text())
                self.txtNumberOfMeteorologicalYear.setText(self.tableWidget.item(rowIndex, 17).text())
                self.txtNdepFileName.setText(self.tableWidget.item(rowIndex, 18).text())
                self.txtNigrogenDepositionRate.setText(self.tableWidget.item(rowIndex, 19).text())
                self.txtIndustrialNitrogenDepTate.setText(self.tableWidget.item(rowIndex, 20).text())
                self.txtWaterInSnowPool.setText(self.tableWidget.item(rowIndex, 21).text())
                self.txtFastMicrobe.setText(self.tableWidget.item(rowIndex, 22).text())
                self.txtMediumMicrobe.setText(self.tableWidget.item(rowIndex, 23).text())
                self.txtSlowMicrobe.setText(self.tableWidget.item(rowIndex, 24).text())
                self.txtRecaltinationSOM.setText(self.tableWidget.item(rowIndex, 25).text())
                self.txtSoilMeneralNitrogetPool.setText(self.tableWidget.item(rowIndex, 26).text())
            else:
                self.clearField()

    def clearField(self):
        self.txtSiteIndex.clear()
        self.txtNoOfVegType.clear()
        self.txtSoilProfileFile.clear()
        self.txtSoilHorizonFile.clear()
        self.txtProfileName.clear()
        self.txtGroundWaterDepth.clear()
        self.cmbGroundWaterFlag.setCurrentIndex(-1)
        self.txtReductionFactor.clear()
        self.txtDehumidificationParam.clear()
        self.txtlDepthOfDehumidification.clear()
        self.txtYearDay.clear()
        self.txtTemperaturTimeLag.clear()
        self.txtAmplitudeofsoilTemperature.clear()
        self.txtIncreaseOfTemperature.clear()
        self.txtSiteElevation.clear()
        self.txtSiteLatitude.clear()
        self.txtMeteorologicalFileName.clear()
        self.txtNumberOfMeteorologicalYear.clear()
        self.txtNdepFileName.clear()
        self.txtNigrogenDepositionRate.clear()
        self.txtIndustrialNitrogenDepTate.clear()
        self.txtWaterInSnowPool.clear()
        self.txtFastMicrobe.clear()
        self.txtMediumMicrobe.clear()
        self.txtSlowMicrobe.clear()
        self.txtRecaltinationSOM.clear()
        self.txtSoilMeneralNitrogetPool.clear()
        # self.tableWidget.setCurrentCell(0,0)

    def lockFields(self, lock):
        self.txtSiteIndex.setReadOnly(lock)
        self.txtNoOfVegType.setReadOnly(lock)
        self.txtSoilProfileFile.setReadOnly(lock)
        self.btnSoilProfileFile.setEnabled(not lock)
        self.txtSoilHorizonFile.setReadOnly(lock)
        self.txtProfileName.setReadOnly(lock)
        self.txtGroundWaterDepth.setReadOnly(lock)
        self.cmbGroundWaterFlag.setEnabled(not lock)
        self.txtReductionFactor.setReadOnly(lock)
        self.btnSoilHorizonFile.setEnabled(not lock)
        self.txtDehumidificationParam.setReadOnly(lock)
        self.txtlDepthOfDehumidification.setReadOnly(lock)
        self.txtYearDay.setReadOnly(lock)
        self.txtTemperaturTimeLag.setReadOnly(lock)
        self.txtAmplitudeofsoilTemperature.setReadOnly(lock)
        self.txtIncreaseOfTemperature.setReadOnly(lock)
        self.txtSiteElevation.setReadOnly(lock)
        self.txtSiteLatitude.setReadOnly(lock)
        self.txtMeteorologicalFileName.setReadOnly(lock)
        self.btnMetFileBrowse.setEnabled(not lock)
        self.btnNdepFile.setEnabled(not lock)
        self.txtNumberOfMeteorologicalYear.setReadOnly(lock)
        self.txtNdepFileName.setReadOnly(lock)
        self.txtNigrogenDepositionRate.setReadOnly(lock)
        self.txtIndustrialNitrogenDepTate.setReadOnly(lock)
        self.txtWaterInSnowPool.setReadOnly(lock)
        self.txtFastMicrobe.setReadOnly(lock)
        self.txtMediumMicrobe.setReadOnly(lock)
        self.txtSlowMicrobe.setReadOnly(lock)
        self.txtRecaltinationSOM.setReadOnly(lock)
        self.txtSoilMeneralNitrogetPool.setReadOnly(lock)

    def btnAddRow_clicked(self):
        if self.btnAddRow.text() == "Add Row":
            self.clearField()
            self.tableWidget.setEnabled(False)
            self.frame_2.setEnabled(False)
            if self.rbtModifyGisFile.isChecked(): self.btnGisFileBrowse.setEnabled(False)
            self.btnEditAndAdd.setEnabled(False)
            self.btnEditRow.setEnabled(False)
            self.btnDelete.setEnabled(False)
            self.btnSave.setEnabled(False)
            self.btnClose.setText("Cancel")
            self.btnAddRow.setText("Save Row")
            self.lockFields(False)
            self.txtSiteIndex.setFocus(True)
        else:
            if self.checkCompleteness():
                site = self.createSiteWithInputValues()
                if site is not None:
                    if self.addSite(site):
                        self.addRowInTable(site)
                        self.tableWidget.setEnabled(True)
                        self.frame_2.setEnabled(True)
                        if self.rbtModifyGisFile.isChecked(): self.btnGisFileBrowse.setEnabled(True)
                        self.btnEditAndAdd.setEnabled(True)
                        self.btnEditRow.setEnabled(True)
                        self.btnDelete.setEnabled(True)
                        self.btnSave.setEnabled(True)
                        self.btnClose.setText("Close")
                        self.btnAddRow.setText("Add Row")
                        self.clearField()
                        self.lockFields(True)
                        self.isModified = True
                        if self.rbtNewGisFile.isChecked():
                            self.btnSave.setEnabled(True)
                            self.btnSaveAs.setEnabled(False)
                        else:
                            self.btnSave.setEnabled(True)
                            self.btnSaveAs.setEnabled(True)
                    else:
                        message = "The site information was not saved. Please check input information."
                        QtGui.QMessageBox.about(self.form, "Add Row", message)
                else:
                    message = "There was a problem in adding the site. Please check input information"
                    QtGui.QMessageBox.about(self.form, "Add Row", message)

    def btnEditAndAdd_clicked(self):
        if self.btnEditAndAdd.text() == "Edit and Add":
            if self.tableWidget.currentRow() >= 0:
                self.txtSiteIndex.clear()
                self.tableWidget.setEnabled(False)
                self.frame_2.setEnabled(False)
                if self.rbtModifyGisFile.isChecked(): self.btnGisFileBrowse.setEnabled(False)
                self.btnAddRow.setEnabled(False)
                self.btnEditRow.setEnabled(False)
                self.btnDelete.setEnabled(False)
                self.btnSave.setEnabled(False)
                self.btnClose.setText("Cancel")
                self.lockFields(False)
                self.btnEditAndAdd.setText("Save Row")
            else:
                if self.tableWidget.rowCount() > 0:
                    message = "No row is selected. Please select a row from the list."
                    QtGui.QMessageBox.about(self.form, "Add Row", message)
        else:
            if self.checkCompleteness():
                site = self.createSiteWithInputValues()
                if site is not None:
                    if self.addSite(site):
                        self.addRowInTable(site)
                        self.tableWidget.setEnabled(True)
                        self.frame_2.setEnabled(True)
                        if self.rbtModifyGisFile.isChecked(): self.btnGisFileBrowse.setEnabled(True)
                        self.btnAddRow.setEnabled(True)
                        self.btnEditRow.setEnabled(True)
                        self.btnDelete.setEnabled(True)
                        self.btnSave.setEnabled(True)
                        self.btnClose.setText("Close")
                        self.lockFields(True)
                        self.btnEditAndAdd.setText("Edit and Add")
                        self.isModified = True
                        if self.rbtNewGisFile.isChecked():
                            self.btnSave.setEnabled(True)
                            self.btnSaveAs.setEnabled(False)
                        else:
                            self.btnSave.setEnabled(True)
                            self.btnSaveAs.setEnabled(True)
                    else:
                        message = "The site information was not saved. Please check input information."
                        QtGui.QMessageBox.about(self.form, "Add Row", message)
                else:
                    message = "There was a problem in adding the site. Please check input information"
                    QtGui.QMessageBox.about(self.form, "Add Row", message)

    def btnEditRow_clicked(self):
        if self.btnEditRow.text() == "Edit Row":
            if self.tableWidget.currentRow() >= 0:
                self.tableWidget.setEnabled(False)
                self.frame_2.setEnabled(False)
                if self.rbtModifyGisFile.isChecked(): self.btnGisFileBrowse.setEnabled(False)
                self.btnEditAndAdd.setEnabled(False)
                self.btnAddRow.setEnabled(False)
                self.btnDelete.setEnabled(False)
                self.btnSave.setEnabled(False)
                self.btnClose.setText("Cancel")
                self.lockFields(False)
                self.txtSiteIndex.setReadOnly(True)
                self.btnEditRow.setText("Update Row")
            else:
                if self.tableWidget.rowCount() > 0:
                    message = "No row is selected. Please select a row from the list."
                    QtGui.QMessageBox.about(self.form, "Add Row", message)
        else:
            if self.checkCompleteness():
                site = self.createSiteWithInputValues()
                if site is not None:
                    if self.editSite(site):
                        self.editRowInTable(site)
                        self.tableWidget.setEnabled(True)
                        self.frame_2.setEnabled(True)
                        if self.rbtModifyGisFile.isChecked(): self.btnGisFileBrowse.setEnabled(True)
                        self.btnEditAndAdd.setEnabled(True)
                        self.btnAddRow.setEnabled(True)
                        self.btnDelete.setEnabled(True)
                        self.btnSave.setEnabled(True)
                        self.btnClose.setText("Close")
                        self.lockFields(True)
                        self.btnEditRow.setText("Edit Row")
                        self.isModified = True
                        if self.rbtNewGisFile.isChecked():
                            self.btnSave.setEnabled(True)
                            self.btnSaveAs.setEnabled(False)
                        else:
                            self.btnSave.setEnabled(True)
                            self.btnSaveAs.setEnabled(True)
                    else:
                        message = "The site information was not saved. Please check input information."
                        QtGui.QMessageBox.about(self.form, "Add Row", message)
                else:
                    message = "There was a problem in adding the site. Please check input information"
                    QtGui.QMessageBox.about(self.form, "Add Row", message)

    def btnDelete_clicked(self):
        ndx = self.tableWidget.currentRow()

        if ndx > -1:
            message = "Are you sure you want delete the selected site?"
            reply = QtGui.QMessageBox.question(self.form, 'Delete Row', message, QtGui.QMessageBox.Yes,
                                                QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                siteIndex = self.tableWidget.item(ndx, 0).text()
                if self.deleteSite(siteIndex):
                    self.deleteRowFromTable(siteIndex)
                    self.isModified = True
                    if self.tableWidget.rowCount() == 0:
                        self.clearField()
                        self.btnEditRow.setEnabled(False)
                        self.btnEditAndAdd.setEnabled(False)
                        self.btnDelete.setEnabled(False)
                        self.btnSave.setEnabled(False)
                        self.btnSaveAs.setEnabled(False)
                        if self.rbtNewGisFile.isChecked():
                            self.isModified = False
                    else:
                        if self.rbtNewGisFile.isChecked():
                            self.btnSave.setEnabled(True)
                            self.btnSaveAs.setEnabled(False)
                        else:
                            self.btnSave.setEnabled(True)
                            self.btnSaveAs.setEnabled(True)
        else:
            if self.tableWidget.rowCount() > 0:
                message = "Please select a row from the table."
                QtGui.QMessageBox.about(self.form, "Initial Setting", message)

    def rbtNewGisFile_toggled(self):
        if self.rbtNewGisFile.isChecked():
            self.txtGisFileName.setEnabled(True)
            self.btnGisFileBrowse.setEnabled(False)
            self.btnInitDirChoose.setEnabled(True)
            self.btnSave.setText("Save")
            self.btnEditRow.setEnabled(False)
            self.btnEditAndAdd.setEnabled(False)
            self.btnDelete.setEnabled(False)
            self.btnSave.setEnabled(False)
            self.btnSaveAs.setEnabled(False)
        else:
            self.txtGisFileName.setEnabled(False)
            self.btnGisFileBrowse.setEnabled(True)
            self.btnInitDirChoose.setEnabled(False)
            self.btnSave.setText("Update")
        self.isModified = False
        self.btnSaveAs.setEnabled(False)
        self.btnSave.setEnabled(False)
        self.txtGisFileName.clear()
        self.txtInitialDirectory.clear()
        if self.tableWidget.rowCount() > 0:
            self.clearTableRows()

    def btnClose_clicked(self):
        if self.btnClose.text() == "Close":
            self.form.parentWidget().close()
        else:
            if self.tableWidget.currentRow() >= 0:
                self.tableWidget_itemSelectionChanged()
            else:
                self.clearField()
            self.tableWidget.setEnabled(True)
            self.frame_2.setEnabled(True)
            if self.rbtModifyGisFile.isChecked(): self.btnGisFileBrowse.setEnabled(True)
            self.btnAddRow.setText("Add Row")
            self.btnEditAndAdd.setText("Edit and Add")
            self.btnEditRow.setText("Edit Row")
            self.btnAddRow.setEnabled(True)
            if self.tableWidget.rowCount() > 0:
                self.btnEditAndAdd.setEnabled(True)
                self.btnEditRow.setEnabled(True)
                self.btnDelete.setEnabled(True)
            else:
                self.btnEditAndAdd.setEnabled(False)
                self.btnEditRow.setEnabled(False)
                self.btnDelete.setEnabled(False)
            self.lockFields(True)
            if self.isModified:
                if self.rbtNewGisFile.isChecked():
                    self.btnSave.setEnabled(True)
                    self.btnSaveAs.setEnabled(False)
                else:
                    self.btnSave.setEnabled(True)
                    self.btnSaveAs.setEnabled(True)
            self.btnClose.setText("Close")

    def btnInitDirChoose_clicked(self):
        startingDir = ApplicationProperty.getScriptPath ()
        folderName = str(QtWidgets.QFileDialog.getExistingDirectory(self.form, "Select Directory", startingDir, QtWidgets.QFileDialog.ShowDirsOnly))
        self.txtInitialDirectory.setText(folderName)

    def btnSoilProfileFile_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory)>0: startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath ()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Text File (*.txt)")
        self.txtSoilProfileFile.setText(filename[0].split("/")[-1])

    def btnSoilHorizonFile_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory)>0: startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath ()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Text File (*.txt)")
        self.txtSoilHorizonFile.setText(filename[0].split("/")[-1])

    def btnMetFileBrowse_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory)>0: startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath ()
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', startingDir, "Text File (*.txt)")
        self.txtMeteorologicalFileName.setText(filename[0].split("/")[-1])

    def btnNdepFile_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory)>0: startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath ()
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', startingDir, "Text File (*.txt)")
        self.txtNdepFileName.setText(filename[0].split("/")[-1])

    def btnSave_clicked(self):
        if self.editMode:
            if self.checkCompleteness():
                site = self.createSiteWithInputValues()
                if site is not None:
                    if self.editSite(site):
                        self.editRowInTable(site)
                self.form.parentWidget().close()
        else:
            if len(self.txtGisFileName.text().strip()) == 0:
                message = "Please enter the GIS file name."
                QtGui.QMessageBox.about(self.form, "Add Row", message)
                self.txtGisFileName.setFocus(True)
            elif len(self.txtInitialDirectory.text().strip()) == 0:
                message = "Please select directory."
                QtGui.QMessageBox.about(self.form, "Add Row", message)
                self.txtInitialDirectory.setFocus(True)
            elif len(self.siteList) == 0:
                message = "There is no site information to save."
                QtGui.QMessageBox.about(self.form, "Add Row", message)
            else:
                fileName = self.txtInitialDirectory.text().strip() + "/ini/" + self.txtGisFileName.text().strip()
                feedback = FileReadWrite.writeGisFile(fileName, self.siteList)
                if feedback:
                    QtGui.QMessageBox.about(self.form, "Save", "The GIS file has been saved successfully.")
                else:
                    QtGui.QMessageBox.about(self.form, "Error", "File not saved.")

    def btnSaveAs_clicked(self):
        if len(self.siteList) == 0:
            message = "There is no site information to save."
            QtGui.QMessageBox.about(self.form, "Add Row", message)
        else:
            startingDir = ""
            if len(ApplicationProperty.currentModelDirectory) > 0: startingDir = ApplicationProperty.currentModelDirectory
            else: startingDir = ApplicationProperty.getScriptPath ()
            fileName = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save File', startingDir, "Text File (*.txt)")

            feedback = FileReadWrite.writeGisFile(fileName, self.siteList)

            if feedback:
                QtGui.QMessageBox.about(self.form, "Save", "The GIS file has been saved successfully.")
            else:
                QtGui.QMessageBox.about(self.form, "Error", "File not saved.")
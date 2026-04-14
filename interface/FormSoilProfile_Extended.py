from interface.FormSoilProfile import Ui_FormSoilProfile
from PyQt5 import QtGui, QtCore, QtWidgets
from parameter import SoilProfile
from parameter import SoilLayer
from application import ApplicationProperty
from file_io import FileReadWrite
import copy
from interface.DialogSoilFileName_Extended import DialogSoilFileName

class FormSoilProfile(Ui_FormSoilProfile):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.addSocket()
        self.formInitialSettings()

        #form variables
        self.listOfSoilProfile = []             #list of soil profile
        self.modelDirectory = ""

        #modify from outside flag
        # self.flag_modification = False

        self.currentProfileIndex = -1

        self.dialog_soil_filename = DialogSoilFileName()

    def addSocket(self):
        self.btnClose.clicked.connect(self.btnClose_clicked)
        self.btnBrowseProfileFile.clicked.connect(self.btnBrowseProfileFile_clicked)
        self.btnBrowseHorizonFile.clicked.connect(self.btnBrowseHorizonFile_clicked)
        self.tableProfileList.itemSelectionChanged.connect(self.tableProfileList_itemSelectionChanged)
        self.btnSave.clicked.connect(self.btnSave_clicked)
        self.btnDeleteLayer.clicked.connect(self.btnDeleteLayer_clicked)
        self.btnAddLayer.clicked.connect(self.btnAddLayer_clicked)
        self.btnCopyAndAdd.clicked.connect(self.btnCopyAndAdd_clicked)
        self.tableLayerDetail.itemChanged.connect(self.tableLayerDetail_itemChanged)
        self.txtProfileName.textChanged.connect(self.txtProfileName_textChanged)
        self.btnAddProfile.clicked.connect(self.btnAddProfile_clicked)
        self.btnDeleteProfile.clicked.connect(self.btnDeleteProfile_clicked)
        self.txtProfileFileName.textChanged.connect(self.profileAndHorizonLineEdit_textChanged)
        self.txtHorizonFileName.textChanged.connect(self.profileAndHorizonLineEdit_textChanged)
        self.rbtNew.toggled.connect(self.rbtNew_toggled)
        self.btnSaveAs.clicked.connect(self.btnSaveAs_clicked)

    def formInitialSettings(self):
        self.tableProfileList.setColumnCount(1)
        self.tableProfileList.setHorizontalHeaderLabels(["Profile Name"])
        self.tableProfileList.setColumnWidth(0, 150)

        self.tableLayerDetail.setColumnCount(16)
        header =  SoilLayer.getParamLabelList()
        # "Horizon Name", "Lower Horizon Border", "Layer Thickness","Correction Factor","Texture",
        #           "pH", "C-org (M%)", "Gravel (Vol.%)", "Sand (M.%)", "Silt (M.%)", "Clay (M.%)", "BD (g/cm³)",
        #           "PV (Vol.%)", "FC Vol.%", "PWP Vol.%", "KS (cm/d)"]

        '''
        Note:
        BD = Bulk Density, PV = Pore Volumn, FC = Field Capacity, PWP = Permanent Wilting Point,
        KS = Saturated Hydraulic Conductivity
        '''

        self.tableLayerDetail.setHorizontalHeaderLabels(header)
        self.tableLayerDetail.setColumnWidth(0, 200)
        self.tableLayerDetail.setColumnWidth(1, 160)
        self.tableLayerDetail.setColumnWidth(2, 160)
        self.tableLayerDetail.setColumnWidth(3, 160)

        for i in range(4, 16):
            self.tableLayerDetail.setColumnWidth(i, 100)

        self.btnBrowseProfileFile.setEnabled(False)
        self.btnBrowseHorizonFile.setEnabled(False)
        self.txtProfileName.setReadOnly(True)
        self.btnAddLayer.setEnabled(False)
        self.btnCopyAndAdd.setEnabled(False)
        self.btnDeleteLayer.setEnabled(False)
        self.btnDeleteProfile.setEnabled(False)
        self.btnSaveAs.setEnabled(False)
        self.btnSave.setEnabled(False)
        self.btnAddProfile.setText("Add Profile")

        self.rbtNew.setChecked(True)

    def rbtNew_toggled(self):
        self.currentProfileIndex = -1
        self.listOfSoilProfile = []

        self.txtProfileFileName.clear()
        self.txtHorizonFileName.clear()
        self.clearTableLayerDetail()
        self.clearTableProfileList()
        self.txtProfileName.clear()

        self.txtProfileName.setReadOnly(True)
        self.btnAddLayer.setEnabled(False)
        self.btnCopyAndAdd.setEnabled(False)
        self.btnDeleteLayer.setEnabled(False)
        self.btnDeleteProfile.setEnabled(False)
        self.btnSaveAs.setEnabled(False)
        self.btnSave.setEnabled(False)

        if self.rbtNew.isChecked():
            self.btnBrowseProfileFile.setEnabled(False)
            self.btnBrowseHorizonFile.setEnabled(False)
            self.txtProfileName.setReadOnly(True)


            self.txtProfileFileName.setReadOnly(False)
            self.txtHorizonFileName.setReadOnly(False)
            self.btnBrowseProfileFile.setEnabled(False)
            self.btnBrowseHorizonFile.setEnabled(False)
            self.btnAddProfile.setEnabled(True)
            self.btnAddProfile.setText("Add Profile")
        else:
            self.txtProfileFileName.setReadOnly(True)
            self.txtHorizonFileName.setReadOnly(True)
            self.btnBrowseProfileFile.setEnabled(True)
            self.btnBrowseHorizonFile.setEnabled(True)
            self.btnAddProfile.setEnabled(False)
            self.btnAddProfile.setText("Copy Profile")

    def btnClose_clicked(self):
        self.form.parentWidget().close()

    def btnSave_clicked(self):
        errorList = self.dataValidity()
        if not self.txtProfileFileName.text().strip():
            message = "Please enter Soil Profile file name."
            QtGui.QMessageBox.about(self.form, "Input Required", message)
            self.txtProfileFileName.setFocus(True)
        elif not self.txtHorizonFileName.text().strip():
            message = "Please enter Horizon file name."
            QtGui.QMessageBox.about(self.form, "Input Required", message)
            self.txtHorizonFileName.setFocus(True)
        elif len(self.listOfSoilProfile) == 0:
            message = "There is no soil profile. Please add soil profile."
            QtGui.QMessageBox.about(self.form, "No Data", message)
        elif len(errorList) > 0:
            self.showErrorMessage(errorList[0])
            self.markError()
        else:
            initialDirectory = ""
            if self.modelDirectory: initialDirectory = self.modelDirectory + "/soil/"
            else:
                #browse model directory folder
                initialDirectory = str(QtWidgets.QFileDialog.getExistingDirectory(self.form, "Select Directory", ApplicationProperty.getScriptPath()
                                                                            , QtWidgets.QFileDialog.ShowDirsOnly))
                if len(initialDirectory) == 0: return False
                else:
                    self.modelDirectory = initialDirectory
                    initialDirectory = initialDirectory + "/soil/"

            profileFileName = initialDirectory + self.txtProfileFileName.text().strip()
            if profileFileName[-4:].lower() != ".txt": profileFileName = profileFileName + ".txt"

            horizonFileName = initialDirectory + self.txtHorizonFileName.text().strip()
            if horizonFileName[-4:].lower() != ".txt": horizonFileName = horizonFileName + ".txt"

            if len(profileFileName) > 0 and len(horizonFileName) > 0:
                saveResult = FileReadWrite.writeSoilProfile(self.listOfSoilProfile, profileFileName, horizonFileName)
                if saveResult:
                    message = "Soil profile(s) and horizon(s) are saved successfully."
                    QtGui.QMessageBox.about(self.form, "Saved Successfully", message)
            else: return False


    def btnBrowseProfileFile_clicked(self):
        initdirectory = ""
        if self.modelDirectory: initdirectory = self.modelDirectory + "/soil/"
        else: initdirectory = ApplicationProperty.getScriptPath()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initdirectory, "Text File (*.txt)")

        if filename:
            temp = filename.split("/")[-1]
            self.txtProfileFileName.setText(temp)
            if not self.modelDirectory: self.modelDirectory = filename.replace("/soil/" + temp, "")

    def btnBrowseHorizonFile_clicked(self):
        initdirectory = ""
        if self.modelDirectory: initdirectory = self.modelDirectory + "/soil/"
        else: initdirectory = ApplicationProperty.getScriptPath()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initdirectory, "Text File (*.txt)")

        if filename:
            temp = filename.split("/")[-1]
            self.txtHorizonFileName.setText(temp)
            if not self.modelDirectory: self.modelDirectory = filename.replace("/soil/" + temp, "")

    def clearTableProfileList(self):
        for i in reversed(range(self.tableProfileList.rowCount())):
            self.tableProfileList.removeRow(i)

    def clearTableLayerDetail(self):
        for i in reversed(range(self.tableLayerDetail.rowCount())):
            self.tableLayerDetail.removeRow(i)

    def profileAndHorizonLineEdit_textChanged(self):
        if self.rbtUpdate.isChecked():
            soilProfileFilePath = self.txtProfileFileName.text().strip()
            soilHorizonFilePath =  self.txtHorizonFileName.text().strip()

            if soilProfileFilePath and soilHorizonFilePath:
                soilProfileFilePath = self.modelDirectory + "/soil/" + soilProfileFilePath
                soilHorizonFilePath = self.modelDirectory + "/soil/" + soilHorizonFilePath

                self.listOfSoilProfile = FileReadWrite.readSoilProfile(soilProfileFilePath, soilHorizonFilePath)
                self.clearTableProfileList()
                self.clearTableLayerDetail()
                if self.listOfSoilProfile:
                    for profile in self.listOfSoilProfile:
                        ndx = self.tableProfileList.rowCount()
                        self.tableProfileList.insertRow(ndx)
                        cell = QtWidgets.QTableWidgetItem(profile.profileName)
                        self.tableProfileList.setItem(ndx, 0, cell)
                        self.tableProfileList.setRowHeight(ndx, 20)
                    self.currentProfileIndex = 0
                    item = self.tableProfileList.item(0,0)
                    self.tableProfileList.setCurrentItem(item)

                    self.btnAddLayer.setEnabled(True)
                    self.btnCopyAndAdd.setEnabled(True)
                    self.btnDeleteLayer.setEnabled(True)
                    self.btnAddProfile.setEnabled(True)
                    self.btnDeleteProfile.setEnabled(True)
                    self.btnSave.setEnabled(True)
                    self.btnSaveAs.setEnabled(True)
                    self.txtProfileName.setReadOnly(False)

    def tableProfileList_itemSelectionChanged(self):
        if self.tableProfileList.rowCount() > 0 and len(self.listOfSoilProfile) > 0:
            rowIndex = self.tableProfileList.currentRow()
            if rowIndex > -1:
                self.currentProfileIndex = rowIndex
                profile = self.listOfSoilProfile[rowIndex]
                if self.tableProfileList.item(rowIndex, 0).text() == profile.profileName:
                    self.txtProfileName.setText(profile.profileName)

                    layerList = profile.soilLayerList
                    self.clearTableLayerDetail()
                    for layer in layerList:
                        rowIndex = self.tableLayerDetail.rowCount()
                        self.tableLayerDetail.insertRow(rowIndex)
                        self.tableLayerDetail.setRowHeight(rowIndex, 20)

                        cell = QtWidgets.QTableWidgetItem(str(layer.horizonName))
                        self.tableLayerDetail.setItem(rowIndex, 0, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.depthOfHorizon))
                        self.tableLayerDetail.setItem(rowIndex, 1, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.layerThickness))
                        self.tableLayerDetail.setItem(rowIndex, 2, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.correctionFactor))
                        self.tableLayerDetail.setItem(rowIndex, 3, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.soilTexture))
                        self.tableLayerDetail.setItem(rowIndex, 4, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.soilPh))
                        self.tableLayerDetail.setItem(rowIndex, 5, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.organicCarbonContent))
                        self.tableLayerDetail.setItem(rowIndex, 6, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.gravelContent))
                        self.tableLayerDetail.setItem(rowIndex, 7, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.sandContent))
                        self.tableLayerDetail.setItem(rowIndex, 8, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.siltContent))
                        self.tableLayerDetail.setItem(rowIndex, 9, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.clayContent))
                        self.tableLayerDetail.setItem(rowIndex, 10, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.bulkDensity))
                        self.tableLayerDetail.setItem(rowIndex, 11, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.poreVolume))
                        self.tableLayerDetail.setItem(rowIndex, 12, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.waterCapacity))
                        self.tableLayerDetail.setItem(rowIndex, 13, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.permanentWiltingPoint))
                        self.tableLayerDetail.setItem(rowIndex, 14, cell)
                        cell = QtWidgets.QTableWidgetItem(str(layer.saturatedHydraulicConductivity))
                        self.tableLayerDetail.setItem(rowIndex, 15, cell)
                    self.markError()

    def btnDeleteLayer_clicked(self):
        # rows = self.tableLayerDetail.selectionModel().selectedRows()
        currentRow = self.tableLayerDetail.currentRow()
        if currentRow >= 0:
            profile = self.listOfSoilProfile[self.currentProfileIndex]

            if profile is not None:
                message = "Are you sure you want to delete this horizon?"
                reply = QtGui.QMessageBox.question(self.form, 'Delete horizon', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.tableLayerDetail.removeRow(currentRow)
                    profile.soilLayerList.pop(currentRow)

    def btnCopyAndAdd_clicked(self):
        if self.currentProfileIndex > -1:
            if self.tableLayerDetail.rowCount() > 0 and self.tableLayerDetail.currentRow() > -1:
                profile = self.listOfSoilProfile[self.currentProfileIndex]
                currentLayer = copy.deepcopy(profile.soilLayerList[self.tableLayerDetail.currentRow()])
                profile.soilLayerList.append(currentLayer)
                profile.sortSoilProfileByDepth()
                self.tableProfileList_itemSelectionChanged()

    def btnAddLayer_clicked(self):
        if self.currentProfileIndex > -1:
            profile = self.listOfSoilProfile[self.currentProfileIndex]

            if profile is not None:
                layer = SoilLayer()
                profile.soilLayerList.append(layer)

                rowCount = self.tableLayerDetail.rowCount()
                self.tableLayerDetail.insertRow(rowCount)
                self.tableLayerDetail.setRowHeight(rowCount, 20)

                self.tableProfileList_itemSelectionChanged()


    def tableLayerDetail_itemChanged(self):
        item = self.tableLayerDetail.currentItem()
        if item is not None:
            colindex = self.tableLayerDetail.currentColumn()
            rowindex = self.tableLayerDetail.currentRow()

            pname = self.tableLayerDetail.horizontalHeaderItem(colindex).text()
            pvalue = item.text()

            if pname and pvalue:
                profile = self.listOfSoilProfile[self.currentProfileIndex]
                layer = profile.soilLayerList[rowindex]
                if colindex > 3:
                    layerName = layer.horizonName
                    for lay in profile.soilLayerList:
                        if lay.horizonName == layerName:
                            lay.setParameterValue(pname, pvalue)
                else: layer.setParameterValue(pname, pvalue)
                if colindex == 1:
                    profile.sortSoilProfileByDepth()
            self.tableProfileList_itemSelectionChanged()
            self.markError()

    def txtProfileName_textChanged(self):
        if self.currentProfileIndex > -1:
            profileName = self.txtProfileName.text().strip()

            if profileName:
                profile = self.listOfSoilProfile[self.currentProfileIndex]
                item = self.tableProfileList.item(self.currentProfileIndex, 0)
                item.setText(profileName)
                profile.profileName = profileName

                self.markProfileNameError()

    def btnAddProfile_clicked(self):
        if self.currentProfileIndex > -1:
            profile = copy.deepcopy(self.listOfSoilProfile[self.currentProfileIndex])
            profile.profileName = "New_Profile"
            self.listOfSoilProfile.append(profile)
            self.clearTableProfileList()
            for profile in self.listOfSoilProfile:
                ndx = self.tableProfileList.rowCount()
                self.tableProfileList.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(profile.profileName)
                self.tableProfileList.setItem(ndx, 0, cell)
                self.tableProfileList.setRowHeight(ndx, 20)
            self.currentProfileIndex = len(self.listOfSoilProfile) - 1
            item = self.tableProfileList.item(self.currentProfileIndex,0)
            self.tableProfileList.setCurrentItem(item)
        else:
            profile = SoilProfile()
            profile.profileName = "New_Profile"
            self.listOfSoilProfile.append(profile)
            self.currentProfileIndex = 0

            self.clearTableProfileList()
            for profile in self.listOfSoilProfile:
                ndx = self.tableProfileList.rowCount()
                self.tableProfileList.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(profile.profileName)
                self.tableProfileList.setItem(ndx, 0, cell)
                self.tableProfileList.setRowHeight(ndx, 20)
            item = self.tableProfileList.item(self.currentProfileIndex,0)
            self.tableProfileList.setCurrentItem(item)

            self.btnAddProfile.setText("Copy Profile")
            self.btnAddLayer.setEnabled(True)
            self.btnCopyAndAdd.setEnabled(True)
            self.btnDeleteLayer.setEnabled(True)
            self.txtProfileName.setReadOnly(False)
            self.btnDeleteProfile.setEnabled(True)
            if self.rbtNew.isChecked():
                self.btnSave.setEnabled(True)
            else:
                self.btnSave.setEnabled(True)
                self.btnSaveAs.setEnabled(True)


    def btnDeleteProfile_clicked(self):
        if self.currentProfileIndex > -1:
            message = "Are you sure you want to delete this profile?"
            reply = QtGui.QMessageBox.question(self.form, 'Delete Profile', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                temp = self.currentProfileIndex
                self.tableProfileList.removeRow(temp)
                self.listOfSoilProfile.pop(temp)

                if len(self.listOfSoilProfile)> -1:
                    self.currentProfileIndex = len(self.listOfSoilProfile) - 1

                if self.currentProfileIndex >  -1:
                    item = self.tableProfileList.item(self.currentProfileIndex,0)
                    self.tableProfileList.setCurrentItem(item)
                else:
                    self.currentProfileIndex = -1
                    self.txtProfileName.clear()
                    self.clearTableLayerDetail()

                    self.btnAddProfile.setText("Add Profile")
                    self.btnDeleteProfile.setEnabled(False)
                    self.btnAddLayer.setEnabled(False)
                    self.btnCopyAndAdd.setEnabled(False)
                    self.btnDeleteLayer.setEnabled(False)
                    self.txtProfileName.setReadOnly(True)
                    self.btnSave.setEnabled(False)
                    self.btnSaveAs.setEnabled(False)

    def dataValidity(self):
        errorList = []
        for profile in self.listOfSoilProfile:
            errorList = self.dataValidityForProfile(profile)

            if errorList:
                result = False
                break
        return errorList

    def dataValidityForProfile(self, profile):
        errorList = []

        #checking profile name
        if 1 not in errorList:
            if profile.profileName == "" or profile.profileName.lower() == "new_profile":
                errorList.append(1)

        for layer in profile.soilLayerList:
            #checking horizon name
            if 2 not in errorList:
                if layer.horizonName == "" or layer.horizonName.lower() == "empty":
                    errorList.append(2)

            #Error-03: checking the sum of sand, silt and clay when soil is not organic
            if 3 not in errorList:
                if layer.soilTexture != "O":
                    if round(layer.sandContent + layer.siltContent + layer.clayContent) != 100:
                        errorList.append(3)
                else:
                    #Error-04: checking sand, silt and clay content for organic soil
                    if 4 not in errorList:
                        if layer.soilTexture == "O":
                            if layer.sandContent != 0 or layer.siltContent != 0 or layer.clayContent != 0:
                                errorList.append(4)

            #checking soil texture
            if 5 not in errorList:
                if layer.soilTexture == "": errorList.append(5)

            #checking null values
            if 6 not in errorList:
                if (layer.depthOfHorizon == -9999 or layer.layerThickness == -9999 or layer.correctionFactor == -9999
                    or layer.soilPh == -9999 or layer.organicCarbonContent == -9999 or layer.gravelContent == -9999
                    or layer.sandContent == -9999 or layer.siltContent == -9999 or layer.clayContent == -9999
                    or layer.bulkDensity == -9999 or layer.poreVolume == -9999 or layer.waterCapacity == -9999
                    or layer.permanentWiltingPoint == -9999 or layer.saturatedHydraulicConductivity == -9999):
                    errorList.append(6)

        #checking if there is no horizon in a profile
        if len(profile.soilLayerList) == 0:
            errorList.append(7)

        #Error-08: Difference between "Lower horizon borders" must be multiplier of 2, 5, 10, or 20
        if 8 not in errorList:
            for layer in profile.soilLayerList:
                prvDepthOfHorizon = 0
                for i in reversed(range(len(profile.soilLayerList))):
                    if profile.soilLayerList[i].depthOfHorizon < layer.depthOfHorizon:
                        prvDepthOfHorizon = profile.soilLayerList[i].depthOfHorizon
                        break
                diff = layer.depthOfHorizon - prvDepthOfHorizon
                if diff % 20 != 0 and diff % 10 != 0 and diff % 5 != 0 and diff % 2 != 0: errorList.append(8)

                if 8 not in errorList:
                    if (diff == 0) or (diff % layer.layerThickness != 0): errorList.append(8)
                    # if diff >= 20:
                    #     if diff % 20 != 0: errorList.append(8)
                    # elif diff >= 10:
                    #     if diff % 10 != 0: errorList.append(8)
                    # elif diff >= 5:
                    #     if diff % 5 != 0: errorList.append(8)
                    # elif diff >= 2:
                    #     if diff % 2: errorList.append(8)

        return errorList

    def showErrorMessage(self, errorCode):
        msgTitle = "Invalid Input (Error Code: " + str(errorCode) + ")"

        if errorCode == 1:
            message = "Profile name(s) are invalid. Please enter valid profile name(s)."
            QtGui.QMessageBox.about(self.form, msgTitle, message)
        elif errorCode == 2:
            message = "Horizon name(s) are invalid. Please enter valid horizon name(s)."
            QtGui.QMessageBox.about(self.form, msgTitle, message)
        elif errorCode == 3:
            message = "Sand, silt and clay content must be 100% altogether. Please check sand, silt and clay content."
            QtGui.QMessageBox.about(self.form, msgTitle, message)
        elif errorCode == 4:
            message = "In case of Organic soil sand, silt and clay content should be 0. Please check sand, silt and clay content."
            QtGui.QMessageBox.about(self.form, msgTitle, message)
        elif errorCode == 5:
            message = "Please enter a valid name for soil texture."
            QtGui.QMessageBox.about(self.form, msgTitle, message)
        elif errorCode == 6:
            message = "Some value are found invalid. Please check values."
            QtGui.QMessageBox.about(self.form,msgTitle, message)
        elif errorCode == 7:
            message = "One or more profiles are empty."
            QtGui.QMessageBox.about(self.form, msgTitle, message)
        elif errorCode == 8:
            message = "Difference in layer depths from the previous layer must be multiplier of layer thickness."
            QtGui.QMessageBox.about(self.form, "Invalid Input", message)


    def markProfileNameError(self):
        color = QtGui.QColor(250,103,140)
        for i in range(self.tableProfileList.rowCount()):
            cell = self.tableProfileList.item(i, 0)
            if not cell.text() or cell.text().lower() == "new_profile":
                cell.setBackgroundColor(color)
                cell.setSelected(False)
            else: cell.setBackgroundColor(QtGui.QColor(255,255,255))

    def markError(self):
        color = QtGui.QColor(250,103,140)
        self.markProfileNameError()

        # for i in range(self.tableProfileList.rowCount()):
        #     cell = self.tableProfileList.item(i, 0)
        #     if not cell.text() or cell.text().lower() == "new_profile":
        #         cell.setBackgroundColor(color)
        #         cell.setSelected(False)
        #     else: cell.setBackgroundColor(QtGui.QColor(255,255,255))

        errorList = self.dataValidityForProfile(self.listOfSoilProfile[self.currentProfileIndex])

        #clear background color for all cells
        for i in range(self.tableLayerDetail.rowCount()):
            for j in range(16):
                self.tableLayerDetail.item(i, j).setBackgroundColor(QtGui.QColor(255, 255, 255))

        for errorCode in errorList:
            if errorCode == 2:
                for i in range(self.tableLayerDetail.rowCount()):
                    cell = self.tableLayerDetail.item(i, 0)
                    if cell.text().strip() == "" or cell.text().strip().lower() == "empty":
                        cell.setBackgroundColor(color)
                        cell.setSelected(False)
            elif errorCode == 3:
                for i in range(self.tableLayerDetail.rowCount()):
                    texture = self.tableLayerDetail.item(i, 4).text()
                    if texture != "O":

                        try:
                            sand = float(self.tableLayerDetail.item(i, 8).text())
                            silt = float(self.tableLayerDetail.item(i, 9).text())
                            clay = float(self.tableLayerDetail.item(i, 10).text())

                            if round(sand + silt + clay, 2) != 100.0:
                                self.tableLayerDetail.item(i, 8).setBackgroundColor(color)
                                self.tableLayerDetail.item(i, 9).setBackgroundColor(color)
                                self.tableLayerDetail.item(i, 10).setBackgroundColor(color)
                        except:
                            self.tableLayerDetail.item(i, 8).setBackgroundColor(color)
                            self.tableLayerDetail.item(i, 9).setBackgroundColor(color)
                            self.tableLayerDetail.item(i, 10).setBackgroundColor(color)
            elif errorCode == 4:
                for i in range(self.tableLayerDetail.rowCount()):
                    texture = self.tableLayerDetail.item(i, 4).text()
                    if texture == "O":
                        try:
                            sand = float(self.tableLayerDetail.item(i, 8).text())
                            silt = float(self.tableLayerDetail.item(i, 9).text())
                            clay = float(self.tableLayerDetail.item(i, 10).text())

                            if sand != 0: self.tableLayerDetail.item(i, 8).setBackgroundColor(color)
                            if silt != 0: self.tableLayerDetail.item(i, 9).setBackgroundColor(color)
                            if clay != 0: self.tableLayerDetail.item(i, 10).setBackgroundColor(color)
                        except:
                            self.tableLayerDetail.item(i, 8).setBackgroundColor(color)
                            self.tableLayerDetail.item(i, 9).setBackgroundColor(color)
                            self.tableLayerDetail.item(i, 10).setBackgroundColor(color)
            elif errorCode == 5:
                for i in range(self.tableLayerDetail.rowCount()):
                    texture = self.tableLayerDetail.item(i, 4).text()
                    if texture == "": self.tableLayerDetail.item(i, 4).setBackgroundColor(color)
            elif errorCode == 6:
                for i in range(self.tableLayerDetail.rowCount()):
                    for j in range(16):
                        cellText = self.tableLayerDetail.item(i, j).text()
                        if cellText == "-9999": self.tableLayerDetail.item(i, j).setBackgroundColor(color)

            elif errorCode == 8:
                prvLrDepth = 0
                lrDepth = 0
                lrThick = 0
                for i in range(self.tableLayerDetail.rowCount()):
                    lrDepth = int(self.tableLayerDetail.item(i, 1).text())
                    lrThick = int(self.tableLayerDetail.item(i, 2).text())
                    if i > 0: prvLrDepth = int(self.tableLayerDetail.item(i - 1, 1).text())
                    diff = lrDepth - prvLrDepth
                    if (diff == 0) or (diff % lrThick != 0):
                        self.tableLayerDetail.item(i, 1).setBackgroundColor(color)
                        self.tableLayerDetail.item(i, 2).setBackgroundColor(color)

    def btnSaveAs_clicked(self):
        errorList = self.dataValidity()
        if len(self.listOfSoilProfile) == 0:
            message = "There is no soil profile. Please add soil profile."
            QtGui.QMessageBox.about(self.form, "No Data", message)
        elif len(errorList) > 0:
            self.showErrorMessage(errorList[0])
            self.markError()
        else:
            self.dialog_soil_filename.listOfSoilProfile = self.listOfSoilProfile
            self.dialog_soil_filename.modelDirectory = self.modelDirectory
            self.dialog_soil_filename.dialog.setModal(True)
            self.dialog_soil_filename.dialog.show()


    def showProfileData(self):
        if self.listOfSoilProfile:
            self.clearTableProfileList()
            for profile in self.listOfSoilProfile:
                ndx = self.tableProfileList.rowCount()
                self.tableProfileList.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(profile.profileName)
                self.tableProfileList.setItem(ndx, 0, cell)
                self.tableProfileList.setRowHeight(ndx, 20)
            self.currentProfileIndex = 0
            item = self.tableProfileList.item(0,0)
            self.tableProfileList.setCurrentItem(item)


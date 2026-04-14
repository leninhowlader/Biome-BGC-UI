from interface.FormVegFile import Ui_FormVegFile
from PyQt5 import QtGui, QtCore, QtWidgets
from file_io import FileReadWrite
from application import ApplicationProperty
from parameter import VegetationParameter

class FormVegFile(Ui_FormVegFile):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.addSocket()
        self.addValidator()

        self.formInitialSetting()
        self.vegList = []
        self.isModified = False

        # allowing modification from outside
        self.editMode = False

    def addSocket(self):
        self.btnBrowseVegFile.clicked.connect(self.btnBrowseVegFile_clicked)
        self.btnClose.clicked.connect(self.btnClose_clicked)
        self.rbtNewVegFile.toggled.connect(self.rbtNewVegFile_toggled)
        self.tableWidget.itemSelectionChanged.connect(self.tableWidget_itemSelectionChanged)
        self.tableWidget.itemPressed.connect(self.tableWidget_itemSelectionChanged)
        self.btnAddNew.clicked.connect(self.btnAddNew_clicked)
        self.btnEditAndAdd.clicked.connect(self.btnEditAndAdd_clicked)
        self.btnEditRow.clicked.connect(self.btnEditRow_clicked)
        self.btnDeleteRow.clicked.connect(self.btnDeleteRow_clicked)
        self.btnBrowseEpcFile.clicked.connect(self.btnBrowseEpcFile_clicked)
        self.btnBrowseSsFile.clicked.connect(self.btnBrowseSsFile_clicked)
        self.btnChooseVegDir.clicked.connect(self.btnChooseVegDir_clicked)
        self.btnSave.clicked.connect(self.btnSave_clicked)
        self.btnSaveAs.clicked.connect(self.btnSaveAs_clicked)

    def addValidator(self):
        rx = QtCore.QRegExp("^(19|20)\d{2}$")
        yearValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("^[0-9]*$")
        integerValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("^[\w\-.]+$")
        fileNameValidator= QtGui.QRegExpValidator(rx)

        self.txtVegetationFileName.setValidator(fileNameValidator)
        self.txtVegNumber.setValidator(integerValidator)
        self.txtEpcFile.setValidator(fileNameValidator)
        self.txtStandDensity.setValidator(decimalValidator)
        self.txtStartingTreeAge.setValidator(integerValidator)
        self.txtStartingRootDepth.setValidator(decimalValidator)
        self.txtGrowthClass.setValidator(integerValidator)
        self.txtTreeHeight.setValidator(decimalValidator)
        self.txtSsFile.setValidator(fileNameValidator)
        self.txtLeafCarbon.setValidator(decimalValidator)
        self.txtStemCarbon.setValidator(decimalValidator)
        self.txtDebrisCarbon.setValidator(decimalValidator)
        self.txtLabilePool.setValidator(decimalValidator)
        self.txtUnshieldedCellulosePool.setValidator(decimalValidator)
        self.txtShieldedCellulose.setValidator(decimalValidator)
        self.txtLigninPool.setValidator(decimalValidator)
        self.txtLitterNitrogenPool.setValidator(decimalValidator)

    def formInitialSetting(self):
        self.tableWidget.setColumnCount(17)
        columnHeaderText = ["Site Index", "Veg. Number", "EPC Filename", "Stand Density", "Starting Tree Age", "Starting Root Depth",
                            "Tree Growth Class", "Tree Height", "Species Sequence File", "Leaf Carbon",
                            "Stem Carbon", "CWD Carbon", "Labile Pool", "Unshielded Cellulose Pool", "Shielded Cellulose Pool",
                            "Lignin Pool", "Nitrogen Labile Pool"]
        self.tableWidget.setHorizontalHeaderLabels(columnHeaderText)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(4, 120)
        self.tableWidget.setColumnWidth(5, 130)
        self.tableWidget.setColumnWidth(6, 130)
        self.tableWidget.setColumnWidth(7, 130)
        self.tableWidget.setColumnWidth(8, 200)
        self.tableWidget.setColumnWidth(13, 150)
        self.tableWidget.setColumnWidth(14, 150)
        self.tableWidget.setColumnWidth(16, 150)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.txtVegetationFileName.setEnabled(True)
        self.btnBrowseVegFile.setEnabled(False)
        self.btnChooseVegDir.setEnabled(True)

        self.txtVegFileDirectory.setEnabled(False)
        self.btnEditAndAdd.setEnabled(False)
        self.btnEditRow.setEnabled(False)
        self.btnDeleteRow.setEnabled(False)
        self.btnSaveAs.setEnabled(False)
        self.btnSave.setEnabled(False)
        self.btnSave.setText("Save")

        self.lockField(True)

    def addInVegList(self, veg):
        siteIndex = veg.siteIndex
        vegNumber = veg.vegetationNumber
        for item in self.vegList:
            if item.siteIndex == siteIndex and item.vegetationNumber == vegNumber:
                QtGui.QMessageBox.about(self.form, 'Message', "This vegetation detail is already added in the list.")
                break
        else:
            self.vegList.append(veg)
            return True
        return False

    def editVegList(self, veg):
        siteIndex = veg.siteIndex
        vegNumber = veg.vegetationNumber
        for item in self.vegList:
            if item.siteIndex == siteIndex and item.vegetationNumber == vegNumber:
                item.epcFileName = veg.epcFileName
                item.standDensity = veg.standDensity
                item.startingTreeAge = veg.startingTreeAge
                item.startingRootDepth = veg.startingRootDepth
                item.treeGrowthClass = veg.treeGrowthClass
                item.treeHeight = veg.treeHeight
                item.speciesSeqFile = veg.speciesSeqFile
                item.leafCarbon = veg.leafCarbon
                item.stemCarbon = veg.stemCarbon
                item.debrisCarbon = veg.debrisCarbon
                item.labilePool = veg.labilePool
                item.unshieldedCellulosePool = veg.unshieldedCellulosePool
                item.shieldedCellulosePool = veg.shieldedCellulosePool
                item.ligninPool = veg.ligninPool
                item.nitrogenLabilePool = veg.nitrogenLabilePool
                break
        else:
            QtGui.QMessageBox.about(self.form, 'Message', "This vegetation detail was not found in the list.")
            return False
        return True

    def deleteVegFromList(self, siteIndex, vegetationNumber):
        for item in self.vegList:
            if item.siteIndex == siteIndex and item.vegetationNumber == vegetationNumber:
                self.vegList.remove(item)
                break
        else:
            QtGui.QMessageBox.about(self.form, 'Message', "This vegetation detail was not found in the list.")
            return False
        return True

    def addRowInTable(self, veg):
        for ndx in range(self.tableWidget.rowCount()):
            siteIndex = self.tableWidget.item(ndx, 0).text()
            vegNumber = self.tableWidget.item(ndx, 1).text()
            if siteIndex == veg.siteIndex and vegNumber == veg.vegetationNumber:
                QtGui.QMessageBox.about(self.form, 'Message', "This vegetation detail is already present in the table.")
                break
        else:
            rowIndex = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowIndex)
            self.tableWidget.setRowHeight(rowIndex, 20)
            self.writeValueInTableRow(rowIndex,veg)
            return True
        return False

    def editRowInTable(self, veg):
        for ndx in range(self.tableWidget.rowCount()):
            siteIndex = self.tableWidget.item(ndx, 0).text()
            vegNumber = int(self.tableWidget.item(ndx, 1).text())
            if siteIndex == veg.siteIndex and vegNumber == veg.vegetationNumber:
                self.writeValueInTableRow(ndx, veg)
                break
        else:
            QtGui.QMessageBox.about(self.form, 'Message', "This vegetation detail is not present in the table.")
            return False
        return True

    def deleteRowFromTable(self, siteIndex, vegNumber):
        for ndx in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(ndx, 0).text() == siteIndex and int(self.tableWidget.item(ndx, 1).text()) == vegNumber:
                break
        else:
            QtGui.QMessageBox.about(self.form, 'Message', "This vegetation detail is not present in the table.")
            return False

        self.tableWidget.removeRow(ndx)
        return True

    def clearTable(self):
        for ndx in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(ndx)

    def writeValueInTableRow(self, rowIndex, veg):
        cell = QtWidgets.QTableWidgetItem(veg.siteIndex)
        self.tableWidget.setItem(rowIndex, 0, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.vegetationNumber))
        self.tableWidget.setItem(rowIndex, 1, cell)
        cell = QtWidgets.QTableWidgetItem(veg.epcFileName)
        self.tableWidget.setItem(rowIndex, 2, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.standDensity))
        self.tableWidget.setItem(rowIndex, 3, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.startingTreeAge))
        self.tableWidget.setItem(rowIndex, 4, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.startingRootDepth))
        self.tableWidget.setItem(rowIndex, 5, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.treeGrowthClass))
        self.tableWidget.setItem(rowIndex, 6, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.treeHeight))
        self.tableWidget.setItem(rowIndex, 7, cell)
        cell = QtWidgets.QTableWidgetItem(veg.speciesSeqFile)
        self.tableWidget.setItem(rowIndex, 8, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.leafCarbon))
        self.tableWidget.setItem(rowIndex, 9, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.stemCarbon))
        self.tableWidget.setItem(rowIndex, 10, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.debrisCarbon))
        self.tableWidget.setItem(rowIndex, 11, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.labilePool))
        self.tableWidget.setItem(rowIndex, 12, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.unshieldedCellulosePool))
        self.tableWidget.setItem(rowIndex, 13, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.shieldedCellulosePool))
        self.tableWidget.setItem(rowIndex, 14, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.ligninPool))
        self.tableWidget.setItem(rowIndex, 15, cell)
        cell = QtWidgets.QTableWidgetItem(str(veg.nitrogenLabilePool))
        self.tableWidget.setItem(rowIndex, 16, cell)

    def showTableDataInField(self, rowIndex):
        self.txtSiteIndex.setText(self.tableWidget.item(rowIndex,0).text())
        self.txtVegNumber.setText(self.tableWidget.item(rowIndex,1).text())
        self.txtEpcFile.setText(self.tableWidget.item(rowIndex,2).text())
        self.txtStandDensity.setText(self.tableWidget.item(rowIndex,3).text())
        self.txtStartingTreeAge.setText(self.tableWidget.item(rowIndex,4).text())
        self.txtStartingRootDepth.setText(self.tableWidget.item(rowIndex,5).text())
        self.txtGrowthClass.setText(self.tableWidget.item(rowIndex,6).text())
        self.txtTreeHeight.setText(self.tableWidget.item(rowIndex,7).text())
        self.txtSsFile.setText(self.tableWidget.item(rowIndex,8).text())
        self.txtLeafCarbon.setText(self.tableWidget.item(rowIndex,9).text())
        self.txtStemCarbon.setText(self.tableWidget.item(rowIndex,10).text())
        self.txtDebrisCarbon.setText(self.tableWidget.item(rowIndex,11).text())
        self.txtLabilePool.setText(self.tableWidget.item(rowIndex,12).text())
        self.txtUnshieldedCellulosePool.setText(self.tableWidget.item(rowIndex,13).text())
        self.txtShieldedCellulose.setText(self.tableWidget.item(rowIndex,14).text())
        self.txtLigninPool.setText(self.tableWidget.item(rowIndex,15).text())
        self.txtLitterNitrogenPool.setText(self.tableWidget.item(rowIndex,16).text())

    def createVegFromFieldData(self):
        veg = VegetationParameter()

        veg.siteIndex = self.txtSiteIndex.text()
        veg.vegetationNumber = int(self.txtVegNumber.text())
        veg.epcFileName = self.txtEpcFile.text()
        veg.standDensity = float(self.txtStandDensity.text())
        veg.startingTreeAge = int(self.txtStartingTreeAge.text())
        veg.startingRootDepth = float(self.txtStartingRootDepth.text())
        veg.treeGrowthClass = int(self.txtGrowthClass.text())
        veg.treeHeight = float(self.txtTreeHeight.text())
        veg.speciesSeqFile = self.txtSsFile.text()
        veg.leafCarbon = float(self.txtLeafCarbon.text())
        veg.stemCarbon = float(self.txtStemCarbon.text())
        veg.debrisCarbon = float(self.txtDebrisCarbon.text())
        veg.labilePool = float(self.txtLabilePool.text())
        veg.unshieldedCellulosePool =float(self.txtUnshieldedCellulosePool.text())
        veg.shieldedCellulosePool = float(self.txtShieldedCellulose.text())
        veg.ligninPool = float(self.txtLigninPool.text())
        veg.nitrogenLabilePool = float(self.txtLitterNitrogenPool.text())

        return veg

    def createVegFromTableData(self, rowIndex):
        veg = VegetationParameter()

        veg.siteIndex = self.tableWidget.item(rowIndex, 0).text()
        veg.vegetationNumber = int(self.tableWidget.item(rowIndex, 1).text())
        veg.epcFileName = self.tableWidget.item(rowIndex, 2).text()
        veg.standDensity = float(self.tableWidget.item(rowIndex, 3).text())
        veg.startingTreeAge = int(self.tableWidget.item(rowIndex, 4).text())
        veg.startingRootDepth = float(self.tableWidget.item(rowIndex, 5).text())
        veg.treeGrowthClass = int(self.tableWidget.item(rowIndex, 6).text())
        veg.treeHeight = float(self.tableWidget.item(rowIndex, 7).text())
        veg.speciesSeqFile = self.tableWidget.item(rowIndex, 8).text()
        veg.leafCarbon = float(self.tableWidget.item(rowIndex, 9).text())
        veg.stemCarbon = float(self.tableWidget.item(rowIndex, 10).text())
        veg.debrisCarbon = float(self.tableWidget.item(rowIndex, 11).text())
        veg.labilePool = float(self.tableWidget.item(rowIndex, 12).text())
        veg.unshieldedCellulosePool = float(self.tableWidget.item(rowIndex, 13).text())
        veg.shieldedCellulosePool = float(self.tableWidget.item(rowIndex, 14).text())
        veg.ligninPool = float(self.tableWidget.item(rowIndex, 15).text())
        veg.nitrogenLabilePool = float(self.tableWidget.item(rowIndex, 16).text())

        return veg

    def clearField(self):
        self.txtSiteIndex.clear()
        self.txtVegNumber.clear()
        self.txtEpcFile.clear()
        self.txtStandDensity.clear()
        self.txtStartingTreeAge.clear()
        self.txtStartingRootDepth.clear()
        self.txtGrowthClass.clear()
        self.txtTreeHeight.clear()
        self.txtSsFile.clear()
        self.txtLeafCarbon.clear()
        self.txtStemCarbon.clear()
        self.txtDebrisCarbon.clear()
        self.txtLabilePool.clear()
        self.txtUnshieldedCellulosePool.clear()
        self.txtShieldedCellulose.clear()
        self.txtLigninPool.clear()
        self.txtLitterNitrogenPool.clear()

    def lockField(self, lock):
        self.txtSiteIndex.setReadOnly(lock)
        self.txtVegNumber.setReadOnly(lock)
        self.txtEpcFile.setReadOnly(lock)
        self.btnBrowseEpcFile.setEnabled(not lock)
        self.txtStandDensity.setReadOnly(lock)
        self.txtStartingTreeAge.setReadOnly(lock)
        self.txtStartingRootDepth.setReadOnly(lock)
        self.txtGrowthClass.setReadOnly(lock)
        self.txtTreeHeight.setReadOnly(lock)
        self.txtSsFile.setReadOnly(lock)
        self.btnBrowseSsFile.setEnabled(not lock)
        self.txtLeafCarbon.setReadOnly(lock)
        self.txtStemCarbon.setReadOnly(lock)
        self.txtDebrisCarbon.setReadOnly(lock)
        self.txtLabilePool.setReadOnly(lock)
        self.txtUnshieldedCellulosePool.setReadOnly(lock)
        self.txtShieldedCellulose.setReadOnly(lock)
        self.txtLigninPool.setReadOnly(lock)
        self.txtLitterNitrogenPool.setReadOnly(lock)

    def checkCompleteness(self):
        if len(self.txtSiteIndex.text().strip()) == 0:
            message = "Please enter site index number."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSiteIndex.setFocus(True)
            return False
        elif len(self.txtVegNumber.text().strip()) == 0:
            message = "Please enter vegetation identification number."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtVegNumber.setFocus(True)
            return False
        elif len(self.txtEpcFile.text().strip()) == 0:
            message = "Please choose EPC file."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtEpcFile.setFocus(True)
            return False
        elif len(self.txtStandDensity.text().strip()) == 0:
            message = "Please enter stand density."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtStandDensity.setFocus(True)
            return False
        elif len(self.txtStartingTreeAge.text().strip()) == 0:
            message = "Please enter starting tree age."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtStartingTreeAge.setFocus(True)
            return False
        elif len(self.txtStartingRootDepth.text().strip()) == 0:
            message = "Please enter starting root depth."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtStartingRootDepth.setFocus(True)
            return False
        elif len(self.txtGrowthClass.text().strip()) == 0:
            message = "Please enter growth class."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtGrowthClass.setFocus(True)
            return False
        elif len(self.txtTreeHeight.text().strip()) == 0:
            message = "Please enter tree height."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtTreeHeight.setFocus(True)
            return False
        elif len(self.txtSsFile.text().strip()) == 0:
            message = "Please choose species sequence file."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtSsFile.setFocus(True)
            return False
        elif len(self.txtLeafCarbon.text().strip()) == 0:
            message = "Please enter amount of maximum leaf carbon in first year."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtLeafCarbon.setFocus(True)
            return False
        elif len(self.txtStemCarbon.text().strip()) == 0:
            message = "Please enter amount of maximum stem carbon in first year."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtStemCarbon.setFocus(True)
            return False
        elif len(self.txtDebrisCarbon.text().strip()) == 0:
            message = "Please enter amount of coarse woody debris carbon."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtDebrisCarbon.setFocus(True)
            return False
        elif len(self.txtLabilePool.text().strip()) == 0:
            message = "Please enter amount of litter carbon in labile pool."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtLabilePool.setFocus(True)
            return False
        elif len(self.txtUnshieldedCellulosePool.text().strip()) == 0:
            message = "Please enter amount of litter carbon in unshielded cellulose pool."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtUnshieldedCellulosePool.setFocus(True)
            return False
        elif len(self.txtShieldedCellulose.text().strip()) == 0:
            message = "Please enter amount of litter carbon in shielded cellulose pool."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtShieldedCellulose.setFocus(True)
            return False
        elif len(self.txtLigninPool.text().strip()) == 0:
            message = "Please enter amount of litter carbon in lignin pool."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtLigninPool.setFocus(True)
            return False
        elif len(self.txtLitterNitrogenPool.text().strip()) == 0:
            message = "Please enter value for litter nitrogen labile pool."
            QtGui.QMessageBox.about(self.form, "No Input", message)
            self.txtLitterNitrogenPool.setFocus(True)
            return False
        else:
            return True

    def addVegListInTable(self):
        for veg in self.vegList:
            self.addRowInTable(veg)

    def tableWidget_itemSelectionChanged(self):
        rowIndex = self.tableWidget.currentRow()
        if rowIndex >= 0:
            self.showTableDataInField(rowIndex)

    def btnSaveAs_clicked(self):
        if len(self.vegList) == 0:
            message = "There is no vegetation detail to save!"
            QtGui.QMessageBox.about(self.form, "No Data", message)
        else:
            initDirectory = ""
            if len(ApplicationProperty.currentModelDirectory)>0: initDirectory = ApplicationProperty.currentModelDirectory
            else: initDirectory = ApplicationProperty.getScriptPath ()
            fileName = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save File', initDirectory, "Init File (*.txt)")

            feedback = FileReadWrite.writeVegFile(fileName, self.vegList)
            if feedback:
                QtGui.QMessageBox.about(self.form, "Save", "The VEG file has been saved successfully.")
            else:
                QtGui.QMessageBox.about(self.form, "Error", "The file could not be saved.")

    def btnSave_clicked(self):
        if self.editMode:
            if self.checkCompleteness():
                veg = self.createVegFromFieldData()
                if veg is not None:
                    self.editVegList(veg)
                    self.editRowInTable(veg)
                self.form.parentWidget().close()
        else:
            if len(self.txtVegetationFileName.text().strip()) == 0:
                message = "Please enter the vegetation file name."
                QtGui.QMessageBox.about(self.form, "File Name Missing", message)
                self.txtVegetationFileName.setFocus(True)
            elif len(self.txtVegFileDirectory.text().strip()) == 0:
                message = "Please choose a directory."
                QtGui.QMessageBox.about(self.form, "Directory Name Missing", message)
                self.txtVegFileDirectory.setFocus(True)
            elif len(self.vegList) == 0:
                message = "There is no vegetation data to save."
                QtGui.QMessageBox.about(self.form, "No Data", message)
            else:
                fileName = self.txtVegFileDirectory.text().replace("/ini", "") + "/ini/" + self.txtVegetationFileName.text().strip()

                feedback = FileReadWrite.writeVegFile(fileName, self.vegList)
                if feedback:
                    QtGui.QMessageBox.about(self.form, "Save", "The VEG file has been saved successfully.")
                else:
                    QtGui.QMessageBox.about(self.form, "Error", "The file could not be saved.")

    def btnChooseVegDir_clicked(self):
        initDirectory = ""
        if len(ApplicationProperty.currentModelDirectory)>0: initDirectory = ApplicationProperty.currentModelDirectory
        else: initDirectory = ApplicationProperty.getScriptPath ()
        folderName = str(QtWidgets.QFileDialog.getExistingDirectory(self.form, "Select Directory", initDirectory, QtWidgets.QFileDialog.ShowDirsOnly))
        self.txtVegFileDirectory.setText(folderName)

    def btnBrowseSsFile_clicked(self):
        initDirectory = ""
        if len(ApplicationProperty.currentModelDirectory)>0: initDirectory = ApplicationProperty.currentModelDirectory
        else: initDirectory = ApplicationProperty.getScriptPath ()
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initDirectory, "Text File (*.ss)")
        if len(fileName) > 0: self.txtSsFile.setText(filename[0].split("/")[-1])

    def btnBrowseEpcFile_clicked(self):
        initDirectory = ""
        if len(ApplicationProperty.currentModelDirectory)>0: initDirectory = ApplicationProperty.currentModelDirectory
        else: initDirectory = ApplicationProperty.getScriptPath ()
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initDirectory, "Text File (*.epc)")
        if len(fileName) > 0: self.txtEpcFile.setText(filename[0].split("/")[-1])

    def btnDeleteRow_clicked(self):
        rowIndex = self.tableWidget.currentRow()
        if rowIndex >= 0:
            message = "Are you sure you want delete the selected site?"
            reply = QtGui.QMessageBox.question(self.form, 'Delete Row', message, QtGui.QMessageBox.Yes,
                                                QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                siteIndex = self.tableWidget.item(rowIndex, 0).text()
                vegetationNumber = int(self.tableWidget.item(rowIndex, 1).text())

                if self.deleteVegFromList(siteIndex, vegetationNumber):
                    if self.deleteRowFromTable(siteIndex, vegetationNumber):
                        self.isModified = True

                        if self.tableWidget.rowCount() == 0:
                            self.btnEditAndAdd.setEnabled(False)
                            self.btnEditRow.setEnabled(False)
                            self.btnDeleteRow.setEnabled(False)
                            self.btnSave.setEnabled(False)
                            self.btnSave.setEnabled(False)
                            self.clearField()
                        else:
                            if self.rbtNewVegFile.isChecked():
                                self.btnSave.setEnabled(True)
                            else:
                                self.btnSave.setEnabled(True)
                                self.btnSaveAs.setEnabled(True)
                    else:
                        veg = self.createVegFromTableData(rowIndex)
                        self.addInVegList(veg)

    def btnEditRow_clicked(self):
        if self.btnEditRow.text() == "Edit Row":
            if self.tableWidget.currentRow() >= 0:
                self.frame_2.setEnabled(False)
                self.frameVegFile.setEnabled(False)
                self.tableWidget.setEnabled(False)
                self.btnAddNew.setEnabled(False)
                self.btnEditAndAdd.setEnabled(False)
                self.btnDeleteRow.setEnabled(False)
                self.btnSave.setEnabled(False)
                self.btnSaveAs.setEnabled(False)
                self.btnClose.setText("Cancel")
                self.lockField(False)
                self.txtSiteIndex.setReadOnly(True)
                self.txtVegNumber.setReadOnly(True)
                self.btnEditRow.setText("Update Row")
        else:
            if self.checkCompleteness():
                veg = self.createVegFromFieldData()
                if veg is not None:
                    if self.editVegList(veg):
                        if self.editRowInTable(veg):
                            self.isModified = True

                            self.frame_2.setEnabled(True)
                            self.frameVegFile.setEnabled(True)
                            self.tableWidget.setEnabled(True)
                            self.btnAddNew.setEnabled(True)
                            self.btnEditAndAdd.setEnabled(True)
                            self.btnDeleteRow.setEnabled(True)

                            self.lockField(True)
                            self.btnClose.setText("Close")

                            if self.rbtNewVegFile.isChecked():
                                self.btnSave.setEnabled(True)
                            else:
                                self.btnSave.setEnabled(True)
                                self.btnSaveAs.setEnabled(True)

                            self.btnEditRow.setText("Edit Row")
                        else:
                            rowIndex = self.tableWidget.currentRow()
                            veg = self.createVegFromTableData(rowIndex)
                            self.editVegList(veg)

    def btnEditAndAdd_clicked(self):
        if self.btnEditAndAdd.text() == "Edit and Add":
            if self.tableWidget.currentRow() >= 0:
                self.frame_2.setEnabled(False)
                self.frameVegFile.setEnabled(False)
                self.tableWidget.setEnabled(False)
                self.btnAddNew.setEnabled(False)
                self.btnEditRow.setEnabled(False)
                self.btnDeleteRow.setEnabled(False)
                self.btnSave.setEnabled(False)
                self.btnSaveAs.setEnabled(False)
                self.btnClose.setText("Cancel")
                self.lockField(False)
                self.btnEditAndAdd.setText("Add Row")
        else:
            if self.checkCompleteness():
                veg = self.createVegFromFieldData()
                if veg is not None:
                    if self.addInVegList(veg):
                        if self.addRowInTable(veg):
                            self.isModified = True

                            self.frame_2.setEnabled(True)
                            self.frameVegFile.setEnabled(True)
                            self.tableWidget.setEnabled(True)
                            self.btnAddNew.setEnabled(True)
                            self.btnEditRow.setEnabled(True)
                            self.btnDeleteRow.setEnabled(True)

                            self.tableWidget.setCurrentCell(self.tableWidget.rowCount() - 1, 0)
                            self.lockField(True)
                            self.btnClose.setText("Close")
                            self.btnEditAndAdd.setText("Edit and Add")

                            if self.rbtNewVegFile.isChecked():
                                self.btnSave.setEnabled(True)
                            else:
                                self.btnSave.setEnabled(True)
                                self.btnSaveAs.setEnabled(True)
                        else:
                            self.deleteVegFromList(veg)

    def btnAddNew_clicked(self):
        if self.btnAddNew.text() == "New Row":
            self.btnEditAndAdd.setEnabled(False)
            self.btnEditRow.setEnabled(False)
            self.btnDeleteRow.setEnabled(False)
            self.btnSave.setEnabled(False)
            self.btnSaveAs.setEnabled(False)
            self.tableWidget.setEnabled(False)
            self.frame_2.setEnabled(False)
            self.frameVegFile.setEnabled(False)
            self.btnClose.setText("Cancel")
            self.btnAddNew.setText("Add Row")
            self.clearField()
            self.lockField(False)
        else:
            if self.checkCompleteness():
                veg = self.createVegFromFieldData()
                if veg is not None:
                    if self.addInVegList(veg):
                        if self.addRowInTable(veg):
                            self.isModified = True

                            self.btnEditAndAdd.setEnabled(True)
                            self.btnEditRow.setEnabled(True)
                            self.btnDeleteRow.setEnabled(True)

                            self.tableWidget.setEnabled(True)
                            self.frame_2.setEnabled(True)
                            self.frameVegFile.setEnabled(True)
                            self.btnClose.setText("Close")
                            self.btnAddNew.setText("New Row")
                            self.lockField(True)

                            if self.rbtNewVegFile.isChecked():
                                self.btnSave.setEnabled(True)
                            else:
                                self.btnSaveAs.setEnabled(True)
                                self.btnSave.setEnabled(True)

                            self.tableWidget.setCurrentCell(self.tableWidget.rowCount() - 1, 0)
                        else:
                            self.deleteVegFromList(veg)

    def btnBrowseVegFile_clicked(self):
        initDirectory = ""
        if len(ApplicationProperty.currentModelDirectory)>0: initDirectory = ApplicationProperty.currentModelDirectory
        else: initDirectory = ApplicationProperty.getScriptPath ()
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initDirectory, "Text File (*.txt)")

        if len(fileName) > 0:
            temp = fileName.split("/")[-1]
            self.txtVegetationFileName.setText(temp)
            self.txtVegFileDirectory.setText(fileName.replace("/" + temp, ""))
            ApplicationProperty.currentModelDirectory = self.txtVegFileDirectory.text()
            self.vegList = FileReadWrite.readVegFile(fileName)
            self.clearTable()
            if len(self.vegList) > 0:
                for veg in self.vegList:
                    self.addRowInTable(veg)
                self.btnSaveAs.setEnabled(True)
                self.btnEditAndAdd.setEnabled(True)
                self.btnEditRow.setEnabled(True)
                self.btnDeleteRow.setEnabled(True)
            else:
                self.btnSaveAs.setEnabled(False)
            self.btnAddNew.setEnabled(True)

    def rbtNewVegFile_toggled(self):
        if self.rbtNewVegFile.isChecked():
            self.btnAddNew.setEnabled(True)
            self.txtVegetationFileName.setEnabled(True)
            self.btnBrowseVegFile.setEnabled(False)
            self.btnChooseVegDir.setEnabled(True)
            self.btnSave.setText("Save")
        else:
            self.btnAddNew.setEnabled(False)
            self.txtVegetationFileName.setEnabled(False)
            self.btnBrowseVegFile.setEnabled(True)
            self.btnChooseVegDir.setEnabled(False)
            self.btnSave.setText("Update")
        self.isModified = False
        self.vegList = []
        self.clearTable()
        self.clearField()
        self.lockField(True)
        self.btnSave.setEnabled(False)
        self.btnSaveAs.setEnabled(False)
        self.btnEditAndAdd.setEnabled(False)
        self.btnEditRow.setEnabled(False)
        self.btnDeleteRow.setEnabled(False)

    def btnClose_clicked(self):
        if self.btnClose.text() == "Cancel":
            self.frame_2.setEnabled(True)
            self.frameVegFile.setEnabled(True)
            self.lockField(True)
            self.tableWidget.setEnabled(True)
            self.btnAddNew.setEnabled(True)
            if len(self.vegList) > 0:
                rowIndex = self.tableWidget.currentRow()
                if rowIndex >= 0:
                    self.showTableDataInField(rowIndex)
                else:
                    self.clearField()
                self.btnEditAndAdd.setEnabled(True)
                self.btnEditRow.setEnabled(True)
                self.btnDeleteRow.setEnabled(True)
                if self.rbtNewVegFile.isChecked():
                    self.btnSave.setEnabled(True)
                else:
                    self.btnSaveAs.setEnabled(True)
                    if self.isModified: self.btnSave.setEnabled(True)
            else: self.clearField()
            self.btnAddNew.setText("New Row")
            self.btnEditAndAdd.setText("Edit and Add")
            self.btnEditRow.setText("Edit Row")
            self.btnClose.setText("Close")
        else:
            self.form.parentWidget().close()
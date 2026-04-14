from interface.FormEpcFile import Ui_FormEpcForm
from PyQt5 import QtGui, QtWidgets
from parameter import EpcParameter
from application import ApplicationProperty
from file_io import FileReadWrite
from PyQt5 import QtCore
import os

class FormEpcFile(Ui_FormEpcForm):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.addSocket()

        self.signalMapper = QtCore.QSignalMapper(self.form)
        self.signalMapper.mapped[QtWidgets.QWidget].connect(self.dynamicCombo_indexChanged)

        self.epc = EpcParameter()

        self.initialSetting()
        self.isModified = False

        #variables required to run this module from "Run Model" module
        self.modelParam = None
        self.siteIndex = ""
        self.vegId = -1
        self.versionText = ""
        self.tailReplace = False


        self.editMode = False

    def addSocket(self):
        self.btnBrowseEpcFile.clicked.connect(self.btnBrowseEpcFile_clicked)
        self.rbtNewEpcFile.toggled.connect(self.rbtNewEpcFile_toggled)
        self.tableParam.itemChanged.connect(self.tableParam_itemChanged)
        self.btnClose.clicked.connect(self.btnClose_clicked)
        self.btnSaveAs.clicked.connect(self.btnSaveAs_clicked)
        self.btnSave.clicked.connect(self.btnSave_clicked)
        self.btnChooseEpcDir.clicked.connect(self.btnChooseEpcDir_clicked)

    def initialSetting(self):
        # self.cmbGrowthForm.addItems(["0. NON-WOODY", "1. WOODY"])
        # self.cmbLeaveHabit.addItems(["0. Deciduous", "1. Evergreen"])
        # self.cmbPhotosyntheticPathway.addItems(["0. C4 PSN", "1. c3 PSN"])
        # self.cmbPhenologyOption.addItems(["0. User-specified", "1. Model Phenology", "2. LNVAR Phenology"])
        # self.cmbThinningRuleOption.addItems(["0. Table", "1. Function"])
        #
        # self.cmbGrowthForm.setCurrentIndex(-1)
        # self.cmbLeaveHabit.setCurrentIndex(-1)
        # self.cmbPhotosyntheticPathway.setCurrentIndex(-1)
        # self.cmbPhenologyOption.setCurrentIndex(-1)
        # self.cmbThinningRuleOption.setCurrentIndex(-1)

        self.txtEpcFileDirectory.setEnabled(False)
        self.txtEpcFileName.setEnabled(True)
        self.btnBrowseEpcFile.setEnabled(False)
        self.btnChooseEpcDir.setEnabled(True)
        self.btnSave.setEnabled(False)
        self.btnSaveAs.setEnabled(False)


        self.tableParam.setColumnCount(3)
        columnHeaderText = ["No.", "EPC Parameter", "Value"]
        self.tableParam.setHorizontalHeaderLabels(columnHeaderText)
        self.tableParam.setColumnWidth(0,100)
        self.tableParam.setColumnWidth(1, 350)
        self.tableParam.setColumnWidth(2, 180)
        self.tableParam.verticalHeader().setVisible(False)
        self.tableParam.horizontalHeader().setVisible(True)
        self.setEpcValueInTable()
        # self.includeComboCell()

    # def includeComboCell(self):
    #     ndx = self.tableParam.rowCount()
    #     self.tableParam.insertRow(ndx)
    #
    #     combobox = QtGui.QComboBox()
    #     combobox.addItem('one')
    #     combobox.addItem('two')
    #     combobox.currentIndexChanged.connect(self.dynamicCombo_eh)
    #     self.tableParam.setCellWidget(ndx, 1, combobox)
    #
    #     self.tableParam.setRowHeight(ndx, 25)
    #     item = self.tableParam.cellWidget(ndx, 1)
    #     print(item.currentText())
    #
    # def dynamicCombo_eh(self):
    #     print("Yes, this is it!")

    def rbtNewEpcFile_toggled(self):
        if self.rbtNewEpcFile.isChecked():
            self.txtEpcFileName.setEnabled(True)
            self.btnBrowseEpcFile.setEnabled(False)
            self.btnChooseEpcDir.setEnabled(True)
        else:
            self.txtEpcFileName.setEnabled(False)
            self.btnBrowseEpcFile.setEnabled(True)
            self.btnChooseEpcDir.setEnabled(False)

        self.btnSaveAs.setEnabled(False)
        self.btnSave.setEnabled(False)
        self.epc = EpcParameter()
        self.setEpcValueInTable()
        self.txtEpcFileName.clear()
        self.txtEpcFileDirectory.clear()
        self.isModified = False


    def btnBrowseEpcFile_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory) > 0: startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath()

        fileName = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Text File (*.epc)")

        if len(fileName)>0:
            self.epc = FileReadWrite.readEpcFile(fileName)

            temp = fileName.split("/")[-1]
            self.txtEpcFileName.setText(temp)
            self.txtEpcFileDirectory.setText(fileName.replace("/" + temp, ""))
            if len(ApplicationProperty.currentModelDirectory) == 0:
                ApplicationProperty.currentModelDirectory = self.txtEpcFileDirectory.text()

            if self.epc is not None:
                # self.writeValuesInInputBox()

                self.setEpcValueInTable()
                self.btnSaveAs.setEnabled(True)

    # def writeValuesInInputBox(self):
    #     self.cmbGrowthForm.setCurrentIndex(int(self.epc.growthForm))
    #     self.cmbLeaveHabit.setCurrentIndex(int(self.epc.leafHabit))
    #     self.cmbPhotosyntheticPathway.setCurrentIndex(int(self.epc.photosyntheticPathway))
    #     self.cmbPhenologyOption.setCurrentIndex(int(self.epc.phenologicalControlOption))
    #     self.txtDayOfYearForStartOfNewLeafGrowth.setText(self.epc.dayOfYearForStartOfNewLeafGrowth)
    #     self.txtDayOfYearForMaxLitterFall.setText(self.epc.dayOfYearForMaxLitterFall)
    #     self.txtGrowthPeriodDurationFraction.setText(self.epc.growthPeriodDurationFraction)
    #     self.txtLitterfallPeriodDurationFraction.setText(self.epc.litterfallPeriodDurationFraction)
    #     self.txtOffsetValueForParallelShift.setText(self.epc.offsetValueForParallelShift)
    #     self.txtInterceptConstantForLeafUnfolding.setText(self.epc.interceptConstantForLeafUnfolding)
    #     self.txtSlopeConstantForLeafUnfolding.setText(self.epc.slopeConstantForLeafUnfolding)
    #     self.txtTempThresholdForChillDay.setText(self.epc.tempThresholdForChillDay)
    #     self.txtTempThresholdForThermalTime.setText(self.epc.tempThresholdForThermalTime)
    #     self.txtCriticalDayLengthForLitterfall.setText(self.epc.criticalDayLengthForLitterfall)
    #     self.txtSoilTempForLitterfall.setText(self.epc.soilTempForLitterfall)
    #     self.txtProlongLitterfallFactor.setText(self.epc.prolongLitterfallFactor)
    #     self.txtAnnualLeafTurnoverFraction.setText(self.epc.annualLeafTurnoverFraction)
    #     self.txtAnnualFineRootTurnoverFraction.setText(self.epc.annualFineRootTurnoverFraction)
    #     self.txtAnnualCoarseRootTurnoverFraction.setText(self.epc.annualCoarseRootTurnoverFraction)
    #     self.txtAnnualLiveWoodTurnoverFraction.setText(self.epc.annualLiveWoodTurnoverFraction)
    #     self.txtAnnualWholePlantMortalityFraction.setText(self.epc.annualWholePlantMortalityFraction)
    #     self.txtAnnualFireMortalityFraction.setText(self.epc.annualFireMortalityFraction)
    #     self.txtRatioOfFineRootToLeafGrowth.setText(self.epc.ratioOfFineRootToLeafGrowth)
    #     self.txtRatioOfStemToLeafGrowth.setText(self.epc.ratioOfStemToLeafGrowth)
    #     self.txtRatioOfLiveWoodToTotalWood.setText(self.epc.ratioOfLiveWoodToTotalWood)
    #     self.txtRatioOfCoarseRootToStemGrowth.setText(self.epc.ratioOfCoarseRootToStemGrowth)
    #     self.txtDailyGrowthProportion.setText(self.epc.dailyGrowthProportion)
    #     self.txtLeafCarbonNitrogenMassRatio.setText(self.epc.leafCarbonNitrogenMassRatio)
    #     self.txtLeafLitterCarbonNitrogenMassRatio.setText(self.epc.leafLitterCarbonNitrogenMassRatio)
    #     self.txtFineRootCarbonNitrogenMassRatio.setText(self.epc.fineRootCarbonNitrogenMassRatio)
    #     self.txtCoarseRootCarbonNitrogenMassRatio.setText(self.epc.coarseRootCarbonNitrogenMassRatio)
    #     self.txtLiveWoodCarbonNitrogenMassRatio.setText(self.epc.liveWoodCarbonNitrogenMassRatio)
    #     self.txtDeadWoodCarbonNitrogenMassRatio.setText(self.epc.deadWoodCarbonNitrogenMassRatio)
    #     self.txtStemCoarseRootLitterFraction.setText(self.epc.stemCoarseRootLitterFraction)
    #     self.txtLeafLitterLabileProportion.setText(self.epc.leafLitterLabileProportion)
    #     self.txtLeafLitterCelluloseProportion.setText(self.epc.leafLitterCelluloseProportion)
    #     self.txtLeafLitterLigninProportion.setText(self.epc.leafLitterLigninProportion)
    #     self.txtFineRootLabileProportion.setText(self.epc.fineRootLabileProportion)
    #     self.txtFineRootCelluloseProportion.setText(self.epc.fineRootCelluloseProportion)
    #     self.txtFineRootLigninProportion.setText(self.epc.fineRootLigninProportion)
    #     self.txtDeadWoodCelluloseProportion.setText(self.epc.deadWoodCelluloseProportion)
    #     self.txtDeadWoodLigninProportion.setText(self.epc.deadWoodLigninProportion)
    #     self.txtCanopyWaterInterceptionHeight.setText(self.epc.canopyWaterInterceptionHeight)
    #     self.txtStemWaterInterceptionHeight.setText(self.epc.stemWaterInterceptionHeight)
    #     self.txtAlbedo.setText(self.epc.albedo)
    #     self.txtCanopyLightExtinctionCoefficient.setText(self.epc.canopyLightExtinctionCoefficient)
    #     self.txtAllsidedToProjectedLeafAreaRatio.setText(self.epc.allsidedToProjectedLeafAreaRatio)
    #     self.txtCanopyAverageSecificLeafArea.setText(self.epc.canopyAverageSecificLeafArea)
    #     self.txtRatioOfShadedToSunlitSLA.setText(self.epc.ratioOfShadedToSunlitSLA)
    #     self.txtMaximumTreeHeight.setText(self.epc.maximumTreeHeight)
    #     self.txtStemWoodMassAtMaxHeight.setText(self.epc.stemWoodMassAtMaxHeight)
    #     self.txtFractionOfLeafNitrogenInRubisco.setText(self.epc.fractionOfLeafNitrogenInRubisco)
    #     self.txtStartAgeGrowthReduction.setText(self.epc.startAgeGrowthReduction)
    #     self.txtEndAgeGrowthReduction.setText(self.epc.endAgeGrowthReduction)
    #     self.txtGrowthReductionFactor.setText(self.epc.growthReductionFactor)
    #     self.txtAllocationReductionFactor.setText(self.epc.allocationReductionFactor)
    #     self.txtNitrogenFixation.setText(self.epc.nitrogenFixation)
    #     self.txtMaxStomatalConductance.setText(self.epc.maxStomatalConductance)
    #     self.txtCuticularConductance.setText(self.epc.cuticularConductance)
    #     self.txtBoundaryLayerConductance.setText(self.epc.boundaryLayerConductance)
    #     self.txtAvailableSoilWaterFactor.setText(self.epc.availableSoilWaterFactor)
    #     self.txtWiltingPointFactor.setText(self.epc.wiltingPointFactor)
    #     self.txtStartOfConductanceReductionForVpd.setText(self.epc.startOfConductanceReductionForVpd)
    #     self.txtCompleteConductanceReductionForVpd.setText(self.epc.completeConductanceReductionForVpd)
    #     self.cmbThinningRuleOption.setCurrentIndex(int(self.epc.thinningRuleOption))
    #     self.txtThinningRuleFileName.setText(self.epc.thinningRuleFileName)
    #     self.txtStemCarbonThresholdFor1stThinning.setText(self.epc.stemCarbonThresholdFor1stThinning)
    #     self.txtFirstThinningFraction.setText(self.epc.firstThinningFraction)
    #     self.txtThinningRuleCoefficientB00.setText(self.epc.thinningRuleCoefficientB00)
    #     self.txtThinningRuleCoefficientB01.setText(self.epc.thinningRuleCoefficientB01)
    #     self.txtThinningRuleCoefficientB10.setText(self.epc.thinningRuleCoefficientB10)
    #     self.txtThinningRuleCoefficientB11.setText(self.epc.thinningRuleCoefficientB11)
    #     self.txtThinningRuleCoefficientB12.setText(self.epc.thinningRuleCoefficientB12)
    #     self.txtStartHarvestCoefficientIntercept.setText(self.epc.startHarvestCoefficientIntercept)
    #     self.txtStartHarvestCoefficientSlope.setText(self.epc.startHarvestCoefficientSlope)
    #     self.txtThinningPeriod.setText(self.epc.thinningPeriod)
    #     self.txtAgeOfClearCut.setText(self.epc.ageOfClearCut)
    #     self.txtHarvestCorrectionFactor.setText(self.epc.harvestCorrectionFactor)
    #     self.txtExportFractionCoefficientIntercept.setText(self.epc.exportFractionCoefficientIntercept)
    #     self.txtExportfractionCoefficientSlope.setText(self.epc.exportfractionCoefficientSlope)
    #     self.txtOptimumTempForRootGrowth.setText(self.epc.optimumTempForRootGrowth)
    #     self.txtMinimumTempForRootGrowth.setText(self.epc.minimumTempForRootGrowth)
    #     self.txtBdCoefForMaxRootGrowth.setText(self.epc.bdCoefForMaxRootGrowth)
    #     self.txtCriticalPorosity.setText(self.epc.criticalPorosity)
    #     self.txtMinPhAllowingRootGrowth.setText(self.epc.minPhAllowingRootGrowth)
    #     self.txtMaxPhAllowingRootGrowth.setText(self.epc.maxPhAllowingRootGrowth)
    #     self.txtMinPhForOptimumRootGrowth.setText(self.epc.minPhForOptimumRootGrowth)
    #     self.txtMaxPhForOptimumRootGrowth.setText(self.epc.maxPhForOptimumRootGrowth)
    #     self.txtWaterSaturationStress.setText(self.epc.waterSaturationStress)
    #     self.txtPotentialVerticalRootGrowthRate.setText(self.epc.potentialVerticalRootGrowthRate)
    #     self.txtMaxAgeOfRootGrowth.setText(self.epc.maxAgeOfRootGrowth)
    #     self.txtZetaPlantParameter.setText(self.epc.zetaPlantParameter)


    def setEpcValueInTable(self):
        if self.epc is not None:
            self.deleteAllTableRows()

            groupBackColor = QtGui.QColor(216,191,216)
            for i in range(1, len(EpcParameter.paramLabelList) + 1):
                if i == 4: self.addNewRowInTable("Group", "Phenology","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 17: self.addNewRowInTable("Group", "Turnover","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 23: self.addNewRowInTable("Group", "Allocation","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 28:  self.addNewRowInTable("Group", "C:N Ratios","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 34: self.addNewRowInTable("Group", "Chemical composition of tissues","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 43: self.addNewRowInTable("Group", "Water","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 45: self.addNewRowInTable("Group", "Radiation","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 50: self.addNewRowInTable("Group", "Height/Mass","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 52: self.addNewRowInTable("Group", "Photosynthesis/Growth","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 58: self.addNewRowInTable("Group", "Stomatal Conductance","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 65: self.addNewRowInTable("Group", "Management","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                elif i == 81: self.addNewRowInTable("Group", "Root growth","", bold=True, weight=100, fontSize=10, backColor=groupBackColor)
                parameterLabel = EpcParameter.paramLabelList[i-1]
                parameterValue = self.epc.getParameterValue(parameterLabel)
                self.addNewRowInTable(i, parameterLabel, parameterValue)

    def deleteAllTableRows(self):
        for i in reversed(range(self.tableParam.rowCount())):
            self.tableParam.removeRow(i)

    def addNewRowInTable(self, paramNo, paramName, paramValue, bold=False, weight=75, fontSize=8.5, backColor=QtGui.QColor(255,255,255)):
        font = QtGui.QFont()
        if bold:
            font.setBold(bold)
            font.setWeight(weight)
        font.setPointSize(fontSize)

        ndx = self.tableParam.rowCount()
        self.tableParam.insertRow(ndx)
        self.tableParam.setRowHeight(ndx, 23)

        cell = QtWidgets.QTableWidgetItem(str(paramNo))
        cell.setFont(font)
        if bold: cell.setBackground(backColor)
        cell.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableParam.setItem(ndx, 0, cell)
        cell = QtWidgets.QTableWidgetItem(paramName)
        cell.setFont(font)
        if bold: cell.setBackground(backColor)
        cell.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableParam.setItem(ndx, 1, cell)

        valueText = str(paramValue)

        if str(paramNo) == '5' and paramValue == -2: valueText = ""
        elif str(paramNo) in ['10', '11', '12', '13'] and paramValue == 0: valueText = ""
        elif str(paramNo) == '15' and paramValue == -273: valueText = ""
        elif paramValue == -1: valueText = ""

        #checking is domain exists
        hasDomain = EpcParameter.hasDomain(paramName)
        if hasDomain:
            comboCell = QtGui.QComboBox()
            comboCell.addItems(EpcParameter.getDomain(paramName))
            currentIndex = -1
            try: currentIndex = int(valueText)
            except: pass
            comboCell.setCurrentIndex(currentIndex)
            comboCell.currentIndexChanged.connect(self.signalMapper.map)
            self.tableParam.setCellWidget(ndx, 2, comboCell)
            comboCell.RowIndex = ndx
            # comboCell.ColumnIndex = i + 1
            self.signalMapper.setMapping(comboCell, comboCell)
        else:

            cell = QtWidgets.QTableWidgetItem(valueText)
            if bold:
                cell.setBackground(backColor)
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
            cell.setFont(font)
            self.tableParam.setItem(ndx, 2, cell)

    @QtCore.pyqtSlot(QtWidgets.QWidget)
    def dynamicCombo_indexChanged(self, comboCell):
        if comboCell.currentIndex() > -1:
            item2000 = self.tableParam.currentItem()

            rowIndex = comboCell.RowIndex
            varPosIndex = int(self.tableParam.item(rowIndex, 0).text())
            paramDesc = self.tableParam.item(rowIndex, 1).text()

            newVal = str(comboCell.currentIndex())
            if len(newVal.strip()) > 0:
                result = None
                if self.modelParam is None:
                    result = self.epc.setParameterValue(varPosIndex, paramDesc, newVal)
                else:
                    result = self.modelParam.updateEpcObject(self.siteIndex, self.vegId, varPosIndex, paramDesc, newVal,
                                                             self.versionText, self.tailReplace)
                if result is not None:
                    comboCell.setCurrentIndex(int(result))
                else:
                    self.isModified = True
                if self.checkCompleteness():
                    self.btnSave.setEnabled(True)
                    if self.rbtModifyEpcFile.isChecked(): self.btnSaveAs.setEnabled(True)
                else:
                    self.btnSave.setEnabled(False)
                    self.btnSaveAs.setEnabled(False)
            else:
                QtGui.QMessageBox.about(self.form, "Input Required", "Please insert value for this parameter.")

    def tableParam_itemChanged(self):
        item = self.tableParam.currentItem()

        if item is not None:
            rowIndex = self.tableParam.currentRow()
            varPosIndex = int(self.tableParam.item(rowIndex, 0).text())
            paramDesc = self.tableParam.item(rowIndex, 1).text()

            newVal = item.text()
            if len(newVal.strip()) > 0:
                result = None
                if self.modelParam is None:
                    result = self.epc.setParameterValue(varPosIndex, paramDesc, newVal)
                else:
                    result = self.modelParam.updateEpcObject(self.siteIndex, self.vegId, varPosIndex, paramDesc, newVal,
                                                             self.versionText, self.tailReplace)
                if result is not None:
                    item.setText(str(result))
                else:
                    self.isModified = True
                if self.checkCompleteness():
                    self.btnSave.setEnabled(True)
                    if self.rbtModifyEpcFile.isChecked(): self.btnSaveAs.setEnabled(True)
                else:
                    self.btnSave.setEnabled(False)
                    self.btnSaveAs.setEnabled(False)
            else:
                QtGui.QMessageBox.about(self.form, "Input Required", "Please insert value for this parameter.")

    def checkCompleteness(self):
        for i in range(self.tableParam.rowCount()):
            if self.tableParam.item(i, 0).text() != "Group":
                item = self.tableParam.item(i, 2)
                if item is not None:
                    if len(self.tableParam.item(i, 2).text().strip()) == 0:
                        break
                else:
                    item = self.tableParam.cellWidget(i,2)
                    if item.currentIndex() == -1: break
        else:
            return True
        False

    def btnChooseEpcDir_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory) > 0: startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath()
        folderName = str(QtWidgets.QFileDialog.getExistingDirectory(self.form, "Select Directory", startingDir, QtWidgets.QFileDialog.ShowDirsOnly))
        self.txtEpcFileDirectory.setText(folderName)

    def btnSaveAs_clicked(self):
        if self.checkCompleteness():
            startingDir = ""
            if len(ApplicationProperty.currentModelDirectory) > 0: startingDir = ApplicationProperty.currentModelDirectory
            else: startingDir = ApplicationProperty.getScriptPath()
            fileName = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save File', startingDir, "EPC File (*.epc)")
            if len(fileName) > 0:
                if FileReadWrite.writeEpcFile(fileName,self.epc):
                    message = "Epc file has been saved successfully."
                    QtGui.QMessageBox.about(self.form, "Saved Successfully", message)

    def btnSave_clicked(self):
        if len(self.txtEpcFileName.text().strip()) == 0:
            QtGui.QMessageBox.about(self.form, "Input Required", "Please enter the file name.")
            self.txtEpcFileName.setFocus(True)
        elif len(self.txtEpcFileDirectory.text().strip()) == 0:
            QtGui.QMessageBox.about(self.form, "Input Required", "Please choose proper directory")
            self.btnChooseEpcDir.setFocus(True)
        else:
            if self.checkCompleteness():
                fileName = os.path.join(self.txtEpcFileDirectory.text().strip().replace("/epc", ""), "epc",
                                        self.txtEpcFileName.text().strip().replace(".epc","") + ".epc")
                # fileName += self.txtEpcFileName.text().strip().replace(".epc","") + ".epc"

                feedback = FileReadWrite.writeEpcFile(fileName, self.epc)
                if feedback:
                    QtGui.QMessageBox.about(self.form, "Save", "The EPC file has been saved successfully.")
                else:
                    QtGui.QMessageBox.about(self.form, "Error", "The file could not be saved.")

    def btnClose_clicked(self):
        self.form.parentWidget().close()
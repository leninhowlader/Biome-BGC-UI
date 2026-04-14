from PyQt5 import QtCore, QtGui, QtWidgets
from interface.FormInitialAndOutputSetting import Ui_FormInitialAndOutputSetting
from domain import ParamOption
from application import ApplicationProperty
from file_io import FileReadWrite
from parameter import InitialParameter
import os

class FormInitialAndOutputSetting(Ui_FormInitialAndOutputSetting):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)

        self.addValidator()
        self.addSocket()

        self.initParam = InitialParameter()

        #reading template flag
        #This flag was used to avoid reading unwanted template file.
        self.read_template_file_flag = False

        self.initialSetting()

        #this boolean control variable was added in order to edit the parameters from
        #outside the form
        self.editMode = False

    def addValidator(self):
        rx = QtCore.QRegExp("^(19|20)\d{2}$")
        yearValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("^[0-9]*$")
        integerValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("^[\w\-.]+$")
        fileNameValidator= QtGui.QRegExpValidator(rx)

        self.txtInitFileName.setValidator(fileNameValidator)
        self.txtGisFileName.setValidator(fileNameValidator)
        self.txtVegFileName.setValidator(fileNameValidator)
        self.txtRestartFileRead.setValidator(fileNameValidator)
        self.txtRestartFileWrite.setValidator(fileNameValidator)
        self.txtCarbonFile.setValidator(fileNameValidator)
        self.txtStartYear.setValidator(integerValidator)
        self.txtEndYear.setValidator(integerValidator)
        self.txtRefYear.setValidator(integerValidator)
        self.txtSpinupYear.setValidator(integerValidator)
        self.txtTmaxOffset.setValidator(decimalValidator)
        self.txtTminOffset.setValidator(decimalValidator)
        self.txtPrecipitationMulp.setValidator(decimalValidator)
        self.txtVpdMulp.setValidator(decimalValidator)
        self.txtRadiationMulp.setValidator(decimalValidator)
        self.txtConsConcentration.setValidator(decimalValidator)
        self.txtLayerSpecificDailySoilDepth.setValidator(integerValidator)
        self.txtLayerSpecificDailyLowerBound.setValidator(integerValidator)
        self.txtLayerSpecificDailySoilDepth_2.setValidator(integerValidator)
        self.txtLayerSpecificDailyLowerBound_2.setValidator(integerValidator)
        self.txtLayerSpecificAnnualSoilDepth.setValidator(integerValidator)
        self.txtLayerSpecificAnnualLowerBound.setValidator(integerValidator)
        self.txtLayerSpecificAnnualSoilDepth_2.setValidator(integerValidator)
        self.txtLayerSpecificAnnualLowerBound_2.setValidator(integerValidator)

    def addSocket(self):
        # self.txtStartYear.textChanged.connect(self.InputIntegerOnly(self.txtStartYear))
        self.ckbShowAllSelectedVegVariable.toggled.connect(self.ckbShowAllSelectedVegVariable_toggled)
        self.ckbShowAllSelectedSiteVariable.toggled.connect(self.ckbShowAllSelectedSiteVariable_toggled)
        self.btnClear.clicked.connect(self.btnClear_clicked)
        # self.btnClearVegVariables.clicked.connect(self.btnClearVegVariables_click)
        # self.btnClearSiteVariables.clicked.connect(self.btnClearSiteVariables_click)
        self.btnClose.clicked.connect(self.btnClose_clicked)
        self.rbtNewInitFile.toggled.connect(self.rbtNewInitFile_toggled)
        self.btnBrowseInitFile.clicked.connect(self.btnBrowseInitFile_clicked)
        self.btnChooseInitDir.clicked.connect(self.btnChooseInitDir_clicked)
        self.btnBrowseGisFile.clicked.connect(self.btnBrowseGisFile_clicked)
        self.btnBrowseVegFile.clicked.connect(self.btnBrowseVegFile_clicked)
        self.ckbWriteRestartFile.clicked.connect(self.ckbWriteRestartFile_toggled)
        self.ckbReadRestartFile.clicked.connect(self.ckbReadRestartFile_toggled)
        self.btnBrowseRestartFileRead.clicked.connect(self.btnBrowseRestartFileRead_clicked)
        self.btnBrowseRestartFileWrite.clicked.connect(self.btnBrowseRestartFileWrite_clicked)
        self.ckbSpinup.toggled.connect(self.ckbSpinup_toggled)
        self.rbtCCContant.toggled.connect(self.rbtCCContant_toggled)
        self.btnCarbonFile.clicked.connect(self.btnCarbonFile_clicked)
        self.ckbUseOutputTemplate.toggled.connect(self.ckbUseOutputTemplate_toggled)
        self.ckbSaveOutputTemplate.toggled.connect(self.ckbSaveOutputTemplate_toggled)
        self.rbtSiteSpecificDailyOutput.toggled.connect(self.rbtSiteSpecificDailyOutput_toggled)
        self.cmbSiteSpecificOutputCategory.currentIndexChanged.connect(self.cmbSiteSpecificOutputCategory_currentIndexChanged)
        self.rbtVegetationSpecificDailyOutput.toggled.connect(self.rbtVegetationSpecificDailyOutput_toggled)
        self.cmbVegetationSpecificCategory.currentIndexChanged.connect(self.cmbVegetationSpecificCategory_currentIndexChanged)
        self.btnSiteSpecificVariableAdd.clicked.connect(self.btnSiteSpecificVariableAdd_clicked)
        self.btnSiteSpecificVariableAddAll.clicked.connect(self.btnSiteSpecificVariableAddAll_clicked)
        self.btnSiteSpecificVariableRemove.clicked.connect(self.btnSiteSpecificVariableRemove_clicked)
        self.btnSiteSpecificVariableRemoveAll.clicked.connect(self.btnSiteSpecificVariableRemoveAll_clicked)
        self.btnVegetationSpecificVariableAdd.clicked.connect(self.btnVegetationSpecificVariableAdd_clicked)
        self.btnVegetationSpecificVariableAddAll.clicked.connect(self.btnVegetationSpecificVariableAddAll_clicked)
        self.btnVegetationSpecificVariableRemove.clicked.connect(self.btnVegetationSpecificVariableRemove_clicked)
        self.btnVegetationSpecificVariableRemoveAll.clicked.connect(self.btnVegetationSpecificVariableRemoveAll_clicked)
        self.btnTotalLayerVariableAdd.clicked.connect(self.btnTotalLayerVariableAdd_clicked)
        self.btnTotalLayerVariableAddAll.clicked.connect(self.btnTotalLayerVariableAddAll_clicked)
        self.btnTotalLayerVariableRemove.clicked.connect(self.btnTotalLayerVariableRemove_clicked)
        self.btnTotalLayerVariableRemoveAll.clicked.connect(self.btnTotalLayerVariableRemoveAll_clicked)
        self.rbtLayerSpecificAnnualSpecificDepth.toggled.connect(self.rbtLayerSpecificAnnualSpecificDepth_toggled)
        self.rbtLayerSpecificAnnualMaxDepth_2.toggled.connect(self.rbtLayerSpecificAnnualMaxDepth_2_toggled)
        self.rbtLayerSpecificDailySpecificDepth.toggled.connect(self.rbtLayerSpecificDailySpecificDepth_toggled)
        self.rbtLayerSpecificDailySpecificDepth_2.toggled.connect(self.rbtLayerSpecificDailySpecificDepth_2_toggled)
        self.btnLayerSpecificDailyVariableAdd.clicked.connect(self.btnLayerSpecificDailyVariableAdd_clicked)
        self.btnLayerSpecificDailyVariableRemove.clicked.connect(self.btnLayerSpecificDailyVariableRemove_clicked)
        self.btnLayerSpecificAnnualVariableAdd.clicked.connect(self.btnLayerSpecificAnnualVariableAdd_clicked)
        self.btnLayerSpecificAnnualVariableRemove.clicked.connect(self.btnLayerSpecificAnnualVariableRemove_clicked)
        self.btnLayerSpecificDailyLayerAdd.clicked.connect(self.btnLayerSpecificDailyLayerAdd_clicked)
        self.btnLayerSpecificDailyLayerRemove.clicked.connect(self.btnLayerSpecificDailyLayerRemove_clicked)
        self.btnLayerSpecificAnnualLayerAdd.clicked.connect(self.btnLayerSpecificAnnualLayerAdd_clicked)
        self.btnLayerSpecificAnnualLayerRemove.clicked.connect(self.btnLayerSpecificAnnualLayerRemove_clicked)
        self.btnSave.clicked.connect(self.btnSave_clicked)
        self.cmbOutputTemplate.currentIndexChanged.connect(self.cmbOutputTemplate_currentIndexChanged)

    def initialSetting(self):
        #design table widget for site specific variables
        self.twSiteSpecificVariable.setColumnCount(3)
        header = ["No.", "Variable Name", "Variable Label"]
        self.twSiteSpecificVariable.setHorizontalHeaderLabels(header)
        self.twSiteSpecificVariable.setColumnWidth(0, 50)
        self.twSiteSpecificVariable.setColumnWidth(1, 180)
        self.twSiteSpecificVariable.setColumnWidth(2, 190)

        #design table widget for veg specific variables
        self.twVegSpecificVariable.setColumnCount(3)
        header = ["No.", "Variable Name", "Variable Label"]
        self.twVegSpecificVariable.setHorizontalHeaderLabels(header)
        self.twVegSpecificVariable.setColumnWidth(0, 50)
        self.twVegSpecificVariable.setColumnWidth(1, 180)
        self.twVegSpecificVariable.setColumnWidth(2, 190)

        #design table widget for site specific selected variables
        self.twVegetationSpecificSelectedVariable.setColumnCount(3)
        header = ["No.", "Variable Name", "Variable Label"]
        self.twVegetationSpecificSelectedVariable.setHorizontalHeaderLabels(header)
        self.twVegetationSpecificSelectedVariable.setColumnWidth(0, 50)
        self.twVegetationSpecificSelectedVariable.setColumnWidth(1, 180)
        self.twVegetationSpecificSelectedVariable.setColumnWidth(2, 190)

        #design table widget for vegetation specific selected variables
        self.twSiteSpecificSelectedVariable.setColumnCount(3)
        header = ["No.", "Variable Name", "Variable Label"]
        self.twSiteSpecificSelectedVariable.setHorizontalHeaderLabels(header)
        self.twSiteSpecificSelectedVariable.setColumnWidth(0, 50)
        self.twSiteSpecificSelectedVariable.setColumnWidth(1, 180)
        self.twSiteSpecificSelectedVariable.setColumnWidth(2, 190)

        #design table widget for layer variables
        self.twTotalLayerVariableList.setColumnCount(3)
        header = ["No.", "Variable Name", "Variable Label"]
        self.twTotalLayerVariableList.setHorizontalHeaderLabels(header)
        self.twTotalLayerVariableList.setColumnWidth(0, 50)
        self.twTotalLayerVariableList.setColumnWidth(1, 180)
        self.twTotalLayerVariableList.setColumnWidth(2, 190)

        #design table widget for selected layer variables
        self.twTotalLayerSelectedVariable.setColumnCount(3)
        header = ["No.", "Variable Name", "Variable Label"]
        self.twTotalLayerSelectedVariable.setHorizontalHeaderLabels(header)
        self.twTotalLayerSelectedVariable.setColumnWidth(0, 50)
        self.twTotalLayerSelectedVariable.setColumnWidth(1, 180)
        self.twTotalLayerSelectedVariable.setColumnWidth(2, 190)


        #design table widget for Layer Specific Daily Variable List
        self.twLayerSpecificDailyVariableList.setColumnCount(3)
        header = ["No.", "Variable Name", "Variable Label"]
        self.twLayerSpecificDailyVariableList.setHorizontalHeaderLabels(header)
        self.twLayerSpecificDailyVariableList.setColumnWidth(0, 50)
        self.twLayerSpecificDailyVariableList.setColumnWidth(1, 180)
        self.twLayerSpecificDailyVariableList.setColumnWidth(2, 190)

        #design table widget for Layer Specific Annual VariableList
        self.twLayerSpecificAnnualVariableList.setColumnCount(3)
        header = ["No.", "Variable Name", "Variable Label"]
        self.twLayerSpecificAnnualVariableList.setHorizontalHeaderLabels(header)
        self.twLayerSpecificAnnualVariableList.setColumnWidth(0, 50)
        self.twLayerSpecificAnnualVariableList.setColumnWidth(1, 180)
        self.twLayerSpecificAnnualVariableList.setColumnWidth(2, 190)

        #loading layer specific variable names
        varlist = self.initParam.output.getLayerSpecificVariableList()
        for var in varlist:
            ndx = self.twTotalLayerVariableList.rowCount()
            self.twTotalLayerVariableList.insertRow(ndx)
            cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
            self.twTotalLayerVariableList.setItem(ndx, 0, cell)
            cell = QtWidgets.QTableWidgetItem(var["varname"])
            self.twTotalLayerVariableList.setItem(ndx, 1, cell)
            cell = QtWidgets.QTableWidgetItem(var["vardesc"])
            self.twTotalLayerVariableList.setItem(ndx, 2, cell)
            self.twTotalLayerVariableList.setRowHeight(ndx, 20)
            self.cmbLayerSpecificAnnualVariableList.addItem("(" + str(var["varid"]) + ") " + var["varname"])
            self.cmbLayerSpecificDailyVariableList.addItem("(" + str(var["varid"]) + ") " + var["varname"])

            ndx = self.twLayerSpecificDailyVariableList.rowCount()
            self.twLayerSpecificDailyVariableList.insertRow(ndx)
            cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
            self.twLayerSpecificDailyVariableList.setItem(ndx, 0, cell)
            cell = QtWidgets.QTableWidgetItem(var["varname"])
            self.twLayerSpecificDailyVariableList.setItem(ndx, 1, cell)
            cell = QtWidgets.QTableWidgetItem(var["vardesc"])
            self.twLayerSpecificDailyVariableList.setItem(ndx, 2, cell)
            self.twLayerSpecificDailyVariableList.setRowHeight(ndx, 20)

            ndx = self.twLayerSpecificAnnualVariableList.rowCount()
            self.twLayerSpecificAnnualVariableList.insertRow(ndx)
            cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
            self.twLayerSpecificAnnualVariableList.setItem(ndx, 0, cell)
            cell = QtWidgets.QTableWidgetItem(var["varname"])
            self.twLayerSpecificAnnualVariableList.setItem(ndx, 1, cell)
            cell = QtWidgets.QTableWidgetItem(var["vardesc"])
            self.twLayerSpecificAnnualVariableList.setItem(ndx, 2, cell)
            self.twLayerSpecificAnnualVariableList.setRowHeight(ndx, 20)


        self.rbtNewInitFile.setChecked(True)
        self.tbwSettings.setCurrentIndex(0)
        self.btnBrowseInitFile.setEnabled(False)
        self.txtInitFileDirectory.setEnabled(False)
        self.txtRestartFileRead.setEnabled(False)
        self.ckbReadRestartFile.setChecked(False)
        self.txtRestartFileWrite.setEnabled(False)
        self.ckbWriteRestartFile.setChecked(False)
        self.btnBrowseRestartFileRead.setEnabled(False)
        self.btnBrowseRestartFileWrite.setEnabled(False)
        self.rbtMetyearNo.setChecked(True)
        self.txtSpinupYear.setEnabled(False)
        self.rbtCCContant.setChecked(True)
        self.cmbOutputTemplate.setEnabled(False)
        self.txtTemplateName.setEnabled(False)
        self.rbtDispProgressYes.setChecked(True)
        self.txtCarbonFile.setEnabled(False)
        self.btnCarbonFile.setEnabled(False)
        self.txtConsConcentration.setText("400")
        self.txtTmaxOffset.setText("0")
        self.txtTminOffset.setText("0")
        self.txtPrecipitationMulp.setText("1")
        self.txtVpdMulp.setText("1")
        self.txtRadiationMulp.setText("1")
        self.txtRefYear.setText("2006")

        #loading nitrogen deposition options
        for item in ParamOption.nitrogenDepositionOptionList:
            self.cmbNitrogenDiposition.addItem(item['param'])
        self.cmbNitrogenDiposition.setCurrentIndex(0)

        #loading daily output options
        for item in ParamOption.dailyOutputOptionList:
            self.cmbDailyOutputType.addItem(item['param'])
        self.cmbDailyOutputType.setCurrentIndex(4)

        #loading annual output options
        for item in ParamOption.annualOutputOptionList:
            self.cmbYearlyOutputType.addItem(item['param'])
        self.cmbYearlyOutputType.setCurrentIndex(4)

        self.rbtSiteSpecificDailyOutput.setChecked(True)
        #loading site specific output category
        for item in self.initParam.output.listOfSiteSpecificCategory:
            self.cmbSiteSpecificOutputCategory.addItem(item["catname"])
        self.cmbSiteSpecificOutputCategory.setCurrentIndex(-1)

        self.rbtVegetationSpecificDailyOutput.setChecked(True)
        #loading vegetation specific output category
        for item in self.initParam.output.listOfVegSpecificCategory:
            self.cmbVegetationSpecificCategory.addItem(item["catname"])
        self.cmbVegetationSpecificCategory.setCurrentIndex(-1)

        self.cmbLayerSpecificAnnualVariableList.setCurrentIndex(-1)
        self.cmbLayerSpecificDailyVariableList.setCurrentIndex(-1)

        self.rbtLayerSpecificAnnualSpecificDepth.setChecked(True)
        self.rbtLayerSpecificAnnualMaxDepth_2.setChecked(True)
        self.rbtLayerSpecificDailySpecificDepth.setChecked(True)
        self.rbtLayerSpecificDailySpecificDepth_2.setChecked(True)

        self.lblLayerSpecificAnnualLowerBound.setVisible(False)
        self.txtLayerSpecificAnnualLowerBound.setVisible(False)
        self.lblLayerSpecificAnnualLowerBound_2.setVisible(False)
        self.txtLayerSpecificAnnualLowerBound_2.setVisible(False)

        self.lblLayerSpecificDailyLowerBound.setVisible(False)
        self.txtLayerSpecificDailyLowerBound.setVisible(False)
        self.lblLayerSpecificDailyLowerBound_2.setVisible(False)
        self.txtLayerSpecificDailyLowerBound_2.setVisible(False)


        #these buttons seem to be of no importance
        self.btnClearSiteVariables.setVisible(False)
        self.btnClearVegVariables.setVisible(False)

        #set no edit trigger
        self.twSiteSpecificVariable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twSiteSpecificSelectedVariable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twVegSpecificVariable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twVegetationSpecificSelectedVariable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twTotalLayerVariableList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twTotalLayerSelectedVariable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twLayerSpecificDailyVariableList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twLayerSpecificAnnualVariableList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.twSiteSpecificVariable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def clearField(self):
        self.txtGisFileName.clear()
        self.txtVegFileName.clear()
        self.ckbReadRestartFile.setChecked(False)
        self.ckbWriteRestartFile.setChecked(False)
        self.txtRestartFileRead.clear()
        self.txtRestartFileWrite.clear()
        self.rbtMetyearNo.setChecked(True)
        self.txtStartYear.clear()
        self.txtEndYear.clear()
        self.ckbSpinup.setChecked(False)
        self.txtSpinupYear.clear()
        self.txtTmaxOffset.setText("0")
        self.txtTminOffset.setText("0")
        self.txtPrecipitationMulp.setText("1")
        self.txtVpdMulp.setText("1")
        self.txtRadiationMulp.setText("1")
        self.rbtCCContant.setChecked(True)
        self.txtConsConcentration.setText("400")
        self.txtCarbonFile.clear()
        self.cmbNitrogenDiposition.setCurrentIndex(0)
        self.txtRefYear.setText("2006")
        self.txtOutputFilePrefix.clear()
        self.rbtDispProgressYes.setChecked(True)
        self.cmbDailyOutputType.setCurrentIndex(4)
        self.ckbMonthAverage.setChecked(False)
        self.ckbYearAverage.setChecked(False)
        self.cmbYearlyOutputType.setCurrentIndex(4)
        self.ckbUseOutputTemplate.setChecked(False)
        self.cmbOutputTemplate.setCurrentIndex(-1)
        self.ckbSaveOutputTemplate.setChecked(False)
        self.txtTemplateName.clear()
        self.ckbShowAllSelectedSiteVariable.setChecked(False)
        self.ckbShowAllSelectedVegVariable.setChecked(False)
        self.clearSelectedVariableList()

    def btnLayerSpecificAnnualLayerRemove_clicked(self):
        if len(self.lstLayerSpecificAnnualSelectedVariableLayer.selectedItems()) > 0:
            varid = self.lstLayerSpecificAnnualSelectedVariableLayer.currentItem().text().split(":")[0].strip()

            if varid:
                self.initParam.output.removeVariableFromAnnualVarLayList(varid)
                self.lstLayerSpecificAnnualSelectedVariableLayer.clear()
                temp = self.initParam.output.getTextLinesFromAnnualVarLayerList()
                self.lstLayerSpecificAnnualSelectedVariableLayer.addItems(temp)

    def btnLayerSpecificAnnualLayerAdd_clicked(self):
        if self.cmbLayerSpecificAnnualVariableList.currentIndex() > -1:
            varname = self.cmbLayerSpecificAnnualVariableList.currentText().split(")")[-1].strip()
            layer = ""
            if self.rbtLayerSpecificAnnualMaxDepth_2.isChecked():
                layer = self.txtLayerSpecificAnnualSoilDepth_2.text().strip()
            else:
                lower = self.txtLayerSpecificAnnualSoilDepth_2.text().strip()
                upper = self.txtLayerSpecificAnnualLowerBound_2.text().strip()
                if lower and upper:
                    if int(lower) < int(upper):
                        layer = lower + "-" + upper
                    else:
                        QtGui.QMessageBox.about(self.form, "Invalid Input", "Lower bound can't be smaller than the upper bound")

            if layer:
                self.initParam.output.addVariableToAnnualVarLayList(varname, layer)
                self.lstLayerSpecificAnnualSelectedVariableLayer.clear()
                temp = self.initParam.output.getTextLinesFromAnnualVarLayerList()
                self.lstLayerSpecificAnnualSelectedVariableLayer.addItems(temp)

                self.txtLayerSpecificDailySoilDepth_2.clear()
                self.txtLayerSpecificDailyLowerBound_2.clear()

    def btnLayerSpecificDailyLayerRemove_clicked(self):
        if len(self.lstLayerSpecificDailySelectedVariableLayer.selectedItems()) > 0:
            varid = self.lstLayerSpecificDailySelectedVariableLayer.currentItem().text().split(":")[0].strip()

            # varname = self.cmbLayerSpecificDailyVariableList.currentText()

            if varid:
                self.initParam.output.removeVariableFromDailyVarLayList(varid)
                self.lstLayerSpecificDailySelectedVariableLayer.clear()
                temp = self.initParam.output.getTextLinesFromDailyVarLayerList()
                self.lstLayerSpecificDailySelectedVariableLayer.addItems(temp)

    def btnLayerSpecificDailyLayerAdd_clicked(self):
        if self.cmbLayerSpecificDailyVariableList.currentIndex() > -1:
            varname = self.cmbLayerSpecificDailyVariableList.currentText().split(")")[-1].strip()
            layer = ""
            if self.rbtLayerSpecificDailySpecificDepth_2.isChecked():
                layer = self.txtLayerSpecificDailySoilDepth_2.text().strip()
            else:
                lower = self.txtLayerSpecificDailySoilDepth_2.text().strip()
                upper = self.txtLayerSpecificDailyLowerBound_2.text().strip()
                if lower and upper:
                    if int(lower) < int(upper):
                        layer = lower + "-" + upper
                    else:
                        QtGui.QMessageBox.about(self.form, "Invalid Input", "Lower bound can't be smaller than the upper bound")

            if layer:
                self.initParam.output.addVariableToDailyVarLayList(varname, layer)
                self.lstLayerSpecificDailySelectedVariableLayer.clear()
                temp = self.initParam.output.getTextLinesFromDailyVarLayerList()
                self.lstLayerSpecificDailySelectedVariableLayer.addItems(temp)

                self.txtLayerSpecificDailySoilDepth_2.clear()
                self.txtLayerSpecificDailyLowerBound_2.clear()

    def btnLayerSpecificAnnualVariableRemove_clicked(self):
        layer = ""
        if len(self.lstLayerSpecificAnnualSelectedLayerVariable.selectedItems()) > 0:
            layer = self.lstLayerSpecificAnnualSelectedLayerVariable.currentItem().text().split(":")[0].strip()

            if layer:
                self.initParam.output.removeVariableFromAnnualLayerVarList(layer)
                self.lstLayerSpecificAnnualSelectedLayerVariable.clear()
                list = self.initParam.output.getTextLinesFromAnnualLayerVarList()
                self.lstLayerSpecificAnnualSelectedLayerVariable.addItems(list)

    def btnLayerSpecificAnnualVariableAdd_clicked(self):
        layer = ""
        if self.rbtLayerSpecificAnnualSpecificDepth.isChecked():
            layer = self.txtLayerSpecificAnnualSoilDepth.text().strip()
        else:
            lower = self.txtLayerSpecificAnnualSoilDepth.text().strip()
            upper = self.txtLayerSpecificAnnualLowerBound.text().strip()
            if lower and upper:
                if int(lower) < int(upper):
                    layer = lower + "-" + upper
                else:
                    QtGui.QMessageBox.about(self.form, "Invalid Input", "Lower bound can't be smaller than the upper bound")

        list = []
        for i in range(self.twLayerSpecificAnnualVariableList.rowCount()):
            if self.twLayerSpecificAnnualVariableList.isItemSelected(self.twLayerSpecificAnnualVariableList.item(i, 1)):
                item = self.twLayerSpecificAnnualVariableList.item(i, 1)
                list.append(item.text())

        if layer and len(list)>0:
            for item in list:
                self.initParam.output.addVariableToAnnualLayerVarList(layer, item)

            self.lstLayerSpecificAnnualSelectedLayerVariable.clear()
            list = self.initParam.output.getTextLinesFromAnnualLayerVarList()
            self.lstLayerSpecificAnnualSelectedLayerVariable.addItems(list)

            #unselect all items
            for i in range(self.twLayerSpecificAnnualVariableList.rowCount()):
                item = self.twLayerSpecificAnnualVariableList.item(i, 0)
                self.twLayerSpecificAnnualVariableList.setItemSelected(item, False)
                item = self.twLayerSpecificAnnualVariableList.item(i, 1)
                self.twLayerSpecificAnnualVariableList.setItemSelected(item, False)
                item = self.twLayerSpecificAnnualVariableList.item(i, 2)
                self.twLayerSpecificAnnualVariableList.setItemSelected(item, False)

    def btnLayerSpecificDailyVariableRemove_clicked(self):
        layer = ""
        if len(self.lstLayerSpecificDailySelectedLayerVariable.selectedItems()) > 0:
            layer = self.lstLayerSpecificDailySelectedLayerVariable.currentItem().text().split(":")[0].strip()

            if layer:
                self.initParam.output.removeVariableFromDailyLayerVarList(layer)
                self.lstLayerSpecificDailySelectedLayerVariable.clear()
                list = self.initParam.output.getTextLinesFromDailyLayerVarList()
                self.lstLayerSpecificDailySelectedLayerVariable.addItems(list)

    def btnLayerSpecificDailyVariableAdd_clicked(self):
        layer = ""
        if self.rbtLayerSpecificDailySpecificDepth.isChecked():
            layer = self.txtLayerSpecificDailySoilDepth.text().strip()
        else:
            lower = self.txtLayerSpecificDailySoilDepth.text().strip()
            upper = self.txtLayerSpecificDailyLowerBound.text().strip()
            if lower and upper:
                if int(lower) < int(upper):
                    layer = lower + "-" + upper
                else:
                    QtGui.QMessageBox.about(self.form, "Invalid Input", "Lower bound can't be smaller than the upper bound")

        list = []

        for i in range(self.twLayerSpecificDailyVariableList.rowCount()):
            if self.twLayerSpecificDailyVariableList.isItemSelected(self.twLayerSpecificDailyVariableList.item(i, 1)):
                item = self.twLayerSpecificDailyVariableList.item(i, 1)
                list.append(item.text())

        if layer and len(list) > 0:
            for item in list:
                self.initParam.output.addVariableToDailyLayerVarList(layer, item)

            self.lstLayerSpecificDailySelectedLayerVariable.clear()
            list = self.initParam.output.getTextLinesFromDailyLayerVarList()
            self.lstLayerSpecificDailySelectedLayerVariable.addItems(list)

            #unselect all items
            for i in range(self.twLayerSpecificDailyVariableList.rowCount()):
                item = self.twLayerSpecificDailyVariableList.item(i, 0)
                self.twLayerSpecificDailyVariableList.setItemSelected(item, False)
                item = self.twLayerSpecificDailyVariableList.item(i, 1)
                self.twLayerSpecificDailyVariableList.setItemSelected(item, False)
                item = self.twLayerSpecificDailyVariableList.item(i, 2)
                self.twLayerSpecificDailyVariableList.setItemSelected(item, False)

    def rbtLayerSpecificDailySpecificDepth_2_toggled(self):
        if self.rbtLayerSpecificDailySpecificDepth_2.isChecked():
            self.lblLayerSpecificDailyLowerBound_2.setVisible(False)
            self.txtLayerSpecificDailyLowerBound_2.setVisible(False)
            self.lblLayerSpecificDailySoilDepth_2.setText("Soil Depth")
        else:
            self.lblLayerSpecificDailyLowerBound_2.setVisible(True)
            self.txtLayerSpecificDailyLowerBound_2.setVisible(True)
            self.lblLayerSpecificDailySoilDepth_2.setText("Upper Bound")

        self.txtLayerSpecificDailySoilDepth_2.clear()
        self.txtLayerSpecificDailyLowerBound_2.clear()

    def rbtLayerSpecificDailySpecificDepth_toggled(self):
        if self.rbtLayerSpecificDailySpecificDepth.isChecked():
            self.lblLayerSpecificDailyLowerBound.setVisible(False)
            self.txtLayerSpecificDailyLowerBound.setVisible(False)
            self.lblLayerSpecificDailySoilDepth.setText("Soil Depth")
        else:
            self.lblLayerSpecificDailyLowerBound.setVisible(True)
            self.txtLayerSpecificDailyLowerBound.setVisible(True)
            self.lblLayerSpecificDailySoilDepth.setText("Upper Bound")

        self.txtLayerSpecificDailySoilDepth.clear()
        self.txtLayerSpecificDailyLowerBound.clear()

    def rbtLayerSpecificAnnualMaxDepth_2_toggled(self):
        if self.rbtLayerSpecificAnnualMaxDepth_2.isChecked():
            self.lblLayerSpecificAnnualLowerBound_2.setVisible(False)
            self.txtLayerSpecificAnnualLowerBound_2.setVisible(False)
            self.lblLayerSpecificAnnualSoilDepth_2.setText("Soil Depth")
        else:
            self.lblLayerSpecificAnnualLowerBound_2.setVisible(True)
            self.txtLayerSpecificAnnualLowerBound_2.setVisible(True)
            self.lblLayerSpecificAnnualSoilDepth_2.setText("Upper Bound")

        self.txtLayerSpecificAnnualSoilDepth_2.clear()
        self.txtLayerSpecificAnnualLowerBound_2.clear()

    def rbtLayerSpecificAnnualSpecificDepth_toggled(self):
        if self.rbtLayerSpecificAnnualSpecificDepth.isChecked():
            self.lblLayerSpecificAnnualLowerBound.setVisible(False)
            self.txtLayerSpecificAnnualLowerBound.setVisible(False)
            self.lblLayerSpecificAnnualSoilDepth.setText("Soil Depth")
        else:
            self.lblLayerSpecificAnnualLowerBound.setVisible(True)
            self.txtLayerSpecificAnnualLowerBound.setVisible(True)
            self.lblLayerSpecificAnnualSoilDepth.setText("Upper Bound")

        self.txtLayerSpecificAnnualSoilDepth.clear()
        self.txtLayerSpecificAnnualLowerBound.clear()

    def btnTotalLayerVariableRemoveAll_clicked(self):
        count = 0
        for i in range(self.twTotalLayerSelectedVariable.rowCount()):
            item = self.twTotalLayerSelectedVariable.item(i, 1)
            self.initParam.output.removeVariableFromSelectedTotalLayer_ByVarName(item.text())
            count += 1

        if count > 0:
            self.clearTotalLayerVariableListTable()
            self.clearTotalLayerSelectedVariableTable()
            varList = self.initParam.output.getUnselectedTotalLayerVariableList()
            for var in varList:
                ndx = self.twTotalLayerVariableList.rowCount()
                self.twTotalLayerVariableList.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twTotalLayerVariableList.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twTotalLayerVariableList.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twTotalLayerVariableList.setItem(ndx, 2, cell)
                self.twTotalLayerVariableList.setRowHeight(ndx, 20)

    def btnTotalLayerVariableRemove_clicked(self):
        count = 0
        for i in range(self.twTotalLayerSelectedVariable.rowCount()):
            if self.twTotalLayerSelectedVariable.isItemSelected(self.twTotalLayerSelectedVariable.item(i, 1)):
                item = self.twTotalLayerSelectedVariable.item(i, 1)
                self.initParam.output.removeVariableFromSelectedTotalLayer_ByVarName(item.text())
                count += 1

        if count > 0:
            self.clearTotalLayerVariableListTable()
            self.clearTotalLayerSelectedVariableTable()
            varList = self.initParam.output.getUnselectedTotalLayerVariableList()
            for var in varList:
                ndx = self.twTotalLayerVariableList.rowCount()
                self.twTotalLayerVariableList.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twTotalLayerVariableList.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twTotalLayerVariableList.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twTotalLayerVariableList.setItem(ndx, 2, cell)
                self.twTotalLayerVariableList.setRowHeight(ndx, 20)
            varList = self.initParam.output.getSelectedTotalLayerVariableList()
            for var in varList:
                ndx = self.twTotalLayerSelectedVariable.rowCount()
                self.twTotalLayerSelectedVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twTotalLayerSelectedVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twTotalLayerSelectedVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twTotalLayerSelectedVariable.setItem(ndx, 2, cell)
                self.twTotalLayerSelectedVariable.setRowHeight(ndx, 20)

    def btnTotalLayerVariableAddAll_clicked(self):
        count = 0
        for i in range(self.twTotalLayerVariableList.rowCount()):
            item = self.twTotalLayerVariableList.item(i, 1)
            self.initParam.output.addVariableToSelectedTotalLayer_ByVarName(item.text())
            count += 1

        if count > 0:
            self.clearTotalLayerVariableListTable()
            self.clearTotalLayerSelectedVariableTable()
            varList = self.initParam.output.getSelectedTotalLayerVariableList()
            for var in varList:
                ndx = self.twTotalLayerSelectedVariable.rowCount()
                self.twTotalLayerSelectedVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twTotalLayerSelectedVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twTotalLayerSelectedVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twTotalLayerSelectedVariable.setItem(ndx, 2, cell)
                self.twTotalLayerSelectedVariable.setRowHeight(ndx, 20)

    def btnTotalLayerVariableAdd_clicked(self):
        count = 0
        for i in range(self.twTotalLayerVariableList.rowCount()):
            if self.twTotalLayerVariableList.isItemSelected(self.twTotalLayerVariableList.item(i, 1)):
                item = self.twTotalLayerVariableList.item(i, 1)
                self.initParam.output.addVariableToSelectedTotalLayer_ByVarName(item.text())
                count += 1

        if count > 0:
            self.clearTotalLayerVariableListTable()
            self.clearTotalLayerSelectedVariableTable()
            varList = self.initParam.output.getUnselectedTotalLayerVariableList()
            for var in varList:
                ndx = self.twTotalLayerVariableList.rowCount()
                self.twTotalLayerVariableList.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twTotalLayerVariableList.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twTotalLayerVariableList.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twTotalLayerVariableList.setItem(ndx, 2, cell)
                self.twTotalLayerVariableList.setRowHeight(ndx, 20)
            varList = self.initParam.output.getSelectedTotalLayerVariableList()
            for var in varList:
                ndx = self.twTotalLayerSelectedVariable.rowCount()
                self.twTotalLayerSelectedVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twTotalLayerSelectedVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twTotalLayerSelectedVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twTotalLayerSelectedVariable.setItem(ndx, 2, cell)
                self.twTotalLayerSelectedVariable.setRowHeight(ndx, 20)

    def btnVegetationSpecificVariableRemoveAll_clicked(self):
        category = self.cmbVegetationSpecificCategory.currentText()
        count = self.twVegetationSpecificSelectedVariable.rowCount()

        if len(category) > 0:
            if count > 0:
                i = 0
                if self.rbtVegetationSpecificDailyOutput.isChecked():
                    while i < count:
                        item = self.twVegetationSpecificSelectedVariable.item(i, 1)
                        self.initParam.output.removeVariableFromSelectedVegetationSpecificList_Daily_ByVarName(category,item.text())
                        i += 1

                    self.clearVegSpecificVariableListTable()
                    self.clearVegSpecificSelectedListTable()

                    for var in self.initParam.output.getUnselectedVegetationSpecificVariableList_Daily(category):
                        ndx = self.twVegSpecificVariable.rowCount()
                        self.twVegSpecificVariable.insertRow(ndx)
                        cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                        self.twVegSpecificVariable.setItem(ndx, 0, cell)
                        cell = QtWidgets.QTableWidgetItem(var["varname"])
                        self.twVegSpecificVariable.setItem(ndx, 1, cell)
                        cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                        self.twVegSpecificVariable.setItem(ndx, 2, cell)
                        self.twVegSpecificVariable.setRowHeight(ndx, 20)
                else:
                    while i < count:
                        item = self.twVegetationSpecificSelectedVariable.item(i, 1)
                        self.initParam.output.removeVariableFromSelectedVegetationSpecificList_Annual_ByVarName(category,item.text())
                        i += 1

                    self.clearVegSpecificVariableListTable()
                    self.clearVegSpecificSelectedListTable()

                    for var in self.initParam.output.getUnselectedVegetationSpecificVariableList_Annual(category):
                        ndx = self.twVegSpecificVariable.rowCount()
                        self.twVegSpecificVariable.insertRow(ndx)
                        cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                        self.twVegSpecificVariable.setItem(ndx, 0, cell)
                        cell = QtWidgets.QTableWidgetItem(var["varname"])
                        self.twVegSpecificVariable.setItem(ndx, 1, cell)
                        cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                        self.twVegSpecificVariable.setItem(ndx, 2, cell)
                        self.twVegSpecificVariable.setRowHeight(ndx, 20)
        else:
            if self.ckbShowAllSelectedVegVariable.isChecked() and count > 0:
                self.btnClearVegVariables_click()

    def btnVegetationSpecificVariableRemove_clicked(self):
        category = self.cmbVegetationSpecificCategory.currentText()

        if len(category) > 0:
            if self.rbtVegetationSpecificDailyOutput.isChecked():
                for i in range(self.twVegetationSpecificSelectedVariable.rowCount()):
                    if self.twVegetationSpecificSelectedVariable.isItemSelected(self.twVegetationSpecificSelectedVariable.item(i, 1)):
                        item = self.twVegetationSpecificSelectedVariable.item(i, 1)
                        self.initParam.output.removeVariableFromSelectedVegetationSpecificList_Daily_ByVarName(category, item.text())

                self.clearVegSpecificVariableListTable()
                self.clearVegSpecificSelectedListTable()

                for var in self.initParam.output.getUnselectedVegetationSpecificVariableList_Daily(category):
                    ndx = self.twVegSpecificVariable.rowCount()
                    self.twVegSpecificVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegSpecificVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegSpecificVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegSpecificVariable.setItem(ndx, 2, cell)
                    self.twVegSpecificVariable.setRowHeight(ndx, 20)

                for var in self.initParam.output.getSelectedVegetationSpecificVariableList_Daily(category):
                    ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                    self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)
            else:
                for i in range(self.twVegetationSpecificSelectedVariable.rowCount()):
                    if self.twVegetationSpecificSelectedVariable.isItemSelected(self.twVegetationSpecificSelectedVariable.item(i, 1)):
                        item = self.twVegetationSpecificSelectedVariable.item(i, 1)
                        self.initParam.output.removeVariableFromSelectedVegetationSpecificList_Annual_ByVarName(category, item.text())

                self.clearVegSpecificVariableListTable()
                self.clearVegSpecificSelectedListTable()

                for var in self.initParam.output.getUnselectedVegetationSpecificVariableList_Annual(category):
                    ndx = self.twVegSpecificVariable.rowCount()
                    self.twVegSpecificVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegSpecificVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegSpecificVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegSpecificVariable.setItem(ndx, 2, cell)
                    self.twVegSpecificVariable.setRowHeight(ndx, 20)

                for var in self.initParam.output.getSelectedVegetationSpecificVariableList_Annual(category):
                    ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                    self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)
        else:
            if self.ckbShowAllSelectedVegVariable.isChecked():
                daily = False
                if self.rbtVegetationSpecificDailyOutput.isChecked(): daily = True

                rlist = self.twVegetationSpecificSelectedVariable.selectionModel().selectedRows()
                if len(rlist) > 0:
                    for r in rlist:
                        category = self.twVegetationSpecificSelectedVariable.item(r.row(), 3).text()
                        varname = self.twVegetationSpecificSelectedVariable.item(r.row(), 1).text()
                        if daily: self.initParam.output.removeVariableFromSelectedVegetationSpecificList_Daily_ByVarName(category, varname)
                        else: self.initParam.output.removeVariableFromSelectedVegetationSpecificList_Annual_ByVarName(category, varname)
                    self.clearVegSpecificSelectedListTable()
                    self.ckbShowAllSelectedVegVariable_toggled()

    def btnVegetationSpecificVariableAddAll_clicked(self):
        category = self.cmbVegetationSpecificCategory.currentText()
        count = self.twVegSpecificVariable.rowCount()

        if len(category) > 0 and count > 0:
            i = 0
            if self.rbtVegetationSpecificDailyOutput.isChecked():
                while i < count:
                    item = self.twVegSpecificVariable.item(i, 1)
                    self.initParam.output.addVariableToSelectedVegetationSpecificList_Daily_ByVarName(category,item.text())
                    i += 1

                self.clearVegSpecificVariableListTable()
                self.clearVegSpecificSelectedListTable()

                for var in self.initParam.output.getSelectedVegetationSpecificVariableList_Daily(category):
                    ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                    self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)
            else:
                while i < count:
                    item = self.twVegSpecificVariable.item(i, 1)
                    self.initParam.output.addVariableToSelectedVegetationSpecificList_Annual_ByVarName(category,item.text())
                    i += 1

                self.clearVegSpecificVariableListTable()
                self.clearVegSpecificSelectedListTable()

                for var in self.initParam.output.getSelectedVegetationSpecificVariableList_Annual(category):
                    ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                    self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)

    def btnVegetationSpecificVariableAdd_clicked(self):
        category = self.cmbVegetationSpecificCategory.currentText()

        if len(category) > 0:
            if self.rbtVegetationSpecificDailyOutput.isChecked():
                for i in range(self.twVegSpecificVariable.rowCount()):
                    if self.twVegSpecificVariable.isItemSelected(self.twVegSpecificVariable.item(i, 1)):
                        item = self.twVegSpecificVariable.item(i, 1)
                        self.initParam.output.addVariableToSelectedVegetationSpecificList_Daily_ByVarName(category, item.text())

                self.clearVegSpecificVariableListTable()
                self.clearVegSpecificSelectedListTable()

                for var in self.initParam.output.getUnselectedVegetationSpecificVariableList_Daily(category):
                    ndx = self.twVegSpecificVariable.rowCount()
                    self.twVegSpecificVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegSpecificVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegSpecificVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegSpecificVariable.setItem(ndx, 2, cell)
                    self.twVegSpecificVariable.setRowHeight(ndx, 20)

                for var in self.initParam.output.getSelectedVegetationSpecificVariableList_Daily(category):
                    ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                    self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)
            else:
                for i in range(self.twVegSpecificVariable.rowCount()):
                    if self.twVegSpecificVariable.isItemSelected(self.twVegSpecificVariable.item(i, 1)):
                        item = self.twVegSpecificVariable.item(i, 1)
                        self.initParam.output.addVariableToSelectedVegetationSpecificList_Annual_ByVarName(category, item.text())

                self.clearVegSpecificVariableListTable()
                self.clearVegSpecificSelectedListTable()

                for var in self.initParam.output.getUnselectedVegetationSpecificVariableList_Annual(category):
                    ndx = self.twVegSpecificVariable.rowCount()
                    self.twVegSpecificVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegSpecificVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegSpecificVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegSpecificVariable.setItem(ndx, 2, cell)
                    self.twVegSpecificVariable.setRowHeight(ndx, 20)

                for var in self.initParam.output.getSelectedVegetationSpecificVariableList_Annual(category):
                    ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                    self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)

    def btnSiteSpecificVariableRemoveAll_clicked(self):
        category = self.cmbSiteSpecificOutputCategory.currentText()
        count = self.twSiteSpecificSelectedVariable.rowCount()

        if len(category) > 0:
            if count > 0:
                i = 0
                if self.rbtSiteSpecificDailyOutput.isChecked():
                    while i < count:
                        item = self.twSiteSpecificSelectedVariable.item(i, 1)
                        self.initParam.output.removeVariableFromSelectedSiteSpecificList_Daily_ByVarName(category,item.text())
                        i += 1

                    self.clearSiteSpecificVariableListTable()
                    self.clearSiteSpecificSelectedListTable()

                    for var in self.initParam.output.getUnselectedSiteSpecificVariableList_Daily(category):
                        ndx = self.twSiteSpecificVariable.rowCount()
                        self.twSiteSpecificVariable.insertRow(ndx)
                        cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                        self.twSiteSpecificVariable.setItem(ndx, 0, cell)
                        cell = QtWidgets.QTableWidgetItem(var["varname"])
                        self.twSiteSpecificVariable.setItem(ndx, 1, cell)
                        cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                        self.twSiteSpecificVariable.setItem(ndx, 2, cell)
                        self.twSiteSpecificVariable.setRowHeight(ndx, 20)
                else:
                    while i < count:
                        item = self.twSiteSpecificSelectedVariable.item(i, 1)
                        self.initParam.output.removeVariableFromSelectedSiteSpecificList_Annual_ByVarName(category,item.text())
                        i += 1

                    self.clearSiteSpecificVariableListTable()
                    self.clearSiteSpecificSelectedListTable()

                    for var in self.initParam.output.getUnselectedSiteSpecificVariableList_Annual(category):
                        ndx = self.twSiteSpecificVariable.rowCount()
                        self.twSiteSpecificVariable.insertRow(ndx)
                        cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                        self.twSiteSpecificVariable.setItem(ndx, 0, cell)
                        cell = QtWidgets.QTableWidgetItem(var["varname"])
                        self.twSiteSpecificVariable.setItem(ndx, 1, cell)
                        cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                        self.twSiteSpecificVariable.setItem(ndx, 2, cell)
                        self.twSiteSpecificVariable.setRowHeight(ndx, 20)
        else:
            if count > 0 and self.ckbShowAllSelectedSiteVariable.isChecked(): self.btnClearSiteVariables_click()

    def btnSiteSpecificVariableRemove_clicked(self):
        category = self.cmbSiteSpecificOutputCategory.currentText()

        if len(category) > 0:
            if self.rbtSiteSpecificDailyOutput.isChecked():
                for i in range(self.twSiteSpecificSelectedVariable.rowCount()):
                    if self.twSiteSpecificSelectedVariable.isItemSelected(self.twSiteSpecificSelectedVariable.item(i, 1)):
                        item = self.twSiteSpecificSelectedVariable.item(i, 1)
                        self.initParam.output.removeVariableFromSelectedSiteSpecificList_Daily_ByVarName(category, item.text())

                self.clearSiteSpecificVariableListTable()
                self.clearSiteSpecificSelectedListTable()

                for var in self.initParam.output.getUnselectedSiteSpecificVariableList_Daily(category):
                    ndx = self.twSiteSpecificVariable.rowCount()
                    self.twSiteSpecificVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificVariable.setRowHeight(ndx, 20)

                for var in self.initParam.output.getSelectedSiteSpecificVariableList_Daily(category):
                    ndx = self.twSiteSpecificSelectedVariable.rowCount()
                    self.twSiteSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)
            else:
                for i in range(self.twSiteSpecificSelectedVariable.rowCount()):
                    if self.twSiteSpecificSelectedVariable.isItemSelected(self.twSiteSpecificSelectedVariable.item(i, 1)):
                        item = self.twSiteSpecificSelectedVariable.item(i, 1)
                        self.initParam.output.removeVariableFromSelectedSiteSpecificList_Annual_ByVarName(category, item.text())

                self.clearSiteSpecificVariableListTable()
                self.clearSiteSpecificSelectedListTable()

                for var in self.initParam.output.getUnselectedSiteSpecificVariableList_Annual(category):
                    ndx = self.twSiteSpecificVariable.rowCount()
                    self.twSiteSpecificVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificVariable.setRowHeight(ndx, 20)

                for var in self.initParam.output.getSelectedSiteSpecificVariableList_Annual(category):
                    ndx = self.twSiteSpecificSelectedVariable.rowCount()
                    self.twSiteSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)
        else:
            if self.ckbShowAllSelectedSiteVariable.isChecked():
                daily = self.rbtSiteSpecificDailyOutput.isChecked()

                rlist = self.twSiteSpecificSelectedVariable.selectionModel().selectedRows()
                if len(rlist) > 0:
                    for r in rlist:
                        varname = self.twSiteSpecificSelectedVariable.item(r.row(), 1).text()
                        category = self.twSiteSpecificSelectedVariable.item(r.row(), 3).text()
                        if daily: self.initParam.output.removeVariableFromSelectedSiteSpecificList_Daily_ByVarName(category, varname)
                        else: self.initParam.output.removeVariableFromSelectedSiteSpecificList_Annual_ByVarName(category, varname)
                    self.clearSiteSpecificSelectedListTable()
                    self.ckbShowAllSelectedSiteVariable_toggled()

    def btnSiteSpecificVariableAddAll_clicked(self):
        category = self.cmbSiteSpecificOutputCategory.currentText()
        count = self.twSiteSpecificVariable.rowCount()

        if len(category) > 0:
            if count > 0:
                i = 0
                if self.rbtSiteSpecificDailyOutput.isChecked():
                    while i < count:
                        item = self.twSiteSpecificVariable.item(i, 1)
                        self.initParam.output.addVariableToSelectedSiteSpecificList_Daily_ByVarName(category,item.text())

                        i += 1

                    # self.lstSiteSpecificVariableList.clear()
                    self.clearSiteSpecificVariableListTable()
                    self.clearSiteSpecificSelectedListTable()

                    for var in self.initParam.output.getSelectedSiteSpecificVariableList_Daily(category):
                        ndx = self.twSiteSpecificSelectedVariable.rowCount()
                        self.twSiteSpecificSelectedVariable.insertRow(ndx)
                        cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                        self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                        cell = QtWidgets.QTableWidgetItem(var["varname"])
                        self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                        cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                        self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                        self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)
                else:
                    while i < count:
                        item = self.twSiteSpecificVariable.item(i, 1)
                        self.initParam.output.addVariableToSelectedSiteSpecificList_Annual_ByVarName(category,item.text())

                        i += 1

                    self.clearSiteSpecificVariableListTable()
                    self.clearSiteSpecificSelectedListTable()

                    for var in self.initParam.output.getSelectedSiteSpecificVariableList_Annual(category):
                        ndx = self.twSiteSpecificSelectedVariable.rowCount()
                        self.twSiteSpecificSelectedVariable.insertRow(ndx)
                        cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                        self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                        cell = QtWidgets.QTableWidgetItem(var["varname"])
                        self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                        cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                        self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                        self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)

    def btnSiteSpecificVariableAdd_clicked(self):
        category = self.cmbSiteSpecificOutputCategory.currentText()

        if len(category) > 0:
            if self.rbtSiteSpecificDailyOutput.isChecked():
                for i in range(self.twSiteSpecificVariable.rowCount()):
                    if self.twSiteSpecificVariable.isItemSelected(self.twSiteSpecificVariable.item(i, 1)):
                        item = self.twSiteSpecificVariable.item(i, 1)
                        self.initParam.output.addVariableToSelectedSiteSpecificList_Daily_ByVarName(category, item.text())

                self.clearSiteSpecificVariableListTable()
                self.clearSiteSpecificSelectedListTable()

                for var in self.initParam.output.getUnselectedSiteSpecificVariableList_Daily(category):
                    ndx = self.twSiteSpecificVariable.rowCount()
                    self.twSiteSpecificVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificVariable.setRowHeight(ndx, 20)

                for var in self.initParam.output.getSelectedSiteSpecificVariableList_Daily(category):
                    ndx = self.twSiteSpecificSelectedVariable.rowCount()
                    self.twSiteSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)

            else:
                for i in range(self.twSiteSpecificVariable.rowCount()):
                    if self.twSiteSpecificVariable.isItemSelected(self.twSiteSpecificVariable.item(i, 1)):
                        item = self.twSiteSpecificVariable.item(i, 1)
                        self.initParam.output.addVariableToSelectedSiteSpecificList_Annual_ByVarName(category, item.text())

                self.clearSiteSpecificVariableListTable()
                self.clearSiteSpecificSelectedListTable()

                for var in self.initParam.output.getUnselectedSiteSpecificVariableList_Annual(category):
                    ndx = self.twSiteSpecificVariable.rowCount()
                    self.twSiteSpecificVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificVariable.setRowHeight(ndx, 20)

                for var in self.initParam.output.getSelectedSiteSpecificVariableList_Annual(category):
                    ndx = self.twSiteSpecificSelectedVariable.rowCount()
                    self.twSiteSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)

    def clearSiteSpecificVariableListTable(self):
        for i in reversed(range(self.twSiteSpecificVariable.rowCount())):
            self.twSiteSpecificVariable.removeRow(i)

    def clearVegSpecificVariableListTable(self):
        for i in reversed(range(self.twVegSpecificVariable.rowCount())):
            self.twVegSpecificVariable.removeRow(i)

    def clearVegSpecificSelectedListTable(self):
        for i in reversed(range(self.twVegetationSpecificSelectedVariable.rowCount())):
            self.twVegetationSpecificSelectedVariable.removeRow(i)

    def clearSiteSpecificSelectedListTable(self):
        for i in reversed(range(self.twSiteSpecificSelectedVariable.rowCount())):
            self.twSiteSpecificSelectedVariable.removeRow(i)

    def clearTotalLayerVariableListTable(self):
        for i in reversed(range(self.twTotalLayerVariableList.rowCount())):
            self.twTotalLayerVariableList.removeRow(i)

    def clearTotalLayerSelectedVariableTable(self):
        for i in reversed(range(self.twTotalLayerSelectedVariable.rowCount())):
            self.twTotalLayerSelectedVariable.removeRow(i)

    def clearLayerSpecificDailyVariableListTable(self):
        for i in reversed(range(self.twLayerSpecificDailyVariableList.rowCount())):
            self.twLayerSpecificDailyVariableList.removeRow(i)


    def clearLayerSpecificAnnualVariableList(self):
        for i in reversed(range(self.twLayerSpecificAnnualVariableList.rowCount())):
            self.twLayerSpecificAnnualVariableList.removeRow(i)


    def cmbVegetationSpecificCategory_currentIndexChanged(self):
        if self.cmbVegetationSpecificCategory.currentIndex() > -1: self.ckbShowAllSelectedVegVariable.setChecked(False)

        category = self.cmbVegetationSpecificCategory.currentText()

        self.clearVegSpecificVariableListTable()
        self.clearVegSpecificSelectedListTable()

        if self.rbtVegetationSpecificDailyOutput.isChecked():
            varList = self.initParam.output.getUnselectedVegetationSpecificVariableList_Daily(category)
            for var in varList:
                ndx = self.twVegSpecificVariable.rowCount()
                self.twVegSpecificVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twVegSpecificVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twVegSpecificVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twVegSpecificVariable.setItem(ndx, 2, cell)
                self.twVegSpecificVariable.setRowHeight(ndx, 20)

            varList = self.initParam.output.getSelectedVegetationSpecificVariableList_Daily(category)
            for var in varList:
                ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)
        else:
            varList = self.initParam.output.getUnselectedVegetationSpecificVariableList_Annual(category)
            for var in varList:
                ndx = self.twVegSpecificVariable.rowCount()
                self.twVegSpecificVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twVegSpecificVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twVegSpecificVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twVegSpecificVariable.setItem(ndx, 2, cell)
                self.twVegSpecificVariable.setRowHeight(ndx, 20)

            varList = self.initParam.output.getSelectedVegetationSpecificVariableList_Annual(category)
            for var in varList:
                ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)

    def rbtVegetationSpecificDailyOutput_toggled(self):
        self.ckbShowAllSelectedVegVariable.setChecked(False)
        self.cmbVegetationSpecificCategory.setCurrentIndex(-1)
        self.clearVegSpecificVariableListTable()
        self.clearVegSpecificSelectedListTable()

    def cmbSiteSpecificOutputCategory_currentIndexChanged(self):
        if self.cmbSiteSpecificOutputCategory.currentIndex() > -1:
            self.ckbShowAllSelectedSiteVariable.setChecked(False)
        category = self.cmbSiteSpecificOutputCategory.currentText()

        # self.lstSiteSpecificVariableList.clear()
        self.clearSiteSpecificVariableListTable()
        self.clearSiteSpecificSelectedListTable()

        if self.rbtSiteSpecificDailyOutput.isChecked():
            varList = self.initParam.output.getUnselectedSiteSpecificVariableList_Daily(category)
            for var in varList:
                ndx = self.twSiteSpecificVariable.rowCount()
                self.twSiteSpecificVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twSiteSpecificVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twSiteSpecificVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twSiteSpecificVariable.setItem(ndx, 2, cell)
                self.twSiteSpecificVariable.setRowHeight(ndx, 20)

            varList = self.initParam.output.getSelectedSiteSpecificVariableList_Daily(category)
            for var in varList:
                ndx = self.twSiteSpecificSelectedVariable.rowCount()
                self.twSiteSpecificSelectedVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)
        else:
            varList = self.initParam.output.getUnselectedSiteSpecificVariableList_Annual(category)
            for var in varList:
                ndx = self.twSiteSpecificVariable.rowCount()
                self.twSiteSpecificVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twSiteSpecificVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twSiteSpecificVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twSiteSpecificVariable.setItem(ndx, 2, cell)
                self.twSiteSpecificVariable.setRowHeight(ndx, 20)

            varList = self.initParam.output.getSelectedSiteSpecificVariableList_Annual(category)
            for var in varList:
                ndx = self.twSiteSpecificSelectedVariable.rowCount()
                self.twSiteSpecificSelectedVariable.insertRow(ndx)
                cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                cell = QtWidgets.QTableWidgetItem(var["varname"])
                self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)

    def rbtSiteSpecificDailyOutput_toggled(self):
        self.ckbShowAllSelectedSiteVariable.setChecked(False)
        self.cmbSiteSpecificOutputCategory.setCurrentIndex(-1)
        # self.lstSiteSpecificVariableList.clear()
        self.clearSiteSpecificVariableListTable()
        self.clearSiteSpecificSelectedListTable()

    def ckbSaveOutputTemplate_toggled(self):
        if self.ckbSaveOutputTemplate.isChecked():
            self.txtTemplateName.setEnabled(True)
            self.txtTemplateName.setFocus(True)
        else:
            self.txtTemplateName.setEnabled(False)
            self.txtTemplateName.clear()

    def ckbUseOutputTemplate_toggled(self):
        if self.ckbUseOutputTemplate.isChecked():

            self.cmbOutputTemplate.clear()
            for item in ParamOption.getOutputTemplateList():
                self.cmbOutputTemplate.addItem(item)
            self.cmbOutputTemplate.setCurrentIndex(-1)
            self.cmbOutputTemplate.setEnabled(True)
            self.read_template_file_flag = True
        else:
            self.read_template_file_flag = False
            self.cmbOutputTemplate.setCurrentIndex(-1)
            self.cmbOutputTemplate.setEnabled(False)

    def btnCarbonFile_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory) > 0:
            startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Text File (*.txt)")

        if filename:
            self.txtCarbonFile.setText(filename[0].split("/")[-1])

    def rbtCCContant_toggled(self):
        if self.rbtCCContant.isChecked():
            self.txtConsConcentration.setEnabled(True)
            self.txtCarbonFile.setEnabled(False)
            self.btnCarbonFile.setEnabled(False)
        else:
            self.txtConsConcentration.setEnabled(False)
            self.txtCarbonFile.setEnabled(True)
            self.btnCarbonFile.setEnabled(True)

    def ckbSpinup_toggled(self):
        if self.ckbSpinup.isChecked():
            self.txtSpinupYear.setEnabled(True)
            self.txtSpinupYear.setFocus(True)
        else: self.txtSpinupYear.setEnabled(False)

    def btnBrowseRestartFileWrite_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory) > 0:
            startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath()
        filename = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save File', startingDir, "Text File (*.txt)")

        if filename: self.txtRestartFileWrite.setText(filename[0].split("/")[-1])

    def btnBrowseRestartFileRead_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory) > 0:
            startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Text File (*.txt)")

        if filename: self.txtRestartFileRead.setText(filename[0].split("/")[-1])

    def ckbReadRestartFile_toggled(self):
        if self.ckbReadRestartFile.isChecked():
            self.txtRestartFileRead.setEnabled(True)
            self.btnBrowseRestartFileRead.setEnabled(True)
        else:
            self.txtRestartFileRead.setEnabled(False)
            self.btnBrowseRestartFileRead.setEnabled(False)
            self.txtRestartFileRead.clear()

    def ckbWriteRestartFile_toggled(self):
        if self.ckbWriteRestartFile.isChecked():
            self.txtRestartFileWrite.setEnabled(True)
            self.btnBrowseRestartFileWrite.setEnabled(True)
        else:
            self.txtRestartFileWrite.setEnabled(False)
            self.btnBrowseRestartFileWrite.setEnabled(False)
            self.txtRestartFileWrite.clear()

    def btnBrowseVegFile_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory) > 0:
            startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Text File (*.txt)")

        if filename: self.txtVegFileName.setText(filename[0].split("/")[-1])

    def btnBrowseGisFile_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory) > 0:
            startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath()
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Text File (*.txt)")

        if filename: self.txtGisFileName.setText(filename[0].split("/")[-1])

    def btnBrowseInitFile_clicked(self):
        startingDir = ""
        if len(ApplicationProperty.currentModelDirectory) > 0:
            startingDir = ApplicationProperty.currentModelDirectory
        else: startingDir = ApplicationProperty.getScriptPath ()

        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDir, "Init File (*.ini)")

        if filename:
            self.initParam = FileReadWrite.readInitialFile(filename)
            self.clearField()
            self.writeParamValuesOnFormComponent()

            temp = filename.split("/")[-1]
            directoryName = filename.replace("/" + temp,"")
            if len(ApplicationProperty.currentModelDirectory) == 0:
                ApplicationProperty.currentModelDirectory = directoryName

            self.txtInitFileName.setText(temp)
            self.txtInitFileDirectory.setText(directoryName)

    def btnChooseInitDir_clicked(self):
        startingDir = ApplicationProperty.getScriptPath ()
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self.form, "Select Directory", startingDir, QtWidgets.QFileDialog.ShowDirsOnly))
        self.txtInitFileDirectory.setText(file)
        ApplicationProperty.currentModelDirectory = file

    def rbtNewInitFile_toggled(self):
        if self.rbtNewInitFile.isChecked():
            self.btnSave.setText("Save")
            self.btnBrowseInitFile.setEnabled(False)
            #self.txtInitFileDirectory.setEnabled(False)
            self.btnChooseInitDir.setEnabled(True)
            #elif self.rbtNewInitFile.isChecked() == False
            self.clearField()
        else:
            self.btnSave.setText("Update")
            self.btnBrowseInitFile.setEnabled(True)
            #self.txtInitFileDirectory.setEnabled(True)
            self.btnChooseInitDir.setEnabled(False)
            self.clearField()

        self.txtInitFileName.setText("")
        self.txtInitFileDirectory.setText("")

    def btnClose_clicked(self):
        self.form.parentWidget().close()

    def cmbOutputTemplate_currentIndexChanged(self):
        if self.read_template_file_flag and  self.cmbOutputTemplate.currentIndex() > -1:
            templateName = self.cmbOutputTemplate.currentText().strip()
            if templateName:
                self.initParam = InitialParameter()
                self.clearSelectedVariableList()
                self.initParam.output = FileReadWrite.readOutputTemplate(templateName)
                self.read_output_list()

    def writeParamValuesOnFormComponent(self):
        self.txtGisFileName.setText(self.initParam.gis_file_name)
        self.txtVegFileName.setText(self.initParam.veg_file_name)

        if self.initParam.restart_read_flag == 1:
            self.ckbReadRestartFile.setChecked(True)
            self.txtRestartFileRead.setText(self.initParam.restart_read_file_name)
        else:
            self.ckbReadRestartFile.setChecked(False)
            self.txtRestartFileRead.setText("")

        if self.initParam.restart_write_flag == 1:
            self.ckbWriteRestartFile.setChecked(True)
            self.txtRestartFileWrite.setText(self.initParam.restart_write_file_name)
        else:
            self.ckbWriteRestartFile.setChecked(False)
            self.txtRestartFileWrite.setText("")

        if self.initParam.restart_metyear_use_flag == 1:
            self.rbtMetyearYes.setChecked(True)
        else: self.rbtMetyearNo.setChecked(True)

        self.txtStartYear.setText(str(self.initParam.sim_start_year))
        self.txtEndYear.setText(str(self.initParam.sim_start_year
                                 + self.initParam.no_of_sim_year - 1))

        if self.initParam.sim_spinup_flag == 1:
            self.ckbSpinup.setChecked(True)
            self.txtSpinupYear.setText(str(self.initParam.no_of_spinup_year))
        else:
            self.ckbSpinup.setChecked(False)
            self.txtSpinupYear.setText("")

        self.txtTmaxOffset.setText(str(self.initParam.Tmax_offset))
        self.txtTminOffset.setText(str(self.initParam.Tmin_offset))
        self.txtPrecipitationMulp.setText(str(self.initParam.precipitation_multiplier))
        self.txtVpdMulp.setText(str(self.initParam.vpd_multiplier))
        self.txtRadiationMulp.setText(str(self.initParam.swave_multiplier))

        if self.initParam.carbon_variability_flag == 0:
            self.rbtCCContant.setChecked(True)
        else: self.rbtCCVariable.setChecked(True)

        self.txtConsConcentration.setText(str(self.initParam.air_constant_carbon))
        self.txtCarbonFile.setText(self.initParam.carbon_file)

        self.cmbNitrogenDiposition.setCurrentIndex(self.initParam.nitrogen_depo_option_flag)
        self.txtRefYear.setText(str(self.initParam.industrial_ref_year))

        self.txtOutputFilePrefix.setText(self.initParam.output_file_prefix)

        if self.initParam.display_flag == 1: self.rbtDispProgressYes.setChecked(True)
        else: self.rbtDispProgressYes.setChecked(False)

        self.cmbDailyOutputType.setCurrentIndex(self.initParam.daily_output_flag)

        if self.initParam.monthly_average_flag == 1: self.ckbMonthAverage.setChecked(True)
        else: self.ckbMonthAverage.setChecked(False)

        if self.initParam.annual_average_flag == 1: self.ckbYearAverage.setChecked(True)
        else: self.ckbYearAverage.setChecked(False)

        self.cmbYearlyOutputType.setCurrentIndex(self.initParam.annual_output_flag)


        self.read_output_list()

    def readParamValuesFromUIComponent(self):
        # self.modelParam = InitialParameter()

        temp = self.txtGisFileName.text().strip()
        if len(temp) > 0 and temp.find("/")== -1:
            temp = "ini/" + temp

        self.initParam.gis_file_name = temp

        temp = self.txtVegFileName.text().strip()
        if len(temp) > 0 and temp.find("/") == -1:
            temp = "ini/" + temp
        self.initParam.veg_file_name = temp

        if self.ckbReadRestartFile.isChecked():
            self.initParam.restart_read_flag = 1
            temp = self.txtRestartFileRead.text().strip()
            if len(temp) > 0 and temp.find("/") == -1:
                temp = "restart/" + temp
            self.initParam.restart_read_file_name = temp
        else:
            self.initParam.restart_read_flag = 0
            self.initParam.restart_read_file_name = "restart/test_01.endpoint"

        if self.ckbWriteRestartFile.isChecked():
            self.initParam.restart_write_flag = 1
            temp = self.txtRestartFileWrite.text().strip()
            if len(temp) > 0 and temp.find("/") == -1:
                temp = "restart/" + temp
            self.initParam.restart_write_file_name = temp
        else:
            self.initParam.restart_write_flag = 0
            self.initParam.restart_write_file_name = "restart/test_01.endpoint"

        if self.rbtMetyearYes.isChecked():
            self.initParam.restart_metyear_use_flag = 1
        else:
            self.initParam.restart_metyear_use_flag = 0

        self.initParam.sim_start_year = int(self.txtStartYear.text().strip())
        self.initParam.no_of_sim_year = (int(self.txtEndYear.text().strip()) - self.initParam.sim_start_year) + 1

        if self.ckbSpinup.isChecked():
            self.initParam.sim_spinup_flag = 1
            self.initParam.no_of_spinup_year = int(self.txtSpinupYear.text().strip())
        else:
            self.initParam.sim_spinup_flag = 0
            self.initParam.no_of_spinup_year = 0

        self.initParam.Tmax_offset = float(self.txtTmaxOffset.text().strip())
        self.initParam.Tmin_offset = float(self.txtTminOffset.text().strip())
        self.initParam.precipitation_multiplier = float(self.txtPrecipitationMulp.text().strip())
        self.initParam.vpd_multiplier = float(self.txtVpdMulp.text().strip())
        self.initParam.swave_multiplier = float(self.txtRadiationMulp.text().strip())

        if self.rbtCCContant.isChecked():
            self.initParam.carbon_variability_flag = 0
        else:
            self.initParam.carbon_variability_flag = 1

        self.initParam.air_constant_carbon = float(self.txtConsConcentration.text().strip())
        temp = self.txtCarbonFile.text().strip().split("/")[-1]
        if len(temp) > 0:
            temp = "co2/" + temp
        else: temp = "co2/default.txt"
        self.initParam.carbon_file = temp

        self.initParam.nitrogen_depo_option_flag = self.cmbNitrogenDiposition.currentIndex()
        self.initParam.industrial_ref_year = int(self.txtRefYear.text().strip())

        temp =  self.txtOutputFilePrefix.text().strip().split("/")[-1]
        if len(temp) > 0:
            temp = "outputs/" + temp
        else: temp = "outputs/default"
        self.initParam.output_file_prefix = temp

        if self.rbtDispProgressYes.isChecked():
            self.initParam.display_flag = 1
        else:
            self.initParam.display_flag = 0

        self.initParam.daily_output_flag = self.cmbDailyOutputType.currentIndex()

        if self.ckbMonthAverage.isChecked():
            self.initParam.monthly_average_flag = 1
        else:
            self.initParam.monthly_average_flag = 0

        if self.ckbYearAverage.isChecked():
            self.initParam.annual_average_flag = 1
        else: self.initParam.annual_average_flag = 0

        self.initParam.annual_output_flag = self.cmbYearlyOutputType.currentIndex()

        if self.ckbSaveOutputTemplate.isChecked:
            self.initParam.output_template_save_flag = 1
            self.initParam.output_template_save_fileName = self.txtTemplateName.text().strip()
        else: self.initParam.output_template_save_flag = 0

        #loading output list
        # self.initParam.initalizeOutputTemplate()
        # self.initParam.output_template.mode = "out"
        # for item in self.initParam.output.listOfSelectedSiteSpecificVariable_Annual:
        #     varname = self.initParam.output.getSiteSpecificVariableName(item["catid"], item["varid"])
        #     self.initParam.output_template.site_specific_annual_output.append([item["varid"], varname])
        #
        # for item in self.initParam.output.listOfSelectedSiteSpecificVariable_Daily:
        #     varname = self.initParam.output.getSiteSpecificVariableName(item["catid"], item["varid"])
        #     self.initParam.output_template.site_specific_daily_output.append([item["varid"], varname])
        #
        # for item in self.initParam.output.listOfSelectedVegSpecificVariable_Annual:
        #     varname = self.initParam.output.getVegetationSpecificVariableName(item["catid"], item["varid"])
        #     self.initParam.output_template.veg_specific_annual_output.append([item["varid"], varname])
        #
        # for item in self.initParam.output.listOfSelectedVegSpecificVariable_Daily:
        #     varname = self.initParam.output.getVegetationSpecificVariableName(item["catid"], item["varid"])
        #     self.initParam.output_template.veg_specific_daily_output.append([item["varid"], varname])
        #
        # for varid in self.initParam.output.listOfSelectedTotalLayerVariable:
        #     varname = self.initParam.output.getLayerSpecificVariableName(varid)
        #     self.initParam.output_template.total_layer_output.append([varid, varname])
        #
        # for item in self.initParam.output.selectedAnnualVarLayerList:
        #     var = item["varid"]
        #     laylist = item["laylist"]
        #     self.initParam.output_template.annual_variable_layer_output.append([var, laylist])
        #
        # for item in self.initParam.output.selectedDailyVarLayerList:
        #     var = item["varid"]
        #     laylist = item["laylist"]
        #     self.initParam.output_template.daily_variable_layer_output.append([var, laylist])
        #
        # for item in self.initParam.output.selectedAnnualLayerVarList:
        #     layer = item["layer"]
        #     varlist = item["varlist"]
        #     self.initParam.output_template.annual_layer_variable_output.append([layer, varlist])
        #
        # for item in self.initParam.output.selectedDailyLayerVarList:
        #     layer = item["layer"]
        #     varlist = item["varlist"]
        #     self.initParam.output_template.daily_layer_variable_output.append([layer, varlist])

    def read_output_list(self):
        self.clearTotalLayerVariableListTable()
        for var in self.initParam.output.getSelectedTotalLayerVariableList():
            ndx = self.twTotalLayerSelectedVariable.rowCount()
            self.twTotalLayerSelectedVariable.insertRow(ndx)
            cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
            self.twTotalLayerSelectedVariable.setItem(ndx, 0, cell)
            cell = QtWidgets.QTableWidgetItem(var["varname"])
            self.twTotalLayerSelectedVariable.setItem(ndx, 1, cell)
            cell = QtWidgets.QTableWidgetItem(var["vardesc"])
            self.twTotalLayerSelectedVariable.setItem(ndx, 2, cell)
            self.twTotalLayerSelectedVariable.setRowHeight(ndx, 20)

        for var in self.initParam.output.getUnselectedTotalLayerVariableList():
            ndx = self.twTotalLayerVariableList.rowCount()
            self.twTotalLayerVariableList.insertRow(ndx)
            cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
            self.twTotalLayerVariableList.setItem(ndx, 0, cell)
            cell = QtWidgets.QTableWidgetItem(var["varname"])
            self.twTotalLayerVariableList.setItem(ndx, 1, cell)
            cell = QtWidgets.QTableWidgetItem(var["vardesc"])
            self.twTotalLayerVariableList.setItem(ndx, 2, cell)
            self.twTotalLayerVariableList.setRowHeight(ndx, 20)

        self.lstLayerSpecificAnnualSelectedVariableLayer.addItems(self.initParam.output.getTextLinesFromAnnualVarLayerList())
        self.lstLayerSpecificDailySelectedVariableLayer.addItems(self.initParam.output.getTextLinesFromDailyVarLayerList())
        self.lstLayerSpecificDailySelectedLayerVariable.addItems(self.initParam.output.getTextLinesFromDailyLayerVarList())
        self.lstLayerSpecificAnnualSelectedLayerVariable.addItems(self.initParam.output.getTextLinesFromAnnualLayerVarList())

    def btnSave_clicked(self):
        if self.editMode:
            self.readParamValuesFromUIComponent()
            self.form.parentWidget().close()
        else:
            if self.checkCompleteness():
                if len(self.txtInitFileDirectory.text().strip()) > 0:
                    targetDir = self.txtInitFileDirectory.text().strip().replace("/","\\")
                else:
                    if len(ApplicationProperty.currentModelDirectory) > 0:
                        targetDir = ApplicationProperty.currentModelDirectory
                    else: targetDir = ApplicationProperty.getScriptPath()

                if targetDir.find("/ini") == -1 : targetDir = os.path.join(targetDir, "ini")

                fileName = os.path.join(targetDir, self.txtInitFileName.text().strip())

                if self.rbtModifyInitFile.isChecked():
                    message = "Do you want to create a new initial file?\nYes = Create New Initial file\nNo = Overwrite Opened File"
                    reply = QtGui.QMessageBox.question(self.form, 'Message', message, QtGui.QMessageBox.Yes,
                                                    QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes: #yes/no message: do you want to save the changes in a new init file?
                        fileName = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save File', targetDir, "Init File (*.ini)")
                        if fileName:
                            temp = fileName.split("/")[-1]
                            self.txtInitFileName.setText(temp)
                            self.txtInitFileDirectory.setText(fileName.replace(temp, ""))
                        else:
                            return False

                if fileName.find(".ini") < 0:
                    fileName += ".ini"

                self.readParamValuesFromUIComponent()

                if FileReadWrite.writeInitialFile(self.initParam, fileName):
                    QtGui.QMessageBox.about(self.form, "Save", "The initial file has been saved successfully.")
                else: QtGui.QMessageBox.about(self.form, "Unsuccessfull", "Initial file could not be created.")

    def clearSelectedVariableList(self):
        self.rbtSiteSpecificDailyOutput.setChecked(True)
        self.cmbSiteSpecificOutputCategory.setCurrentIndex(-1)
        self.clearSiteSpecificVariableListTable()
        self.clearSiteSpecificSelectedListTable()
        self.rbtVegetationSpecificDailyOutput.setChecked(True)
        self.cmbVegetationSpecificCategory.setCurrentIndex(-1)
        self.clearVegSpecificVariableListTable()
        self.clearVegSpecificSelectedListTable()
        self.clearTotalLayerVariableListTable()
        self.clearTotalLayerSelectedVariableTable()

        varlist = self.initParam.output.getUnselectedTotalLayerVariableList()
        for var in varlist:
            ndx = self.twTotalLayerVariableList.rowCount()
            self.twTotalLayerVariableList.insertRow(ndx)
            cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
            self.twTotalLayerVariableList.setItem(ndx, 0, cell)
            cell = QtWidgets.QTableWidgetItem(var["varname"])
            self.twTotalLayerVariableList.setItem(ndx, 1, cell)
            cell = QtWidgets.QTableWidgetItem(var["vardesc"])
            self.twTotalLayerVariableList.setItem(ndx, 2, cell)
            self.twTotalLayerVariableList.setRowHeight(ndx, 20)

        self.rbtLayerSpecificAnnualSpecificDepth.setChecked(True)
        self.txtLayerSpecificAnnualSoilDepth.clear()
        self.txtLayerSpecificAnnualLowerBound.clear()
        self.clearLayerSpecificAnnualVariableList()
        self.clearLayerSpecificDailyVariableListTable()

        varlist = self.initParam.output.getLayerSpecificVariableList()
        for var in varlist:
            ndx = self.twLayerSpecificAnnualVariableList.rowCount()
            self.twLayerSpecificAnnualVariableList.insertRow(ndx)
            cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
            self.twLayerSpecificAnnualVariableList.setItem(ndx, 0, cell)
            cell = QtWidgets.QTableWidgetItem(var["varname"])
            self.twLayerSpecificAnnualVariableList.setItem(ndx, 1, cell)
            cell = QtWidgets.QTableWidgetItem(var["vardesc"])
            self.twLayerSpecificAnnualVariableList.setItem(ndx, 2, cell)
            self.twLayerSpecificAnnualVariableList.setRowHeight(ndx, 20)

            ndx = self.twLayerSpecificDailyVariableList.rowCount()
            self.twLayerSpecificDailyVariableList.insertRow(ndx)
            cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
            self.twLayerSpecificDailyVariableList.setItem(ndx, 0, cell)
            cell = QtWidgets.QTableWidgetItem(var["varname"])
            self.twLayerSpecificDailyVariableList.setItem(ndx, 1, cell)
            cell = QtWidgets.QTableWidgetItem(var["vardesc"])
            self.twLayerSpecificDailyVariableList.setItem(ndx, 2, cell)
            self.twLayerSpecificDailyVariableList.setRowHeight(ndx, 20)

        self.lstLayerSpecificAnnualSelectedLayerVariable.clear()
        self.cmbLayerSpecificAnnualVariableList.setCurrentIndex(-1)
        self.rbtLayerSpecificAnnualMaxDepth_2.setChecked(True)
        self.txtLayerSpecificAnnualSoilDepth_2.clear()
        self.txtLayerSpecificAnnualLowerBound_2.clear()
        self.lstLayerSpecificAnnualSelectedVariableLayer.clear()
        self.rbtLayerSpecificDailySpecificDepth.setChecked(True)
        self.txtLayerSpecificDailySoilDepth.clear()
        self.txtLayerSpecificDailyLowerBound.clear()
        self.lstLayerSpecificDailySelectedLayerVariable.clear()
        self.cmbLayerSpecificDailyVariableList.setCurrentIndex(-1)
        self.rbtLayerSpecificDailySpecificDepth_2.setChecked(True)
        self.txtLayerSpecificDailySoilDepth_2.clear()
        self.txtLayerSpecificDailyLowerBound_2.clear()
        self.lstLayerSpecificDailySelectedVariableLayer.clear()

    def checkCompleteness(self):
        if not self.txtInitFileName.text().strip():
            message = "Initial File Name is missing! Please enter initial file name."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.txtInitFileName.clear()
            self.txtInitFileName.setFocus(True)
            return False
        elif not self.txtGisFileName.text().strip():
            message = "GIS File Name is missing! Please enter GIS file name"
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtGisFileName.setFocus(True)
            return False
        elif not self.txtVegFileName.text().strip():
            message = "Vegetation file is missing! Please enter the name of Vegetation File."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtVegFileName.setFocus(True)
            return False
        elif self.ckbReadRestartFile.isChecked()and not self.txtRestartFileRead.text():
            message = "Restart input file name is missing! Please enter the name of restart input file."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtRestartFileRead.setFocus(True)
            return False
        elif self.ckbWriteRestartFile.isChecked() and not self.txtRestartFileWrite.text():
            message = "Restart output file name is missing! Please enter the name of restart output file."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtRestartFileWrite.setFocus(True)
            return False
        elif not self.txtStartYear.text():
            message = "Starting year is missing! Please enter starting year."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtStartYear.setFocus(True)
            return False
        elif not self.txtEndYear.text():
            message = "End year is missing! Please enter end year."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtEndYear.setFocus(True)
            return False
        elif self.ckbSpinup.isChecked() and not self.txtSpinupYear.text():
            message = "No of spinup years is missing! Please enter spinup number."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtSpinupYear.setFocus(True)
            return False
        elif not self.txtTmaxOffset.text():
            message = "Maximum Temperature Offset is missing! Please enter T-Max Offset."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtTmaxOffset.setFocus(True)
            return False
        elif not self.txtTminOffset.text():
            message = "Minimum Temperature Offset is missing! Please enter T-Min Offset."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtTminOffset.setFocus(True)
            return False
        elif not self.txtPrecipitationMulp.text():
            message = "Multiplier for precipitation is missing! Please enter precipitation multiplier."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtPrecipitationMulp.setFocus(True)
            return False
        elif not self.txtVpdMulp.text():
            message = "Multiplier for vapour pressure deficits is missing! Please enter VPD multiplier."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtVpdMulp.setFocus(True)
            return False
        elif not self.txtRadiationMulp.text():
            message = "Multiplier for SW radiation is missing! Please enter SW radiation multiplier."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtRadiationMulp.setFocus(True)
            return False
        elif self.rbtCCContant.isChecked() and not self.txtConsConcentration.text():
            message = "Atmospheric CO2 constant is missing! Please enter CO2 Constant."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtConsConcentration.setFocus(True)
            return False
        elif self.rbtCCVariable.isChecked() and not self.txtCarbonFile.text():
            message = "Carbon file is missing! Please enter Carbon file name."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtCarbonFile.setFocus(True)
            return False
        elif self.cmbNitrogenDiposition.currentIndex() == -1:
            message = "Please choose a Nitrogen Diposition option."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.cmbNitrogenDiposition.setFocus(True)
            return False
        elif not self.txtRefYear.text():
            message = "Industrial reference year is missing! Please enter Industrial Reference Year."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(0)
            self.txtRefYear.setFocus(True)
            return False
        elif not self.txtOutputFilePrefix.text():
            message = "Please enter the output file name prefix."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(1)
            self.txtOutputFilePrefix.setFocus(True)
            return False
        elif self.cmbDailyOutputType.currentIndex() == -1:
            message = "Choose daily output option."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(1)
            self.cmbDailyOutputType.setFocus(True)
            return False
        elif self.cmbYearlyOutputType.currentIndex() == -1:
            message = "Please choose annual output option."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(1)
            self.cmbYearlyOutputType.setFocus(True)
            return False
        elif self.ckbSaveOutputTemplate.isChecked() and not self.txtTemplateName.text():
            message = "Please write the template name."
            QtGui.QMessageBox.about(self.form, "Initial Setting", message)
            self.tbwSettings.setCurrentIndex(1)
            self.txtTemplateName.setFocus(True)
            return False
        else: return True

    def lockInputComponent(self, lock):
        self.groupBoxGisVegFile.setEnabled(not lock)
        self.groupBoxRestart.setEnabled(not lock)
        self.groupBoxTimeSetting.setEnabled(not lock)
        self.groupBoxClimateSetting.setEnabled(not lock)
        self.groupBoxCo2Control.setEnabled(not lock)
        self.groupBoxNDeposition.setEnabled(not lock)
        # self.txtGisFileName.setReadOnly(lock)
        # txtVegFileName
        # btnBrowseGisFile
        # btnBrowseVegFile
        # ckbReadRestartFile
        # txtRestartFileRead
        # btnBrowseRestartFileRead
        # ckbWriteRestartFile
        # txtRestartFileWrite
        # btnBrowseRestartFileWrite
        # rbtMetyearYes
        # rbtMetyearNo
        # txtStartYear
        # txtEndYear
        # ckbSpinup
        # txtSpinupYear
        # txtTmaxOffset
        # txtTminOffset
        # txtPrecipitationMulp
        # txtVpdMulp
        # txtRadiationMulp
        # rbtCCContant
        # rbtCCVariable
        # txtConsConcentration
        # txtCarbonFile
        # btnCarbonFile
        # cmbNitrogenDiposition
        # txtRefYear
        self.groupBoxOutputSetting.setEnabled(not lock)
        self.groupBoxTimeSetting_2.setEnabled(not lock)
        self.btnSiteSpecificVariableAdd.setEnabled(not lock)
        self.btnSiteSpecificVariableAddAll.setEnabled(not lock)
        self.btnSiteSpecificVariableRemove.setEnabled(not lock)
        self.btnSiteSpecificVariableRemoveAll.setEnabled(not lock)
        self.btnVegetationSpecificVariableAdd.setEnabled(not lock)
        self.btnVegetationSpecificVariableAddAll.setEnabled(not lock)
        self.btnVegetationSpecificVariableRemove.setEnabled(not lock)
        self.btnVegetationSpecificVariableRemoveAll.setEnabled(not lock)
        self.gpbTotalLayerOutput.setEnabled(not lock)
        self.gpbLayerSpecificDailyLayerVariable.setEnabled(not lock)
        self.gpbLayerSpecificDailyVariableLayer.setEnabled(not lock)
        self.gpbLayerSpecificAnnualLayerVariable.setEnabled(not lock)
        self.gpbLayerSpecificAnnualVariableLayer.setEnabled(not lock)

    def btnClearSiteVariables_click(self):
        #clear all selected site variable
        if self.rbtSiteSpecificDailyOutput.isChecked():
            self.initParam.output.clearSiteSpecificSelectedList(dailyVar=True)
        else:
            self.initParam.output.clearSiteSpecificSelectedList(annualVar=True)

        self.cmbSiteSpecificOutputCategory.setCurrentIndex(-1)
        self.ckbShowAllSelectedSiteVariable.setChecked(False)

    def btnClearVegVariables_click(self):
        if self.rbtVegetationSpecificDailyOutput.isChecked():
            self.initParam.output.clearVegSpecificSelectedList(dailyVar=True)
        else:
            self.initParam.output.clearVegSpecificSelectedList(annualVar=True)
        self.cmbVegetationSpecificCategory.setCurrentIndex(-1)
        self.ckbShowAllSelectedVegVariable.setChecked(False)

    def btnClear_clicked(self):
        self.initParam.output.clear()
        self.cmbSiteSpecificOutputCategory.setCurrentIndex(-1)
        self.cmbVegetationSpecificCategory.setCurrentIndex(-1)
        self.ckbShowAllSelectedSiteVariable.setChecked(False)
        self.ckbShowAllSelectedVegVariable.setChecked(False)
        self.clearTotalLayerSelectedVariableTable()
        self.lstLayerSpecificDailySelectedLayerVariable.clear()
        self.lstLayerSpecificDailySelectedVariableLayer.clear()
        self.lstLayerSpecificAnnualSelectedLayerVariable.clear()
        self.lstLayerSpecificAnnualSelectedVariableLayer.clear()

    def ckbShowAllSelectedSiteVariable_toggled(self):
        if self.ckbShowAllSelectedSiteVariable.isChecked():
            self.cmbSiteSpecificOutputCategory.setCurrentIndex(-1)
            if self.rbtSiteSpecificDailyOutput.isChecked():
                varList = self.initParam.output.getAllSelectedSiteSpecificVariableList(daily=True)
            else: varList = self.initParam.output.getAllSelectedSiteSpecificVariableList(annual=True)

            if len(varList) > 0:
                #set table structure
                if self.twSiteSpecificSelectedVariable.columnCount() == 3:
                    self.twSiteSpecificSelectedVariable.setColumnCount(4)
                    self.twSiteSpecificSelectedVariable.setHorizontalHeaderLabels(["No.", "Variable Name", "Variable Label", "Category"])
                    self.twSiteSpecificSelectedVariable.setColumnWidth(3, 200)
                for var in varList:
                    ndx = self.twSiteSpecificSelectedVariable.rowCount()
                    self.twSiteSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 2, cell)
                    self.twSiteSpecificSelectedVariable.setRowHeight(ndx, 20)
                    cell = QtWidgets.QTableWidgetItem(str(var["catname"]))
                    self.twSiteSpecificSelectedVariable.setItem(ndx, 3, cell)
        else:
            self.clearSiteSpecificSelectedListTable()
            if self.twSiteSpecificSelectedVariable.columnCount() == 4:
                self.twSiteSpecificSelectedVariable.removeColumn(3)

    def ckbShowAllSelectedVegVariable_toggled(self):
        if self.ckbShowAllSelectedVegVariable.isChecked():
            self.cmbVegetationSpecificCategory.setCurrentIndex(-1)
            if self.rbtVegetationSpecificDailyOutput.isChecked():
                varList = self.initParam.output.getAllSelectedVegetationSpecificVariableList(daily=True)
            else: varList = self.initParam.output.getAllSelectedVegetationSpecificVariableList(annual=True)

            if len(varList) > 0:
                if self.twVegetationSpecificSelectedVariable.columnCount() == 3:
                    self.twVegetationSpecificSelectedVariable.setColumnCount(4)
                    self.twVegetationSpecificSelectedVariable.setHorizontalHeaderLabels(["No.", "Variable Name",
                                                                                         "Variable Label", "Variable Category"])
                    self.twVegetationSpecificSelectedVariable.setColumnWidth(3, 200)
                for var in varList:
                    ndx = self.twVegetationSpecificSelectedVariable.rowCount()
                    self.twVegetationSpecificSelectedVariable.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(str(var["varid"]))
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(var["varname"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(var["vardesc"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 2, cell)
                    cell = QtWidgets.QTableWidgetItem(var["catname"])
                    self.twVegetationSpecificSelectedVariable.setItem(ndx, 3, cell)
                    self.twVegetationSpecificSelectedVariable.setRowHeight(ndx, 20)
        else:
            if self.twVegetationSpecificSelectedVariable.columnCount() == 4:
                self.twVegetationSpecificSelectedVariable.removeColumn(3)
            self.clearVegSpecificSelectedListTable()
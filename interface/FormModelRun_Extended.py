from interface.FormModelRun import Ui_FormModelRun
from PyQt5 import QtGui, QtCore, QtWidgets
from file_io import FileReadWrite
from application import ApplicationProperty
from parameter import *
from parameter_set import BiomeBGCParameterSet
from interface.FormInitialAndOutputSetting_Extended import FormInitialAndOutputSetting
from interface.FormGisFile_Extended import FormGisFile
from interface.FormVegFile_Extended import FormVegFile
from interface.FormEpcFile_Extended import FormEpcFile
from interface.FormSoilProfile_Extended import FormSoilProfile
from interface.DialogVersionSettings_Extended import DialogVersionSettings, model_version
from interface.DialogGraphCompare_Extended import DialogGraphCompare
import copy
from output import output
import subprocess
import os
from graph import ModelGraph, ModelPlot, DataSeries, DataSource
from draw_graph import BiomeBgcGraphDummy
from interface.DialogShowLog_Extended import DialogLogShow
import sys

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


class FormModelRun(Ui_FormModelRun):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.addSocket()

        self.signalMapper = QtCore.QSignalMapper(self.form)
        self.signalMapper.mapped[QtWidgets.QWidget].indexChanged.connect(self.dynamicCombo_indexChanged)

        self.signalMapper_gconfig_checkbox = QtCore.QSignalMapper(self.form)
        self.signalMapper_gconfig_checkbox.mapped[QtWidgets.QWidget].connect(self.refresh_configuration)

        self.signalMapper_gconfig_combo = QtCore.QSignalMapper(self.form)
        self.signalMapper_gconfig_combo.mapped[QtWidgets.QWidget].connect(self.gconfig_combo_indexChanged)

        self.listModelParam = []

        #listBatchFile holds Batch File Path
        self.listBatchFile = []

        #listInitFileName was added later to store the names of initial files.
        self.listInitFileName = []

        self.currentVersionIndex = -1
        self.versionModifyMode = False
        # self.isModifiedVersionSaved = False
        # self.modelDirectory = ""
        # self.comparingVersionNoList = []

        self.initform = FormInitialAndOutputSetting()
        self.gisform = FormGisFile()
        self.vegform = FormVegFile()
        self.epcform = FormEpcFile()
        self.soilform = FormSoilProfile()
        self.dialog_version_control = DialogVersionSettings()

        self.flag_startNewVersion = True                #alternative: continue from previous versioning
        self.flag_versioningFromInitFile = False        #only valid when flag_startNewVersion is False
                                                        #alternative: versioningFromAnArbitraryPosition
        self.flag_addVersionNoAtTheEndOfFiles = True    #alternative: replace last two digit of previous file name

        self.initialSetting()
        self.addValidator()

        self.graph_configuration = graph_configuration()
        self.dialog_graph_compare = None
        self.dialog_show_log = None

    def addSocket(self):
        self.btnBrowseInitialFile.clicked.connect(self.btnBrowseInitialFile_clicked)
        self.btnModify.clicked.connect(self.btnModify_clicked)
        self.btnClose.clicked.connect(self.btnClose_clicked)
        # self.btnView.clicked.connect(self.btnView_clicked)
        self.btnRun.clicked.connect(self.btnRun_clicked)
        self.btnModelProgramBrowse.clicked.connect(self.btnModelProgramBrowse_clicked)
        self.cmbParameterFile.currentIndexChanged.connect(self.cmbParameterFile_currentIndexChanged)
        self.btnCompare.clicked.connect(self.btnCompare_clicked)
        # self.btnClear.clicked.connect(self.btnClear_clicked)
        self.ckbShowRefValue.toggled.connect(self.ckbShowRefValue_toggled)
        self.buttonVersionSettings.clicked.connect(self.buttonVersionSettings_clicked)
        self.txtStartingVersionNo.textChanged.connect(self.txtStartingVersionNo_textChanged)
        self.btnSaveVersion.clicked.connect(self.btnSaveVersion_clicked)
        self.ckbShowVersion.toggled.connect(self.ckbShowVersion_toggled)
        self.btnNewVersion.clicked.connect(self.btnNewVersion_clicked)
        self.buttonFirstVersion.clicked.connect(self.buttonFirstVersion_clicked)
        self.buttonPreviousVersion.clicked.connect(self.buttonPreviousVersion_clieked)
        self.buttonNextVersion.clicked.connect(self.buttonNextVersion_clicked)
        self.buttonLastVersion.clicked.connect(self.buttonLastVersion_clicked)
        self.btnLoadVersion.clicked.connect(self.btnLoadVersion_clicked)
        self.txtVersionNo.textChanged.connect(self.txtVersionNo_textChanged)
        self.tableParameterView.itemChanged.connect(self.tableParameterView_itemChanged)
        # self.radioButtonStartNewVersion.toggled(self.radioButtonStartNewVersion_toggled())
        # self.radioButtonContinuePreviousVersioning.toggled.connect(self.radioButtonContinuePreviousVersioning_toggled)
        # self.radioButtonStartNewVersion.toggled.connect(self.radioButtonStartNewVersion_toggled)
        # self.checkBoxContinueFromInitFile.toggled.connect(self.checkBoxContinueFromInitFile_toggled)
        # self.checkBoxContinueFrom.toggled.connect(self.checkBoxContinueFrom_toggled)
        # self.textCurrentVersion.textChanged.connect(self.textCurrentVersion_textChanged)
        self.btnRefresh.clicked.connect(self.btnRefresh_clicked)
        self.comboGraphName.currentIndexChanged.connect(self.comboGraphName_currentIndexChanged)
        self.checkBoxGraphShow.toggled.connect(self.checkBoxGraphShow_toggled)
        self.buttonSaveConfiguration.clicked.connect(self.buttonSaveConfiguration_clicked)
        self.buttonLoadConfiguration.clicked.connect(self.buttonLoadConfiguration_clicked)
        self.buttonShowGraph.clicked.connect(self.buttonShowGraph_clicked)
        self.buttonGraphFirst.clicked.connect(self.buttonGraphFirst_clicked)
        self.buttonGraphLast.clicked.connect(self.buttonGraphLast_clicked)
        self.buttonGraphBack.clicked.connect(self.buttonGraphBack_clicked)
        self.buttonGraphNext.clicked.connect(self.buttonGraphNext_clicked)
        self.buttonOriginalView.clicked.connect(self.buttonOriginalView_clicked)
        self.buttonCompare.clicked.connect(self.buttonCompare_clicked)

    def initialSetting(self):
        self.tableParameterFile.setColumnCount(2)
        header = ["Parameter", "File Name"]
        self.tableParameterFile.setHorizontalHeaderLabels(header)
        self.tableParameterFile.setColumnWidth(0, 120)
        self.tableParameterFile.setColumnWidth(1, 180)
        self.tableParameterFile.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        #geometry of frameVersionSetting : 430, 10, 451, 211


        self.txtVersionNo.setReadOnly(True)
        self.txtInitialFile.setReadOnly(True)
        self.txtModelProgram.setReadOnly(True)

        self.tableParameterView.setColumnCount(2)
        header = ["Param Name", "Value"]
        self.tableParameterView.setHorizontalHeaderLabels(header)
        self.tableParameterView.setColumnWidth(0, 250)
        self.tableParameterView.setColumnWidth(1, 90)

        self.cmbParameterFile.addItems(["Initial Parameter", "GIS Parameter", "Veg Parameter", "Soil Parameter", "Epc Parameter"])
        self.cmbParameterFile.setEnabled(False)
        self.cmbParameterFile.setCurrentIndex(-1)

        self.txtStartingVersionNo.setReadOnly(True)
        self.ckbShowVersion.setChecked(True)

        self.ckbShowVersion.setEnabled(False)
        self.ckbShowRefValue.setEnabled(False)
        self.btnCompare.setEnabled(False)
        # self.btnClear.setEnabled(False)
        self.btnModelProgramBrowse.setEnabled(False)
        self.btnRun.setEnabled(False)
        self.btnSaveVersion.setEnabled(False)
        self.txtVersionCompare.setReadOnly(True)
        # self.txtComparingVersion.setReadOnly(True)
        self.btnModify.setEnabled(False)
        self.btnRefresh.setEnabled(False)
        self.lblActiveVersion.setText("")

        self.enable_graph_show(False)
        self.enable_graph_option(False)
        self.tableParameterCompare.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.load_graph_template()
        self.comboGraphName.setCurrentIndex(-1)


        self.tableConfiguration.setColumnCount(3)
        self.tableConfiguration.setHorizontalHeaderLabels(["Graph Object", "Version", "Change"])
        self.tableConfiguration.setColumnWidth(0, 180)
        self.tableConfiguration.setColumnWidth(1, 50)
        self.tableConfiguration.setColumnWidth(2, 50)

    def load_graph_template(self):
        list_of_graph = ModelGraph.read_binary_template_list()
        if len(list_of_graph) > 0: self.comboGraphName.addItems(list_of_graph)

    def enable_graph_option(self, flag_bool):
        self.frameGraphOption.setEnabled(flag_bool)

    def enable_graph_show(self, flag_bool):
        self.labelCurrentGraphName.clear()
        self.buttonShowGraph.setEnabled(flag_bool)
        if not flag_bool:
            self.buttonOriginalView.setEnabled(flag_bool)
            self.buttonCompare.setEnabled(flag_bool)
            self.buttonGraphFirst.setEnabled(flag_bool)
            self.buttonGraphBack.setEnabled(flag_bool)
            self.buttonGraphNext.setEnabled(flag_bool)
            self.buttonGraphLast.setEnabled(flag_bool)
        self.graphicsView.setScene(None)

    def addValidator(self):
        rx = QtCore.QRegExp("^[0-9]{2}$")
        versionValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("^[\w\-.]+$")
        fileNameValidator= QtGui.QRegExpValidator(rx)
        # rx = QtCore.QRegExp("^[\d]$")
        # versionsValidator = QtGui.QRegExpValidator(rx)

        self.txtStartingVersionNo.setValidator(versionValidator)
        self.txtVersionNo.setValidator(versionValidator)
        # self.txtVersionCompare.setValidator(versionsValidator)
        # self.txtComparingVersion.setValidator(versionValidator)

    def txtVersionNo_textChanged(self):
        self.lblActiveVersion.setText("Current Version No. : " + self.txtVersionNo.text())
        if self.graph_configuration.number_of_graphs() > 0:
            version_text = self.txtVersionNo.text().strip()
            if self.graph_configuration.graph_availability(version_text):
                if self.graph_configuration.change_image_souce(version_text):
                    self.graph_configuration.current_graph_index = 0
                    self.display_graph()
                    return True
                else: self.graphicsView.setScene(None)
            else: self.graphicsView.setScene(None)
        else: self.graphicsView.setScene(None)
        self.graphicsView.show()

    def buttonFirstVersion_clicked(self):
        starting_vertion_text = self.txtStartingVersionNo.text().strip()
        if len(self.listModelParam) > 1:
            if not self.versionModifyMode:
                self.currentVersionIndex = 0
                self.txtVersionNo.setText(starting_vertion_text.rjust(2,"0"))
                self.findLinkedFile(self.currentVersionIndex)
                self.cmbParameterFile_currentIndexChanged()
            else:
                message = "The current version is not saved. Please save the current version first."
                QtGui.QMessageBox.about(self.form, "Pending Version", message)
        else: self.txtVersionNo.setText(starting_vertion_text.rjust(2,"0"))

    def buttonPreviousVersion_clieked(self):
        if len(self.listModelParam) > 1:
            if not self.versionModifyMode:
                temp = self.currentVersionIndex - 1
                if temp >= 0:
                    self.currentVersionIndex = temp
                    startingVersion = int(self.txtStartingVersionNo.text())
                    self.txtVersionNo.setText(str(startingVersion + temp).rjust(2,"0"))
                    self.findLinkedFile(temp)
                    self.cmbParameterFile_currentIndexChanged()
            else:
                message = "The current version is not saved. Please save the current version first."
                QtGui.QMessageBox.about(self.form, "Pending Version", message)

    def buttonNextVersion_clicked(self):
        if len(self.listModelParam) > 1:
            if not self.versionModifyMode:
                temp = self.currentVersionIndex + 1
                if temp < len(self.listModelParam):
                    self.currentVersionIndex = temp
                    startingVersion = int(self.txtStartingVersionNo.text())
                    self.txtVersionNo.setText(str(startingVersion + temp).rjust(2,"0"))
                    self.findLinkedFile(self.currentVersionIndex)
                    self.cmbParameterFile_currentIndexChanged()
            else:
                message = "The current version is not saved. Please save the current version first."
                QtGui.QMessageBox.about(self.form, "Pending Version", message)

    def buttonLastVersion_clicked(self):
        if len(self.listModelParam) > 1:
            if not self.versionModifyMode:
                self.currentVersionIndex = len(self.listModelParam) - 1
                startingVersion = int(self.txtStartingVersionNo.text())
                self.txtVersionNo.setText(str(startingVersion + self.currentVersionIndex).rjust(2,"0"))
                self.findLinkedFile(self.currentVersionIndex)
                self.cmbParameterFile_currentIndexChanged()
            else:
                message = "The current version is not saved. Please save the current version first."
                QtGui.QMessageBox.about(self.form, "Pending Version", message)

    def txtStartingVersionNo_textChanged(self):
        startVersion = self.txtStartingVersionNo.text()
        if len(startVersion) > 0:
            self.buttonFirstVersion_clicked()
            self.comboGraphName.setCurrentIndex(-1)

            # self.currentVersionIndex = 0

    def buttonVersionSettings_clicked(self):
        if len(self.txtInitialFile.text().strip()) > 0:
            self.dialog_version_control.model_version.first_initial_filename = self.txtInitialFile.text().strip()
            if self.flag_startNewVersion:
                self.dialog_version_control.model_version.start_from_zero = True
            else:
                self.dialog_version_control.model_version.start_from_zero = False
                if self.flag_versioningFromInitFile:
                    self.dialog_version_control.model_version.continue_from_initial_parameter_version = True
                else:
                    self.dialog_version_control.model_version.continue_from_initial_parameter_version = False
                    startVersion = self.txtStartingVersionNo.text()
                    try: startVersion = int(startVersion)
                    except: startVersion = 0
                    if startVersion > 0:
                        self.dialog_version_control.model_version.start_version_number_from = startVersion
            if self.flag_addVersionNoAtTheEndOfFiles:
                self.dialog_version_control.model_version.replace_last_two_digit = False
            else:
                self.dialog_version_control.model_version.replace_last_two_digit = True
            self.dialog_version_control.buttonOk.clicked.connect(self.version_control_dialog_ok_button_clicked)
            self.dialog_version_control.initial_setting()
            self.dialog_version_control.form.show()

    def version_control_dialog_ok_button_clicked(self):
        model_version = self.dialog_version_control.buttonOk_clicked()
        start_version = model_version.starting_version_number()
        if start_version >= 0:
            self.txtStartingVersionNo.setText(str(start_version).rjust(2,"0"))
            self.flag_startNewVersion = model_version.start_from_zero
            self.flag_versioningFromInitFile = model_version.continue_from_initial_parameter_version
            self.flag_addVersionNoAtTheEndOfFiles = not model_version.replace_last_two_digit
        else:
            if start_version == -1: message = "Starting version number could not be read from initial file."
            else: message = "Version settings is improper. Please try again."
            QtGui.QMessageBox.about(self.form, "Version Error", message)

            self.dialog_version_control.form.show()




    def deleteRowsFromParamFileTable(self):
        for i in reversed(range(self.tableParameterFile.rowCount())):
            self.tableParameterFile.removeRow(i)

    def btnBrowseInitialFile_clicked(self):
        startingDirectory = ApplicationProperty.currentModelDirectory
        if startingDirectory == "": startingDirectory = ApplicationProperty.getScriptPath ()
        initFullPath = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDirectory, "Text File (*.ini)")

        previousModelDirectory = ""
        if len(initFullPath) > 0:
            initFileName = initFullPath.split("/")[-1]
            temp = initFullPath.replace(initFileName, "").replace("/ini/", "")
            if os.path.exists(temp):
                if ApplicationProperty.currentModelDirectory != temp:
                    previousModelDirectory = ApplicationProperty.currentModelDirectory
                    ApplicationProperty.currentModelDirectory = temp

            modelParam = None
            if ApplicationProperty.currentModelDirectory: modelParam = self.ReadModelParameter(initFullPath)

            if modelParam is not None:
                modelParam.fileNameChangeFlag = False

                self.listModelParam = []
                self.listModelParam.append(modelParam)
                self.listBatchFile.append("")
                self.listInitFileName.append(initFileName)
                self.currentVersionIndex = 0

                self.txtInitialFile.setText(initFileName)
                # self.txtModelDirectory.setText(ApplicationProperty.currentModelDirectory)


                #version controlling statements
                self.flag_startNewVersion = True
                self.flag_versioningFromInitFile = False
                self.flag_addVersionNoAtTheEndOfFiles = True
                self.txtStartingVersionNo.setText("00")



                self.findLinkedFile(self.currentVersionIndex)
                self.cmbParameterFile.setEnabled(True)
                self.cmbParameterFile.setCurrentIndex(-1)
                # self.ckbShowVersion.setChecked(True)
                # self.ckbShowRefValue.setChecked(False)
                self.buttonVersionSettings.setEnabled(True)
                self.ckbShowVersion.setEnabled(True)
                # self.ckbShowRefValue.setEnabled(True)
                self.btnCompare.setEnabled(True)
                # self.btnClear.setEnabled(True)
                self.btnModelProgramBrowse.setEnabled(True)
                self.btnRun.setEnabled(True)
                self.btnSaveVersion.setEnabled(True)
                self.txtVersionCompare.setReadOnly(False)
                # self.txtComparingVersion.setReadOnly(False)
                self.btnModify.setEnabled(True)
                self.btnRefresh.setEnabled(True)
                # else: self.btnModify.setEnabled(True)
                # self.versionModifyMode = True
                self.enable_graph_option(True)
        else:
            self.enable_graph_option(False)
            if previousModelDirectory != "": ApplicationProperty.currentModelDirectory = previousModelDirectory

    def btnLoadVersion_clicked(self):
        if len(self.listModelParam) > 0 and not self.versionModifyMode:
            startDirectory = ApplicationProperty.currentModelDirectory
            initFullPath = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startDirectory, "Text File (*.ini)")

            if len(initFullPath) > 0:
                temp = initFullPath.split("/")[-1]
                if temp in self.listInitFileName:
                    message = "This version is already loaded."
                    QtGui.QMessageBox.about(self.form, "Input Required", message)
                    return False

                modelParam = self.ReadModelParameter(initFullPath)
                if modelParam is not None:
                    modelParam.fileNameChangeFlag = False

                    initFileName = initFullPath.split("/")[-1]
                    self.listInitFileName.append(initFileName)
                    self.listModelParam.append(modelParam)
                    self.listBatchFile.append("")

                    #version controlling statements
                    self.currentVersionIndex = len(self.listModelParam) - 1
                    startingVersion = int(self.txtStartingVersionNo.text())
                    self.txtVersionNo.setText(str(startingVersion + self.currentVersionIndex).rjust(2,"0"))
                    self.findLinkedFile(self.currentVersionIndex)
                    self.cmbParameterFile_currentIndexChanged()

                    #update graph configuration [increase version index by 1]
                    if self.graph_configuration.number_of_graphs() > 0:
                        for g in self.graph_configuration.list_of_changing_graph:
                            for p in g.edit_plot_list:
                                for i in range(len(p.init_version_list)):
                                    p.init_version_list[i] += 1
                    self.comboGraphName.setCurrentIndex(-1)
                    self.enable_graph_option(True)

        elif len(self.listModelParam) == 0:
            self.btnBrowseInitialFile_clicked()

    def findLinkedFile(self, versionIndex):
        linkedFileList = []     #structure: [{"fileType": "Initial File", "fileName": ini_90_09.ini}, {}]

        if versionIndex < len(self.listModelParam):
            initFileName = self.listInitFileName[versionIndex]
            item = {"type":"Initial Parameter", "fileName": initFileName}
            linkedFileList.append(item)

            modelParam = self.listModelParam[versionIndex]
            # linkedFileList.append(modelParam.findLinkedFiles())
            for item in modelParam.findLinkedFiles():
                linkedFileList.append(item)

            if len(linkedFileList) > 0:
                self.deleteRowsFromParamFileTable()
                for item in linkedFileList:
                    ndx = self.tableParameterFile.rowCount()
                    self.tableParameterFile.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(item["type"])
                    self.tableParameterFile.setItem(ndx, 0, cell)
                    cell = QtWidgets.QTableWidgetItem(item["fileName"])
                    self.tableParameterFile.setItem(ndx, 1, cell)
                    self.tableParameterFile.setRowHeight(ndx, 20)

    def btnNewVersion_clicked(self):
        if len(self.listModelParam) > 0 and self.versionModifyMode == False:
            self.btnBrowseInitialFile.setEnabled(False)
            self.buttonVersionSettings.setEnabled(False)
            self.listBatchFile.append("")
            self.cmbParameterFile.setCurrentIndex(-1)
            self.ckbShowVersion.setChecked(True)
            self.ckbShowRefValue.setChecked(False)
            # self.btnClear_clicked()
            self.tabWidgetParameter.setCurrentIndex(0)

            modelParam = self.listModelParam[self.currentVersionIndex]
            modelParam.resetAllUpdateFlag()
            newModelParam = copy.deepcopy(modelParam)
            newModelParam.fileNameChangeFlag = True

            self.listModelParam.append(newModelParam)

            self.currentVersionIndex = len(self.listModelParam) - 1
            currentVersion = int(self.txtStartingVersionNo.text()) + self.currentVersionIndex
            self.txtVersionNo.setText(str(currentVersion).rjust(2, "0"))

            versionText = self.txtVersionNo.text()
            outputPrefix = newModelParam.initParam.output_file_prefix

            if self.flag_addVersionNoAtTheEndOfFiles:
                outputPrefix = outputPrefix + "_" + versionText
            else:
                temp = outputPrefix[-2:]
                print(temp, versionText)
                if temp.isnumeric():
                   outputPrefix = outputPrefix[:-2] + versionText
                else:
                    outputPrefix = outputPrefix + "_" + versionText
            newModelParam.initParam.output_file_prefix = outputPrefix



            initFileName = self.listInitFileName[0]
            if self.currentVersionIndex > 0:
                versionText = self.txtVersionNo.text()

                if self.flag_addVersionNoAtTheEndOfFiles:
                    initFileName = initFileName.replace(".", "_" + versionText + ".")
                else:
                    temp = initFileName.replace(".ini", "")[-2:]
                    if temp.isnumeric():
                        temp += ".ini"
                        initFileName = initFileName.replace(temp, versionText + ".ini")
                    else:
                        initFileName = initFileName.replace(".", "_" + versionText + ".")
            self.listInitFileName.append(initFileName)

            #update file name links inside new version
            # self.updateLinkedFileName()
            self.findLinkedFile(self.currentVersionIndex)

            self.versionModifyMode = True
            self.btnClose.setText("Abort")

            self.btnLoadVersion.setEnabled(False)
            self.btnNewVersion.setEnabled(False)
            self.btnModify.setEnabled(True)

            #update graph configuration [increase version index by 1]
            if self.graph_configuration.number_of_graphs() > 0:
                for g in self.graph_configuration.list_of_changing_graph:
                    for p in g.edit_plot_list:
                        for i in range(len(p.init_version_list)):
                            p.init_version_list[i] += 1
            self.comboGraphName.setCurrentIndex(-1)


    def btnModify_clicked(self):
        if True: # This check will be removed. Previously it was ..(self.versionModifyMode == True:)
            ndx = self.tableParameterFile.currentRow()
            if ndx > -1:
                #____following two variables are required to change the file names
                versionText = self.txtVersionNo.text()
                tailReplacement = not self.flag_addVersionNoAtTheEndOfFiles
                #____


                cat = self.tableParameterFile.item(ndx, 0).text()
                if cat == "Initial Parameter":
                    tempInit = self.listModelParam[self.currentVersionIndex].initParam
                    self.initform = FormInitialAndOutputSetting()
                    self.initform.editMode = True
                    self.initform.initParam = tempInit
                    self.initform.frame_2.setDisabled(True)
                    self.initform.groupBoxInitFile.setDisabled(True)
                    self.initform.writeParamValuesOnFormComponent()
                    self.initform.btnSave.setText("Update")
                    self.parent.mdiArea.addSubWindow(self.initform.form)
                    self.initform.form.show()


                elif cat == "GIS Parameter":
                    modelParam = self.listModelParam[self.currentVersionIndex]
                    tempGis = modelParam.gisParam
                    if not modelParam.updateFlag_gis:
                        modelParam.updateGisfilename(versionText, tailReplacement)
                        self.findLinkedFile(self.currentVersionIndex)

                    self.gisform = FormGisFile()
                    self.gisform.editMode = True
                    for gis in tempGis:
                        self.gisform.siteList.append(gis["gis"])
                    self.gisform.showSiteListInTable()
                    self.gisform.tableWidget.setCurrentCell(0,0)
                    self.gisform.frame_2.setEnabled(False)
                    self.gisform.frame_2.setEnabled(False)
                    self.gisform.btnAddRow.setEnabled(False)
                    self.gisform.btnSaveAs.setVisible(False)
                    self.gisform.btnSave.setEnabled(True)
                    self.gisform.btnSave.setText("Update")
                    self.gisform.lockFields(False)
                    self.gisform.txtSiteIndex.setEnabled(False)
                    self.parent.mdiArea.addSubWindow(self.gisform.form)
                    self.gisform.form.show()
                elif cat == "VEG Parameter":
                    modelParam = self.listModelParam[self.currentVersionIndex]
                    tempVeg = modelParam.vegParam
                    if not modelParam.updateFlag_veg:
                        modelParam.updateVegFilename(versionText, tailReplacement)
                        self.findLinkedFile(self.currentVersionIndex)

                    self.vegform = FormVegFile()
                    self.vegform.editMode = True
                    for veg in tempVeg:
                        self.vegform.vegList.append(veg["veg"])
                    self.vegform.addVegListInTable()
                    self.vegform.tableWidget.setCurrentCell(0,0)
                    self.vegform.lockField(False)
                    self.vegform.txtSiteIndex.setEnabled(False)
                    self.vegform.txtVegNumber.setEnabled(False)
                    self.vegform.frame_2.setEnabled(False)
                    self.vegform.frameVegFile.setEnabled(False)
                    self.vegform.btnAddNew.setEnabled(False)
                    self.vegform.btnSaveAs.setVisible(False)
                    self.vegform.btnSave.setEnabled(True)
                    self.vegform.btnSave.setText("Update")
                    self.parent.mdiArea.addSubWindow(self.vegform.form)
                    self.vegform.form.show()
                elif cat == "EPC Parameter":
                    epcFileName = self.tableParameterFile.item(ndx, 1).text()
                    modelParam = self.listModelParam[self.currentVersionIndex]
                    tempEpc = modelParam.findEpcObject_filename(epcFileName)

                    temp = modelParam.findEpcSiteIndexAndVegid_filename(epcFileName)
                    siteIndex = temp["siteIndex"]
                    vegid = temp["vegid"]
                    # modelParam.updateEpcFilename(siteIndex, vegid, versionText, tailReplacement)
                    # modelParam.updateVegFilename(versionText, tailReplacement)
                    # self.findLinkedFile(self.currentVersionIndex)

                    if tempEpc is not None:
                        self.epcform = FormEpcFile()
                        self.epcform.frame_2.setEnabled(False)
                        self.epcform.frameEpcFile.setEnabled(False)
                        self.epcform.btnSave.setVisible(False)
                        self.epcform.btnSaveAs.setVisible(False)
                        self.epcform.modelParam = modelParam
                        self.epcform.siteIndex = siteIndex
                        self.epcform.vegId = vegid
                        self.epcform.versionText = versionText
                        self.epcform.tailReplace = tailReplacement
                        self.epcform.epc = tempEpc
                        self.epcform.setEpcValueInTable()
                        self.parent.mdiArea.addSubWindow(self.epcform.form)
                        self.epcform.form.show()

                    # self.cmbParameterFile_currentIndexChanged()
                elif cat in ["Soil Profile","Soil Horizon"]:
                    modelParam = self.listModelParam[self.currentVersionIndex]
                    soilProfileList = modelParam.getSoilProfileList()
                    modelParam.updateFlag_soil = True
                    modelParam.updateGisfilename(versionText, tailReplacement)
                    self.findLinkedFile(self.currentVersionIndex)

                    profileFile = "No Profile File"
                    fileList = modelParam.getSoilProfileFilenames()
                    if len(fileList) == 1: profileFile = fileList[0]
                    elif len(fileList) > 1: profileFile = "Multiple Files"

                    horizonFile = "No Horizon File"
                    fileList = modelParam.getSoilHorizonFilenames()
                    if len(fileList) == 1: horizonFile = fileList[0]
                    elif len(fileList) > 1: horizonFile = "Multiple Files"

                    self.soilform = FormSoilProfile()
                    #soil form components
                    self.soilform.rbtNew.setVisible(False)
                    self.soilform.rbtUpdate.setVisible(False)
                    self.soilform.btnBrowseProfileFile.setVisible(False)
                    self.soilform.btnBrowseHorizonFile.setVisible(False)
                    self.soilform.btnSave.setVisible(False)
                    self.soilform.btnSaveAs.setVisible(False)

                    self.soilform.txtProfileFileName.setText(profileFile)
                    self.soilform.txtHorizonFileName.setText(horizonFile)

                    self.soilform.btnDeleteProfile.setEnabled(True)
                    self.soilform.btnAddProfile.setEnabled(True)
                    self.soilform.btnDeleteLayer.setEnabled(True)
                    self.soilform.btnAddLayer.setEnabled(True)
                    self.soilform.btnCopyAndAdd.setEnabled(True)

                    self.soilform.txtProfileName.setReadOnly(False)
                    self.soilform.txtProfileFileName.setReadOnly(True)
                    self.soilform.txtHorizonFileName.setReadOnly(True)

                    self.soilform.listOfSoilProfile = soilProfileList
                    # self.soilform.flag_modification = True
                    self.soilform.showProfileData()
                    self.soilform.form.setWindowModality(QtCore.Qt.ApplicationModal)
                    self.parent.mdiArea.addSubWindow(self.soilform.form)
                    self.soilform.form.show()


                else:
                    QtGui.QMessageBox.about(self.form, "Not Modifiable!", "This file cannot be modified.")

    def updateLinkedFileName(self):
        modelParam = self.listModelParam[self.currentVersionIndex]
        versionText = self.txtVersionNo.text()

        #updating epc file name(s) in veg file
        for epc in modelParam.epcParam:
            epcid = epc["epcid"]

            #reading epc file name
            epcFileName = ""
            for ve in self.listModelParam[0].vegEpc:
                if ve["epcid"] == epcid:
                    siteIndex = ve["siteIndex"]
                    for veg in self.listModelParam[0].vegParam:
                        if veg["siteIndex"] == siteIndex:
                            epcFileName = veg["veg"].epcFileName
                            break
                    break

            if self.flag_addVersionNoAtTheEndOfFiles:
                epcFileName = epcFileName.replace(".", "_" + versionText + ".")
            else:
                temp = epcFileName.replace(".epc", "").split("_")[-1]
                if len(temp) > 0:
                    temp += ".epc"
                    epcFileName = epcFileName.replace(temp, versionText + ".epc")
                else:
                    epcFileName = epcFileName.replace(".", "_" + versionText + ".")


            #updating epcFileName in veg file rows
            for ve in modelParam.vegEpc:
                if ve["epcid"] == epcid:
                    siteIndex = ve["siteIndex"]
                    for veg in modelParam.vegParam:
                        if veg["siteIndex"] == siteIndex:
                            veg["veg"].epcFileName = epcFileName
                            break

        #updatign soil file names
        for gis in modelParam.gisParam:
            profileFileName = ""
            horizonFileName = ""
            siteIndex = gis["siteIndex"]

            for g in self.listModelParam[0].gisParam:
                if g["siteIndex"] == siteIndex:
                    profileFileName = g["gis"].soilProfileFileName
                    horizonFileName = g["gis"].soilHorizonFileName
                    break

            if self.flag_addVersionNoAtTheEndOfFiles:
                profileFileName = profileFileName.replace(".txt", "_" + versionText + ".txt")
                horizonFileName = horizonFileName.replace(".txt", "_" + versionText + ".txt")
            else:
                temp = profileFileName.replace(".txt", "").split("_")[-1]
                if len(temp) > 0:
                    temp += ".txt"
                    profileFileName = profileFileName.replace(temp, versionText + ".txt")
                else:
                    profileFileName = profileFileName.replace(".txt", "_" + versionText + ".txt")

                temp = horizonFileName.replace(".txt", "").split("_")[-1]
                if len(temp) > 0:
                    temp += ".txt"
                    horizonFileName = horizonFileName.replace(temp, versionText + ".txt")
                else:
                    horizonFileName = horizonFileName.replace(".txt", "_" + versionText + ".txt")

            gis["gis"].soilProfileFileName = profileFileName
            gis["gis"].soilHorizonFileName = horizonFileName

        #updating veg file name in init file and saving veg file
        vegFileName = self.listModelParam[0].initParam.veg_file_name
        if self.flag_addVersionNoAtTheEndOfFiles:
            vegFileName = vegFileName.replace(".", "_" + versionText + ".")
        else:
            temp = vegFileName.replace(".txt", "").split("_")[-1]
            if len(temp) > 0:
                temp += ".txt"
                vegFileName = vegFileName.replace(temp, versionText + ".txt")
            else:
                vegFileName = vegFileName.replace(".", "_" + versionText + ".")
        modelParam.initParam.veg_file_name = vegFileName

        #updating gis file name in init file
        gisFileName = self.listModelParam[0].initParam.gis_file_name
        if self.flag_addVersionNoAtTheEndOfFiles:
            gisFileName = gisFileName.replace(".", "_" + versionText + ".")
        else:
            temp = gisFileName.replace(".txt", "").split("_")[-1]
            if len(temp) > 0:
                temp += ".txt"
                gisFileName = gisFileName.replace(temp, versionText + ".txt")
            else:
                gisFileName = gisFileName.replace(".", "_" + versionText + ".")
        modelParam.initParam.gis_file_name = gisFileName

        #update output file prefix
        outputFilePrefix = self.listModelParam[0].initParam.output_file_prefix
        if self.flag_addVersionNoAtTheEndOfFiles:
            outputFilePrefix = outputFilePrefix + "_" + versionText
        else:
            temp = outputFilePrefix[:-3] + "_" + versionText
            outputFilePrefix = temp

        modelParam.initParam.output_file_prefix = outputFilePrefix


    # def btnView_clicked(self):
    #     ndx = self.tableParameterFile.currentRow()
    #     if ndx > -1:
    #         cat = self.tableParameterFile.item(ndx, 0).text()
    #         if cat == "Initial Parameter":
    #             tempInit = copy.deepcopy(self.listModelParam[self.currentVersionIndex].initParam)
    #             self.initform = FormInitialAndOutputSetting()
    #             self.initform.modelParam = tempInit
    #             self.initform.frame.setDisabled(True)
    #             self.initform.groupBoxInitFile.setDisabled(True)
    #             self.initform.writeParamValuesOnFormComponent()
    #             self.initform.lockInputComponent(True)
    #             self.initform.btnSave.setVisible(False)
    #             self.initform.form.show()
    #
    #         elif cat == "GIS Parameter":
    #             tempGis = self.listModelParam[self.currentVersionIndex].gisParam
    #             self.gisform = FormGisFile()
    #             for gis in tempGis:
    #                 self.gisform.siteList.append(copy.deepcopy(gis["gis"]))
    #             self.gisform.showSiteListInTable()
    #             self.gisform.tableWidget.setCurrentCell(0,0)
    #             self.gisform.frame.setEnabled(False)
    #             self.gisform.frame_2.setEnabled(False)
    #             self.gisform.btnAddRow.setEnabled(False)
    #             self.gisform.btnSaveAs.setVisible(False)
    #             self.gisform.btnSave.setVisible(False)
    #             self.gisform.form.show()
    #         elif cat == "VEG Parameter":
    #             tempVeg = self.listModelParam[self.currentVersionIndex].vegParam
    #             self.vegform = FormVegFile()
    #             for veg in tempVeg:
    #                 self.vegform.vegList.append(copy.deepcopy(veg["veg"]))
    #             self.vegform.addVegListInTable()
    #             self.vegform.tableWidget.setCurrentCell(0,0)
    #             self.vegform.frame.setEnabled(False)
    #             self.vegform.frameVegFile.setEnabled(False)
    #             self.vegform.btnAddNew.setEnabled(False)
    #             self.vegform.btnSaveAs.setVisible(False)
    #             self.vegform.btnSave.setVisible(False)
    #             self.vegform.form.show()
    #         elif cat == "EPC Parameter":
    #             epcFileName = self.tableParameterFile.item(ndx, 1).text()
    #             siteIndex = ""
    #             for veg in self.listModelParam[self.currentVersionIndex].vegParam:
    #                 if veg["veg"].epcFileName == epcFileName:
    #                     siteIndex = veg["siteIndex"]
    #                     break
    #             epcid = -1
    #             for ve in self.listModelParam[self.currentVersionIndex].vegEpc:
    #                 if ve["siteIndex"] == siteIndex:
    #                     epcid = ve["epcid"]
    #                     break
    #             tempEpc = None
    #             for epc in self.listModelParam[self.currentVersionIndex].epcParam:
    #                 if epc["epcid"] == epcid:
    #                     tempEpc = copy.deepcopy(epc["epc"])
    #
    #             self.epcform = FormEpcFile()
    #             self.epcform.frame.setEnabled(False)
    #             self.epcform.frameEpcFile.setEnabled(False)
    #             self.epcform.btnSave.setVisible(False)
    #             self.epcform.btnSaveAs.setVisible(False)
    #             self.epcform.epc = tempEpc
    #             self.epcform.setEpcValueInTable()
    #             self.epcform.tableParam.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    #             self.epcform.form.show()
    #         else:
    #             QtGui.QMessageBox.about(self.form, "Not Complete!", "This file cannot be shown.")

    def checkCompleteness(self):
        if len(self.txtInitialFile.text().strip()) == 0:
            message = "Please choose an initial file."
            QtGui.QMessageBox.about(self.form, "Input Required", message)
            self.btnBrowseInitialFile.setFocus(True)
            return False
        else:
            return True

    def btnRun_clicked(self):
        if not self.versionModifyMode and len(self.listModelParam) > 0:
            if len(self.txtModelProgram.text().strip()) == 0:
                message = "Please choose the model program."
                QtGui.QMessageBox.about(self.form, "Model Program Needed", message)
                self.txtModelProgram.setFocus(True)
                return False
            else:
                command_line_text = ""

                if sys.platform == "linux" or sys.platform == "linux2":
                    hash_file = os.path.join(ApplicationProperty.currentModelDirectory, "bgc_zalf.sh")
                    if os.path.exists(hash_file):
                        command_line_text = " nohup ./bgc_zalf.sh " + self.listInitFileName[self.currentVersionIndex] + ' \r'
                    else:
                        message = "A hash file is required. Please create a hash file manually"
                        QtGui.QMessageBox.about(self.form, "Hash file needed", message)
                        return False
                elif sys.platform == "win32":
                    batch_file = os.path.join(ApplicationProperty.currentModelDirectory, "bgc_zalf.bat")
                    if os.path.exists(batch_file):
                        command_line_text = "bgc_zalf.bat ini/" + self.listInitFileName[self.currentVersionIndex] + ' \r'
                    else:
                        message = "A batch file is required. Please create a batch file manually"
                        QtGui.QMessageBox.about(self.form, "Batch file needed", message)
                        return False

                if command_line_text:
                    try:
                        p = subprocess.Popen(command_line_text, shell=True, cwd=ApplicationProperty.currentModelDirectory ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                        log_success = True
                        log_file = os.path.join(ApplicationProperty.currentModelDirectory, "log.txt")

                        f = None
                        try:
                            f = open(log_file, 'w')

                            for line in p.stdout.readlines():
                                lineText = str(line)[2:-1].replace("\\n", "\n").replace("\\r", "\n").replace("\\t", "\t")
                                lineText = lineText.replace("\\\\", "\\") #+ "\n"
                                f.write(lineText)
                        except: log_success = False
                        finally:
                            try: f.close()
                            except: pass

                        if log_success:
                            reply = QtGui.QMessageBox.question(self.form, 'View Log', "Do you want to open the log file?", QtGui.QMessageBox.Yes,
                                                                QtGui.QMessageBox.No)
                            if reply == QtGui.QMessageBox.Yes:
                                self.dialog_show_log = DialogLogShow()
                                self.dialog_show_log.show_log_file(log_file)
                                self.dialog_show_log.form.show()
                    except Exception as ex:
                        message = "Following error occured: " + str(ex.args)
                        QtGui.QMessageBox.about(self.form, "Input Required", message)
        else:
            QtGui.QMessageBox.about(self.form, "Version Not Saved", "Please save the current version first.")

    def clearTableParameterView(self):
        #deleting all rows
        for i in reversed(range(self.tableParameterView.rowCount())):
            self.tableParameterView.removeRow(i)
        #deleting all columns
        for i in reversed(range(self.tableParameterView.columnCount())):
            self.tableParameterView.removeColumn(i)

    def cmbParameterFile_currentIndexChanged(self):
        """
        when one item (type of the parameter file) will be selected, parameter list from the selected type
        will be shown inside the table. If the check box, "show all version", is checked all values in all
        all version will be shown; otherwise the current version data will be shown.
        For some types (e.g., epc, veg), it is possible to have multiple files under a single version, in
        such case data from different files will be shown in separate columns under the same version. The
        title of the column will be, in such cases, like 'ver-00 (file-1)'.
        """
        paramType = self.cmbParameterFile.currentText()
        if self.ckbShowRefValue.isChecked(): self.ckbShowRefValue.setChecked(False)
        if len(paramType) > 0 and len(self.txtStartingVersionNo.text()) > 0:
            self.clearTableParameterView()

            paramList = []          #structure: [["parameter", [valueForVersion1, valueForVersion2,...]], [ , []]]
            headerText = []
            headerText.append("Parameter")
            startVersion = int(self.txtStartingVersionNo.text())
            editableColumns = 0     #number of editable columns
            if paramType == "Initial Parameter":
                self.ckbShowRefValue.setEnabled(False)
                if self.ckbShowVersion.isChecked():
                    for i in range(len(self.listModelParam)):
                        if i == 0:
                            valueList = self.listModelParam[i].initParam.showParameterValue()
                            for j in range(len(valueList)):
                                paramList.append([valueList[j]["pname"], [valueList[j]["pvalue"]]])
                        else:
                            valueList = self.listModelParam[i].initParam.showParameterValue()
                            for j in range(len(valueList)):
                                paramList[j][1].append(valueList[j]["pvalue"])

                        versionText = "Ver-" + str(startVersion + i).rjust(2, "0")
                        headerText.append(versionText)
                else:
                    valueList = self.listModelParam[self.currentVersionIndex].initParam.showParameterValue()
                    for j in range(len(valueList)):
                        paramList.append([valueList[j]["pname"], [valueList[j]["pvalue"]]])

                    versionText = "Ver-" + str(startVersion + self.currentVersionIndex).rjust(2, "0")
                    headerText.append(versionText)

                #editable column fixing
                if self.currentVersionIndex == len(self.listModelParam) - 1:
                    editableColumns = 1
            elif paramType == "GIS Parameter":
                self.ckbShowRefValue.setEnabled(False)
                if self.ckbShowVersion.isChecked():
                    for i in range(len(self.listModelParam)):
                        gisParam = self.listModelParam[i].gisParam
                        versionText = "Ver-" + str(startVersion + i).rjust(2, "0")
                        for gis in gisParam:
                            headerText.append(versionText + " (" + gis["siteIndex"] + ")")

                            if len(paramList) == 0:
                                valueList = gis["gis"].showParameterValue()
                                for j in range(len(valueList)):
                                    paramList.append([valueList[j]["pname"], [valueList[j]["pvalue"]]])
                            else:
                                valueList = gis["gis"].showParameterValue()
                                for j in range(len(valueList)):
                                    paramList[j][1].append(valueList[j]["pvalue"])
                else:
                    gisParam = self.listModelParam[self.currentVersionIndex].gisParam
                    versionText = "Ver-" + str(startVersion + self.currentVersionIndex).rjust(2, "0")
                    for gis in gisParam:
                        headerText.append(versionText + " (" + gis["siteIndex"] + ")")

                        if len(paramList) == 0:
                            valueList = gis["gis"].showParameterValue()
                            for j in range(len(valueList)):
                                paramList.append([valueList[j]["pname"], [valueList[j]["pvalue"]]])
                        else:
                            valueList = gis["gis"].showParameterValue()
                            for j in range(len(valueList)):
                                paramList[j][1].append(valueList[j]["pvalue"])

                if self.currentVersionIndex == len(self.listModelParam) - 1:
                    editableColumns = len(self.listModelParam[self.currentVersionIndex].gisParam)

            elif paramType == "Veg Parameter":
                self.ckbShowRefValue.setEnabled(False)
                if self.ckbShowVersion.isChecked():
                    for i in range(len(self.listModelParam)):
                        vegParam = self.listModelParam[i].vegParam
                        versionText = "Ver-" + str(startVersion + i).rjust(2, "0")
                        for veg in vegParam:
                            headerText.append(versionText + " (" + veg["siteIndex"] + ":" + str(veg["veg"].vegetationNumber) + ")")

                            if len(paramList) == 0:
                                valueList = veg["veg"].showParameterValue()
                                for j in range(len(valueList)):
                                    paramList.append([valueList[j]["pname"], [valueList[j]["pvalue"]]])
                            else:
                                valueList = veg["veg"].showParameterValue()
                                for j in range(len(valueList)):
                                    paramList[j][1].append(valueList[j]["pvalue"])
                else:
                    vegParam = self.listModelParam[self.currentVersionIndex].vegParam
                    versionText = "Ver-" + str(startVersion + self.currentVersionIndex).rjust(2, "0")
                    for veg in vegParam:
                        headerText.append(versionText + " (" + veg["siteIndex"] + ":" + str(veg["veg"].vegetationNumber) + ")")

                        if len(paramList) == 0:
                            valueList = veg["veg"].showParameterValue()
                            for j in range(len(valueList)):
                                paramList.append([valueList[j]["pname"], [valueList[j]["pvalue"]]])
                        else:
                            valueList = veg["veg"].showParameterValue()
                            for j in range(len(valueList)):
                                paramList[j][1].append(valueList[j]["pvalue"])

                if self.currentVersionIndex == len(self.listModelParam) - 1:
                    editableColumns = len(self.listModelParam[self.currentVersionIndex].vegParam)

            elif paramType == "Epc Parameter":
                self.ckbShowRefValue.setEnabled(True)
                if self.ckbShowVersion.isChecked():
                    for i in range(len(self.listModelParam)):
                        epcParam = self.listModelParam[i].epcParam
                        vegEpc = self.listModelParam[i].vegEpc

                        versionText = "Ver-" + str(startVersion + i).rjust(2, "0")
                        for epc in epcParam:
                            epcid = epc["epcid"]

                            siteIndex = ""
                            vegid = -1
                            for ve in vegEpc:
                                if ve["epcid"] == epcid:
                                    siteIndex = ve["siteIndex"]
                                    vegid = ve["vegid"]
                                    break

                            headerText.append(versionText + " (" + siteIndex + ":" + str(vegid) + ")")
                            if len(paramList) == 0:
                                valueList = epc["epc"].showParameterValue()
                                for j in range(len(valueList)):
                                    paramList.append([valueList[j]["pname"], [valueList[j]["pvalue"]]])
                            else:
                                valueList = epc["epc"].showParameterValue()
                                for j in range(len(valueList)):
                                    paramList[j][1].append(valueList[j]["pvalue"])
                else:
                    epcParam = self.listModelParam[self.currentVersionIndex].epcParam
                    vegEpc = self.listModelParam[self.currentVersionIndex].vegEpc
                    versionText = "Ver-" + str(startVersion + self.currentVersionIndex).rjust(2, "0")
                    for epc in epcParam:
                        epcid = epc["epcid"]

                        siteIndex = ""
                        vegid = -1
                        for ve in vegEpc:
                            if ve["epcid"] == epcid:
                                siteIndex = ve["siteIndex"]
                                vegid = ve["vegid"]
                                break

                        headerText.append(versionText + " (" + siteIndex + ":" + str(vegid) + ")")
                        if len(paramList) == 0:
                            valueList = epc["epc"].showParameterValue()
                            for j in range(len(valueList)):
                                paramList.append([valueList[j]["pname"], [valueList[j]["pvalue"]]])
                        else:
                            valueList = epc["epc"].showParameterValue()
                            for j in range(len(valueList)):
                                paramList[j][1].append(valueList[j]["pvalue"])

                if self.currentVersionIndex == len(self.listModelParam) - 1:
                    editableColumns = len(self.listModelParam[self.currentVersionIndex].epcParam)
            elif paramType == "Soil Parameter":
                self.ckbShowRefValue.setEnabled(False)
                # self.tableParameterView.insertRow(self.tableParameterFile.rowCount())
                # verticalHeaderItem = QtWidgets.QTableWidgetItem("ver-00")
                # verticalHeaderItem.setTextAlignment()

                self.tableParameterView.setColumnCount(18)
                header = ["Site Index", "Profile Name", "Horizon Name", "Lower Horizon Border", "Layer Thickness",
                          "Correction Factor", "Texture", "pH", "C-org (M%)", "Gravel (Vol.%)", "Sand (M.%)",
                          "Silt (M.%)", "Clay (M.%)", "BD (g/cm³)", "PV (Vol.%)", "FC Vol.%", "PWP Vol.%", "KS (cm/d)"]
                self.tableParameterView.insertRow(self.tableParameterFile.rowCount())
                self.tableParameterView.setHorizontalHeaderLabels(header)

                if self.ckbShowVersion.isChecked():
                    for i in reversed(range(len(self.listModelParam))):
                        rowIndex = self.tableParameterView.rowCount()
                        self.tableParameterView.insertRow(rowIndex)
                        self.tableParameterView.setRowHeight(rowIndex, 20)

                        cell = QtWidgets.QTableWidgetItem("Version - " + str(i + startVersion).rjust(2, "0"))
                        font =  QtGui.QFont()
                        font.setBold(True)
                        font.setPointSize(9)
                        cell.setFont(font)
                        color = QtGui.QColor(216,191,216)
                        cell.setBackgroundColor(color)
                        cell.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterView.setItem(rowIndex, 0, cell)

                        for j in range(1, 18):
                            cell = QtWidgets.QTableWidgetItem("")
                            cell.setBackgroundColor(color)
                            cell.setFlags(QtCore.Qt.ItemIsEnabled)
                            self.tableParameterView.setItem(rowIndex, j, cell)

                        modelParam = self.listModelParam[i]
                        if i == len(self.listModelParam) - 1: self.showSoilDataInParameterViewTable(modelParam, True)
                        else: self.showSoilDataInParameterViewTable(modelParam, False)
                else:
                    modelParam = self.listModelParam[self.currentVersionIndex]
                    if self.currentVersionIndex == len(self.listModelParam) -1:
                        self.showSoilDataInParameterViewTable(modelParam, True)
                    else: self.showSoilDataInParameterViewTable(modelParam, False)

            if len(paramList) > 0:
                columnCount = len(paramList[0][1]) + 1
                self.tableParameterView.setColumnCount(columnCount)
                #seting column width
                for i in range(columnCount):
                    if i == 0: self.tableParameterView.setColumnWidth(i, 170)
                    else: self.tableParameterView.setColumnWidth(i, 150)
                #setting column header
                for i in range(columnCount):
                    cell = QtWidgets.QTableWidgetItem(headerText[i])
                    self.tableParameterView.setHorizontalHeaderItem(i, cell)

                for item in paramList:
                    hasDomain = False
                    domain = []
                    if paramType.lower() == "initial parameter":
                        hasDomain = InitialParameter.hasDomain(item[0])
                        if hasDomain: domain = InitialParameter.getDomain(item[0])
                    elif paramType.lower() == "gis parameter":
                        hasDomain = GisParameter.hasDomain(item[0])
                        if hasDomain: domain = GisParameter.getDomain(item[0])
                    elif paramType.lower() == "veg parameter":
                        hasDomain = VegetationParameter.hasDomain(item[0])
                        if hasDomain: domain = VegetationParameter.getDomain(item[0])
                    elif paramType.lower() == "epc parameter":
                        hasDomain = EpcParameter.hasDomain(item[0])
                        if hasDomain: domain = EpcParameter.getDomain(item[0])

                    ndx = self.tableParameterView.rowCount()
                    self.tableParameterView.insertRow(ndx)
                    cell = QtWidgets.QTableWidgetItem(item[0])
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(ndx, 0, cell)

                    itemLen = len(item[1])
                    for i in range(itemLen):
                        if hasDomain:
                            comboCell = QtGui.QComboBox()
                            comboCell.currentIndexChanged.connect(self.signalMapper.map)
                            comboCell.addItems(domain)
                            comboCell.setCurrentIndex(int(item[1][i]))
                            if i < (itemLen - editableColumns): comboCell.setEnabled(False)
                            self.tableParameterView.setCellWidget(ndx, i + 1, comboCell)
                            comboCell.row = ndx
                            comboCell.column = i + 1
                            self.signalMapper.setMapping(comboCell, comboCell)
                        else:
                            cell = QtWidgets.QTableWidgetItem(str(item[1][i]))
                            if i < (itemLen - editableColumns): cell.setFlags(QtCore.Qt.ItemIsEnabled)
                            self.tableParameterView.setItem(ndx, i + 1, cell)

                    self.tableParameterView.setRowHeight(ndx, 20)
            if self.tableParameterView.rowCount()> 0:
                item = self.tableParameterView.item(0,0)
                item.setSelected(True)
                # item.setCheckState(Qt.Checked)
                # self.tableParameterView.setItemSelected(self.tableParameterView.item(0,0), True)
        else:
            self.clearTableParameterView()
            self.ckbShowVersion.setChecked(True)
            self.ckbShowRefValue.setChecked(False)
            self.ckbShowRefValue.setEnabled(False)

    @QtCore.pyqtSlot(QtWidgets.QWidget)
    def dynamicCombo_indexChanged(self, comboCell):
        if comboCell.row > -1 and comboCell.column > -1:
            paramType = self.cmbParameterFile.currentText()

            #reading version no [for soil parameters the version no. has to read differently]
            verIndex = -1
            colIndex = comboCell.column
            headerText = self.tableParameterView.horizontalHeaderItem(colIndex).text()
            try: verIndex = int(headerText[4:6]) - int(self.txtStartingVersionNo.text())
            except: pass

            #reading site index [for soil parameters the version no. has to read differently]
            #and vegetation number (id) necessary only for vegetation and epc parameters
            #site index is required for all parameters types except initial control parameters
            siteIndex = ""
            vegid = -1
            if headerText.find("(") > -1:
                siteIndex = headerText[headerText.find("(") + 1: headerText.find(")")]
                if siteIndex.find(":") > -1:
                    vegid = int(siteIndex.split(":")[-1])
                    siteIndex = siteIndex.split(":")[0]

            #reading parameter name and parameter values [both are in text format]
            rowIndex = comboCell.row
            paramName = self.tableParameterView.item(rowIndex, 0).text()
            paramValue = comboCell.currentIndex()

            #variables required for changing filenames
            versionText = self.txtVersionNo.text()
            tailReplacement = not self.flag_addVersionNoAtTheEndOfFiles

            result = None
            if paramType == "Initial Parameter":
                if verIndex > -1:
                    result = self.listModelParam[verIndex].initParam.setParameterValue(paramName, paramValue)
            elif paramType == "GIS Parameter":
                if len(siteIndex) > 0:
                    result = self.listModelParam[verIndex].updateGisObject(siteIndex, paramName, paramValue, versionText, tailReplacement)
                    if paramName == "Site Index": self.cmbParameterFile_currentIndexChanged()
            elif paramType == "Veg Parameter":
                if len(siteIndex) > 0 and vegid > -1:
                    result = self.listModelParam[verIndex].updateVegObject(siteIndex, vegid, paramName, paramValue, versionText, tailReplacement)
                    if paramName in ["Site Index", "Vegetation No."]: self.cmbParameterFile_currentIndexChanged()
            elif paramType == "Epc Parameter":
                if len(siteIndex) > 0 and vegid > -1:
                    result = self.listModelParam[verIndex].updateEpcObject(siteIndex, vegid, rowIndex + 1, paramName,
                                                                              paramValue, versionText, tailReplacement)
            elif paramType == "Soil Parameter":
                verIndex = len(self.listModelParam) - 1
                modelParam = self.listModelParam[verIndex]

                #searching for the concerning profile
                siteIndex = self.tableParameterView.item(rowIndex, 0).text()
                for i in range(self.tableParameterView.rowCount()):
                    if self.tableParameterView.item(i, 0).text() == siteIndex: break
                layerIndex = rowIndex - i

                paramName = self.tableParameterView.horizontalHeaderItem(colIndex).text()
                result = modelParam.updateSoilProfile(siteIndex, paramName, paramValue, layerIndex, versionText, tailReplacement)
                # self.cmbParameterFile_currentIndexChanged()
                # item = self.tableParameterView.item(rowIndex, colIndex)
                # self.tableParameterView.setCurrentItem(item)

            if result is not None:
                # message = "Parameter value was not updated."
                comboCell.setCurrentIndex(int(result))
                # self.cmbParameterFile_currentIndexChanged()
            else:
                self.versionModifyMode = True
                if self.currentVersionIndex != len(self.listModelParam) - 1:
                    self.currentVersionIndex = len(self.listModelParam) - 1
                    startingVersion = int(self.txtStartingVersionNo.text())
                    self.txtVersionNo.setText(str(startingVersion + self.currentVersionIndex).rjust(2,"0"))
                self.findLinkedFile(self.currentVersionIndex)
                self.btnNewVersion.setEnabled(False)
                self.btnClose.setText("Abort")
                self.btnModify.setEnabled(True)
                self.btnLoadVersion.setEnabled(False)
                self.buttonVersionSettings.setEnabled(False)

    def showSoilDataInParameterViewTable(self, modelParam, editable):
        siteIndex = ""
        for soilObj in modelParam.soilParam:
            spfid = soilObj["spfid"]
            for gs in modelParam.gisSoil:
                if gs["spfid"] == spfid:
                    siteIndex = gs["siteIndex"]

            profileName = ""
            for gis in modelParam.gisParam:
                if gis["siteIndex"] == siteIndex:
                    profileName = gis["gis"].profileName
                    break

            profile = soilObj["sp"]

            # rowIndex = self.tableParameterView.rowCount()
            # self.tableParameterView.insertRow(rowIndex)
            # cell = QtWidgets.QTableWidgetItem(profile.profileName)
            # self.tableParameterView.setItem(rowIndex, 0, cell)
            # self.tableParameterView.setRowHeight(rowIndex, 20)

            for layer in profile.soilLayerList:
                rowIndex = self.tableParameterView.rowCount()
                self.tableParameterView.insertRow(rowIndex)
                self.tableParameterView.setRowHeight(rowIndex, 20)

                cell = QtWidgets.QTableWidgetItem(siteIndex)
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableParameterView.setItem(rowIndex, 0, cell)

                if editable:
                    cell = QtWidgets.QTableWidgetItem(profile.profileName)
                    self.tableParameterView.setItem(rowIndex, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.horizonName))
                    self.tableParameterView.setItem(rowIndex, 2, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.depthOfHorizon))
                    self.tableParameterView.setItem(rowIndex, 3, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.layerThickness))
                    self.tableParameterView.setItem(rowIndex, 4, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.correctionFactor))
                    self.tableParameterView.setItem(rowIndex, 5, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.soilTexture))
                    self.tableParameterView.setItem(rowIndex, 6, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.soilPh))
                    self.tableParameterView.setItem(rowIndex, 7, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.organicCarbonContent))
                    self.tableParameterView.setItem(rowIndex, 8, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.gravelContent))
                    self.tableParameterView.setItem(rowIndex, 9, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.sandContent))
                    self.tableParameterView.setItem(rowIndex, 10, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.siltContent))
                    self.tableParameterView.setItem(rowIndex, 11, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.clayContent))
                    self.tableParameterView.setItem(rowIndex, 12, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.bulkDensity))
                    self.tableParameterView.setItem(rowIndex, 13, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.poreVolume))
                    self.tableParameterView.setItem(rowIndex, 14, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.waterCapacity))
                    self.tableParameterView.setItem(rowIndex, 15, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.permanentWiltingPoint))
                    self.tableParameterView.setItem(rowIndex, 16, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.saturatedHydraulicConductivity))
                    self.tableParameterView.setItem(rowIndex, 17, cell)
                else:
                    cell = QtWidgets.QTableWidgetItem(profile.profileName)
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 1, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.horizonName))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 2, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.depthOfHorizon))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 3, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.layerThickness))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 4, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.correctionFactor))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 5, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.soilTexture))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 6, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.soilPh))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 7, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.organicCarbonContent))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 8, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.gravelContent))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 9, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.sandContent))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 10, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.siltContent))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 11, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.clayContent))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 12, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.bulkDensity))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 13, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.poreVolume))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 14, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.waterCapacity))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 15, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.permanentWiltingPoint))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 16, cell)
                    cell = QtWidgets.QTableWidgetItem(str(layer.saturatedHydraulicConductivity))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableParameterView.setItem(rowIndex, 17, cell)

    def btnModelProgramBrowse_clicked(self):
        initdir =  ApplicationProperty.currentModelDirectory
        if len(initdir) == 0: initdir = ApplicationProperty.getScriptPath()

        fileName = ""
        if sys.platform == "linux" or sys.platform == "linux2":
            fileName = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initdir)

            if fileName:
                executable_name = fileName.split("/")[-1]
                bash_file_name = fileName.replace(executable_name, "bgc_zalf.sh")
                self.txtModelProgram.setText(executable_name)
                if not FileReadWrite.write_bash_file_for_linux(bash_file_name, executable_name):
                    message = "Hash file could not be created. Please create a hash file manually to run the model."
                    QtGui.QMessageBox.about(self.form, "Hash file error", message)
                else: os.chmod(bash_file_name, 0o0744)
        elif sys.platform == "win32":
            fileName = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initdir, "Executable File (*.exe)")

            if fileName:
                executable_name = fileName.split("/")[-1]
                batch_file_name = fileName.replace(executable_name, "bgc_zalf.bat")
                self.txtModelProgram.setText(executable_name)
                if not FileReadWrite.write_batch_file_for_windows(batch_file_name, executable_name):
                    message = "Batch file could not be created. Please create a batch file manually to run the model."
                    QtGui.QMessageBox.about(self.form, "Batch file error", message)

    def btnClose_clicked(self):
        if self.btnClose.text() == "Abort":
            if self.currentVersionIndex > 0:
                self.listModelParam.pop(self.currentVersionIndex)
                self.listBatchFile.pop(self.currentVersionIndex)
                self.listInitFileName.pop(self.currentVersionIndex)
                self.versionModifyMode = False
                self.currentVersionIndex -= 1

                startVersionNumber = int(self.txtStartingVersionNo.text())
                self.txtVersionNo.setText(str(startVersionNumber + self.currentVersionIndex).rjust(2, "0"))
                self.btnBrowseInitialFile.setEnabled(True)

                self.findLinkedFile(self.currentVersionIndex)
                self.cmbParameterFile.setCurrentIndex(-1)
                self.ckbShowVersion.setChecked(True)
                self.ckbShowRefValue.setChecked(False)
                self.buttonVersionSettings.setEnabled(True)
                # self.btnClear_clicked()
                self.tabWidgetParameter.setCurrentIndex(0)

                if len(self.listModelParam) == 1: self.buttonVersionSettings.setEnabled(True)
                #self.btnModify.setEnabled(False)
                # else: self.btnModify.setEnabled(True)
                self.btnNewVersion.setEnabled(True)
                self.btnLoadVersion.setEnabled(True)

                self.txtVersionCompare.clear()
                self.clearTableParameterCompare()

                #update graph configuration [decrease version index by 1]
                if self.graph_configuration.number_of_graphs() > 0:
                    for g in self.graph_configuration.list_of_changing_graph:
                        for p in g.edit_plot_list:
                            for i in range(len(p.init_version_list)):
                                p.init_version_list[i] -= 1
                self.comboGraphName.setCurrentIndex(-1)
            else:
                self.btnBrowseInitialFile_clicked()         #check again
            self.btnClose.setText("Close")
        else:
            self.form.parentWidget().close()

    def btnCompare_clicked(self):
        self.clearTableParameterCompare()
        if len(self.listModelParam) > 1:
            #reading version numbers
            listVersion = []
            startingNumber = int(self.txtStartingVersionNo.text())
            maxVersionNumber = startingNumber + len(self.listModelParam)
            versionHeader = ["Parameter Name"]
            for v in self.txtVersionCompare.text().strip().split(","):
                try:
                    temp = int(v.strip())
                    if temp <= maxVersionNumber and temp >=startingNumber:
                        listVersion.append(temp - startingNumber)
                        versionHeader.append("Version-" + v.strip())
                except Exception as ex: pass
            if len(listVersion) > 1:
                # self.compareVersions2000(listVersion)
                listOfModelParam = []
                for v in listVersion:
                    listOfModelParam.append(self.listModelParam[v])
                self.compareVersions2000(listOfModelParam, versionHeader)
            else:
                message = "For version comparison at least two versions are required. Please enter two valid version Number."
                QtGui.QMessageBox.about(self.form, "Version Comparison", message)
        else:
            message = "No enough versions to compare."
            QtGui.QMessageBox.about(self.form, "Invalid Request", message)

    def compareVersions2000(self, listOfVersion, versionHeader):
        compResult = BiomeBGCParameterSet.versionComparison(listOfVersion, [0,1])
        self.clearTableParameterCompare()
        if len(compResult) > 0:
            versionCount = len(listOfVersion)
            self.tableParameterCompare.setColumnCount(versionCount + 1)
            self.tableParameterCompare.setHorizontalHeaderLabels(versionHeader)
            self.tableParameterCompare.setColumnWidth(0, 210)
            for i in range(1, self.tableParameterCompare.columnCount()):
                self.tableParameterCompare.setColumnWidth(i, 150)
            for resultItem in compResult:
                groupName = resultItem[0]
                rowIndex = self.tableParameterCompare.rowCount()
                self.tableParameterCompare.insertRow(rowIndex)
                self.tableParameterCompare.setRowHeight(rowIndex, 22)
                cell = QtWidgets.QTableWidgetItem(groupName)
                cell.setBackgroundColor(QtGui.QColor(202, 236, 244))
                self.tableParameterCompare.setItem(rowIndex, 0, cell)
                cell = QtWidgets.QTableWidgetItem("")
                cell.setBackgroundColor(QtGui.QColor(202, 236, 244))
                self.tableParameterCompare.setItem(rowIndex, 1, cell)
                cell = QtWidgets.QTableWidgetItem("")
                cell.setBackgroundColor(QtGui.QColor(202, 236, 244))
                self.tableParameterCompare.setItem(rowIndex, 2, cell)

                for key, value in resultItem[1].items():
                    rowIndex = self.tableParameterCompare.rowCount()
                    self.tableParameterCompare.insertRow(rowIndex)
                    self.tableParameterCompare.setRowHeight(rowIndex, 22)
                    cell = QtWidgets.QTableWidgetItem(key)
                    self.tableParameterCompare.setItem(rowIndex, 0, cell)
                    for i in range(len(value)):
                        cell = QtWidgets.QTableWidgetItem(str(value[i]))
                        self.tableParameterCompare.setItem(rowIndex, i + 1, cell)

    def clearTableParameterCompare(self):
        #clearing previous rows and columns if any
        for i in reversed(range(self.tableParameterCompare.rowCount())):
            self.tableParameterCompare.removeRow(i)
        for i in reversed(range(self.tableParameterCompare.columnCount())):
            self.tableParameterCompare.removeColumn(i)

    def compareVersions(self, versionNoList):
        initParamList = []
        gisParamList = []
        vegParamList = []
        epcParamList = []

        for ver in versionNoList:
            initParamList.append(self.listModelParam[ver].initParam)

            for gis in self.listModelParam[ver].gisParam:
                gisParamList.append(gis["gis"])

            for veg in self.listModelParam[ver].vegParam:
                vegParamList.append(veg["veg"])

            for epc in self.listModelParam[ver].epcParam:
                epcParamList.append(epc["epc"])

        l = len(initParamList)
        if len(gisParamList) == l and len(vegParamList) == l and len(epcParamList) == l:
            #setting up table
            self.tableParameterCompare.setColumnCount(len(versionNoList) + 1)
            headerText = ["Parameter Name"]
            for ver in versionNoList:
                headerText.append("Version " + str(ver))
            self.tableParameterCompare.setHorizontalHeaderLabels(headerText)

            #comparing initial parameters
            compResult = InitialParameter.compare(initParamList)
            if len(compResult) > 0:
                ndx = self.tableParameterCompare.rowCount()
                self.tableParameterCompare.insertRow(ndx)
                self.tableParameterCompare.setRowHeight(ndx, 20)
                cell = QtWidgets.QTableWidgetItem("Initial Parameters")
                cell.setBackground(QtGui.QColor(216,191,216))
                self.tableParameterCompare.setItem(ndx, 0, cell)
                for i in range(l):
                    cell = QtWidgets.QTableWidgetItem("")
                    cell.setBackground(QtGui.QColor(216,191,216))
                    self.tableParameterCompare.setItem(ndx, i + 1, cell)

                for param, valueList in compResult.items():
                    ndx = self.tableParameterCompare.rowCount()
                    self.tableParameterCompare.insertRow(ndx)
                    self.tableParameterCompare.setRowHeight(ndx, 20)
                    cell = QtWidgets.QTableWidgetItem(param)
                    self.tableParameterCompare.setItem(ndx, 0, cell)

                    i = 1
                    for value in valueList:
                        cell = QtWidgets.QTableWidgetItem(str(value))
                        self.tableParameterCompare.setItem(ndx, i, cell)
                        i += 1

            #comparing gis parameters
            compResult = GisParameter.compare(gisParamList)
            if len(compResult) > 0:
                ndx = self.tableParameterCompare.rowCount()
                self.tableParameterCompare.insertRow(ndx)
                self.tableParameterCompare.setRowHeight(ndx, 20)
                cell = QtWidgets.QTableWidgetItem("GIS Parameters")
                cell.setBackground(QtGui.QColor(216,191,216))
                self.tableParameterCompare.setItem(ndx, 0, cell)
                for i in range(l):
                    cell = QtWidgets.QTableWidgetItem("")
                    cell.setBackground(QtGui.QColor(216,191,216))
                    self.tableParameterCompare.setItem(ndx, i + 1, cell)


                for param, valueList in compResult.items():
                    ndx = self.tableParameterCompare.rowCount()
                    self.tableParameterCompare.insertRow(ndx)
                    self.tableParameterCompare.setRowHeight(ndx, 20)
                    cell = QtWidgets.QTableWidgetItem(param)
                    self.tableParameterCompare.setItem(ndx, 0, cell)

                    i = 1
                    for value in valueList:
                        cell = QtWidgets.QTableWidgetItem(str(value))
                        self.tableParameterCompare.setItem(ndx, i, cell)
                        i += 1

            #comparing veg parameters
            compResult = VegetationParameter.compare(vegParamList)
            if len(compResult) > 0:
                ndx = self.tableParameterCompare.rowCount()
                self.tableParameterCompare.insertRow(ndx)
                self.tableParameterCompare.setRowHeight(ndx, 20)
                cell = QtWidgets.QTableWidgetItem("VEG Parameters")
                cell.setBackground(QtGui.QColor(216,191,216))
                self.tableParameterCompare.setItem(ndx, 0, cell)
                for i in range(l):
                    cell = QtWidgets.QTableWidgetItem("")
                    cell.setBackground(QtGui.QColor(216,191,216))
                    self.tableParameterCompare.setItem(ndx, i + 1, cell)


                for param, valueList in compResult.items():
                    ndx = self.tableParameterCompare.rowCount()
                    self.tableParameterCompare.insertRow(ndx)
                    self.tableParameterCompare.setRowHeight(ndx, 20)
                    cell = QtWidgets.QTableWidgetItem(param)
                    self.tableParameterCompare.setItem(ndx, 0, cell)

                    i = 1
                    for value in valueList:
                        cell = QtWidgets.QTableWidgetItem(str(value))
                        self.tableParameterCompare.setItem(ndx, i, cell)
                        i += 1

            #comparing epc parameters
            compResult = EpcParameter.compare(epcParamList)
            if len(compResult) > 0:
                ndx = self.tableParameterCompare.rowCount()
                self.tableParameterCompare.insertRow(ndx)
                self.tableParameterCompare.setRowHeight(ndx, 20)
                cell = QtWidgets.QTableWidgetItem("EPC Parameters")
                cell.setBackground(QtGui.QColor(216,191,216))
                self.tableParameterCompare.setItem(ndx, 0, cell)
                for i in range(l):
                    cell = QtWidgets.QTableWidgetItem("")
                    cell.setBackground(QtGui.QColor(216,191,216))
                    self.tableParameterCompare.setItem(ndx, i + 1, cell)

                    
                for param, valueList in compResult.items():
                    ndx = self.tableParameterCompare.rowCount()
                    self.tableParameterCompare.insertRow(ndx)
                    self.tableParameterCompare.setRowHeight(ndx, 20)
                    cell = QtWidgets.QTableWidgetItem(param)
                    self.tableParameterCompare.setItem(ndx, 0, cell)

                    i = 1
                    for value in valueList:
                        cell = QtWidgets.QTableWidgetItem(str(value))
                        self.tableParameterCompare.setItem(ndx, i, cell)
                        i += 1
        else:
            message = "This comparison is designed for single site vegetation. Files having multiple site info cannot be compared."
            QtGui.QMessageBox.about(self.form, "Invalid Request", message)

    # def btnClear_clicked(self):
    #     self.txtReferenceVersion.clear()
    #     self.txtComparingVersion.clear()
    #     for i in reversed(range(self.tableParameterCompare.rowCount())):
    #         self.tableParameterCompare.removeRow(i)
    #     for i in reversed(range(self.tableParameterCompare.columnCount())):
    #             self.tableParameterCompare.removeColumn(i)
    #     self.comparingVersionNoList = []

    def ckbShowRefValue_toggled(self):
        if self.ckbShowRefValue.isChecked() == True:
            temp = self.cmbParameterFile.currentText()
            color = QtGui.QColor(255, 242, 0)
            if temp == "Epc Parameter":
                epcList = FileReadWrite.readReferenceData("EPC Parameter")

                for epcItem in epcList:
                    colIndex = self.tableParameterView.columnCount()
                    self.tableParameterView.setColumnCount(colIndex + 1)
                    cell = QtWidgets.QTableWidgetItem(epcItem["name"])
                    self.tableParameterView.setHorizontalHeaderItem(colIndex, cell)
                    epc = epcItem["epc"]
                    for item in epc.showParameterValue():
                        for j in range(self.tableParameterView.rowCount()):
                            if self.tableParameterView.item(j, 0).text() == item["pname"]:
                                cell = QtWidgets.QTableWidgetItem(str(item["pvalue"][0]))
                                cell.setBackgroundColor(color)
                                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.tableParameterView.setItem(j, colIndex, cell)
                                break
        else:
            self.cmbParameterFile_currentIndexChanged()


    def btnSaveVersion_clicked(self):
        if self.versionModifyMode:
            if self.checkCompleteness() and len(ApplicationProperty.currentModelDirectory) > 0:
                modelParam = self.listModelParam[self.currentVersionIndex]
                modelDirectory = ApplicationProperty.currentModelDirectory

                versionSaveResult = True

                #saving epc file(s)
                updatedEpcFileList = modelParam.findUpdatedEpcFiles()
                if len(updatedEpcFileList) > 0:
                    for fileName in updatedEpcFileList:
                        epc = modelParam.findEpcObject_filename(fileName)

                        #saving epc file
                        epcFileName = modelDirectory + "/epc/" + fileName
                        versionSaveResult = FileReadWrite.writeEpcFile(epcFileName, epc)

                    if versionSaveResult: modelParam.resetEpcUpdateFlag()

                #saving veg file
                if versionSaveResult:
                    if modelParam.updateFlag_veg:
                        vegFileName = modelParam.initParam.veg_file_name

                        vegList = []
                        for veg in modelParam.vegParam:
                            vegList.append(veg["veg"])

                        versionSaveResult = FileReadWrite.writeVegFile(modelDirectory + "/" + vegFileName, vegList)

                        if versionSaveResult: modelParam.updateFlag_veg = False

                #saving soil files
                if versionSaveResult:
                    if modelParam.updateFlag_soil:
                        profileList = modelParam.getSoilProfileList()
                        profileFileName = ""
                        horizonFileName = ""

                        fileName = modelParam.getSoilProfileFilenames()
                        if len(fileName) == 1:
                            profileFileName = fileName[0]
                        elif len(fileName) > 1:
                            profileFileName = fileName[0].replace(".txt", "_" + self.txtVersionNo.text() + ".txt")
                            modelParam.updateSoilProfileAndHorizonFileNameInGISObjects(profileFilename=profileFileName)

                        fileName = modelParam.getSoilHorizonFilenames()
                        if len(fileName) == 1:
                            horizonFileName = fileName[0]
                        elif len(fileName) > 1:
                            horizonFileName = fileName[0].replace(".txt", "_" + self.txtVersionNo.text() + ".txt")
                            modelParam.updateSoilProfileAndHorizonFileNameInGISObjects(horizonFilename=horizonFileName)

                        if len(profileList) > 0 and len(profileFileName) > 0 and len(horizonFileName) > 0:
                            profileFileName = modelDirectory + "/soil/" + profileFileName
                            horizonFileName = modelDirectory + "/soil/" + horizonFileName
                            versionSaveResult = FileReadWrite.writeSoilProfile(profileList, profileFileName, horizonFileName)

                        if versionSaveResult: modelParam.updateFlag_soil = False

                #saving gis file
                if versionSaveResult:
                    if modelParam.updateFlag_gis:
                        gisFileName = modelParam.initParam.gis_file_name

                        gisList = []
                        for gis in modelParam.gisParam:
                            gisList.append(gis["gis"])
                        versionSaveResult = FileReadWrite.writeGisFile(modelDirectory + "/" + gisFileName, gisList)

                        if versionSaveResult: modelParam.updateFlag_gis = False

                #saving init file
                initialFileName = ""
                if versionSaveResult:
                    initialFileName = self.listInitFileName[self.currentVersionIndex]
                    versionSaveResult = FileReadWrite.writeInitialFile(modelParam.initParam, modelDirectory + "/ini/" + initialFileName)


                if versionSaveResult:
                    self.versionModifyMode = False
                    self.btnNewVersion.setEnabled(True)
                    self.btnLoadVersion.setEnabled(True)
                    self.btnModify.setEnabled(False)
                    # else: self.btnModify.setEnabled(True)
                    self.btnClose.setText("Close")
                    QtGui.QMessageBox.about(self.form, "Save", "Current version has been saved successfully.")
                else:
                    QtGui.QMessageBox.about(self.form, "Error", "Files were not saved. Check the error in each input file.")
        else:
            message = "There is no new or modified version to save."
            QtGui.QMessageBox.about(self.form, "No Version", message)

    def ckbShowVersion_toggled(self):
        self.cmbParameterFile_currentIndexChanged()

    def tableParameterView_itemChanged(self):
        item = self.tableParameterView.currentItem()
        if item is not None:
            paramType = self.cmbParameterFile.currentText()

            #reading version no [for soil parameters the version no. has to read differently]
            verIndex = -1
            colIndex = self.tableParameterView.currentColumn()
            headerText = self.tableParameterView.horizontalHeaderItem(colIndex).text()
            try: verIndex = int(headerText[4:6]) - int(self.txtStartingVersionNo.text())
            except: pass

            #reading site index [for soil parameters the version no. has to read differently]
            #and vegetation number (id) necessary only for vegetation and epc parameters
            #site index is required for all parameters types except initial control parameters
            siteIndex = ""
            vegid = -1
            if headerText.find("(") > -1:
                siteIndex = headerText[headerText.find("(") + 1: headerText.find(")")]
                if siteIndex.find(":") > -1:
                    vegid = int(siteIndex.split(":")[-1])
                    siteIndex = siteIndex.split(":")[0]

            #reading parameter name and parameter values [both are in text format]
            rowIndex = self.tableParameterView.currentRow()
            paramName = self.tableParameterView.item(rowIndex, 0).text()
            paramValue = item.text()

            #variables required for changing filenames
            versionText = self.txtVersionNo.text()
            tailReplacement = not self.flag_addVersionNoAtTheEndOfFiles

            result = None
            if paramType == "Initial Parameter":
                if verIndex > -1:
                    result = self.listModelParam[verIndex].initParam.setParameterValue(paramName, paramValue)
            elif paramType == "GIS Parameter":
                if len(siteIndex) > 0:
                    result = self.listModelParam[verIndex].updateGisObject(siteIndex, paramName, paramValue, versionText, tailReplacement)
                    if paramName == "Site Index": self.cmbParameterFile_currentIndexChanged()
            elif paramType == "Veg Parameter":
                if len(siteIndex) > 0 and vegid > -1:
                    result = self.listModelParam[verIndex].updateVegObject(siteIndex, vegid, paramName, paramValue, versionText, tailReplacement)
                    if paramName in ["Site Index", "Vegetation No."]: self.cmbParameterFile_currentIndexChanged()
            elif paramType == "Epc Parameter":
                if len(siteIndex) > 0 and vegid > -1:
                    result = self.listModelParam[verIndex].updateEpcObject(siteIndex, vegid, rowIndex + 1, paramName,
                                                                              paramValue, versionText, tailReplacement)
            elif paramType == "Soil Parameter":
                verIndex = len(self.listModelParam) - 1
                modelParam = self.listModelParam[verIndex]

                #searching for the concerning profile
                siteIndex = self.tableParameterView.item(rowIndex, 0).text()
                for i in range(self.tableParameterView.rowCount()):
                    if self.tableParameterView.item(i, 0).text() == siteIndex: break
                layerIndex = rowIndex - i

                paramName = self.tableParameterView.horizontalHeaderItem(colIndex).text()
                result = modelParam.updateSoilProfile(siteIndex, paramName, paramValue, layerIndex, versionText, tailReplacement)
                # self.cmbParameterFile_currentIndexChanged()
                # item = self.tableParameterView.item(rowIndex, colIndex)
                # self.tableParameterView.setCurrentItem(item)

            if result is not None:
                # message = "Parameter value was not updated."
                item.setText(str(result))
                # self.cmbParameterFile_currentIndexChanged()
            else:
                self.versionModifyMode = True
                if self.currentVersionIndex != len(self.listModelParam) - 1:
                    self.currentVersionIndex = len(self.listModelParam) - 1
                    startingVersion = int(self.txtStartingVersionNo.text())
                    self.txtVersionNo.setText(str(startingVersion + self.currentVersionIndex).rjust(2,"0"))
                self.findLinkedFile(self.currentVersionIndex)
                self.btnNewVersion.setEnabled(False)
                self.btnClose.setText("Abort")
                self.btnModify.setEnabled(True)
                self.btnLoadVersion.setEnabled(False)
                self.buttonVersionSettings.setEnabled(False)

    def ReadModelParameter(self, initialFilename):
        modelParam = None

        modelDirectory = ApplicationProperty.currentModelDirectory
        initParam = FileReadWrite.readInitialFile(initialFilename)
        if initParam is not None:
            #reading gis file
            gisParam = []
            filename = modelDirectory + "/" + initParam.gis_file_name
            gisList = FileReadWrite.readGisFile(filename)
            for gis in gisList:
                gisItem = {"siteIndex": gis.siteIndex, "gis": gis}
                gisParam.append(gisItem)

            if len(gisParam) > 0:
                #reading veg files and epc files
                vegParam = []
                filename = modelDirectory + "/" + initParam.veg_file_name
                vegList = FileReadWrite.readVegFile(filename)

                vegEpc = []             #structure: [{"siteIndex": siteIndex, "epcid": epcid}, {}]
                epcParam = []           #structure: [{"epcid": epcid, "epc": epcObject}, {}]
                temp = []               #structure: [{"epcid": epcid, "fileName": epcFileName}, {}]
                epcid = 0

                for veg in vegList:
                    vegItem = {"siteIndex": veg.siteIndex, "vegid": veg.vegetationNumber, "veg": veg}
                    vegParam.append(vegItem)

                    #because epc parameters were separated from initial parameter in order to
                    #allow using the same epc for different sites, here all distinct epc objects
                    #will be stored in dictionary and an array of index is used to maintain
                    #the relation between site and epc object.

                    for i in range(len(temp)):
                        if temp[i]["fileName"] == veg.epcFileName: break
                    else:
                        epcid += 1
                        epcFileNameItem = {"epcid": epcid, "fileName": veg.epcFileName}
                        temp.append(epcFileNameItem)

                    vegEpcItem = {"siteIndex": veg.siteIndex, "vegid": veg.vegetationNumber, "epcid": epcid}
                    vegEpc.append(vegEpcItem)

                for epcFileNameItem in temp:
                    filename = modelDirectory + "/epc/" + epcFileNameItem["fileName"]
                    epc = FileReadWrite.readEpcFile(filename)
                    epcItem = {"epcid": epcFileNameItem["epcid"], "epc": epc, "updateFlag": False}
                    epcParam.append(epcItem)

                #read soil profile files and soil horizon files
                temp = []   #structure: [{"siteIndex": profileFileId, "pFileName": profileFileName, "hFileName": horizonFileName,
                                        # "profileName": profileName},{}]
                gisSoil = []
                soilParam = []
                for gpo in gisParam:
                    for i in range(len(temp)):
                        if temp[i]["siteIndex"] == gpo["gis"].siteIndex: break
                    else:
                        gis = gpo["gis"]
                        soilFileItem = {"siteIndex": gis.siteIndex, "pFileName": gis.soilProfileFileName,
                                               "hFileName": gis.soilHorizonFileName, "profileName": gis.profileName}
                        temp.append(soilFileItem)

                if len(temp) > 0:
                    spfid = 0
                    for sp in temp:
                        profileList = FileReadWrite.readSoilProfile(modelDirectory + "/soil/" + sp["pFileName"],
                                                                        modelDirectory + "/soil/" + sp["hFileName"])
                        for profile in profileList:
                            if profile.profileName == sp["profileName"]:
                                spfid += 1
                                gisSoilItem = {"siteIndex": sp["siteIndex"], "spfid": spfid}
                                gisSoil.append(gisSoilItem)

                                soilParamItem = {"spfid": spfid, "sp": profile}
                                soilParam.append(soilParamItem)

                if (len(vegParam) > 0 and len(vegEpc) > 0 and len(epcParam) > 0 and
                    len(gisSoil) > 0 and len(soilParam) > 0):
                    modelParam = BiomeBGCParameterSet()
                    modelParam.initParam = initParam
                    modelParam.gisParam = gisParam
                    modelParam.vegParam = vegParam
                    modelParam.vegEpc = vegEpc
                    modelParam.epcParam = epcParam
                    modelParam.gisSoil = gisSoil
                    modelParam.soilParam = soilParam

        return modelParam

    def showVersionExample(self):
        example = self.txtInitialFile.text()
        if self.radioButtonStartNewVersion.isChecked():
            if self.radioButtonAddVersionNoToFile.isChecked():
                example = example.replace(".ini", "_01.ini")
            else:
                l2d = example.replace(".ini", "")[-2:]
                if l2d.isnumeric():
                    example = example.replace(l2d + ".ini", "01.ini")
                else: example = ""
        else:
            if self.checkBoxContinueFromInitFile.isChecked():
                l2d = example.replace(".ini", "")[-2:]
                if l2d.isnumeric():
                    example = example.replace(l2d + ".ini", str(int(l2d) + 1).rjust(2, "0") + ".ini")
                else: example = ""
            elif self.checkBoxContinueFrom.isChecked() and len(self.textCurrentVersion.text()) > 0:
                if self.radioButtonAddVersionNoToFile.isChecked():
                    verText = self.textCurrentVersion.text().strip()
                    if verText.isnumeric():
                        example = example.replace(".ini", "_" + str(int(verText) + 1).rjust(2, "0") + ".ini")
                    else: example = ""
                else:
                    l2d = example.replace(".ini", "")[-2:]
                    verText = self.textCurrentVersion.text().strip()
                    if l2d.isnumeric() and verText.isnumeric():
                        example = example.replace(l2d + ".ini", str(int(verText) + 1).rjust(2, "0") + ".ini")
                    else: example = ""
            else: example = ""

        if len(example) > 0: self.lblExample.setText("Next Version: " + example)
        else: self.lblExample.clear()

    def btnRefresh_clicked(self):
        self.findLinkedFile(self.currentVersionIndex)


    def comboGraphName_currentIndexChanged(self):

        if self.listModelParam and self.comboGraphName.currentIndex() >= 0:
            if self.checkBoxGraphShow.isChecked(): self.checkBoxGraphShow_toggled()
            else: self.checkBoxGraphShow.setChecked(True)
        else:
            self.checkBoxGraphShow.setChecked(False)
            self.clear_graph_configuration_table()
            self.enable_graph_show(False)

    def checkBoxGraphShow_toggled(self):
        graph_name = self.comboGraphName.currentText()
        self.clear_graph_configuration_table()
        if self.checkBoxGraphShow.isChecked():
            if self.comboGraphName.currentIndex() >= 0:
                model_graph = ModelGraph.read_graph_template(os.path.join("graphs", graph_name))
                if model_graph is not None:
                    self.show_graph_object(model_graph, graph_name)
                else:
                    self.checkBoxGraphShow.setChecked(False)

                if self.graph_configuration.number_of_graphs() > 0: self.enable_graph_show(True)
        else:
            gndx = self.graph_configuration.find_graph_index(graph_name)
            if gndx >= 0:
                self.graph_configuration.list_of_changing_graph.pop(gndx)
                if self.graph_configuration.number_of_graphs() == 0: self.enable_graph_show(False)



    def show_graph_object(self, model_graph, graph_name):
        edit_graph = None
        graph_index = self.graph_configuration.find_graph_index(graph_name)
        if graph_index >= 0: edit_graph = self.graph_configuration.list_of_changing_graph[graph_index]


        starting_version = int(self.txtStartingVersionNo.text().strip())
        version_list = []
        for i in range(len(self.listModelParam)): version_list.append(str(starting_version + i))


        for plot in model_graph.list_of_plot:
            edit_plot = None
            if edit_graph:
                plot_index = edit_graph.find_plot_index(plot.plot_title)
                edit_plot = edit_graph.edit_plot_list[plot_index]

            #checking the datasource: if data source is model output only then the series variables will be shown
            series_title_list = []
            ini_file_list = []
            for series in plot.list_of_series:
                if series.data_source.source_type == 0:
                    series_title_list.append(series.series_title)
                    if series.data_source.initial_filename not in ini_file_list:
                        ini_file_list.append(series.data_source.initial_filename)

            if len(series_title_list) > 0:
                row_index = self.tableConfiguration.rowCount()
                self.tableConfiguration.insertRow(row_index)
                self.tableConfiguration.setRowHeight(row_index, 20)
                item = QtWidgets.QTableWidgetItem("Plot: " + plot.plot_title)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setBackground(QtGui.QColor(125,204,249))
                self.tableConfiguration.setItem(row_index, 0, item)
                item = QtWidgets.QTableWidgetItem("")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setBackground(QtGui.QColor(125,204,249))
                self.tableConfiguration.setItem(row_index, 1, item)

                if len(ini_file_list) == 1:
                    for series in plot.list_of_series:
                        row_index = self.tableConfiguration.rowCount()
                        self.tableConfiguration.insertRow(row_index)
                        self.tableConfiguration.setRowHeight(row_index, 20)
                        item = QtWidgets.QTableWidgetItem(series.series_title)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableConfiguration.setItem(row_index, 0, item)
                        item = QtGui.QComboBox()
                        item.row_index = row_index
                        item.addItems(version_list)
                        item.currentIndexChanged.connect(self.signalMapper_gconfig_combo.map)
                        self.signalMapper_gconfig_combo.setMapping(item, item)
                        self.tableConfiguration.setCellWidget(row_index, 1, item)
                        item = QtGui.QCheckBox("")
                        item.row_index = row_index
                        vndx = -1
                        if edit_plot and (series.series_title in edit_plot.series_name_list):
                            item.setChecked(True)
                            sndx = edit_plot.series_name_list.index(series.series_title)
                            vndx = edit_plot.init_version_list[sndx]
                        item.setLayoutDirection(QtCore.Qt.RightToLeft)
                        item.toggled.connect(self.signalMapper_gconfig_checkbox.map)
                        self.signalMapper_gconfig_checkbox.setMapping(item, item)
                        self.tableConfiguration.setCellWidget(row_index, 2, item)

                        if vndx == -1: self.tableConfiguration.cellWidget(row_index, 1).setCurrentIndex(self.currentVersionIndex)
                        else: self.tableConfiguration.cellWidget(row_index, 1).setCurrentIndex(vndx)

                else:
                    version_index_temp = self.currentVersionIndex
                    for init_file in ini_file_list:
                        for series in plot.list_of_series:
                            if series.data_source.initial_filename == init_file:
                                row_index = self.tableConfiguration.rowCount()
                                self.tableConfiguration.insertRow(row_index)
                                self.tableConfiguration.setRowHeight(row_index, 20)
                                item = QtWidgets.QTableWidgetItem(series.series_title)
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.tableConfiguration.setItem(row_index, 0, item)
                                item = QtGui.QComboBox()
                                item.row_index = row_index
                                item.addItems(version_list)
                                item.currentIndexChanged.connect(self.signalMapper_gconfig_combo.map)
                                self.signalMapper_gconfig_combo.setMapping(item, item)
                                self.tableConfiguration.setCellWidget(row_index, 1, item)
                                item = QtGui.QCheckBox("")
                                item.row_index = row_index
                                vndx = -1
                                if edit_plot and (series.series_title in edit_plot.series_name_list):
                                    item.setChecked(True)
                                    sndx = edit_plot.series_name_list.index(series.series_title)
                                    vndx = edit_plot.init_version_list[sndx]
                                item.setLayoutDirection(QtCore.Qt.RightToLeft)
                                item.toggled.connect(self.signalMapper_gconfig_checkbox.map)
                                self.signalMapper_gconfig_checkbox.setMapping(item, item)
                                self.tableConfiguration.setCellWidget(row_index, 2, item)

                                if vndx == -1: self.tableConfiguration.cellWidget(row_index, 1).setCurrentIndex(version_index_temp)
                                else: self.tableConfiguration.cellWidget(row_index, 1).setCurrentIndex(vndx)

                        if version_index_temp != -1: version_index_temp -= 1

    @QtCore.pyqtSlot(QtWidgets.QWidget)
    def gconfig_combo_indexChanged(self, combo):
        cell = self.tableConfiguration.cellWidget(combo.row_index, 1)
        ckb_cell = self.tableConfiguration.cellWidget(combo.row_index, 2)
        if cell.currentIndex() >= 0:
            ckb_cell.setEnabled(True)
            if ckb_cell.isChecked(): self.refresh_configuration(ckb_cell)
        else: ckb_cell.setEnabled(False)

    @QtCore.pyqtSlot(QtWidgets.QWidget)
    def refresh_configuration(self, check_box):
        row_index = check_box.row_index
        if row_index >= 0:
            init_version = self.tableConfiguration.cellWidget(row_index, 1).currentIndex()
            series_name = self.tableConfiguration.item(row_index, 0).text()
            if len(series_name) > 0:
                graph_name = self.comboGraphName.currentText()
                plot_name = ""
                for i in reversed(range(row_index)):
                    item = self.tableConfiguration.item(i, 0)
                    if item.text().split(":")[0].strip().lower() == "plot":
                        plot_name = item.text().split(":")[-1].strip()
                        break
                if len(plot_name) > 0:
                    if check_box.isChecked():
                        graph_index = self.graph_configuration.find_graph_index(graph_name)
                        if graph_index >= 0:
                            g = self.graph_configuration.list_of_changing_graph[graph_index]
                            pndx = g.find_plot_index(plot_name)
                            if pndx >= 0:
                                p = g.edit_plot_list[pndx]
                                if series_name not in p.series_name_list:
                                    p.series_name_list.append(series_name)
                                    p.init_version_list.append(init_version)
                                else:
                                    sndx = p.series_name_list.index(series_name)
                                    p.init_version_list[sndx] = init_version
                        else:
                            g = edit_graph(graph_name)
                            p = edit_plot(plot_name)
                            p.series_name_list.append(series_name)
                            p.init_version_list.append(init_version)
                            g.edit_plot_list.append(p)
                            self.graph_configuration.list_of_changing_graph.append(g)
                    else:
                        graph_index = self.graph_configuration.find_graph_index(graph_name)
                        if graph_index >= 0:
                            g = self.graph_configuration.list_of_changing_graph[graph_index]
                            pndx = g.find_plot_index(plot_name)
                            if pndx >= 0:
                                p = g.edit_plot_list[pndx]
                                if series_name in p.series_name_list:
                                    sndx = p.series_name_list.index(series_name)
                                    p.series_name_list.pop(sndx)
                                    p.init_version_list.pop(sndx)

        if self.graph_configuration.number_of_graphs() > 0: self.enable_graph_show(True)
        else: self.enable_graph_show(False)

    def clear_graph_configuration_table(self):
        for i in reversed(range(self.tableConfiguration.rowCount())):
            self.tableConfiguration.removeRow(i)

    def buttonSaveConfiguration_clicked(self):
        if self.graph_configuration.list_of_changing_graph:
            initial_directory = "graphs"
            file_name = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save Configuration', initial_directory, "Graph Configuration (*.gcf)")
            if file_name:
                if graph_configuration.save_configuration(self.graph_configuration, file_name):
                    message = "Configuration file has been saved successfully."
                    QtGui.QMessageBox.about(self.form, "Success", message)
                else:
                    message = "Configuration file could not be saved."
                    QtGui.QMessageBox.about(self.form, "File Error", message)
        else:
            message = "Graph option is not configured. Please configure your graph options."
            QtGui.QMessageBox.about(self.form, "File Error", message)

    def buttonLoadConfiguration_clicked(self):
        initial_directory = "graphs"
        file_name = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Save Configuration', initial_directory, "Graph Configuration (*.gcf)")
        if file_name:
            if graph_configuration.load_configuration(file_name, self.graph_configuration):
                #check invalid version indexing
                invalid_vndx = False
                for g in self.graph_configuration.list_of_changing_graph:
                    for p in g.edit_plot_list:
                        for vndx in p.init_version_list:
                            if vndx > len(self.listModelParam) - 1:
                                invalid_vndx = True
                                break

                if invalid_vndx:
                    message = "The configuration file has invalid version indices. Do you want to clean them?"
                    reply = QtGui.QMessageBox.question(self.form, 'Message', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        for g in self.graph_configuration.list_of_changing_graph:
                            for p in g.edit_plot_list:
                                for ndx in reversed(range(len(p.init_version_list))):
                                    if p.init_version_list[ndx] > len(self.listModelParam) - 1:
                                        p.init_version_list.pop(ndx)
                                        p.series_name_list.pop(ndx)
                else:
                    message = "Configuration has been loaded successfully."
                    QtGui.QMessageBox.about(self.form, "Success", message)

                self.comboGraphName.setCurrentIndex(-1)
                if self.graph_configuration.number_of_graphs() > 0: self.enable_graph_show(True)
                else: self.enable_graph_show(False)

            else:
                message = "Configuration could not be loaded."
                QtGui.QMessageBox.about(self.form, "File Error", message)

    def buttonShowGraph_clicked(self):
        if self.generate_graphs():
            self.buttonCompare.setEnabled(True)
            self.buttonOriginalView.setEnabled(True)

            if self.graph_configuration.number_of_graphs() > 1:
                self.buttonGraphFirst.setEnabled(True)
                self.buttonGraphBack.setEnabled(True)
                self.buttonGraphNext.setEnabled(True)
                self.buttonGraphLast.setEnabled(True)
            else:
                self.buttonGraphFirst.setEnabled(False)
                self.buttonGraphBack.setEnabled(False)
                self.buttonGraphNext.setEnabled(False)
                self.buttonGraphLast.setEnabled(False)

            self.display_graph()

    def generate_graphs(self):
        proceed = True
        starting_version = int(self.txtStartingVersionNo.text())

        version_index_list = []
        for i in range(self.graph_configuration.number_of_graphs()):
            g = self.graph_configuration.list_of_changing_graph[i]
            for j in range(len(g.edit_plot_list)):
                p = g.edit_plot_list[j]
                for vndx in p.init_version_list:
                    if vndx not in version_index_list: version_index_list.append(vndx)

        if len(version_index_list) > 0:
            if (self.currentVersionIndex in version_index_list and self.versionModifyMode):
                #check if the version is saved
                message = "Current version is not saved. Please save the version and execute model."
                QtGui.QMessageBox.about(self.form, "Version not saved", message)
                return False

            for vi in version_index_list:
                #check if the version was executed
                output_prefix = self.listModelParam[vi].initParam.output_file_prefix.replace("outputs/","")
                target_directory = ApplicationProperty.currentModelDirectory + "/outputs"
                output_file_list = [f for f in os.listdir(target_directory) if f.lower().find(output_prefix + ".") != -1 and os.path.isfile(os.path.join(target_directory,f)) ]
                if len(output_file_list) == 0:
                    message = "Version " + str(vi).rjust(2, "0") + " was never executed. Please execute the version."
                    QtGui.QMessageBox.about(self.form, "No Output", message)
                    return False

            #changing data source
            if proceed:
                for g in self.graph_configuration.list_of_changing_graph:
                    model_graph = ModelGraph.load_binary_template("graphs/" + g.graph_name)
                    if model_graph is not None:
                        for p in g.edit_plot_list:
                            model_plot = model_graph.find_plot_by_title(p.plot_name)
                            if model_plot:
                                for sndx in range(len(p.series_name_list)):
                                    s = p.series_name_list[sndx]
                                    if proceed:
                                        data_series = model_plot.find_series_by_title(s)
                                        if data_series:
                                            data_series.data_source.model_directory = ApplicationProperty.currentModelDirectory
                                            data_series.data_source.initial_filename = self.listInitFileName[p.init_version_list[sndx]]
                                        else: proceed = False
                            else: proceed = False

                        #collecting new data
                        if proceed:
                            for vndx in version_index_list:
                                ModelGraph.read_data_from_specific_model_output(model_graph, ApplicationProperty.currentModelDirectory, self.listInitFileName[vndx])

                            image_file_name = "temp/" + g.graph_name.split(".")[0] + "_" + str(max(version_index_list) + starting_version).rjust(2, "0") + ".png"

                            if BiomeBgcGraphDummy.ShowGraph(model_graph, 1, display=False, save_file_filename=image_file_name):
                                g.graph_image_address = image_file_name
                            else: proceed = False
                        if proceed: self.graph_configuration.current_graph_index = 0
                    else: proceed = False
            return proceed
        else: return False

    def display_graph(self):
        self.labelCurrentGraphName.clear()
        g = self.graph_configuration.current_graph_object()
        if g:
            image_address = g.graph_image_address
            if os.path.exists(image_address):
                scene = QtGui.QGraphicsScene()
                pix_map = QtGui.QPixmap(image_address)
                w = pix_map.width()
                h = pix_map.height()
                scene.addPixmap(pix_map)
                self.graphicsView.setScene(scene)
                self.graphicsView.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
                self.labelCurrentGraphName.setText("Current Graph: " + g.graph_name.split(".")[0])
            else: self.graphicsView.setScene(None)
        else: self.graphicsView.setScene(None)
        self.graphicsView.show()

    def buttonGraphFirst_clicked(self):
        if self.graph_configuration.number_of_graphs() > 0:
            self.graph_configuration.current_graph_index = 0
            self.display_graph()

    def buttonGraphLast_clicked(self):
        if self.graph_configuration.number_of_graphs() > 0:
            self.graph_configuration.current_graph_index = self.graph_configuration.number_of_graphs() - 1
            self.display_graph()

    def buttonGraphBack_clicked(self):
        if self.graph_configuration.number_of_graphs() > 0 and self.graph_configuration.current_graph_index > 0:
            self.graph_configuration.current_graph_index -= 1
            self.display_graph()

    def buttonGraphNext_clicked(self):
        n = self.graph_configuration.number_of_graphs()
        if n > 0 and self.graph_configuration.current_graph_index < (n-1):
            self.graph_configuration.current_graph_index += 1
            self.display_graph()

    def buttonCompare_clicked(self):
        self.dialog_graph_compare = DialogGraphCompare()
        start_version = int(self.txtStartingVersionNo.text().strip())
        for g in self.graph_configuration.list_of_changing_graph:
            graph_name = g.graph_name.split(".")[0]
            self.dialog_graph_compare.comboGraphName.addItem(graph_name)

            #generating list of all available graphs
            for i in range(len(self.listModelParam)):
                version = start_version + i
                image_filename = "temp/" + graph_name + "_" + str(version).rjust(2, "0") + ".png"
                if os.path.exists(image_filename):
                    item = {"version_index": version, "graph_name": graph_name, "image_file": image_filename}
                    self.dialog_graph_compare.all_available_graphs.append(item)
        if len(self.dialog_graph_compare.all_available_graphs) == 0:
            message = "There is no available graph to compare. Please generate the graphs first."
            QtGui.QMessageBox.about(self.form, "No Graph", message)
            self.dialog_graph_compare = None
        else:
            self.dialog_graph_compare.current_version_index = start_version + self.currentVersionIndex
            self.dialog_graph_compare.comboGraphName.setCurrentIndex(-1)
            self.dialog_graph_compare.comboGraphName.setEnabled(False)
            self.dialog_graph_compare.form.show()
            self.dialog_graph_compare.radio_button_toggled()


    def buttonOriginalView_clicked(self):
        if self.graph_configuration.current_graph_index >= 0:
            g = self.graph_configuration.list_of_changing_graph[self.graph_configuration.current_graph_index]
            model_graph = ModelGraph.load_binary_template("graphs/" + g.graph_name)
            if model_graph is not None:
                for p in g.edit_plot_list:
                    model_plot = model_graph.find_plot_by_title(p.plot_name)
                    if model_plot:
                        for sndx in range(len(p.series_name_list)):
                            s = p.series_name_list[sndx]
                            data_series = model_plot.find_series_by_title(s)
                            if data_series:
                                data_series.data_source.model_directory = ApplicationProperty.currentModelDirectory
                                data_series.data_source.initial_filename = self.listInitFileName[p.init_version_list[sndx]]

                version_index_list = []
                for i in range(len(g.edit_plot_list)):
                    p = g.edit_plot_list[i]
                    for vndx in p.init_version_list:
                        if vndx not in version_index_list: version_index_list.append(vndx)

                for vndx in version_index_list:
                    ModelGraph.read_data_from_specific_model_output(model_graph, ApplicationProperty.currentModelDirectory, self.listInitFileName[vndx])

                BiomeBgcGraphDummy.ShowGraph(model_graph, 1, display=True)



class graph_configuration:
    def __init__(self):
        self.list_of_changing_graph = []
        self.current_graph_index = -1

    def current_graph_object(self):
        if len(self.list_of_changing_graph) > 0:
            if (self.current_graph_index >=0) and (self.current_graph_index < self.number_of_graphs()):
                return self.list_of_changing_graph[self.current_graph_index]
        return None

    def number_of_graphs(self): return len(self.list_of_changing_graph)

    def find_graph_index(self, graph_name):
        for i in range(self.number_of_graphs()):
            g = self.list_of_changing_graph[i]
            if g.graph_name == graph_name: return i
        else: return -1

    def graph_availability(self, version_text):
        for g in self.list_of_changing_graph:
            graph_image_name = g.graph_name.split(".")[0].strip() + "_" + version_text + ".png"
            if not os.path.exists("temp/" + graph_image_name): return False
        return True

    #this function should only use when graph_availability function returns a True
    def change_image_souce(self, version_text):
        for g in self.list_of_changing_graph:
            if g.graph_image_address:
                g.graph_image_address = g.graph_image_address[:-6] + version_text + ".png"
            else: return False
        return True

    @staticmethod
    def save_configuration(graph_config_obj, file_name):
        if file_name and graph_config_obj:
            f = None
            try:
                f = open(file_name, 'w')
                f.write("Graph Configuration File \n")

                for g in graph_config_obj.list_of_changing_graph:
                    f.write("\n")
                    f.write("Graph Name: " + g.graph_name + "\n")
                    for p in g.edit_plot_list:
                        f.write("Plot Name: " + p.plot_name + "\n")
                        series_list = str(p.series_name_list).replace("[", "").replace("]", "").replace("'", "")
                        f.write("Series List: " + series_list + "\n")
                        init_version_list = str(p.init_version_list).replace("[", "").replace("]", "").replace("'", "")
                        f.write("Series Version: " + init_version_list + "\n")
            except: return False
            finally:
                try: f.close()
                except: pass
            return True
        else: return False

    @staticmethod
    def load_configuration(file_name, configure_obj_out):
        if file_name and configure_obj_out:
            configure_obj_out.list_of_changing_graph = []
            g = None
            p = None

            f = None
            try:
                f = open(file_name, 'r')
                for line in f.readlines():
                    line = line.strip().strip("\n")
                    if line:
                        temp = line.split(":")
                        if temp[0].strip() == "Graph Name":
                            graph_name = temp[1].strip()
                            if os.path.exists("graphs/" + graph_name):
                                g = edit_graph(temp[1].strip())
                            else: g = None
                        elif g and temp[0].strip() == "Plot Name":
                            p = edit_plot(temp[1].strip())
                        elif g and p and temp[0].strip() == "Series List":
                            s_list = temp[1].strip().split(",")
                            for i in reversed(range(len(s_list))):
                                s_list[i] = s_list[i].strip()
                                if len(s_list[i]) == 0: s_list.pop(i)
                            p.series_name_list = s_list
                        elif g and p and temp[0].strip() == "Series Version":
                            v_list = temp[1].strip().split(",")
                            for i in reversed(range(len(v_list))):
                                v_list[i] = v_list[i].strip()
                                if len(v_list[i]) == 0: v_list.pop(i)

                            p.init_version_list = []
                            for vndx in v_list:
                                try: p.init_version_list.append(int(vndx))
                                except: pass

                            g.edit_plot_list.append(p)

                            g_index = configure_obj_out.find_graph_index(g.graph_name)
                            if g_index == -1:
                                configure_obj_out.list_of_changing_graph.append(g)
            except: return False
            finally:
                try: f.close()
                except: pass
            return True
        else: return False

class edit_graph:
    def __init__(self, graph_name):
        self.graph_name = graph_name
        self.graph_image_address = ""
        self.edit_plot_list = []

    def find_plot_index(self, plot_title):
        for i in range(len(self.edit_plot_list)):
            p = self.edit_plot_list[i]
            if p.plot_name == plot_title: return i
        else: return -1

class edit_plot:
    def __init__(self, plot_name):
        self.plot_name = plot_name
        self.series_name_list = []
        self.init_version_list = []
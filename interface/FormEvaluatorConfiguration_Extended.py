from interface.FormEvaluatorConfiguration import Ui_FormEvaluatorConfiguration
from PyQt5 import QtGui, QtCore, QtWidgets
from parameter import EpcParameter, VegetationParameter, GisParameter, SoilLayer, SoilProfile
from parameter_set import BiomeBGCParameterSet
from hopspack.configure import TargetParameter, Comparing_Variable, Configure
from application import ApplicationProperty
from file_io import FileReadWrite
from read_output import ReadBinaryOutput, ReadExternalOutput
import os
from copy import copy

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class FormEvaluatorConfiguration(Ui_FormEvaluatorConfiguration):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.add_socket()
        self.add_validator()


        self.signalMapper = QtCore.QSignalMapper(self.form)
        self.signalMapper.mapped[QtWidgets.QWidget].connect(self.checkbox_toggled)

        self.indexComboSignalMapper = QtCore.QSignalMapper(self.form)
        self.indexComboSignalMapper.mapped[QtWidgets.QWidget].connect(self.indexCombo_currentIndexChanged)

        self.deletePamamButtonSignalMapper = QtCore.QSignalMapper(self.form)
        self.deletePamamButtonSignalMapper.mapped[QtWidgets.QWidget].connect(self.deleteParamButton_clicked)

        self.deleteVariableButtonSignalMapper = QtCore.QSignalMapper(self.form)
        self.deleteVariableButtonSignalMapper.mapped[QtWidgets.QWidget].connect(self.deleteVariableButton_clicked)

        self.objectiveFunctionComboSignalMapper = QtCore.QSignalMapper(self.form)
        self.objectiveFunctionComboSignalMapper.mapped[QtWidgets.QWidget].connect(self.objectiveFunctionCombo_currentIndexChanged)

        self.biomeBGCParamSet = None

        self.parameter_list = []
        self.comparing_variable_list = []
        self.config = Configure()

        self.color_error = QtGui.QColor('orange')
        self.color_ok = QtGui.QColor('white')

        self.obj_function_list = ['Root Mean Square Error', 'Coefficient of Determination', 'Absolute Average Deviation',
                                   'Index of Agreement', 'Mean Absolute Error', 'Mean Square Error', 'Percentage Bias',
                                   'RMSE-Observed Stdv. Ratio', 'Nash-Sutcliffe Efficiency']

        self.objective_targets = ['Minimize Error', 'Maximize Fit']
        self.normalization_option = ['Normalize data using Observation Max', 'Normalize data using Observation Mean',
                                     'Normalize data using Predicted Max', 'Normalize data using Predicted Mean']
        self.penalty_function = ['Linear Distance', 'Squared Distance', 'Cubic Distance', 'Logistic Function']
        self.param_sequence_options = ['As the order of parameters in Parameter-Map file (default)',
                                       'As specified in the selected Parameter-Map file',
                                       'Generate a Random Sequence', 'Manual Sequencing']
        self.selected_config_file = ''
        self.initial_setting()

    def add_socket(self):
        self.tableParameterSelection.itemChanged.connect(self.tableParameterSelection_itemChanged)
        self.buttonSave.clicked.connect(self.buttonSave_clicked)
        self.comboObservationDataType.currentIndexChanged.connect(self.comboObservationDataType_currentIndexChanged)
        self.buttonInitializationFile.clicked.connect(self.buttonInitializationFile_clicked)
        self.comboOutputFileType.currentIndexChanged.connect(self.comboOutputFileType_currentIndexChanged)
        self.buttonMeasuredDataFile.clicked.connect(self.buttonMeasuredDataFile_clicked)
        self.buttonModelOutputVariable.clicked.connect(self.buttonModelOutputVariable_clicked)
        self.buttonMeasuredVariable.clicked.connect(self.buttonMeasuredVariable_clicked)
        self.buttonModelPairingVariable.clicked.connect(self.buttonModelPairingVariable_clicked)
        self.buttonMeasuredPairingVariable.clicked.connect(self.buttonMeasuredPairingVariable_clicked)
        self.lineEditModelVariableConversionFactor.textChanged.connect(self.lineEditModelVariableConversionFactor_textChanged)
        self.buttonAddComparisonOption.clicked.connect(self.buttonAddComparisonOption_clicked)
        self.lineEditMeasuredDataFile.textChanged.connect(self.lineEditMeasuredDataFile_textChanged)
        self.lineEditInitializationFile.textChanged.connect(self.lineEditInitializationFile_textChanged)
        self.buttonClose.clicked.connect(self.buttonClose_clicked)
        self.buttonLoad.clicked.connect(self.buttonLoad_clicked)
        self.comboBoxParameterType.currentIndexChanged.connect(self.comboBoxParameterType_currentIndexChanged)
        self.checkBoxSpecifyIndex.toggled.connect(self.checkBoxSpecifyIndex_toggled)
        self.pushButtonInitialFile.clicked.connect(self.pushButtonInitialFile_clicked)
        self.buttonAddToList.clicked.connect(self.buttonAddToList_clicked)
        self.checkBoxPreferred.toggled.connect(self.checkBoxPreferred_toggled)
        self.tableSelectedParameters.itemChanged.connect(self.tableSelectedParameters_itemChanged)
        self.buttonLoadFromFile.clicked.connect(self.buttonLoadFromFile_clicked)
        self.checkBoxOverrideObjFun.toggled.connect(self.checkBoxOverrideObjFun_toggled)
        self.tableComparisonOption.itemChanged.connect(self.tableComparisonOption_itemChanged)
        self.radioButtonCreateConfigFile.toggled.connect(self.radioButtonConfigFile_toggled)
        self.checkBoxSaveStatistics.toggled.connect(self.checkBoxSaveStatistics_toggled)
        self.checkBoxNormalizeData.toggled.connect(self.checkBoxNormalizeData_toggled)
        self.checkBoxUseGlobalObjFun.toggled.connect(self.checkBoxUseGlobalObjFun_toggled)
        self.checkBoxUsePenaltyFun.toggled.connect(self.checkBoxUsePenaltyFun_toggled)
        self.comboBoxParamSequenceOption.currentIndexChanged.connect(self.comboBoxParamSequenceOption_currentIndexChanged)
        self.buttonChooseConfigFile.clicked.connect(self.buttonChooseConfigFile_clicked)
        self.buttonBGCHomeDir.clicked.connect(self.buttonBGCHomeDir_clicked)
        self.pushButtonSelectInitialFile.clicked.connect(self.pushButtonSelectInitialFile_clicked)
        self.checkBoxRelativePath.toggled.connect(self.checkBoxRelativePath_toggled)
        self.radioButtonDefaultHPDirectory.toggled.connect(self.radioButtonDefaultHPDirectory_toggled)
        self.pushButtonRefDirectory.clicked.connect(self.pushButtonRefDirectory_clicked)
        self.tabWidget.currentChanged.connect(self.tabWidget_currentChanged)
        self.buttonSelectSequenceFromParamFile.clicked.connect(self.buttonSelectSequenceFromParamFile_clicked)
        self.pushButtonSelectParameterMapFile.clicked.connect(self.pushButtonSelectParameterMapFile_clicked)
        self.pushButtonSelectComparisonMapFile.clicked.connect(self.pushButtonSelectComparisonMapFile_clicked)
        self.pushButtonSelectStatisticFile.clicked.connect(self.pushButtonSelectStatisticFile_clicked)

    def add_validator(self):
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)

        self.lineEditModelVariableConversionFactor.setValidator(decimalValidator)
        self.lineEditMeasuredVariableConversionFactor.setValidator(decimalValidator)
        self.lineEditWeighingFactor.setValidator(decimalValidator)
        self.lineEditPenaltyConstant.setValidator(decimalValidator)

    def initial_setting(self):
        self.comboBoxParameterType.addItems(['GIS Parameter', 'Vegetation Parameter', 'EPC Parameter', 'Soil Parameter'])
        self.comboBoxParameterType.setCurrentIndex(-1)

        observation_data_type_list = ['Model Output', 'Measured Data']
        self.comboObservationDataType.addItems(observation_data_type_list)
        self.comboObservationDataType.setCurrentIndex(1)


        self.comboCostFunction.addItems(self.obj_function_list)
        self.comboCostFunction.setCurrentIndex(0)

        self.tableComparisonOption.setColumnCount(11)
        comparison_table_header_list = ['Variable (sim)', 'Variable (obs)', 'Group Name', 'Observation Data Filename',
                                        'Pair Variable (sim)', 'Pair Variable (obs)', 'Conv. Factor (sim)',
                                        'Conv. Factor (obs)', 'Wt. Factor', 'Objective Function', '']
        self.tableComparisonOption.setHorizontalHeaderLabels(comparison_table_header_list)
        self.tableComparisonOption.setColumnWidth(0, 180)
        self.tableComparisonOption.setColumnWidth(1, 180)
        self.tableComparisonOption.setColumnWidth(2, 220)
        self.tableComparisonOption.setColumnWidth(3, 250)
        self.tableComparisonOption.setColumnWidth(4, 180)
        self.tableComparisonOption.setColumnWidth(5, 180)
        self.tableComparisonOption.setColumnWidth(6, 120)
        self.tableComparisonOption.setColumnWidth(7, 120)
        self.tableComparisonOption.setColumnWidth(8, 100)
        self.tableComparisonOption.setColumnWidth(9, 200)
        self.tableComparisonOption.setColumnWidth(10, 50)

        self.checkBoxSpecifyIndex.setEnabled(False)
        self.pushButtonInitialFile.setEnabled(False)
        self.labelNotes.setText('')

        self.tableSelectedParameters.setColumnCount(8)
        self.tableSelectedParameters.setHorizontalHeaderLabels(['Parameter Name', 'Type', 'Identifying Info', 'Sequence',
                                                                'Start Value', 'Lower Bound', 'Upper Bound', ''])
        self.tableSelectedParameters.setColumnWidth(0, 200)
        self.tableSelectedParameters.setColumnWidth(1, 150)
        self.tableSelectedParameters.setColumnWidth(2, 350)
        self.tableSelectedParameters.setColumnWidth(3, 120)
        self.tableSelectedParameters.setColumnWidth(4, 120)
        self.tableSelectedParameters.setColumnWidth(5, 120)
        self.tableSelectedParameters.setColumnWidth(6, 120)
        self.tableSelectedParameters.setColumnWidth(7, 40)
        self.checkBoxOverrideObjFun.setChecked(True)

        #initial settings for evaluator configuration options
        self.radioButtonCreateConfigFile.setChecked(True)
        self.comboBoxNormalizationOption.addItems(self.normalization_option)
        self.comboBoxNormalizationOption.setCurrentIndex(-1)
        self.comboBoxObjectiveFunction.addItems(self.obj_function_list)
        self.comboBoxObjectiveFunction.setCurrentIndex(-1)
        self.comboBoxObjectiveTarget.addItems(self.objective_targets)
        self.comboBoxObjectiveTarget.setCurrentIndex(-1)
        self.comboBoxPenaltyFunction.addItems(self.penalty_function)
        self.comboBoxPenaltyFunction.setCurrentIndex(-1)
        self.comboBoxParamSequenceOption.addItems(self.param_sequence_options)
        self.comboBoxParamSequenceOption.setCurrentIndex(-1)
        self.buttonChooseConfigFile.setEnabled(False)
        self.labelSelectedConfigFile.setText('')
        self.labelSelectedConfigFile.setVisible(False)
        self.frameReferenceDirectory.setEnabled(False)
        self.labelReferenceDirectory.setText(os.path.join(ApplicationProperty.getScriptPath(), 'hopspack/'))
        self.buttonSave.setText('Save Parameter')
        self.comboBoxNormalizationOption.setEnabled(False)
        self.comboBoxObjectiveFunction.setEnabled(False)
        self.comboBoxPenaltyFunction.setEnabled(False)
        self.lineEditPenaltyConstant.setEnabled(False)
        self.lineEditStatFileName.setEnabled(False)
        self.pushButtonSelectStatisticFile.setEnabled(False)

    def pushButtonSelectComparisonMapFile_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Comparison Variable-Map File', init_dir, 'Comparison File (*.txt)')
        if filename: self.lineEditConfigComparisonMapFile.setText(filename)

    def pushButtonSelectStatisticFile_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        filename = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Statistics File', init_dir, 'Statistics File (*.txt)')
        if filename: self.lineEditStatFileName.setText(filename)


    def pushButtonSelectParameterMapFile_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')

        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Parameter-Map File', init_dir, 'Parameter File (*.txt)')
        if filename:
            self.lineEditConfigParameterFile.setText(filename)

    def buttonSelectSequenceFromParamFile_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Parameter-Map File', init_dir, 'Parameter File (*.txt)')
        if filename:
            param_list = []
            TargetParameter.read_parameter_list(filename, param_list)
            if param_list:
                seq = TargetParameter.ParameterSequence(param_list)
                self.lineEditSequence.setText(str(seq)[1:-1])

    def tabWidget_currentChanged(self):
        ndx = self.tabWidget.currentIndex()
        if ndx == 0: self.buttonSave.setText('Save Parameter')
        elif ndx == 1: self.buttonSave.setText('Save Comp. Variable')
        elif ndx == 2: self.buttonSave.setText('Save Configuration')

    def pushButtonRefDirectory_clicked(self):
        init_dir = ApplicationProperty.getScriptPath()
        home_dir = QtWidgets.QFileDialog.getExistingDirectory(self.form, 'HOPSPACK Home Directory', init_dir)
        if home_dir:
            self.labelReferenceDirectory.setText(home_dir)
            target_filename = self.lineEditBBGCHomeDir.text().strip()
            if target_filename: self.lineEditBBGCHomeDir.setText(os.path.relpath(target_filename, home_dir))
            target_filename = self.lineEditConfigParameterFile.text().strip()
            if target_filename: self.lineEditConfigParameterFile.setText(os.path.relpath(target_filename, home_dir))
            target_filename = self.lineEditConfigComparisonMapFile.text().strip()
            if target_filename: self.lineEditConfigComparisonMapFile.setText(os.path.relpath(target_filename, home_dir))
            target_filename = self.lineEditStatFileName.text().strip()
            if target_filename: self.lineEditStatFileName.setText(os.path.relpath(target_filename, home_dir))

    def checkBoxRelativePath_toggled(self):
        if self.checkBoxRelativePath.isChecked():
            self.frameReferenceDirectory.setEnabled(True)
            if not self.radioButtonDefaultHPDirectory.isChecked():
                self.radioButtonDefaultHPDirectory.setChecked(True)
            else:
                self.radioButtonDefaultHPDirectory_toggled()

        else:
            home_dir = self.labelReferenceDirectory.text()
            if home_dir:
                target_filename = self.lineEditBBGCHomeDir.text().strip()
                if target_filename: self.lineEditBBGCHomeDir.setText(ApplicationProperty.get_absolute_path(target_filename, home_dir))
                target_filename = self.lineEditConfigParameterFile.text().strip()
                if target_filename: self.lineEditConfigParameterFile.setText(ApplicationProperty.get_absolute_path(target_filename, home_dir))
                target_filename = self.lineEditConfigComparisonMapFile.text().strip()
                if target_filename: self.lineEditConfigComparisonMapFile.setText(ApplicationProperty.get_absolute_path(target_filename, home_dir))
                target_filename = self.lineEditStatFileName.text().strip()
                if target_filename: self.lineEditStatFileName.setText(ApplicationProperty.get_absolute_path(target_filename, home_dir))
            self.frameReferenceDirectory.setEnabled(False)

    def radioButtonDefaultHPDirectory_toggled(self):
        if self.radioButtonDefaultHPDirectory.isChecked():
            self.pushButtonRefDirectory.setEnabled(False)
            self.labelReferenceDirectory.setText(os.path.join(ApplicationProperty.getScriptPath(), 'hopspack/'))
            home_dir = self.labelReferenceDirectory.text()
            if home_dir:
                target_filename = self.lineEditBBGCHomeDir.text().strip()
                if target_filename: self.lineEditBBGCHomeDir.setText(os.path.relpath(target_filename, home_dir))
                target_filename = self.lineEditConfigParameterFile.text().strip()
                if target_filename: self.lineEditConfigParameterFile.setText(os.path.relpath(target_filename, home_dir))
                target_filename = self.lineEditConfigComparisonMapFile.text().strip()
                if target_filename: self.lineEditConfigComparisonMapFile.setText(os.path.relpath(target_filename, home_dir))
                target_filename = self.lineEditStatFileName.text().strip()
                if target_filename: self.lineEditStatFileName.setText(os.path.relpath(target_filename, home_dir))
        else:
            home_dir = self.labelReferenceDirectory.text()
            if home_dir:
                target_filename = self.lineEditBBGCHomeDir.text().strip()
                if target_filename: self.lineEditBBGCHomeDir.setText(ApplicationProperty.get_absolute_path(target_filename, home_dir))
                target_filename = self.lineEditConfigParameterFile.text().strip()
                if target_filename: self.lineEditConfigParameterFile.setText(ApplicationProperty.get_absolute_path(target_filename, home_dir))
                target_filename = self.lineEditConfigComparisonMapFile.text().strip()
                if target_filename: self.lineEditConfigComparisonMapFile.setText(ApplicationProperty.get_absolute_path(target_filename, home_dir))
                target_filename = self.lineEditStatFileName.text().strip()
                if target_filename: self.lineEditStatFileName.setText(ApplicationProperty.get_absolute_path(target_filename, home_dir))

            self.pushButtonRefDirectory.setEnabled(True)
            self.labelReferenceDirectory.setText('')

    def pushButtonSelectInitialFile_clicked(self):
        cur_dir = ApplicationProperty.currentModelDirectory
        if not cur_dir: cur_dir = ApplicationProperty.getScriptPath()

        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Select Initialization File', cur_dir, 'Initial File (*.ini)')
        if filename:
            self.lineEditConfigInitializationFile.setText(os.path.split(filename)[1])

    def buttonChooseConfigFile_clicked(self):
        cur_dir = ApplicationProperty.getScriptPath()

        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Select File', cur_dir, "Configuration File (*.txt)")

        if filename:
            config = Configure(filename)
            if config:
                if not config.relative_path_flag and config.is_relative_address_used(): config.relative_path_flag = True

                self.config = config
                self.labelSelectedConfigFile.setVisible(True)
                self.labelSelectedConfigFile.setText('(' + filename + ')')
                self.set_evaluator_configuration_filed_values()
            else:
                self.labelSelectedConfigFile.setText('')
                self.labelSelectedConfigFile.setVisible(False)

    def buttonBGCHomeDir_clicked(self):
        cur_dir = ApplicationProperty.currentModelDirectory
        if not cur_dir: cur_dir = ApplicationProperty.getScriptPath()

        dir_name = QtWidgets.QFileDialog.getExistingDirectory(self.form, 'Model Home Directory', cur_dir)
        if dir_name:
            if not ApplicationProperty.currentModelDirectory: ApplicationProperty.currentModelDirectory = dir_name
            self.lineEditBBGCHomeDir.setText(dir_name)

    def comboBoxParamSequenceOption_currentIndexChanged(self):
        cur_ndx = self.comboBoxParamSequenceOption.currentIndex()

        if cur_ndx == 1:
            self.buttonSelectSequenceFromParamFile.setEnabled(True)
            self.lineEditSequence.clear()
            self.lineEditSequence.setEnabled(True)
            pm_filename = self.lineEditConfigParameterFile.text()
            if pm_filename:
                param_list = []
                TargetParameter.read_parameter_list(pm_filename, param_list)
                if param_list:
                    seq = TargetParameter.ParameterSequence(param_list)
                    self.lineEditSequence.setText(str(seq)[1:-1])
        elif cur_ndx == 2:
            self.buttonSelectSequenceFromParamFile.setEnabled(False)
            self.lineEditSequence.setEnabled(True)
            pm_filename = self.lineEditConfigParameterFile.text()
            if pm_filename:
                param_list = []
                TargetParameter.read_parameter_list(pm_filename, param_list)
                if param_list:
                    seq = TargetParameter.GenerateRandomSequence(len(param_list))
                    self.lineEditSequence.setText(str(seq)[1:-1])
        elif cur_ndx == 3:
            self.buttonSelectSequenceFromParamFile.setEnabled(False)
            self.lineEditSequence.clear()
            self.lineEditSequence.setEnabled(True)
        else:
            self.buttonSelectSequenceFromParamFile.setEnabled(False)
            self.lineEditSequence.clear()
            self.lineEditSequence.setEnabled(False)

    def radioButtonConfigFile_toggled(self):
        if self.radioButtonCreateConfigFile.isChecked():
            self.buttonChooseConfigFile.setEnabled(False)
            self.labelSelectedConfigFile.setVisible(False)
            self.clear_evaluator_configuration_fileds()
        else:
            self.buttonChooseConfigFile.setEnabled(True)
            if not self.selected_config_file:
                self.labelSelectedConfigFile.setText('')
                self.clear_evaluator_configuration_fileds()
            else:
                self.labelSelectedConfigFile.setText('(' + self.selected_config_file + ')')
                self.config = Configure(self.selected_config_file)
                if self.config:
                    self.set_evaluator_configuration_filed_values()
            self.labelSelectedConfigFile.setVisible(True)

    def clear_evaluator_configuration_fileds(self):
        self.lineEditBBGCHomeDir.clear()
        self.lineEditConfigInitializationFile.clear()
        self.lineEditConfigParameterFile.clear()
        self.lineEditConfigComparisonMapFile.clear()
        self.lineEditFileExtensionPostFix.clear()
        self.checkBoxSaveStatistics.setChecked(False)
        self.checkBoxNormalizeData.setChecked(False)
        self.checkBoxUseGlobalObjFun.setChecked(False)
        self.comboBoxObjectiveTarget.setCurrentIndex(-1)
        self.checkBoxUsePenaltyFun.setChecked(False)
        self.checkBoxRelativePath.setChecked(False)

    def set_evaluator_configuration_filed_values(self):
        if self.config:
            # relative path
            if self.config.relative_path_flag:
                self.checkBoxRelativePath.setChecked(True)
                if self.config.reference_directory:
                    self.radioButtonSetHPDirectory.setChecked(True)
                    self.labelReferenceDirectory.setText(self.config.reference_directory)
            else: self.checkBoxRelativePath.setChecked(False)

            self.lineEditBBGCHomeDir.setText(self.config.model_directory)
            self.lineEditConfigInitializationFile.setText(self.config.initial_filename)
            self.lineEditConfigParameterFile.setText(self.config.parameterMap_file)
            self.lineEditConfigComparisonMapFile.setText(self.config.comparisonMap_file)
            self.lineEditFileExtensionPostFix.setText(self.config.extension_postfix)

            # saving statistics option
            if self.config.stat_filename: self.checkBoxSaveStatistics.setChecked(True)
            else: self.checkBoxSaveStatistics.setChecked(False)

            # normalization option
            if self.config.normalization_option_flag > -1:
                self.checkBoxNormalizeData.setChecked(True)
            else: self.checkBoxNormalizeData.setChecked(False)

            # objective function
            if self.config.objective_function: self.checkBoxUseGlobalObjFun.setChecked(True)
            else: self.checkBoxUseGlobalObjFun.setChecked(False)

            # objective target
            if self.config.objective_target in ['Maximize Fit']:
                self.comboBoxObjectiveTarget.setCurrentIndex(0)
            elif self.config.objective_target in ['Minimize Error']:
                self.comboBoxObjectiveTarget.setCurrentIndex(1)
            else: self.comboBoxObjectiveTarget.setCurrentIndex(-1)

            # penalty function
            if self.config.penalty_option_flag == -1:
                self.checkBoxUsePenaltyFun.setChecked(False)
            else: self.checkBoxUsePenaltyFun.setChecked(True)

            if self.config.parameter_sequence:
                self.comboBoxParamSequenceOption.setCurrentIndex(3)
                self.lineEditSequence.setText(str(self.config.parameter_sequence)[1:-1])
            else:
                self.comboBoxParamSequenceOption.setCurrentIndex(0)

    def read_configuration_field_values(self):

        home_directory = self.lineEditBBGCHomeDir.text().strip()
        initial_filename = self.lineEditConfigInitializationFile.text().strip()
        param_map_file = self.lineEditConfigParameterFile.text().strip()
        comp_map_file = self.lineEditConfigComparisonMapFile.text().strip()
        extention_postfix = self.lineEditFileExtensionPostFix.text().strip()
        stat_filename, normalization_option, objective_function, penalty_function, reference_directory = '', '', '', '', ''
        stat_flag = self.checkBoxSaveStatistics.isChecked()
        normalize_flag = self.checkBoxNormalizeData.isChecked()
        objfun_flag = self.checkBoxUseGlobalObjFun.isChecked()
        penalty_flag = self.checkBoxUsePenaltyFun.isChecked()
        relative_path_flag = self.checkBoxRelativePath.isChecked()
        if stat_flag: stat_filename = self.lineEditStatFileName.text().strip()
        if normalize_flag: normalization_option = self.comboBoxNormalizationOption.currentText()
        if objfun_flag: objective_function = self.comboBoxObjectiveFunction.currentText()
        objective_target = self.comboBoxObjectiveTarget.currentText()
        penalty_constant = -9999
        if penalty_flag:
            penalty_function = self.comboBoxPenaltyFunction.currentText()
            try: penalty_constant = float(self.lineEditPenaltyConstant.text())
            except: pass
        seq_option = self.comboBoxParamSequenceOption.currentIndex()
        param_seq = self.lineEditSequence.text()
        if relative_path_flag:  reference_directory = self.labelReferenceDirectory.text()

        if not home_directory:
            message = 'Please insert Biome BGC Model home directory.'
            self.lineEditBBGCHomeDir.setFocus(True)
        elif not initial_filename:
            message = 'Please insert or select model initialization filename.'
            self.lineEditConfigInitializationFile.setFocus(True)
        elif not param_map_file:
            message = 'Please insert parameter-map file.'
            self.lineEditConfigParameterFile.setFocus(True)
        elif not comp_map_file:
            message = 'Please insert comparison variable-map file.'
            self.lineEditConfigComparisonMapFile.setFocus(True)
        elif not extention_postfix:
            message = 'Please insert extention postfix for temporary files to avoid collision.'
            self.lineEditFileExtensionPostFix.setFocus(True)
        elif stat_flag and not stat_filename:
            message = 'Satatics file is not specified. Please insert statistics filename.'
            self.lineEditStatFileName.setFocus(True)
        elif normalize_flag and not normalization_option:
            message = 'Normalization option is not selected. Please select normalization option.'
            self.comboBoxNormalizationOption.setFocus(True)
        elif objfun_flag and not objective_function:
            message = 'Objective function is not specified. Please choose objective function.'
            self.checkBoxUseGlobalObjFun.setFocus(True)
        elif not objective_target:
            message = 'Objective target is not chosen. Please select objective target.'
            self.comboBoxObjectiveTarget.setFocus(True)
        elif penalty_flag and (not penalty_function or penalty_constant == -9999):
            if not penalty_function:
                message = 'Penalty function was not chosen. Please choose penalty function.'
                self.comboBoxPenaltyFunction.setFocus(True)
            else:
                message = 'Please insert penalty constant.'
                self.lineEditPenaltyConstant.setFocus(True)
        elif seq_option == -1:
            message = 'Please choose parameter sequence option.'
            self.comboBoxParamSequenceOption.setFocus(True)
        elif seq_option > 0 and not param_seq:
            message = 'Please insert parameter sequence.'
            self.comboBoxParamSequenceOption.setFocus(True)
        elif relative_path_flag and not reference_directory:
            message = 'Please set the reference directory.'
        else:
            if self.radioButtonUpdateConfigFile.isChecked():
                if self.config:
                    self.config.model_directory = home_directory
                    self.config.initial_filename = initial_filename
                    self.config.parameterMap_file = param_map_file
                    self.config.comparisonMap_file = comp_map_file
                    self.config.extension_postfix = extention_postfix
                    if stat_flag: self.config.stat_filename = stat_filename
                    self.config.normalization_option_flag = self.config.get_normalization_flag(normalization_option)
                    if objfun_flag: self.config.objective_function = objective_function
                    self.config.objective_target = objective_target
                    self.config.penalty_option_flag = self.config.get_penalty_flag(penalty_function)
                    if penalty_flag: self.config.penalty_constant = penalty_constant
                    self.config.relative_path_flag = relative_path_flag
                    self.config.reference_directory = reference_directory

                    temp = param_seq.split(',')
                    for i in range(len(temp)):
                        try: temp[i] = int(temp[i])
                        except:
                            temp = []
                            break
                    self.config.parameter_sequence = temp
                    return True
            else:
                config = Configure()
                config.model_directory = home_directory
                config.initial_filename = initial_filename
                config.parameterMap_file = param_map_file
                config.comparisonMap_file = comp_map_file
                config.extension_postfix = extention_postfix
                if stat_flag: config.stat_filename = stat_filename
                config.normalization_option_flag = config.get_normalization_flag(normalization_option)
                if objfun_flag: config.objective_function = objective_function
                config.objective_target = objective_target
                config.penalty_option_flag = config.get_penalty_flag(penalty_function)
                if penalty_flag: config.penalty_constant = penalty_constant
                config.relative_path_flag = relative_path_flag
                config.reference_directory = reference_directory

                temp = param_seq.split(',')
                for i in range(len(temp)):
                    try: temp[i] = int(temp[i])
                    except:
                        temp = []
                        break
                config.parameter_sequence = temp
                self.config = config
                return True

        if message:
            QtGui.QMessageBox.about(self.form, 'Input Required', message)
        return False

    def checkBoxSaveStatistics_toggled(self):
        self.lineEditStatFileName.clear()
        if not self.checkBoxSaveStatistics.isChecked():
            self.lineEditStatFileName.setEnabled(False)
            self.pushButtonSelectStatisticFile.setEnabled(False)
        else:
            if self.config:
                self.lineEditStatFileName.setText(self.config.stat_filename)
            self.lineEditStatFileName.setEnabled(True)
            self.pushButtonSelectStatisticFile.setEnabled(True)

    def checkBoxNormalizeData_toggled(self):
        self.comboBoxNormalizationOption.setCurrentIndex(-1)
        if not self.checkBoxNormalizeData.isChecked():
            self.comboBoxNormalizationOption.setEnabled(False)
        else:
            if self.config:
                self.comboBoxNormalizationOption.setCurrentIndex(self.config.normalization_option_flag)
            self.comboBoxNormalizationOption.setEnabled(True)

    def checkBoxUseGlobalObjFun_toggled(self):
        self.comboBoxObjectiveFunction.setCurrentIndex(-1)

        if not self.checkBoxUseGlobalObjFun.isChecked():
            self.comboBoxObjectiveFunction.setEnabled(False)
        else:
            if self.config:
                for i in range(len(self.obj_function_list)):
                    fun = self.obj_function_list[i]
                    if fun == self.config.objective_function:
                        self.comboBoxObjectiveFunction.setCurrentIndex(i)
                        break

            self.comboBoxObjectiveFunction.setEnabled(True)

    def checkBoxUsePenaltyFun_toggled(self):
        if not self.checkBoxUsePenaltyFun.isChecked():
            self.comboBoxPenaltyFunction.setCurrentIndex(-1)
            self.comboBoxPenaltyFunction.setEnabled(False)
            self.lineEditPenaltyConstant.clear()
            self.lineEditPenaltyConstant.setEnabled(False)
        else:
            if self.config:
                self.comboBoxPenaltyFunction.setCurrentIndex(self.config.penalty_option_flag)
                if self.config.penalty_constant > 0:
                    self.lineEditPenaltyConstant.setText(str(self.config.penalty_constant))
            else:
                self.comboBoxPenaltyFunction.setCurrentIndex(-1)
                self.lineEditPenaltyConstant.setText('')
            self.comboBoxPenaltyFunction.setEnabled(True)
            self.lineEditPenaltyConstant.setEnabled(True)

    def checkBoxOverrideObjFun_toggled(self):
        if self.checkBoxOverrideObjFun.isChecked(): self.comboCostFunction.setEnabled(True)
        else: self.comboCostFunction.setEnabled(False)

    def buttonLoadFromFile_clicked(self):
        target_dir = ApplicationProperty.currentModelDirectory
        if not target_dir: target_dir = ApplicationProperty.getScriptPath()

        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Select Parameter File', target_dir, 'Parameter File (*.txt)')

        if filename:
            param_list = []

            if TargetParameter.read_parameter_list(filename, param_list):
                for param in param_list:
                    param.sequence = len(self.parameter_list)
                    self.parameter_list.append(param)
                self.show_selected_parameter_list()
            else:
                message = 'Parameter file could not be oppened. Please check the parameter file.'
                QtGui.QMessageBox.about(self.form, 'Invalid Parameter File', message)

    def checkBoxPreferred_toggled(self):
        self.clear_selected_parameter_table()

        if self.checkBoxPreferred.isChecked():
            self.tableSelectedParameters.setColumnCount(10)
            header_item = ['Parameter Name', 'Type', 'Identifying Info', 'Sequence', 'Start Value', 'Lower Bound (H)', 'Lower Bound (P)',
                           'Upper Bound (P)', 'Upper Bound (H)', '']
            self.tableSelectedParameters.setHorizontalHeaderLabels(header_item)
            self.tableSelectedParameters.setColumnWidth(0, 200)
            self.tableSelectedParameters.setColumnWidth(1, 150)
            self.tableSelectedParameters.setColumnWidth(2, 350)
            self.tableSelectedParameters.setColumnWidth(3, 120)
            self.tableSelectedParameters.setColumnWidth(4, 120)
            self.tableSelectedParameters.setColumnWidth(5, 120)
            self.tableSelectedParameters.setColumnWidth(6, 120)
            self.tableSelectedParameters.setColumnWidth(7, 120)
            self.tableSelectedParameters.setColumnWidth(8, 120)
            self.tableSelectedParameters.setColumnWidth(9, 40)
        else:
            self.tableSelectedParameters.setColumnCount(8)
            header_item = ['Parameter Name', 'Type', 'Identifying Info', 'Sequence', 'Start Value', 'Lower Bound', 'Upper Bound', '']
            self.tableSelectedParameters.setHorizontalHeaderLabels(header_item)
            self.tableSelectedParameters.setColumnWidth(0, 200)
            self.tableSelectedParameters.setColumnWidth(1, 150)
            self.tableSelectedParameters.setColumnWidth(2, 350)
            self.tableSelectedParameters.setColumnWidth(3, 120)
            self.tableSelectedParameters.setColumnWidth(4, 120)
            self.tableSelectedParameters.setColumnWidth(5, 120)
            self.tableSelectedParameters.setColumnWidth(6, 120)
            self.tableSelectedParameters.setColumnWidth(7, 40)

        self.comboBoxParameterType_currentIndexChanged()

    def clear_selected_parameter_table(self):
        for i in reversed(range(self.tableSelectedParameters.rowCount())):
            self.tableSelectedParameters.removeRow(i)

        for i in reversed(range(self.tableSelectedParameters.columnCount())):
            self.tableSelectedParameters.removeColumn(i)

    def buttonAddToList_clicked(self):
        validate = self.validate_chosen_parameter()
        if not validate:
            message = 'The values for bounds and starting value are found inconsistent. Inconsistent values are ' +\
                      'marked by red. Please check the values in colored cells.'
            QtGui.QMessageBox.about(self.form, 'Check input values', message)
        else:
            has_index = self.checkBoxSpecifyIndex.isChecked()
            has_preferred_boundary = self.checkBoxPreferred.isChecked()

            nrow = self.tableParameterSelection.rowCount()
            if has_preferred_boundary:
                for i in range(nrow):
                    checkbox = self.tableParameterSelection.cellWidget(i, 1).findChildren(QtGui.QCheckBox)[0]
                    if checkbox.isChecked():
                        param = TargetParameter()

                        param.name = self.tableParameterSelection.item(i, 0).text()
                        param.type = self.comboBoxParameterType.currentText()
                        param.has_index = has_index

                        param.has_preferred_boundary = has_preferred_boundary

                        start_val, lbound_hrd, lbound_prf, ubound_prf, ubound_hrd = None, None, None, None, None

                        try:
                            start_val = float(self.tableParameterSelection.item(i, 2).text())
                            lbound_hrd = float(self.tableParameterSelection.item(i, 3).text())
                            lbound_prf = float(self.tableParameterSelection.item(i, 4).text())
                            ubound_prf = float(self.tableParameterSelection.item(i, 5).text())
                            ubound_hrd = float(self.tableParameterSelection.item(i, 6).text())
                        except: pass
                        if (start_val is not None and lbound_hrd is not None and lbound_prf is not None and
                            ubound_prf is not None and ubound_hrd is not None):
                            param.starting_value = start_val
                            param.current_value = start_val

                            param.hard_lower_bound = lbound_hrd
                            param.lower_bound = lbound_prf
                            param.upper_bound = ubound_prf
                            param.hard_upper_bound = ubound_hrd

                        if has_index:
                            if param.type in ['GIS Parameter', 'Vegetation Parameter']:
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 5).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo.currentIndex() > -1: param.site_index = tmp_combo.currentText()
                            elif param.type == 'EPC Parameter':
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 5).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1: param.site_index = tmp_combo.currentText()
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 6).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1:
                                    try: param.veg_no = int(tmp_combo.currentText())
                                    except: pass
                            elif param.type == 'Soil Parameter':
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 5).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1: param.site_index = tmp_combo.currentText()
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 6).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1: param.profile_name = tmp_combo.currentText()
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 7).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1: param.horizon_name = tmp_combo.currentText()

                        if param.is_complete():
                            ndx = self.find_parameter_from_selected_list(param.name, param.type, param.get_index_text())

                            if ndx > -1:
                                message = 'Parameter \'' + param.name + '\' of type ' + param.type
                                if param.get_index_text(): message += ' (' + param.get_index_text() + ') '
                                message += 'already exists in the selected list. Do you want to overwrite the existing parameter?'
                                reply = QtGui.QMessageBox.question(self.form, 'Message', message, QtGui.QMessageBox.Yes,
                                                    QtGui.QMessageBox.No)
                                if reply == QtGui.QMessageBox.Yes:
                                    self.parameter_list[ndx] = param
                            else: self.parameter_list.append(param)
                            checkbox.setChecked(False)
            else:
                for i in range(nrow):
                    checkbox = self.tableParameterSelection.cellWidget(i, 1).findChildren(QtGui.QCheckBox)[0]
                    if checkbox.isChecked():
                        param = TargetParameter()

                        param.name = self.tableParameterSelection.item(i, 0).text()
                        param.type = self.comboBoxParameterType.currentText()
                        param.has_index = has_index

                        param.has_preferred_boundary = has_preferred_boundary

                        start_val, lbound, ubound = None, None, None
                        try:
                            start_val = float(self.tableParameterSelection.item(i, 2).text())
                            lbound = float(self.tableParameterSelection.item(i, 3).text())
                            ubound = float(self.tableParameterSelection.item(i, 4).text())
                        except: pass
                        if start_val is not None and lbound is not None and ubound is not None:
                            param.starting_value = start_val
                            param.current_value = start_val
                            param.lower_bound = lbound
                            param.upper_bound = ubound

                        if has_index:
                            if param.type in ['GIS Parameter', 'Vegetation Parameter']:
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 5).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo.currentIndex() > -1: param.site_index = tmp_combo.currentText()
                            elif param.type == 'EPC Parameter':
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 5).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1: param.site_index = tmp_combo.currentText()
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 6).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1:
                                    try: param.veg_no = int(tmp_combo.currentText())
                                    except: pass
                            elif param.type == 'Soil Parameter':
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 5).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1: param.site_index = tmp_combo.currentText()
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 6).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1: param.profile_name = tmp_combo.currentText()
                                tmp_combo = self.tableParameterSelection.cellWidget(i, 7).findChildred(QtGui.QComboBox)[0]
                                if tmp_combo and tmp_combo.currentIndex() > -1: param.horizon_name = tmp_combo.currentText()

                        if param.is_complete():
                            ndx = self.find_parameter_from_selected_list(param.name, param.type, param.get_index_text())

                            if ndx > -1:
                                message = 'Parameter \'' + param.name + '\' of type ' + param.type
                                if param.get_index_text(): message += ' (' + param.get_index_text() + ') '
                                message += 'already exists in the selected list. Do you want to overwrite the existing parameter?'
                                reply = QtGui.QMessageBox.question(self.form, 'Message', message, QtGui.QMessageBox.Yes,
                                                    QtGui.QMessageBox.No)
                                if reply == QtGui.QMessageBox.Yes:
                                    param.sequence = ndx
                                    self.parameter_list[ndx] = param
                            else:
                                param.sequence = len(self.parameter_list)
                                self.parameter_list.append(param)
                            checkbox.setChecked(False)

            self.show_selected_parameter_list()

    def find_parameter_from_selected_list(self, param_name, param_type, param_ref):
        for i in range(len(self.parameter_list)):
            p = self.parameter_list[i]

            if p.name == param_name and p.type == param_type and p.get_index_text() == param_ref:
                return i
        return -1

    def show_selected_parameter_list(self):
        #delete existing rows
        for i in reversed(range(self.tableSelectedParameters.rowCount())): self.tableSelectedParameters.removeRow(i)

        preferred_bound = self.checkBoxPreferred.isChecked()
        if preferred_bound:
            for param in self.parameter_list:
                rindex = self.tableSelectedParameters.rowCount()
                self.tableSelectedParameters.insertRow(rindex)
                self.tableSelectedParameters.setRowHeight(rindex, 22)
                item = QtWidgets.QTableWidgetItem(param.name)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableSelectedParameters.setItem(rindex, 0, item)
                item = QtWidgets.QTableWidgetItem(param.type)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableSelectedParameters.setItem(rindex, 1, item)
                item = QtWidgets.QTableWidgetItem(param.get_index_text())
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableSelectedParameters.setItem(rindex, 2, item)
                item = QtWidgets.QTableWidgetItem(str(param.sequence))
                self.tableSelectedParameters.setItem(rindex, 3, item)
                item = QtWidgets.QTableWidgetItem(int(param.starting_value))
                self.tableSelectedParameters.setItem(rindex, 4, item)
                item = QtWidgets.QTableWidgetItem(int(param.hard_lower_bound))
                self.tableSelectedParameters.setItem(rindex, 5, item)
                item = QtWidgets.QTableWidgetItem(int(param.lower_bound))
                self.tableSelectedParameters.setItem(rindex, 6, item)
                item = QtWidgets.QTableWidgetItem(int(param.upper_bound))
                self.tableSelectedParameters.setItem(rindex, 7, item)
                item = QtWidgets.QTableWidgetItem(int(param.hard_upper_bound))
                self.tableSelectedParameters.setItem(rindex, 8, item)
                item = QtGui.QPushButton()
                item.setMaximumWidth(35)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/delete.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(icon)
                item.rindex = rindex
                item.clicked.connect(self.deletePamamButtonSignalMapper.map)
                self.deletePamamButtonSignalMapper.setMapping(item, item)
                layout = QtGui.QHBoxLayout()
                layout.addWidget(item)
                layout.setAlignment(QtCore.Qt.AlignCenter)
                layout.setContentsMargins(0,0,0,0)
                cell = QtWidgets.QWidget()
                cell.setLayout(layout)
                self.tableSelectedParameters.setCellWidget(rindex, 9, cell)
        else:
            for param in self.parameter_list:
                rindex = self.tableSelectedParameters.rowCount()
                self.tableSelectedParameters.insertRow(rindex)
                self.tableSelectedParameters.setRowHeight(rindex, 22)
                item = QtWidgets.QTableWidgetItem(param.name)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableSelectedParameters.setItem(rindex, 0, item)
                item = QtWidgets.QTableWidgetItem(param.type)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableSelectedParameters.setItem(rindex, 1, item)
                item = QtWidgets.QTableWidgetItem(param.get_index_text())
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableSelectedParameters.setItem(rindex, 2, item)
                item = QtWidgets.QTableWidgetItem(str(param.sequence))
                self.tableSelectedParameters.setItem(rindex, 3, item)
                item = QtWidgets.QTableWidgetItem(str(param.starting_value))
                self.tableSelectedParameters.setItem(rindex, 4, item)
                item = QtWidgets.QTableWidgetItem(str(param.lower_bound))
                self.tableSelectedParameters.setItem(rindex, 5, item)
                item = QtWidgets.QTableWidgetItem(str(param.upper_bound))
                self.tableSelectedParameters.setItem(rindex, 6, item)
                item = QtGui.QPushButton()
                item.setMaximumWidth(35)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/delete.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(icon)
                item.rindex = rindex
                item.clicked.connect(self.deletePamamButtonSignalMapper.map)
                self.deletePamamButtonSignalMapper.setMapping(item, item)
                layout = QtGui.QHBoxLayout()
                layout.addWidget(item)
                layout.setAlignment(QtCore.Qt.AlignCenter)
                layout.setContentsMargins(0,0,0,0)
                cell = QtWidgets.QWidget()
                cell.setLayout(layout)
                self.tableSelectedParameters.setCellWidget(rindex, 7, cell)

    def tableSelectedParameters_itemChanged(self):
        item = self.tableSelectedParameters.currentItem()

        if item and item.text():
            pndx = item.row()
            param = self.parameter_list[pndx]

            message = ''

            attribute = self.tableSelectedParameters.horizontalHeaderItem(item.column()).text().lower()
            if attribute == 'sequence':
                try:
                    seq = int(item.text())
                    if seq >= len(self.parameter_list):
                        message = 'Sequence cannot be equal or greater than total number of selected parameter.'
                    else: param.sequence = seq
                except: message = 'Value is not exceptable. Please enter a valid value'
            elif attribute == 'start value':
                try:
                    val = float(item.text())
                    param.starting_value = val
                except: message = 'Value is not exceptable. Please enter a valid value'
            elif attribute == 'lower bound (h)':
                try: param.hard_lower_bound = float(item.text())
                except: message = 'Value is not exceptable. Please enter a valid value'
            elif attribute in ['lower bound', 'lower bound (p)']:
                try: param.lower_bound = float(item.text())
                except: message = 'Value is not exceptable. Please enter a valid value'
            elif attribute in ['upper bound', 'upper bound (p)']:
                try: param.upper_bound = float(item.text())
                except: message = 'Value is not exceptable. Please enter a valid value'
            elif attribute == 'upper bound (h)':
                try: param.hard_upper_bound = float(item.text())
                except: message = 'Value is not exceptable. Please enter a valid value'

            #'Start Value', 'Lower Bound', 'Upper Bound'
            if message: QtGui.QMessageBox.about(self.form, 'Invalid Input', message)

            self.show_selected_parameter_list()




    def deleteParamButton_clicked(self, button_del_param):
        message = 'Are you sure you want to delete this parameter?'
        reply = QtGui.QMessageBox.question(self.form, 'Delete Parameter', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.parameter_list.pop(button_del_param.rindex)
            self.show_selected_parameter_list()

    def pushButtonInitialFile_clicked(self):
        mdir = ApplicationProperty.currentModelDirectory

        if not mdir:
            mdir = ApplicationProperty.getScriptPath()

        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Select Initialization File', mdir, 'Init File (*.ini)')

        if filename:
            if not ApplicationProperty.currentModelDirectory:
                ApplicationProperty.currentModelDirectory = filename.split('ini')[0][:-1]

            model_directory = ApplicationProperty.currentModelDirectory
            bgc_param_set = BiomeBGCParameterSet.ReadBBGCParameterSet(model_directory, filename)

            if bgc_param_set:
                self.biomeBGCParamSet = bgc_param_set
                self.labelNotes.setText('Parameter indices are generated from ' + filename)
                self.labelNotes.setVisible(True)

                site_index_list = self.biomeBGCParamSet.getSiteIndexList()
                cindex = self.column_index('Site Index')
                if cindex > -1:
                        for i in range(self.tableParameterSelection.rowCount()):
                            item = self.tableParameterSelection.cellWidget(i, cindex).findChildren(QtGui.QComboBox)[0]
                            item.clear()
                            item.addItems(site_index_list)

    def column_index(self, column_name):
        for i in range(self.tableParameterSelection.columnCount()):
            if self.tableParameterSelection.horizontalHeaderItem(i).text() == column_name:
                return i
        return -1

    def checkBoxSpecifyIndex_toggled(self):
        if self.checkBoxSpecifyIndex.isChecked():
            self.pushButtonInitialFile.setEnabled(True)
            if self.biomeBGCParamSet: self.labelNotes.setVisible(True)

            if self.tableParameterSelection.rowCount() > 0:
                ncol_add = 0
                header_label_add = []

                cur_ndx = self.comboBoxParameterType.currentIndex()
                if cur_ndx in [0, 1]:
                    ncol_add = 1
                    header_label_add = ['Site Index']
                elif cur_ndx == 2:
                    ncol_add = 2
                    header_label_add = ['Site Index', 'Veg. No.']
                elif cur_ndx == 3:
                    ncol_add = 3
                    header_label_add = ['Site Index', 'Profile Name', 'Horizon Name']

                ncol = self.tableParameterSelection.columnCount()
                self.tableParameterSelection.setColumnCount(ncol + ncol_add)
                if ncol_add == 3: self.tableParameterSelection.setColumnWidth(ncol + ncol_add - 1, 150)

                for i in range(ncol_add):
                    cndx = ncol + i
                    item = QtWidgets.QTableWidgetItem(header_label_add[i])
                    self.tableParameterSelection.setHorizontalHeaderItem(cndx, item)

                    combo_items = []
                    if header_label_add[i] == 'Site Index' and self.biomeBGCParamSet:
                        combo_items = self.biomeBGCParamSet.getSiteIndexList()

                    nrow = self.tableParameterSelection.rowCount()
                    for rndx in range(nrow):
                        item = QtGui.QComboBox()
                        item.setCurrentIndex(-1)
                        item.setMaximumHeight(22)
                        if i == 2: item.setMinimumWidth(120)
                        item.cindex = cndx
                        item.rindex = rndx
                        item.addItems(combo_items)
                        item.isactive = True
                        layout = QtGui.QHBoxLayout()
                        layout.addWidget(item)
                        layout.setAlignment(QtCore.Qt.AlignRight)
                        layout.setContentsMargins(0,0,0,0)
                        cell = QtWidgets.QWidget()
                        cell.setLayout(layout)
                        item.currentIndexChanged.connect(self.indexComboSignalMapper.map)
                        self.indexComboSignalMapper.setMapping(item, item)
                        self.tableParameterSelection.setCellWidget(rndx, cndx, cell)

                #this recurssion is necessary
                item = self.tableParameterSelection.cellWidget(0, ncol).findChildren(QtGui.QComboBox)[0]
                self.indexCombo_currentIndexChanged(item)

        else:
            self.pushButtonInitialFile.setEnabled(False)
            self.labelNotes.setVisible(False)
            if self.tableParameterSelection.rowCount() > 0:
                ncol = self.tableParameterSelection.columnCount()

                ncol_rmov = 0
                if self.checkBoxPreferred.isChecked(): ncol_rmov = ncol - 7
                else: ncol_rmov = ncol - 5

                for i in range(ncol_rmov):
                    self.tableParameterSelection.removeColumn(self.tableParameterSelection.columnCount() - 1)

    def indexCombo_currentIndexChanged(self, indexCombo):
        if indexCombo.isactive and indexCombo.currentIndex() > -1:
            column_name = self.tableParameterSelection.horizontalHeaderItem(indexCombo.cindex).text()

            next_column_combo_items = []
            if self.biomeBGCParamSet:
                if column_name == 'Site Index':
                    if self.comboBoxParameterType.currentText() == 'EPC Parameter':
                        next_column_combo_items = self.biomeBGCParamSet.getVegNoList(indexCombo.currentText())
                    elif self.comboBoxParameterType.currentText() == 'Soil Parameter':
                        next_column_combo_items = [self.biomeBGCParamSet.getProfileName(indexCombo.currentText())]
                elif column_name == 'Profile Name' and self.comboBoxParameterType.currentText() == 'Soil Parameter':
                    item = self.tableParameterSelection.cellWidget(indexCombo.rindex, indexCombo.cindex - 1).findChildren(QtGui.QComboBox)[0]
                    site_index = item.currentText()
                    next_column_combo_items = self.biomeBGCParamSet.getHorizonNameList(site_index)

                if next_column_combo_items:
                    for i in range(len(next_column_combo_items)):
                        try: next_column_combo_items[i] = str(next_column_combo_items[i])
                        except: pass

                    item = None
                    next_column_index = indexCombo.cindex + 1
                    for i in range(self.tableParameterSelection.rowCount()):
                        item =  self.tableParameterSelection.cellWidget(i, next_column_index).findChildren(QtGui.QComboBox)[0]
                        item.isactive = False
                        item.clear()
                        item.addItems(next_column_combo_items)
                        item.isactive = True
                        #item.setCurrentIndex(0)

                    #this recussion is required
                    item =  self.tableParameterSelection.cellWidget(indexCombo.rindex, next_column_index).findChildren(QtGui.QComboBox)[0]
                    self.indexCombo_currentIndexChanged(item)

            for rndx in range(self.tableParameterSelection.rowCount()):
                item = self.tableParameterSelection.cellWidget(rndx, indexCombo.cindex).findChildren(QtGui.QComboBox)[0]
                item.isactive = False
                item.setCurrentIndex(indexCombo.currentIndex())
                item.isactive = True

    def clear_Parameter_table(self):
        for i in reversed(range(self.tableParameterSelection.rowCount())):
            self.tableParameterSelection.removeRow(i)

        for i in reversed(range(self.tableParameterSelection.columnCount())):
            self.tableParameterSelection.removeColumn(i)

    def comboBoxParameterType_currentIndexChanged(self):
        cur_ndx = self.comboBoxParameterType.currentIndex()

        self.clear_Parameter_table()

        if cur_ndx >= 0:
            self.checkBoxSpecifyIndex.setEnabled(True)

            param_list = {}
            rem_item_list = []

            if cur_ndx == 0:        #GIS Parameter
                param_list = copy(GisParameter.paramLabelList)
                rem_item_list = [0, 1, 2, 3, 4, 6, 16, 17, 18]
            elif cur_ndx == 1:      #Vegetation Parameter
                param_list = copy(VegetationParameter.paramLabelList)
                rem_item_list = [0, 1, 2, 6, 8]
            elif cur_ndx == 2:      #EPC parameter
                param_list = copy(EpcParameter.paramLabelList)
                rem_item_list = [0, 1, 2, 3, 64]
            elif cur_ndx == 3:      #Soil Parameter
                param_list = copy(SoilLayer.paramLabelList)
                rem_item_list = [0]

            if rem_item_list:
                for item in rem_item_list: param_list.pop(item)

            if not self.checkBoxPreferred.isChecked():
                parameterHeader = ['Parameter Name', 'Select', 'Starting Value', 'Lower Bound', 'Upper Bound']
                self.tableParameterSelection.setColumnCount(5)
                self.tableParameterSelection.setHorizontalHeaderLabels(parameterHeader)
                self.tableParameterSelection.setColumnWidth(0, 350)
                self.tableParameterSelection.setColumnWidth(1, 100)
                self.tableParameterSelection.setColumnWidth(2, 100)
                self.tableParameterSelection.setColumnWidth(3, 100)
                self.tableParameterSelection.setColumnWidth(4, 100)

                if param_list:
                    for i in sorted(param_list.keys()):
                        row_index = self.tableParameterSelection.rowCount()
                        self.tableParameterSelection.insertRow(row_index)
                        self.tableParameterSelection.setRowHeight(row_index, 24)
                        item = QtWidgets.QTableWidgetItem(param_list[i])
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 0, item)
                        checkbox = QtGui.QCheckBox()
                        checkbox.row_index = row_index
                        layout = QtGui.QHBoxLayout()
                        layout.addWidget(checkbox)
                        layout.setAlignment(QtCore.Qt.AlignCenter)
                        layout.setContentsMargins(0,0,0,0)
                        item = QtWidgets.QWidget()
                        item.setLayout(layout)
                        self.tableParameterSelection.setCellWidget(row_index, 1, item)
                        item = QtWidgets.QTableWidgetItem('')
                        item.h_flag = True
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 2, item)
                        item = QtWidgets.QTableWidgetItem('')
                        item.h_flag = True
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 3, item)
                        item = QtWidgets.QTableWidgetItem('')
                        item.h_flag = True
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 4, item)
                        checkbox.toggled.connect(self.signalMapper.map)
                        self.signalMapper.setMapping(checkbox, checkbox)
            else:
                parameterHeader = ['Parameter Name', 'Select', 'Starting Value', 'Lower Bound (H)', 'Lower Bound (P)',
                                   'Upper Bound (P)', 'Upper Bound (H)']
                self.tableParameterSelection.setColumnCount(7)
                self.tableParameterSelection.setHorizontalHeaderLabels(parameterHeader)
                self.tableParameterSelection.setColumnWidth(0, 350)
                self.tableParameterSelection.setColumnWidth(1, 100)
                self.tableParameterSelection.setColumnWidth(2, 120)
                self.tableParameterSelection.setColumnWidth(3, 120)
                self.tableParameterSelection.setColumnWidth(4, 120)
                self.tableParameterSelection.setColumnWidth(5, 120)
                self.tableParameterSelection.setColumnWidth(6, 120)

                if param_list:
                    for i in sorted(param_list.keys()):
                        row_index = self.tableParameterSelection.rowCount()
                        self.tableParameterSelection.insertRow(row_index)
                        self.tableParameterSelection.setRowHeight(row_index, 24)
                        item = QtWidgets.QTableWidgetItem(param_list[i])
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 0, item)
                        checkbox = QtGui.QCheckBox()
                        checkbox.row_index = row_index
                        layout = QtGui.QHBoxLayout()
                        layout.addWidget(checkbox)
                        layout.setAlignment(QtCore.Qt.AlignCenter)
                        layout.setContentsMargins(0,0,0,0)
                        item = QtWidgets.QWidget()
                        item.setLayout(layout)
                        self.tableParameterSelection.setCellWidget(row_index, 1, item)
                        item = QtWidgets.QTableWidgetItem('')
                        item.h_flag = True
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 2, item)
                        item = QtWidgets.QTableWidgetItem('')
                        item.h_flag = True
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 3, item)
                        item = QtWidgets.QTableWidgetItem('')
                        item.h_flag = True
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 4, item)
                        item = QtWidgets.QTableWidgetItem('')
                        item.h_flag = True
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 5, item)
                        item = QtWidgets.QTableWidgetItem('')
                        item.h_flag = True
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableParameterSelection.setItem(row_index, 6, item)

                        checkbox.toggled.connect(self.signalMapper.map)
                        self.signalMapper.setMapping(checkbox, checkbox)

            self.checkBoxSpecifyIndex.setChecked(False)
            if self.biomeBGCParamSet: self.checkBoxSpecifyIndex.setChecked(True)

        else:
            self.checkBoxSpecifyIndex.setEnabled(False)


    def buttonLoad_clicked(self):
        initial_directory = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        file_name = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Load Comparison Variable', initial_directory, 'Comparison-Map File (*.txt)')
        if file_name:
            self.comparing_variable_list = Comparing_Variable.read_comparing_variables(file_name)
            if self.comparing_variable_list:
                self.show_comparing_variable_list()


    def buttonClose_clicked(self):
        self.form.parentWidget().close()

    def lineEditInitializationFile_textChanged(self):
        filename = os.path.join(ApplicationProperty.currentModelDirectory, 'ini', self.lineEditInitializationFile.text())
        init_param = FileReadWrite.readInitialFile(filename)
        if init_param is not None:
            #generating list of output files and check their availability
            output_file_list = ReadBinaryOutput.GenerateListOfOutputFiles(init_param, ApplicationProperty.currentModelDirectory)

            #inserting output file names in combo box
            if len(output_file_list) > 0:
                self.comboOutputFileType.addItems(output_file_list)
                self.comboOutputFileType.setCurrentIndex(-1)

    def lineEditMeasuredDataFile_textChanged(self):
        filename = self.lineEditMeasuredDataFile.text()
        if filename and self.comboObservationDataType.currentIndex() == 1:
            external_output = ReadExternalOutput.read_csv_file(filename, ',', True)
            if external_output is not None: self.listMeasuredVariable.addItems(external_output.get_header_variable())

    def buttonDeleteComparisonOption_clicked(self):
        row_index = self.tableComparisonOption.currentRow()
        if row_index >= 0:
            self.comparing_variable_list.pop(row_index)
            self.tableComparisonOption.removeRow(row_index)

    def buttonAddComparisonOption_clicked(self):
        message = ''
        if len(self.lineEditModelOutputVariable.text()) == 0:
            message = 'Please enter Model Output Variable name'
        elif len(self.lineEditMeasuredVariable.text()) == 0:
            message = 'Please enter Measured Variable name'
        elif len(self.lineEditModelPairingVariable.text()) > 0 and len(self.lineEditMeasuredPairingVariable.text()) == 0:
            message = 'Please enter pairing variable name for observation data.'
        elif len(self.lineEditModelPairingVariable.text()) == 0 and len(self.lineEditMeasuredPairingVariable.text()) > 0:
            message = 'Please enter pairing variable name for model output.'
        elif len(self.lineEditMeasuredDataFile.text()) == 0:
            message = 'Please choose observation data file.'
        else:
            output_file_type = self.comboOutputFileType.currentText()
            modelOutputVariable = self.lineEditModelOutputVariable.text()
            observationDataType = self.comboObservationDataType.currentIndex()
            observationFilename = self.lineEditMeasuredDataFile.text()
            observationVariable = self.lineEditModelOutputVariable.text()
            modelPairingVariable = self.lineEditModelPairingVariable.text()
            observationPairingVar = self.lineEditMeasuredPairingVariable.text()

            pairFlag = False
            if modelPairingVariable and observationPairingVar: pairFlag = True

            modelVarConversionFactor = 1
            observationVarConversionFactor = 1
            if len(self.lineEditModelVariableConversionFactor.text()) > 0:
                try: modelVarConversionFactor = float(self.lineEditModelVariableConversionFactor.text())
                except: pass
            if len(self.lineEditMeasuredVariableConversionFactor.text()) > 0:
                try: observationVarConversionFactor = float(self.lineEditMeasuredVariableConversionFactor.text())
                except: pass

            weighingFactor = 1
            if len(self.lineEditWeighingFactor.text()) > 0:
                try: weighingFactor = float(self.lineEditWeighingFactor.text())
                except: pass

            group_name = self.lineEditGroupName.text()
            obj_fun = ''
            if self.checkBoxOverrideObjFun.isChecked():
                obj_fun = self.comboCostFunction.currentText()

            com_var = Comparing_Variable()
            com_var.model_file_type = output_file_type
            com_var.model_variable_name = modelOutputVariable
            com_var.observation_type = observationDataType
            com_var.observation_filename = observationFilename
            com_var.observation_variable_name = observationVariable
            com_var.pairing_flag = pairFlag
            com_var.pairing_model_variable = modelPairingVariable
            com_var.pairing_observation_variable = observationPairingVar
            com_var.model_data_conversion_factor = modelVarConversionFactor
            com_var.observation_data_conversion_factor = observationVarConversionFactor
            com_var.weighing_factor = weighingFactor
            com_var.group_name = group_name
            if obj_fun: com_var.objective_function = obj_fun

            if com_var.is_complete(): self.comparing_variable_list.append(com_var)
            self.show_comparing_variable_list()

        if len(message) > 0:
            QtGui.QMessageBox.about(self.form, 'Input Required', message)

    def clear_comparaing_variable_table(self):
        for rndx in reversed(range(self.tableComparisonOption.rowCount())):
            self.tableComparisonOption.removeRow(rndx)

    def show_comparing_variable_list(self):
        self.clear_comparaing_variable_table()
        if len(self.comparing_variable_list) > 0:
            for i in reversed(range(self.tableComparisonOption.rowCount())):
                self.tableComparisonOption.removeRow(i)

            for comp_var in self.comparing_variable_list:
                row_index = self.tableComparisonOption.rowCount()
                self.tableComparisonOption.insertRow(row_index)
                self.tableComparisonOption.setRowHeight(row_index, 22)

                item = QtWidgets.QTableWidgetItem(comp_var.model_variable_name)
                self.tableComparisonOption.setItem(row_index, 0, item)
                item = QtWidgets.QTableWidgetItem(comp_var.observation_variable_name)
                self.tableComparisonOption.setItem(row_index, 1, item)
                item = QtWidgets.QTableWidgetItem(str(comp_var.group_name))
                self.tableComparisonOption.setItem(row_index, 2, item)
                item = QtWidgets.QTableWidgetItem(str(comp_var.observation_filename))
                self.tableComparisonOption.setItem(row_index, 3, item)
                item = QtWidgets.QTableWidgetItem(comp_var.pairing_model_variable)
                self.tableComparisonOption.setItem(row_index, 4, item)
                item = QtWidgets.QTableWidgetItem(comp_var.pairing_observation_variable)
                self.tableComparisonOption.setItem(row_index, 5, item)
                item = QtWidgets.QTableWidgetItem(str(comp_var.model_data_conversion_factor))
                self.tableComparisonOption.setItem(row_index, 6, item)
                item = QtWidgets.QTableWidgetItem(str(comp_var.observation_data_conversion_factor))
                self.tableComparisonOption.setItem(row_index, 7, item)
                item = QtWidgets.QTableWidgetItem(str(comp_var.weighing_factor))
                self.tableComparisonOption.setItem(row_index, 8, item)
                #item = QtWidgets.QTableWidgetItem(comp_var.objective_function)
                item = QtGui.QComboBox()
                item.setMaximumWidth(180)
                item.addItems(self.obj_function_list)
                item.rindex = row_index
                item.setCurrentIndex(-1)
                if comp_var.objective_function in self.obj_function_list:
                    for i in range(len(self.obj_function_list)):
                        if comp_var.objective_function == self.obj_function_list[i]:
                            item.setCurrentIndex(i)
                            break
                item.currentIndexChanged.connect(self.objectiveFunctionComboSignalMapper.map)
                self.objectiveFunctionComboSignalMapper.setMapping(item, item)
                layout = QtGui.QHBoxLayout()
                layout.addWidget(item)
                layout.setAlignment(QtCore.Qt.AlignRight)
                layout.setContentsMargins(0,0,0,0)
                cell = QtWidgets.QWidget()
                cell.setLayout(layout)
                self.tableComparisonOption.setCellWidget(row_index, 9, cell)
                item = QtGui.QPushButton()
                item.setMaximumWidth(35)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/delete.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(icon)
                item.rindex = row_index
                item.clicked.connect(self.deleteVariableButtonSignalMapper.map)
                self.deleteVariableButtonSignalMapper.setMapping(item, item)
                layout = QtGui.QHBoxLayout()
                layout.addWidget(item)
                layout.setAlignment(QtCore.Qt.AlignCenter)
                layout.setContentsMargins(0,0,0,0)
                cell = QtWidgets.QWidget()
                cell.setLayout(layout)
                self.tableComparisonOption.setCellWidget(row_index, 10, cell)

    def objectiveFunctionCombo_currentIndexChanged(self, combo):
        if combo.currentIndex() > -1:
            rindex = combo.rindex

            com_var = None
            if rindex > -1 and rindex < len(self.comparing_variable_list):
                com_var = self.comparing_variable_list[rindex]
                com_var.objective_function = combo.currentText()

    def tableComparisonOption_itemChanged(self):
        item = self.tableComparisonOption.currentItem()
        if item:
            rindex = item.row()
            cindex = item.column()

            com_var = None
            if -1 < rindex < len(self.comparing_variable_list):
                com_var = self.comparing_variable_list[rindex]

                if com_var:
                    val = item.text().strip()

                    if cindex in [6, 7, 8]:
                        try: val = float(val)
                        except:
                            message = 'The value must be numeric in this field. Please enter a valid number.'
                            QtGui.QMessageBox.about(self.form, 'Invalid Input', message)
                            val = None

                    if val is not None:
                        if cindex == 0: com_var.model_variable_name = val
                        elif cindex == 1: com_var.observation_variable_name = val
                        elif cindex == 2: com_var.group_name = val
                        elif cindex == 3: com_var.observation_filename = val
                        elif cindex == 4: com_var.pairing_model_variable = val
                        elif cindex == 5: com_var.pairing_observation_variable = val
                        elif cindex == 6: com_var.model_data_conversion_factor = val
                        elif cindex == 7: com_var.observation_data_conversion_factor = val
                        elif cindex == 8: com_var.weighing_factor = val
                        elif cindex == 9: com_var.objective_function = val

                        if com_var.pairing_model_variable and com_var.pairing_observation_variable:
                            com_var.pairing_flag = True
                        else: com_var.pairing_flag = False

                    self.show_comparing_variable_list()


    def deleteVariableButton_clicked(self, button):
        if button and button.rindex > -1:
            message = 'Are you sure you want to delete the selected comparing variable?'
            reply = QtGui.QMessageBox.question(self.form, 'Delete Comparing Variable', message, QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.Yes)

            if reply == QtGui.QMessageBox.Yes:
                self.comparing_variable_list.pop(button.rindex)
                self.show_comparing_variable_list()

    def lineEditModelVariableConversionFactor_textChanged(self):
        if self.comboObservationDataType.currentIndex() == 0:
            self.lineEditMeasuredVariableConversionFactor.setText(self.lineEditModelVariableConversionFactor.text())

    def buttonMeasuredPairingVariable_clicked(self):
        if self.buttonMeasuredPairingVariable.text() == '>':
            if self.listMeasuredVariable.count() > 0:
                if len(self.listMeasuredVariable.selectedItems()) > 0:
                    item = self.listMeasuredVariable.selectedItems()[0]
                    if item:
                        self.lineEditMeasuredPairingVariable.setText(item.text())
                        self.buttonMeasuredPairingVariable.setText('<')
        else:
            self.lineEditMeasuredPairingVariable.clear()
            self.buttonMeasuredPairingVariable.setText('>')

    def buttonModelPairingVariable_clicked(self):
        if self.buttonModelPairingVariable.text() == '>':
            if self.listOutputVariable.count() > 0:
                if len(self.listOutputVariable.selectedItems()) > 0:
                    item = self.listOutputVariable.selectedItems()[0]
                    if item:
                        self.lineEditModelPairingVariable.setText(item.text())
                        self.buttonModelPairingVariable.setText('<')
                        if self.comboObservationDataType.currentIndex() == 0:
                            self.lineEditMeasuredPairingVariable.setText(item.text())
        else:
            self.lineEditModelPairingVariable.setText('')
            self.buttonModelPairingVariable.setText('>')
            if self.comboObservationDataType.currentIndex() == 0:
                self.lineEditMeasuredPairingVariable.clear()

    def buttonMeasuredVariable_clicked(self):
        if self.buttonMeasuredVariable.text() == '>':
            if self.listMeasuredVariable.count() > 0:
                if len(self.listMeasuredVariable.selectedItems()) > 0:
                    item = self.listMeasuredVariable.selectedItems()[0]
                    if item:
                        self.lineEditMeasuredVariable.setText(item.text())
                        self.buttonMeasuredVariable.setText('<')
        else:
            self.lineEditMeasuredVariable.setText('')
            self.buttonMeasuredVariable.setText('>')

    def buttonModelOutputVariable_clicked(self):
        if self.buttonModelOutputVariable.text() == '>':
            if self.listOutputVariable.count() > 0:
                if len(self.listOutputVariable.selectedItems()) > 0:
                    item = self.listOutputVariable.selectedItems()[0]
                    if item:
                        self.lineEditModelOutputVariable.setText(item.text())
                        self.buttonModelOutputVariable.setText('<')
                        if self.comboObservationDataType.currentIndex() == 0:
                            self.lineEditMeasuredVariable.setText(item.text())
        else:
            self.lineEditModelOutputVariable.setText('')
            self.buttonModelOutputVariable.setText('>')
            if self.comboObservationDataType.currentIndex() == 0:
                self.lineEditMeasuredVariable.clear()

    def buttonMeasuredDataFile_clicked(self):
        self.listMeasuredVariable.clear()
        self.lineEditMeasuredDataFile.clear()

        initial_directory = ApplicationProperty.currentModelDirectory
        if len(initial_directory) == 0: initial_directory = ApplicationProperty.getScriptPath()

        filename = ''
        if self.comboObservationDataType.currentIndex() == 0:
            filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initial_directory, "Text File (*.ini)")
        else:
            filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initial_directory, "Text File (*.csv)")

        if len(filename) > 0:
            self.lineEditMeasuredDataFile.setText(filename)

            # if self.comboObservationDataType.currentIndex() == 1:
            #     external_output = ReadExternalOutput.read_csv_file(filename, ',', True)
            #     if external_output is not None: self.listMeasuredVariable.addItems(external_output.get_header_variable())



    def comboOutputFileType_currentIndexChanged(self):
        self.listOutputVariable.clear()

        if self.comboOutputFileType.currentIndex() >= 0:
            file_type = self.comboOutputFileType.currentText()
            if len(file_type) > 0:
                model_output = ReadBinaryOutput.ReadModelOutput(ApplicationProperty.currentModelDirectory, self.lineEditInitializationFile.text().strip(),
                                                                           file_type, trim=True, post_processing=True, ucf=True)

                if model_output is not None: self.listOutputVariable.addItems(model_output.get_header_variable())


    def buttonInitializationFile_clicked(self):
        initial_directory = ApplicationProperty.currentModelDirectory
        if initial_directory == '':
            initial_directory = ApplicationProperty.getScriptPath()

        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', initial_directory, "Text File (*.ini)")
        if len(filename) > 0:
            init_param = FileReadWrite.readInitialFile(filename)
            if init_param is not None:
                temp = filename.split("/")[-1]
                if len(ApplicationProperty.currentModelDirectory) == 0:
                    ApplicationProperty.currentModelDirectory = filename.replace("ini/" + temp, "")
                self.lineEditInitializationFile.setText(temp)


                # #generating list of output files and check their availability
                # self.output_file_list = ReadBinaryOutput.GenerateListOfOutputFiles(init_param, ApplicationProperty.currentModelDirectory)
                #
                # #inserting output file names in combo box
                # if len(self.output_file_list) > 0:
                #     self.comboOutputFileType.addItems(self.output_file_list)
                #     self.comboOutputFileType.setCurrentIndex(-1)
            else:
                message = "The initial file could not be opened. Please choose a valid initial file."
                QtGui.QMessageBox.about(self.form, "Invalid Initial File", message)

    def comboObservationDataType_currentIndexChanged(self):
        if self.comboObservationDataType.currentIndex() >= 0:
            self.lineEditMeasuredDataFile.clear()
            self.listMeasuredVariable.clear()
            if self.comboObservationDataType.currentIndex() == 0:
                self.labelObservationDataFile.setText('Choose Initial File')
                self.buttonMeasuredVariable.setText('>')
                self.buttonMeasuredVariable.setEnabled(False)
                if len(self.lineEditModelOutputVariable.text()) > 0:
                    self.lineEditMeasuredVariable.setText(self.lineEditModelOutputVariable.text())
                else: self.lineEditMeasuredVariable.clear()
                self.buttonMeasuredPairingVariable.setText('>')
                self.buttonMeasuredPairingVariable.setEnabled(False)
                if len(self.lineEditModelPairingVariable.text()) > 0:
                    self.lineEditMeasuredPairingVariable.setText(self.lineEditModelPairingVariable.text())
                else: self.lineEditMeasuredPairingVariable.clear()
                if len(self.lineEditModelVariableConversionFactor.text()) > 0:
                    self.lineEditMeasuredVariableConversionFactor.setText(self.lineEditModelVariableConversionFactor.text())
                else: self.lineEditMeasuredVariableConversionFactor.clear()
                self.lineEditMeasuredVariableConversionFactor.setReadOnly(True)
            else:
                self.labelObservationDataFile.setText('Measured Datafile (CSV)')
                self.buttonMeasuredVariable.setEnabled(True)
                self.buttonMeasuredPairingVariable.setEnabled(True)
                self.lineEditMeasuredVariable.clear()
                self.lineEditMeasuredPairingVariable.clear()
                self.lineEditMeasuredVariableConversionFactor.clear()
                self.lineEditMeasuredVariableConversionFactor.setReadOnly(False)


    def checkbox_toggled(self, checkbox):
        if checkbox.isChecked():
            row_index = checkbox.row_index
            item = self.tableParameterSelection.item(row_index, 2)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

            item = self.tableParameterSelection.item(row_index, 3)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

            item = self.tableParameterSelection.item(row_index, 4)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

            if self.checkBoxPreferred.isChecked():
                item = self.tableParameterSelection.item(row_index, 5)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

                item = self.tableParameterSelection.item(row_index, 6)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
        else:
            row_index = checkbox.row_index
            item = self.tableParameterSelection.item(row_index, 2)
            item.setFlags(QtCore.Qt.ItemIsEnabled)

            item = self.tableParameterSelection.item(row_index, 3)
            item.setFlags(QtCore.Qt.ItemIsEnabled)

            item = self.tableParameterSelection.item(row_index, 4)
            item.setFlags(QtCore.Qt.ItemIsEnabled)

            if self.checkBoxPreferred.isChecked():
                item = self.tableParameterSelection.item(row_index, 5)
                item.setFlags(QtCore.Qt.ItemIsEnabled)

                item = self.tableParameterSelection.item(row_index, 6)
                item.setFlags(QtCore.Qt.ItemIsEnabled)

    def tableParameterSelection_itemChanged(self):
        item = self.tableParameterSelection.currentItem()
        cindex = self.tableParameterSelection.currentColumn()

        if not item: return False
        if not item.h_flag: return False
        elif cindex < 2: return False
        elif self.checkBoxPreferred.isChecked() and cindex > 6: return False
        elif not self.checkBoxPreferred.isChecked() and cindex > 4: return False
        else:
            if len(item.text()) > 0:
                value = None
                try: value = float(item.text())
                except:
                    #item.setText('')
                    message = 'Only numeric values are allowed.'
                    QtGui.QMessageBox.about(self.form, 'Numeric Only', message)
                    return False

                if value is not None:
                    row_index = item.row()

                    if self.checkBoxPreferred.isChecked():
                        start_val, lbound_hrd, lbound_prf, ubound_prf, ubound_hrd = None, None, None, None, None
                        ok_start_val, ok_lbound_hrd, ok_lbound_prf, ok_ubound_prf, ok_ubound_hrd = True, True, True, True, True

                        try:
                            start_val = float(self.tableParameterSelection.item(row_index, 2).text())
                        except: pass
                        try:
                            lbound_hrd = float(self.tableParameterSelection.item(row_index, 3).text())
                        except: pass
                        try:
                            lbound_prf = float(self.tableParameterSelection.item(row_index, 4).text())
                        except: pass
                        try:
                            ubound_prf = float(self.tableParameterSelection.item(row_index, 5).text())
                        except: pass
                        try:
                            ubound_hrd = float(self.tableParameterSelection.item(row_index, 6).text())
                        except: pass

                        if start_val is not None:
                            if lbound_hrd is not None and lbound_hrd > start_val: ok_start_val, ok_lbound_hrd = False, False
                            if lbound_prf is not None and lbound_prf > start_val: ok_start_val, ok_lbound_prf = False, False
                            if ubound_prf is not None and ubound_prf < start_val: ok_start_val, ok_ubound_prf = False, False
                            if ubound_hrd is not None and ubound_hrd < start_val: ok_start_val, ok_ubound_hrd = False, False

                        if lbound_hrd is not None:
                            if lbound_prf is not None and lbound_prf < lbound_hrd: ok_lbound_hrd, ok_lbound_prf = False, False
                            if ubound_prf is not None and ubound_prf < lbound_hrd: ok_lbound_hrd, ok_ubound_prf = False, False
                            if ubound_hrd is not None and ubound_hrd < lbound_hrd: ok_lbound_hrd, ok_ubound_hrd = False, False

                        if lbound_prf is not None:
                            if ubound_prf is not None and ubound_prf < lbound_prf: ok_lbound_prf, ok_ubound_prf = False, False
                            if ubound_hrd is not None and ubound_hrd < lbound_prf: ok_lbound_prf, ok_ubound_hrd = False, False

                        if ubound_prf is not None and ubound_hrd is not None and ubound_hrd < ubound_prf:
                            ok_ubound_prf, ok_ubound_hrd = False, False

                        item.h_flag = False
                        if not ok_start_val: self.tableParameterSelection.item(row_index, 2).setBackgroundColor(self.color_error)
                        else: self.tableParameterSelection.item(row_index, 2).setBackgroundColor(self.color_ok)
                        if not ok_lbound_hrd: self.tableParameterSelection.item(row_index, 3).setBackgroundColor(self.color_error)
                        else: self.tableParameterSelection.item(row_index, 3).setBackgroundColor(self.color_ok)
                        if not ok_lbound_prf: self.tableParameterSelection.item(row_index, 4).setBackgroundColor(self.color_error)
                        else: self.tableParameterSelection.item(row_index, 4).setBackgroundColor(self.color_ok)
                        if not ok_ubound_prf: self.tableParameterSelection.item(row_index, 5).setBackgroundColor(self.color_error)
                        else: self.tableParameterSelection.item(row_index, 5).setBackgroundColor(self.color_ok)
                        if not ok_ubound_hrd: self.tableParameterSelection.item(row_index, 6).setBackgroundColor(self.color_error)
                        else: self.tableParameterSelection.item(row_index, 6).setBackgroundColor(self.color_ok)
                        item.h_flag = True

                    else:
                        start_val, lbound, ubound = None, None, None
                        ok_start_val, ok_lbound, ok_ubound = True, True, True

                        try:
                            start_val = float(self.tableParameterSelection.item(row_index, 2).text())
                        except: pass
                        try:
                            lbound = float(self.tableParameterSelection.item(row_index, 3).text())
                        except: pass
                        try:
                            ubound = float(self.tableParameterSelection.item(row_index, 4).text())
                        except: pass

                        if start_val is not None :
                            if lbound is not None and lbound > start_val: ok_start_val, ok_lbound = False, False
                            if ubound is not None and ubound < start_val: ok_start_val, ok_ubound = False,  False
                        if lbound is not None and ubound is not None and lbound > ubound: ok_lbound, ok_ubound = False, False

                        item.h_flag = False
                        if not ok_start_val: self.tableParameterSelection.item(row_index, 2).setBackgroundColor(self.color_error)
                        else: self.tableParameterSelection.item(row_index, 2).setBackgroundColor(self.color_ok)
                        if not ok_lbound: self.tableParameterSelection.item(row_index, 3).setBackgroundColor(self.color_error)
                        else: self.tableParameterSelection.item(row_index, 3).setBackgroundColor(self.color_ok)
                        if not ok_ubound: self.tableParameterSelection.item(row_index, 4).setBackgroundColor(self.color_error)
                        else: self.tableParameterSelection.item(row_index, 4).setBackgroundColor(self.color_ok)
                        item.h_flag = True
                else: return False
            else: return False
        return True

    def validate_chosen_parameter(self):
        ret_val = True

        nrow = self.tableParameterSelection.rowCount()
        if self.checkBoxPreferred.isChecked():
            for i in range(nrow):
                checkbox = self.tableParameterSelection.cellWidget(i, 1).findChildren(QtGui.QCheckBox)[0]
                if checkbox.isChecked():
                    start_val, lbound_hrd, lbound_prf, ubound_prf, ubound_hrd = None, None, None, None, None
                    ok_start_val, ok_lbound_hrd, ok_lbound_prf, ok_ubound_prf, ok_ubound_hrd = True, True, True, True, True

                    try: start_val = float(self.tableParameterSelection.item(i, 2).text())
                    except: ok_start_val, ret_val = False, False
                    try: lbound_hrd = float(self.tableParameterSelection.item(i, 3).text())
                    except: ok_lbound_hrd, ret_val = False, False
                    try: lbound_prf = float(self.tableParameterSelection.item(i, 4).text())
                    except: lbound_prf, ret_val = False, False
                    try: ubound_prf = float(self.tableParameterSelection.item(i, 5).text())
                    except: ubound_prf, ret_val = False, False
                    try: ubound_hrd = float(self.tableParameterSelection.item(i, 6).text())
                    except: ubound_hrd, ret_val = False, False

                    if start_val is not None:
                        if lbound_hrd is not None and lbound_hrd > start_val: ok_start_val, ok_lbound_hrd = False, False
                        if lbound_prf is not None and lbound_prf > start_val: ok_start_val, ok_lbound_prf = False, False
                        if ubound_prf is not None and ubound_prf < start_val: ok_start_val, ok_ubound_prf = False, False
                        if ubound_hrd is not None and ubound_hrd < start_val: ok_start_val, ok_ubound_hrd = False, False

                    if lbound_hrd is not None:
                        if lbound_prf is not None and lbound_prf < lbound_hrd: ok_lbound_hrd, ok_lbound_prf = False, False
                        if ubound_prf is not None and ubound_prf < lbound_hrd: ok_lbound_hrd, ok_ubound_prf = False, False
                        if ubound_hrd is not None and ubound_hrd < lbound_hrd: ok_lbound_hrd, ok_ubound_hrd = False, False

                    if lbound_prf is not None:
                        if ubound_prf is not None and ubound_prf < lbound_prf: ok_lbound_prf, ok_ubound_prf = False, False
                        if ubound_hrd is not None and ubound_hrd < lbound_prf: ok_lbound_prf, ok_ubound_hrd = False, False

                    if ubound_prf is not None and ubound_hrd is not None and ubound_hrd < ubound_prf:
                        ok_ubound_prf, ok_ubound_hrd = False, False

                    self.tableParameterSelection.currentItem().h_flag = False
                    if not ok_start_val: self.tableParameterSelection.item(i, 2).setBackgroundColor(self.color_error)
                    else: self.tableParameterSelection.item(i, 2).setBackgroundColor(self.color_ok)
                    if not ok_lbound_hrd: self.tableParameterSelection.item(i, 3).setBackgroundColor(self.color_error)
                    else: self.tableParameterSelection.item(i, 3).setBackgroundColor(self.color_ok)
                    if not ok_lbound_prf: self.tableParameterSelection.item(i, 4).setBackgroundColor(self.color_error)
                    else: self.tableParameterSelection.item(i, 4).setBackgroundColor(self.color_ok)
                    if not ok_ubound_prf: self.tableParameterSelection.item(i, 5).setBackgroundColor(self.color_error)
                    else: self.tableParameterSelection.item(i, 5).setBackgroundColor(self.color_ok)
                    if not ok_ubound_hrd: self.tableParameterSelection.item(i, 6).setBackgroundColor(self.color_error)
                    else: self.tableParameterSelection.item(i, 6).setBackgroundColor(self.color_ok)
                    self.tableParameterSelection.currentItem().h_flag = True
        else:
            for i in range(nrow):
                checkbox = self.tableParameterSelection.cellWidget(i, 1).findChildren(QtGui.QCheckBox)[0]
                if checkbox.isChecked():
                    #checking if the boundary values and start value are entered properly
                    lbound, ubound, start_val = None, None, None
                    ok_lbound, ok_ubound, ok_start_val = True, True, True

                    try: start_val = float(self.tableParameterSelection.item(i, 2).text())
                    except: ok_start_val, ret_val = False, False
                    try: lbound = float(self.tableParameterSelection.item(i, 3).text())
                    except: ok_ubound, ret_val = False, False
                    try: ubound = float(self.tableParameterSelection.item(i, 4).text())
                    except: ok_ubound, ret_val = False, False

                    if start_val is not None :
                        if lbound is not None and lbound > start_val: ok_start_val, ok_lbound, ret_val = False, False, False
                        if ubound is not None and ubound < start_val: ok_start_val, ok_ubound, ret_val = False,  False, False
                    if lbound is not None and ubound is not None and lbound > ubound: ok_lbound, ok_ubound, ret_val = False, False, False

                    self.tableParameterSelection.currentItem().h_flag = False
                    if not ok_start_val: self.tableParameterSelection.item(i, 2).setBackgroundColor(self.color_error)
                    else: self.tableParameterSelection.item(i, 2).setBackgroundColor(self.color_ok)
                    if not ok_lbound: self.tableParameterSelection.item(i, 3).setBackgroundColor(self.color_error)
                    else: self.tableParameterSelection.item(i, 3).setBackgroundColor(self.color_ok)
                    if not ok_ubound: self.tableParameterSelection.item(i, 4).setBackgroundColor(self.color_error)
                    else: self.tableParameterSelection.item(i, 4).setBackgroundColor(self.color_ok)
                    self.tableParameterSelection.currentItem().h_flag = True
        return ret_val

    def buttonSave_clicked(self):
        if self.tabWidget.currentIndex() == 0:
            #saving parameter list
            if len(self.parameter_list) > 0:
                tar_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
                filename = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Parameter Filename', tar_dir, 'Parameter File (*.txt)')
                if filename:
                    if TargetParameter.write_parameter_file(self.parameter_list, filename):
                        message = 'Parameter set has been successfully saved.'
                        QtGui.QMessageBox.about(self.form, 'Parameter File', message)
                    else:
                        message = 'Parameter set could not be saved.'
                        QtGui.QMessageBox.about(self.form, 'Write Error', message)
        elif self.tabWidget.currentIndex() == 1:
            #saving comparing variables
            if len(self.comparing_variable_list) > 0:
                init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
                filename = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Comparison Variable-Map File', init_dir, 'Comparison File (*.txt)')
                if filename:
                    if Comparing_Variable.write_compmap_file(self.comparing_variable_list, filename):
                        message = 'Policy file for comparison has been created successfully.'
                        QtGui.QMessageBox.about(self.form, 'Comparison Policy File', message)
                    else:
                        message = 'Comparison policy could not be saved.'
                        QtGui.QMessageBox.about(self.form, 'Error', message)
        elif self.tabWidget.currentIndex() == 2:
            #evaluator configuration
            if self.read_configuration_field_values():
                if self.config:
                    if self.radioButtonUpdateConfigFile.isChecked():
                        filename = self.labelSelectedConfigFile.text()[1:-1]
                        if filename:
                            message = 'This update will cause permanant changes to the existing file. Do you want to continue?'
                            reply = QtGui.QMessageBox.question(self.form, 'Update Configuration', message, QtGui.QMessageBox.No,
                                                               QtGui.QMessageBox.Yes)
                            if reply == QtGui.QMessageBox.Yes:
                                if self.config.write_configuration_file(filename):
                                    message = 'The evaluation configuration file has been updated successfully'
                                    QtGui.QMessageBox.about(self.form, 'Successful Update', message)
                                else:
                                    message = 'The evaluation configuration file could not be updated. Please check all inputs and try agian.'
                                    QtGui.QMessageBox.about(self.form, 'Update Failed', message)
                    else:
                        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
                        filename = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Configuration File', init_dir, 'Configuration File (*.txt)')

                        if filename:
                            if self.config.write_configuration_file(filename):
                                message = 'The evaluation configuration file has been saved successfully.'
                                QtGui.QMessageBox.about(self.form, 'Saved Successfully', message)
                            else:
                                message = 'The evaluation configuratio file could not be saved. Please check all inputs and try again.'
                                QtGui.QMessageBox.about(self.form, 'Saved Failed', message)
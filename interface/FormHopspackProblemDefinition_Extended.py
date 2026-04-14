from interface.FormHopspackProblemDefinition import Ui_FormProblemDefinition
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from application import ApplicationProperty
from hopspack.configure import OptimizationProblem, TargetParameter, HopspackCitizen


class FormHopspackProblemDefinition(Ui_FormProblemDefinition):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.add_socket()
        self.add_validator()

        self.objective_type = ['Minimize', 'Maximize']
        self.mediator_display_option = ['Only final solution', 'Final solution and input parameters', 'The above, and all evaluated points',
                                       'The above, and all trial points', 'The above, and execution details']
        self.evaluation_types = ['System Call']
        self.problem_display_option = ['None', 'Problem Summary', 'All Details']
        self.citizen_display_option = ['None', 'Final solution and each new best point', 'The above, and all trial points',
                                       'The above, and all search directions']
        self.citizen_types = ['Generate Set Searching (GSS)', 'GSS with Non-linear constraints (GSS-NLC)']
        self.initial_settings()

    def add_socket(self):
        self.checkBoxExtractFromParamFile.toggled.connect(self.checkBoxExtractFromParamFile_toggled)
        self.radioButtonNewDefinitionFile.toggled.connect(self.radioButtonNewDefinitionFile_toggled)
        self.buttonClose.clicked.connect(self.buttonClose_clicked)
        self.pushButtonChooseDefinitionFile.clicked.connect(self.pushButtonChooseDefinitionFile_clicked)
        self.buttonChooseParamFile.clicked.connect(self.buttonChooseParamFile_clicked)
        self.checkBoxEvaluatorRelativeAddress.toggled.connect(self.checkBoxEvaluatorRelativeAddress_toggled)
        self.pushButtonChooseEvaluator.clicked.connect(self.pushButtonChooseEvaluator_clicked)
        self.pushButtonEvaluatorReferenceDirectory.clicked.connect(self.pushButtonEvaluatorReferenceDirectory_clicked)
        self.checkBoxSolutionRelativeAddress.toggled.connect(self.checkBoxSolutionRelativeAddress_toggled)
        self.pushButtonSolutionFileRefDirectory.clicked.connect(self.pushButtonSolutionFileRefDirectory_clicked)
        self.pushButtonChooseSolutionFile.clicked.connect(self.pushButtonChooseSolutionFile_clicked)
        self.buttonSave.clicked.connect(self.buttonSave_clicked)


    def add_validator(self):
        rx = QtCore.QRegExp("^[0-9]*$")
        integerValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)

        self.lineEditNoOfParameters.setValidator(integerValidator)
        self.lineEditFilePrecision.setValidator(integerValidator)
        self.lineEditNoOfCitizen.setValidator(integerValidator)
        self.lineEditMaxEvaluation.setValidator(integerValidator)
        self.lineEditNoOfThread.setValidator(integerValidator)
        self.lineEditSolutionFilePrecision.setValidator(integerValidator)
        self.lineEditStepTolerence.setValidator(decimalValidator)

    def initial_settings(self):
        self.buttonChooseParamFile.setEnabled(False)
        self.labelParamFilename.clear()
        self.comboBoxOptimizationObjectiveType.addItems(self.objective_type)
        self.comboBoxProblemDisplayOption.addItems(self.problem_display_option)
        self.comboBoxProblemDisplayOption.setCurrentIndex(1)
        self.comboBoxEvaluatorType.addItems(self.evaluation_types)
        self.comboBoxMediatorDisplayOption.addItems(self.mediator_display_option)
        self.comboBoxMediatorDisplayOption.setCurrentIndex(3)
        self.comboBoxCitizenDisplay.addItems(self.citizen_display_option)
        self.comboBoxCitizenType.addItems(self.citizen_types)
        self.comboBoxCitizenDisplay.setCurrentIndex(2)

        self.pushButtonChooseDefinitionFile.setEnabled(False)
        self.labelProblemDefinitionFile.clear()

        self.labelEvaluatorReferenceDirectory.clear()
        self.pushButtonEvaluatorReferenceDirectory.setEnabled(False)

        self.pushButtonSolutionFileRefDirectory.setEnabled(False)
        self.labelSolutionFileRefDirectory.clear()

    def buttonSave_clicked(self):
        opt_problem = self.read_problem_definition_property_from_fields()
        if opt_problem:
            if self.radioButtonNewDefinitionFile.isChecked():
                init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
                filename = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Problem Definition File', init_dir, 'Problem Definition (*.txt)')

                if filename:
                    if opt_problem.write_problem_definition_file(filename):
                        message = 'The problem definition file has been saved successfully.'
                        QtGui.QMessageBox.about(self.form, 'Saved Successfully', message)
                    else:
                        message = 'The problem definition file could not be saved. Please check all input and try again.'
                        QtGui.QMessageBox.about(self.form, 'Save Failed', message)
            else:
                filename = self.labelProblemDefinitionFile.text()[1:-1]
                if filename:
                    message = 'Do you want to over-write the existing file?'
                    reply = QtGui.QMessageBox.question(self.form, 'Over-write file', message, QtGui.QMessageBox.No,
                                                       QtGui.QMessageBox.Yes)
                    if reply == QtGui.QMessageBox.No:
                        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
                        filename = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Problem Definition File', init_dir, 'Problem Definition (*.txt)')

                    if filename:
                        if opt_problem.write_problem_definition_file(filename):
                            message = 'The problem definition file has been saved successfully.'
                            QtGui.QMessageBox.about(self.form, 'Saved Successfully', message)
                        else:
                            message = 'The problem definition file could not be saved. Please check all input and try again.'
                            QtGui.QMessageBox.about(self.form, 'Save Failed', message)

    def pushButtonChooseSolutionFile_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        sol_path = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Solution File', init_dir, 'Solution Fie (*.txt)')

        if sol_path:
            if self.checkBoxSolutionRelativeAddress.isChecked():
                ref_dir = self.labelSolutionFileRefDirectory.text()[1:-1]
                if ref_dir:
                    sol_path = os.path.relpath(sol_path, ref_dir)
            self.lineEditSolutionFile.setText(sol_path)

    def pushButtonSolutionFileRefDirectory_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        ref_dir = QtWidgets.QFileDialog.getExistingDirectory(self.form, 'Reference Directory', init_dir)

        if ref_dir:
            sol_path = self.lineEditSolutionFile.text().strip()
            if sol_path:
                cur_ref_dir = self.labelSolutionFileRefDirectory.text()[1:-1]
                if cur_ref_dir: sol_path = ApplicationProperty.get_absolute_path(sol_path, cur_ref_dir)
                sol_path = os.path.relpath(sol_path, ref_dir)
                self.lineEditSolutionFile.setText(sol_path)
            self.labelSolutionFileRefDirectory.setText('(' + ref_dir + ')')
    def checkBoxSolutionRelativeAddress_toggled(self):
        if self.checkBoxSolutionRelativeAddress.isChecked():
            sol_path = self.lineEditSolutionFile.text().strip()
            if sol_path:
                ref_dir = os.path.split(sol_path)[0]
                if ref_dir:
                    sol_path = os.path.split(sol_path)[1]
                    self.lineEditSolutionFile.setText(sol_path)
                    self.labelSolutionFileRefDirectory.setText('(' + ref_dir + ')')
            else: self.labelSolutionFileRefDirectory.clear()
            self.pushButtonSolutionFileRefDirectory.setEnabled(True)
        else:
            sol_path = self.lineEditSolutionFile.text().strip()
            ref_dir = self.labelSolutionFileRefDirectory.text()[1:-1]
            if sol_path and ref_dir:
                sol_path = ApplicationProperty.get_absolute_path(sol_path, ref_dir)
                self.lineEditSolutionFile.setText(sol_path)
            self.labelSolutionFileRefDirectory.clear()
            self.pushButtonSolutionFileRefDirectory.setEnabled(False)

    def pushButtonEvaluatorReferenceDirectory_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        dirpath = QtWidgets.QFileDialog.getExistingDirectory(self.form, 'Reference Directory', init_dir)

        if dirpath:
            eval_path = self.lineEditEvaluatorFilename.text().strip()
            if eval_path:
                cur_ref_dir = self.labelEvaluatorReferenceDirectory.text()[1:-1]
                if cur_ref_dir: eval_path = ApplicationProperty.get_absolute_path(eval_path, cur_ref_dir)
                eval_path = os.path.relpath(eval_path, dirpath)
                self.lineEditEvaluatorFilename.setText(eval_path)
            self.labelEvaluatorReferenceDirectory.setText('(' + dirpath + ')')
        else: self.labelEvaluatorReferenceDirectory.clear()

    def pushButtonChooseEvaluator_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Select Evaluator', init_dir, 'Python File (*.py)')
        if filename:
            if self.checkBoxEvaluatorRelativeAddress.isChecked():
                ref_dir = self.labelEvaluatorReferenceDirectory.text()[1:-1]
                if ref_dir:
                    filename = os.path.relpath(filename, ref_dir)
            self.lineEditEvaluatorFilename.setText(filename)

    def checkBoxEvaluatorRelativeAddress_toggled(self):
        if self.checkBoxEvaluatorRelativeAddress.isChecked():
            eval_path = self.lineEditEvaluatorFilename.text().strip()
            if eval_path:
                ref_dir = os.path.split(eval_path)[0]
                if ref_dir:
                    eval_path = os.path.split(eval_path)[1]
                    self.lineEditEvaluatorFilename.setText(eval_path)
                    self.labelEvaluatorReferenceDirectory.setText('(' + ref_dir + ')')
            else: self.labelEvaluatorReferenceDirectory.clear()
            self.pushButtonEvaluatorReferenceDirectory.setEnabled(True)
        else:
            ref_dir = self.labelEvaluatorReferenceDirectory.text()[1:-1]
            eval_path = self.lineEditEvaluatorFilename.text().strip()
            if ref_dir and eval_path:
                eval_path = ApplicationProperty.get_absolute_path(eval_path, ref_dir)
                self.lineEditEvaluatorFilename.setText(eval_path)
                self.labelEvaluatorReferenceDirectory.clear()
            self.pushButtonEvaluatorReferenceDirectory.setEnabled(False)

    def checkBoxExtractFromParamFile_toggled(self):
        self.labelParamFilename.clear()
        if self.checkBoxExtractFromParamFile.isChecked():
            self.buttonChooseParamFile.setEnabled(True)
        else:
            self.buttonChooseParamFile.setEnabled(False)

    def radioButtonNewDefinitionFile_toggled(self):
        self.clear_fields()
        self.labelProblemDefinitionFile.clear()
        if self.radioButtonNewDefinitionFile.isChecked():
            self.pushButtonChooseDefinitionFile.setEnabled(False)
        else: self.pushButtonChooseDefinitionFile.setEnabled(True)

    def show_hopspack_problem_definition(self, opt_prob):
        self.clear_fields()

        if opt_prob.no_of_parameters > 0:
            self.lineEditNoOfParameters.setText(str(opt_prob.no_of_parameters))
        if opt_prob.upper_bound:
            self.lineEditUpperBounds.setText(str(opt_prob.upper_bound)[1:-1].replace(',', ''))
        if opt_prob.lower_bound:
            self.lineEditLowerBounds.setText(str(opt_prob.lower_bound)[1:-1].replace(',', ''))
        if opt_prob.initial_value:
            self.lineEditInitialParamValue.setText(str(opt_prob.initial_value)[1:-1].replace(',', ''))
        if opt_prob.initial_fvalue:
            self.lineEditInitFunValue.setText(str(opt_prob.initial_fvalue)[1:-1].replace(',', ''))
        if opt_prob.optimization_objective:
            ndx = -1
            try: ndx = self.objective_type.index(opt_prob.optimization_objective)
            except: pass
            self.comboBoxOptimizationObjectiveType.setCurrentIndex(ndx)
        self.comboBoxProblemDisplayOption.setCurrentIndex(opt_prob.definition_display_option)

        # evaluator settings
        if opt_prob.evaluator_type:
            ndx = -1
            try: ndx = self.evaluation_types.index(opt_prob.evaluator_type)
            except: pass
            self.comboBoxEvaluatorType.setCurrentIndex(ndx)
        if opt_prob.executable_name:
            self.lineEditEvaluatorFilename.setText(opt_prob.executable_name)
        if opt_prob.file_precision > 0:
            self.lineEditFilePrecision.setText(str(opt_prob.file_precision))
        if opt_prob.input_prefix: self.lineEditInputPrefix.setText(opt_prob.input_prefix)
        if opt_prob.output_prefix: self.lineEditOutputPrefix.setText(opt_prob.output_prefix)
        if opt_prob.save_io_file_flag: self.radioButtonSaveIOYes.setChecked(True)
        if opt_prob.display_debug_info_flag: self.radioButtonDebugInfoYes.setChecked(True)

        # mediator settings
        if opt_prob.citizen_count > 0:
            self.lineEditNoOfCitizen.setText(str(opt_prob.citizen_count))

        if opt_prob.maximum_evaluations > 0: self.lineEditMaxEvaluation.setText(str(opt_prob.maximum_evaluations))
        if opt_prob.thread_count > 0: self.lineEditNoOfThread.setText(str(opt_prob.thread_count))
        if opt_prob.synchronize_evaluation_flag:  self.radioButtonSynchronusYes.setChecked(True)

        self.comboBoxMediatorDisplayOption.setCurrentIndex(opt_prob.mediator_display_option)
        if opt_prob.solution_filename: self.lineEditSolutionFile.setText(opt_prob.solution_filename)
        if opt_prob.solution_file_precision > 0: self.lineEditSolutionFilePrecision.setText(str(opt_prob.solution_file_precision))

        # citizen setting
        if opt_prob.citizen_list:
            citizen = opt_prob.citizen_list[0]

            ndx = -1
            if citizen.citizen_type.lower() == 'gss':
                ndx = 0
            elif citizen.citizen_type.lower() == 'gss-nlc':
                ndx = 1
            self.comboBoxCitizenType.setCurrentIndex(ndx)

            if citizen.step_tolerence > 0:  self.lineEditStepTolerence.setText(str(citizen.step_tolerence))
            self.comboBoxCitizenDisplay.setCurrentIndex(citizen.citizen_display_option)

    def clear_fields(self):
        self.checkBoxExtractFromParamFile.setChecked(False)
        self.lineEditNoOfParameters.clear()
        self.lineEditUpperBounds.clear()
        self.lineEditLowerBounds.clear()
        self.lineEditInitialParamValue.clear()
        self.lineEditInitFunValue.clear()
        self.comboBoxOptimizationObjectiveType.setCurrentIndex(0)
        self.comboBoxProblemDisplayOption.setCurrentIndex(1)

        self.comboBoxEvaluatorType.setCurrentIndex(0)
        self.lineEditEvaluatorFilename.clear()
        self.checkBoxEvaluatorRelativeAddress.setChecked(False)
        self.lineEditFilePrecision.clear()
        self.lineEditInputPrefix.clear()
        self.lineEditOutputPrefix.clear()
        self.radioButtonSaveIONo.setChecked(True)
        self.radioButtonDebugInfoNo.setChecked(True)

        self.lineEditNoOfCitizen.setText('1')
        self.lineEditMaxEvaluation.clear()
        self.lineEditNoOfThread.clear()
        self.radioButtonSynchronousNo.setChecked(True)
        self.checkBoxSolutionRelativeAddress.setChecked(False)
        self.lineEditSolutionFilePrecision.clear()
        self.comboBoxMediatorDisplayOption.setCurrentIndex(3)
        self.lineEditSolutionFile.clear()

        self.comboBoxCitizenType.setCurrentIndex(0)
        self.lineEditStepTolerence.clear()
        self.comboBoxCitizenDisplay.setCurrentIndex(2)

    def buttonChooseParamFile_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Select parameter file', init_dir, 'Parameter File (*.txt)')

        if filename:
            param_list = []
            TargetParameter.read_parameter_list(filename, param_list)
            if param_list:
                no_of_param = len(param_list)
                upper_bounds = []
                lower_bounds = []
                start_val_list = []

                for param in param_list:
                    upper_bounds.append(param.upper_bound)
                    lower_bounds.append(param.lower_bound)
                    start_val_list.append(param.starting_value)

                self.lineEditNoOfParameters.setText(str(no_of_param))
                self.lineEditUpperBounds.setText(str(upper_bounds)[1:-1].replace(',', ''))
                self.lineEditLowerBounds.setText(str(lower_bounds)[1:-1].replace(',', ''))
                self.lineEditInitialParamValue.setText(str(start_val_list)[1:-1].replace(',',''))
                self.lineEditInitFunValue.clear()
                self.labelParamFilename.setText('(' + filename + ')')


    def buttonClose_clicked(self):
        self.form.parentWidget().close()

    def pushButtonChooseDefinitionFile_clicked(self):
        init_dir = os.path.join(ApplicationProperty.getScriptPath(), 'hopspack')
        filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Select Problem Definition File', init_dir)

        if filename:
            prob_def = OptimizationProblem.read_problem_definition_file(filename)
            if prob_def:
                self.labelProblemDefinitionFile.setText('(' + filename + ')')
                self.show_hopspack_problem_definition(prob_def)


    def read_problem_definition_property_from_fields(self):
        no_of_parameter = -1
        try: no_of_parameter = int (self.lineEditNoOfParameters.text().strip())
        except: pass
        if no_of_parameter < 1:
            message = 'No. of parameter filed is empty or has invalid value. Please enter a valid number of parameters.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.lineEditNoOfParameters.setFocus(True)
            return False

        upper_bounds = []
        temp = self.lineEditUpperBounds.text().strip().split(' ')
        for i in range(len(temp)):
            try: temp[i] = float(temp[i])
            except:
                temp = []
                break
        upper_bounds = temp

        if len(upper_bounds) != no_of_parameter:
            message = 'Upper bound is either blank or the number of bounds is not equal to the no. of parameters. Pleae check the values.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.lineEditUpperBounds.setFocus(True)
            return False

        lower_bounds = []
        temp = self.lineEditLowerBounds.text().strip().split(' ')
        for i in range(len(temp)):
            try: temp[i] = float(temp[i])
            except:
                temp = []
                break
        lower_bounds = temp

        if len(lower_bounds) != no_of_parameter:
            message = 'Lower bound is either blank or the number of bounds is not equal to the no. of parameters. Pleae check the values.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.lineEditLowerBounds.setFocus(True)
            return False

        start_values = []
        temp = self.lineEditInitialParamValue.text().strip().split(' ')
        for i in range(len(temp)):
            try: temp[i] = float(temp[i])
            except:
                temp = []
                break
        start_values = temp

        if start_values and len(start_values) != no_of_parameter:
            message = 'List of start values has differen number of values than the no. of parameters. Pleae check the values.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.lineEditInitialParamValue.setFocus(True)
            return False

        init_fvals = []
        temp = self.lineEditInitFunValue.text().strip().split(' ')
        for i in range(len(temp)):
            try: temp[i] = float(temp[i])
            except:
                temp = []
                break
        init_fvals = temp

        if init_fvals and len(init_fvals) != no_of_parameter:
            message = 'List of initial function values has different number of values than the no. of parameters. Pleae check the values.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.lineEditInitFunValue.setFocus(True)
            return False

        objective_type = self.comboBoxOptimizationObjectiveType.currentText()
        if not objective_type:
            message = 'Please select Objective Type.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.comboBoxOptimizationObjectiveType.setFocus(True)
            return False

        problem_display_option = self.comboBoxProblemDisplayOption.currentIndex()

        evaluator_type = self.comboBoxEvaluatorType.currentText()
        if not evaluator_type:
            message = 'Please select Evaluator Type.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.comboBoxEvaluatorType.setFocus(True)
            return False

        evaluator_path = self.lineEditEvaluatorFilename.text().strip()
        if not evaluator_path:
            message = 'Please select Evaluator Filename.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.lineEditEvaluatorFilename.setFocus(True)
            return False

        file_precision = 0
        try: file_precision = int(self.lineEditFilePrecision.text().strip())
        except: pass

        input_file_prefix = self.lineEditInputPrefix.text().strip()
        output_file_prefix = self.lineEditOutputPrefix.text().strip()
        save_io_files = self.radioButtonSaveIOYes.isChecked()
        show_debug_info = self.radioButtonDebugInfoYes.isChecked()

        #mediator's options
        no_of_citizen = 0
        try: no_of_citizen = int(self.lineEditNoOfCitizen.text().strip())
        except: pass
        if no_of_citizen < 1:
            message = 'HOPSPACK requires at least one citizen. Please insert the no. of citizen.'
            QtGui.QMessageBox.about(self.form, 'Required Input Missing', message)
            self.lineEditNoOfCitizen.setFocus(True)
            return False

        max_evaluations = -1
        try: max_evaluations = int(self.lineEditMaxEvaluation.text().strip())
        except: pass

        no_of_threads = -1
        try: no_of_threads = int(self.lineEditNoOfThread.text().strip())
        except: pass

        synchronous_evaluation = self.radioButtonSynchronusYes.isChecked()
        solution_filename = self.lineEditSolutionFile.text().strip()
        solution_file_precision = -1
        try: solution_file_precision = int(self.lineEditSolutionFilePrecision.text().strip())
        except: pass

        mediator_display_option = self.comboBoxMediatorDisplayOption.currentIndex()

        citizen_type = 'GSS'
        if self.comboBoxCitizenType.currentIndex() == 1: citizen_type = 'GSS-NLC'

        step_tolarence = -1
        try: step_tolarence = float(self.lineEditStepTolerence.text().strip())
        except: pass

        citizen_display_option = self.comboBoxCitizenDisplay.currentIndex()

        #creating new optimization problem
        opt_problem = OptimizationProblem()
        opt_problem.no_of_parameters = no_of_parameter
        opt_problem.upper_bound = upper_bounds
        opt_problem.lower_bound = lower_bounds
        if start_values: opt_problem.initial_value = start_values
        if init_fvals: opt_problem.initial_fvalue = init_fvals
        opt_problem.optimization_objective = objective_type
        if problem_display_option > -1: opt_problem.definition_display_option = problem_display_option
        opt_problem.evaluator_type = evaluator_type
        opt_problem.executable_name = evaluator_path
        if file_precision > 0: opt_problem.file_precision = file_precision
        opt_problem.input_prefix = input_file_prefix
        opt_problem.output_prefix = output_file_prefix
        opt_problem.save_io_file_flag = save_io_files
        opt_problem.display_debug_info_flag = show_debug_info
        opt_problem.citizen_count = no_of_citizen
        if max_evaluations > 0: opt_problem.maximum_evaluations = max_evaluations
        if no_of_threads > 1: opt_problem.thread_count = no_of_threads
        opt_problem.synchronize_evaluation_flag = synchronous_evaluation
        opt_problem.solution_filename = solution_filename
        if solution_file_precision > 0: opt_problem.solution_file_precision = solution_file_precision
        opt_problem.mediator_display_option = mediator_display_option

        #creating a citizen
        citizen = HopspackCitizen()
        citizen.citizen_type = citizen_type
        if step_tolarence > 0: citizen.step_tolerence = step_tolarence
        citizen.citizen_display_option = citizen_display_option
        opt_problem.citizen_list.append(citizen)

        return opt_problem



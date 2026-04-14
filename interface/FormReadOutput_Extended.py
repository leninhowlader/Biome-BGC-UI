from interface.FormReadOutput import Ui_FormReadOutput
from PyQt5 import QtGui, QtCore, QtWidgets
from application import ApplicationProperty
from file_io import FileReadWrite
from read_output import ReadBinaryOutput, DataReadResult
import re
import numpy as np


class FormReadOutput(Ui_FormReadOutput):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)

        self.addSocket()


        self.initParam = None
        self.output_file_list = []
        self.header_variable = None
        self.list_of_record = []
        self.table_struct = None

        self.read_output_result = DataReadResult()

        self.initialSetting()


    def addSocket(self):
        self.buttonRead.clicked.connect(self.buttonRead_clicked)
        self.buttonBrowseInitFile.clicked.connect(self.buttonBrowseInitFile_clicked)
        self.comboOutputFiles.currentIndexChanged.connect(self.comboOutputFiles_currentIndexChanged)
        self.buttonClose.clicked.connect(self.buttonClose_clicked)
        self.txtSRowCount.textChanged.connect(self.txtSRowCount_textChanged)
        self.listAllVariable.itemDoubleClicked.connect(self.listAllVariable_itemDoubleClicked)
        self.buttonCompute.clicked.connect(self.buttonCompute_clicked)
        self.comboBoxFilterVariable.currentIndexChanged.connect(self.comboBoxFilterVariable_currentIndexChanged)
        self.buttonFilter.clicked.connect(self.buttonFilter_clicked)
        self.buttonExportCSV.clicked.connect(self.buttonExportCSV_clicked)

    def initialSetting(self):
        self.lableOutputFileDirectory.setText("")
        self.txtSRowCount.setText("200")
        self.checkBoxUnitConversion.setChecked(True)
        self.comboOutputFiles.setEnabled(False)
        self.groupBoxComputeField.setEnabled(False)
        self.groupBoxFilter.setEnabled(False)
        self.buttonExportCSV.setEnabled(False)

    def clear_read_result(self):
        self.listAllVariable.clear()
        self.comboBoxFilterVariable.clear()
        self.ClearDataTable()
        self.groupBoxComputeField.setEnabled(False)
        self.lineEditNewVariableName.clear()
        self.textEditEquation.clear()
        self.lineEditFilterCondition.clear()
        self.groupBoxFilter.setEnabled(False)
        self.buttonExportCSV.setEnabled(False)
        self.read_output_result = DataReadResult()
        self.txtSRowCount.setText("200")

    def comboOutputFiles_currentIndexChanged(self):
        if self.comboOutputFiles.currentIndex() != -1:
            self.clear_read_result()

    def buttonRead_clicked(self):
        self.ClearDataTable()

        file_type = ""
        if self.comboOutputFiles.currentIndex() != -1:
            file_type = self.comboOutputFiles.currentText()

        if len(file_type) > 0:
            if self.checkBoxUnitConversion.isChecked():
                self.read_output_result = ReadBinaryOutput.ReadModelOutput(ApplicationProperty.currentModelDirectory, self.txtInitFile.text().strip(),
                                                                           file_type, trim=True, post_processing=True, ucf=True)
            else:
                self.read_output_result = ReadBinaryOutput.ReadModelOutput(ApplicationProperty.currentModelDirectory, self.txtInitFile.text().strip(),
                                                                           file_type, trim=True, post_processing=True, ucf=False)

            if self.read_output_result.record_list:
                self.refresh_data_display()

                self.groupBoxComputeField.setEnabled(True)
                self.groupBoxFilter.setEnabled(True)
                self.buttonExportCSV.setEnabled(True)

    def ClearDataTable(self):
        for i in reversed(range(self.tableData.rowCount())):
            self.tableData.removeRow(i)
        for i in reversed(range(self.tableData.columnCount())):
            self.tableData.removeColumn(i)


    def buttonBrowseInitFile_clicked(self):
        init_dir = ApplicationProperty.currentModelDirectory
        if len(init_dir) == 0: init_dir = ApplicationProperty.getScriptPath()

        file_name = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', init_dir, "Initial File (*.ini)")

        if len(file_name) > 0:
            self.initParam = FileReadWrite.readInitialFile(file_name)
            if self.initParam is not None:
                temp = file_name.split("/")[-1]
                self.txtInitFile.setText(temp)
                if len(ApplicationProperty.currentModelDirectory) == 0:
                    ApplicationProperty.currentModelDirectory = file_name.replace("ini/" + temp, "")

                #generating list of output files and check their availability
                self.output_file_list = ReadBinaryOutput.GenerateListOfOutputFiles(self.initParam, ApplicationProperty.currentModelDirectory)

                #inserting output file names in combo box
                if len(self.output_file_list) > 0:
                    self.comboOutputFiles.addItems(self.output_file_list)
                    self.comboOutputFiles.setCurrentIndex(-1)
                    self.lableOutputFileDirectory.setText(ApplicationProperty.currentModelDirectory + "output/")
                    self.comboOutputFiles.setEnabled(True)

                    self.clear_read_result()


            else:
                message = "The initial file could not be opened. Please choose a valid initial file."
                QtGui.QMessageBox.about(self.form, "Invalid Initial File", message)


    def txtSRowCount_textChanged(self):
        row_count = 0
        try: row_count = int(self.txtSRowCount.text().strip())
        except: pass

        if row_count > 0 and len(self.read_output_result.record_list) > 0:
            #clear all table rows
            for i in reversed(range(self.tableData.rowCount())): self.tableData.removeRow(i)
            self.display_record(row_count)

    def refresh_data_display(self):
        if len(self.read_output_result.header_variable) > 0:
            self.listAllVariable.clear()
            self.listAllVariable.addItems(self.read_output_result.header_variable)

            self.comboBoxFilterVariable.clear()
            self.comboBoxFilterVariable.addItems(self.read_output_result.header_variable)
            self.comboBoxFilterVariable.setCurrentIndex(-1)

            self.ClearDataTable()
            self.tableData.setColumnCount(len(self.read_output_result.header_variable))
            self.tableData.setHorizontalHeaderLabels(self.read_output_result.header_variable)

            display_count = 0
            try: display_count = int(self.txtSRowCount.text())
            except: pass

            self.display_record(display_count)


    def display_record(self, no_of_record):
        total_record_count = len(self.read_output_result.record_list)
        if total_record_count > 0:
            if no_of_record == 0 or no_of_record > total_record_count: no_of_record = total_record_count

            for i in range(no_of_record):
                tp = self.read_output_result.record_list[i]
                row_index = self.tableData.rowCount()
                self.tableData.insertRow(row_index)
                self.tableData.setRowHeight(row_index, 20)
                for j in range(len(tp)):
                    try: temp = str(round(tp[j], 3))
                    except: temp = str(tp[j])
                    item = QtWidgets.QTableWidgetItem(temp)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableData.setItem(row_index, j, item)

    def listAllVariable_itemDoubleClicked(self):
        if len(self.lineEditNewVariableName.text().strip()) > 0:
            var_name = "[" + self.listAllVariable.selectedItems()[0].text() + "]"
            self.textEditEquation.insertPlainText(var_name)

    def check_equation(self, equation_str):
        if equation_str:
            var_list = re.findall("\w+", equation_str)

            #remove number from var_list
            for i in reversed(range(len(var_list))):
                var = var_list[i]
                try:
                    x = eval(var)
                    var_list.pop(i)
                except: pass

            #check if the  variables exist in header variable
            undefined_var = []
            exist = True
            for var in var_list:
                if var not in self.read_output_result.header_variable:
                    undefined_var.append(var)
                    exist = False

            if len(undefined_var) > 0:
                message = "Following variables are unknown...\n"
                for var in undefined_var: message += var
                QtGui.QMessageBox.about(self.form, "Unknown Variable", message)
                return False

            #equation evaluation
            temp = equation_str
            for var in var_list: temp = temp.replace(var, "x")
            temp = temp.replace("[", "").replace("]", "")
            try:
                x = 1
                x = eval(temp)
            except:
                message = "Equation evaluation failed. Please check the equation."
                QtGui.QMessageBox.about(self.form, "Invalid Equation", message)
                return False

            return True
        else: return False

    def buttonCompute_clicked(self):
        new_field_name = self.lineEditNewVariableName.text().strip()
        equation_str = self.textEditEquation.toPlainText().strip()
        if new_field_name in self.read_output_result.header_variable:
            message = "New field name is conflicting with an existing field name. Please choose a different name."
            QtGui.QMessageBox.about(self.form, "Conflicting Name", message)
        else:
            if len(new_field_name) > 0 and self.check_equation(equation_str):
                var_list = re.findall("\w+", equation_str)

                #remove number from var_list
                for i in reversed(range(len(var_list))):
                    var = var_list[i]
                    try:
                        x = eval(var)
                        var_list.pop(i)
                    except: pass

                equation_str = equation_str.replace("[","").replace("]","")

                succeed = True
                data_list = []
                for i in range(len(var_list)):
                    var = var_list[i]
                    temp = ReadBinaryOutput.ExtractColumnRecord(var, self.read_output_result.header_variable, self.read_output_result.record_list)
                    if temp:
                        data_list.append(np.array(temp))
                        equation_str = equation_str.replace(var, "data_list["+ str(i) +"]")
                    else:
                        succeed = False
                        break

                if succeed:
                    new_record = []
                    try:
                        new_record = list(eval(equation_str))
                    except: succeed = False

                    if succeed and self.read_output_result.add_new_field(new_field_name, new_record):
                        self.refresh_data_display()

                        message = "New variable has been successfully computed."
                        QtGui.QMessageBox.about(self.form, "Success", message)
                        self.lineEditNewVariableName.clear()
                        self.textEditEquation.clear()

                        return True

                message = "New variable computation was not successfull!"
                QtGui.QMessageBox.about(self.form, "Unknown Error", message)

    def comboBoxFilterVariable_currentIndexChanged(self):
        if self.comboBoxFilterVariable.currentIndex() >= 0:
            self.lineEditFilterCondition.clear()

    def buttonFilter_clicked(self):
        if self.comboBoxFilterVariable.currentIndex() >= 0:
            filter_variable = self.comboBoxFilterVariable.currentText()
            filter_str = self.lineEditFilterCondition.text().strip()
            if filter_variable and filter_str:
                validate = True
                try:
                    x = 5
                    x = eval("x " + filter_str)
                except: validate = False

                if validate:
                    total_record = len(self.read_output_result.record_list)

                    filter_record = ReadBinaryOutput.ExtractColumnRecord(filter_variable, self.read_output_result.header_variable, self.read_output_result.record_list)
                    for i in reversed(range(len(filter_record))):
                        condition = True
                        try:
                            condition = eval(str(filter_record[i]) + " " + filter_str)
                            if not condition: self.read_output_result.record_list.pop(i)
                        except: pass

                    self.txtSRowCount_textChanged()
                    message = "Data has been filtered. " + str(total_record - len(self.read_output_result.record_list)) + " record(s) has been removed."
                    QtGui.QMessageBox.about(self.form, "Success", message)

                else:
                    message = "Filter condition is not valid. Please enter valid condition"
                    QtGui.QMessageBox.about(self.form, "Invalid Condition", message)

    def buttonExportCSV_clicked(self):
        if len(self.read_output_result.header_variable) > 0:
            initial_directory = ApplicationProperty.currentModelDirectory
            if not initial_directory: initial_directory = ApplicationProperty.getScriptPath()

            csv_filename = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save Output', initial_directory, "CSV Files (*.csv)")

            if csv_filename:
                if ReadBinaryOutput.write_csv(self.read_output_result.header_variable, self.read_output_result.record_list, csv_filename):
                    message = "Data has been successfully exported."
                    QtGui.QMessageBox.about(self.form, "Success", message)
                else:
                    message = "Data could not be saved."
                    QtGui.QMessageBox.about(self.form, "Unknown Error", message)

    def buttonClose_clicked(self):
        self.form.parentWidget().close()
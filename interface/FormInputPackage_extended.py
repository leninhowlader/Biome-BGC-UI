from interface.FormInputPackage import Ui_FormInputPackage
from PyQt5 import QtGui, QtCore, QtWidgets
from application import ApplicationProperty
import os
from parameter_set import input_package
from file_io import FileReadWrite

class FormInputPackage(Ui_FormInputPackage):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.addSocket()

        self.initial_settings()

        self.signalMapper = QtCore.QSignalMapper(self.form)
        self.signalMapper.mapped[QtWidgets.QWidget].connect(self.dynamicPushButton_clicked)

        self.model_directory = ApplicationProperty.currentModelDirectory

    def addSocket(self):
        self.pushButtonBrowse.clicked.connect(self.pushButtonBrowse_clicked)
        self.pushButtonOk.clicked.connect(self.pushButtonOk_clicked)

    def initial_settings(self):
        header = ["Input File Type", "Address", "Link", "Valid", "Change"]
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(header)

        # row_index = self.tableWidget.rowCount()
        # self.tableWidget.addRow()

    def delete_table_rows(self):
        for i in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)

    def pushButtonBrowse_clicked(self):
        init_dir = self.model_directory
        if len(init_dir) == 0:
            init_dir = ApplicationProperty.getScriptPath()
        init_file_name = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Initial File', init_dir, "Init File (*.ini)")

        if os.path.exists(init_file_name):
            self.lineEditInitialFile.setText(init_file_name.split("/")[-1].split("\\")[-1])
            if not self.model_directory:
                temp = init_file_name.split("/")[-1]
                self.model_directory = init_file_name.replace("ini/"+ temp,"")[:-1]

            self.input_file_validity_check(init_file_name)

    def input_file_validity_check(self, init_file_name):
        self.delete_table_rows()
        result = input_package.check_input_file_linkage(self.model_directory, init_file_name)

        if len(result) > 0:
            for item in result:
                row_index = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_index)
                self.tableWidget.setRowHeight(row_index, 23)

                cell = QtWidgets.QTableWidgetItem(item[0])
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_index, 0, cell)

                cell = QtWidgets.QTableWidgetItem(item[1].replace("\\", "/"))
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_index, 1, cell)

                if item[2] == True:
                    cell = QtWidgets.QTableWidgetItem("OK")
                    cell.setTextColor(QtGui.QColor("green"))
                else:
                    cell = QtWidgets.QTableWidgetItem("Not Found")
                    cell.setTextColor(QtGui.QColor("red"))
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_index, 2, cell)

                if item[3] is None:
                    cell = QtWidgets.QTableWidgetItem("Not Checked")
                    cell.setTextColor(QtGui.QColor("green"))
                elif item[3] == True:
                    cell = QtWidgets.QTableWidgetItem("Valid")
                    cell.setTextColor(QtGui.QColor("green"))
                else:
                    cell = QtWidgets.QTableWidgetItem("Not Valid")
                    cell.setTextColor(QtGui.QColor("red"))
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_index, 3, cell)

                buttonCell = QtGui.QPushButton("..")
                buttonCell.rowIndex = row_index
                buttonCell.clicked.connect(self.signalMapper.map)
                self.tableWidget.setCellWidget(row_index, 4, buttonCell)
                self.signalMapper.setMapping(buttonCell, buttonCell)

    def dynamicPushButton_clicked(self, buttonCell):
        ret_val  = False

        cell_item = self.tableWidget.item(buttonCell.rowIndex, 0)

        #reading file type, (site index and vegetation number)
        temp = cell_item.text()

        file_type = ""
        site_index = ""
        veg_no = -1
        if temp.find(")") != -1:
            temp = temp.strip("(").split(")")

            file_type = temp[-1].strip()

            if temp[0].find(":") != 1:
                temp = temp[0].split(":")

                site_index = temp[0].strip()
                try: veg_no = int(temp[-1].strip())
                except: pass
        else: file_type = temp.strip()

        initial_filename = os.path.join(self.model_directory, "ini", self.lineEditInitialFile.text())

        if file_type == "Initial File":
            message = "Sorry, you can not change the initial file here. Please open initial file module."
            QtGui.QMessageBox.about(self.form, "Sorry", message)
        elif file_type == "NDEP File":
            message = ""
            new_ndep_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "All file (*.txt)")
            if len(new_ndep_filename) > 0: ret_val = input_package.change_ndep_file(initial_filename, new_ndep_filename)
            # else: message = "Unexpected Error."
            if len(message) > 0: QtGui.QMessageBox.about(self.form, "Sorry", message)
        elif file_type == "MET File":
            message = ""
            new_met_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "All file (*.txt)")
            if len(new_met_filename) > 0: ret_val = input_package.change_ndep_file(initial_filename, new_met_filename)
            # else: message = "Unexpected Error."
            if len(message) > 0: QtGui.QMessageBox.about(self.form, "Sorry", message)
        elif file_type == "Restart Read File":
            new_restart_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "All file (*.endpoint)")
            if len(new_restart_filename) > 0: ret_val = input_package.change_restart_read_file(initial_filename, new_restart_filename)
        elif file_type == "Cabor-di-oxide File":
            new_carbon_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "All file (*.txt)")
            if len(new_carbon_filename) > 0: ret_val = input_package.change_carbon_file(initial_filename, new_carbon_filename)
        elif file_type == "GIS File":
            new_gis_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "All file (*.txt)")
            if len(new_gis_filename) > 0: ret_val = input_package.change_gis_file(initial_filename, new_gis_filename)
        elif file_type == "Vegetation File":
            new_veg_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "All file (*.txt)")
            if len(new_veg_filename) > 0: ret_val = input_package.change_veg_file(initial_filename, new_veg_filename)
        elif file_type == "Soil Profile File":
            message = ""
            if len(site_index) > 0:
                init_param = FileReadWrite.readInitialFile(initial_filename)
                if init_param is not None:
                    gis_filename = os.path.join(self.model_directory, init_param.gis_file_name)
                    new_soil_profile_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "All file (*.txt)")
                    if len(new_soil_profile_filename) > 0: ret_val = input_package.change_soil_profile_file(gis_filename, site_index, new_soil_profile_filename)
                else: message = "File I/O Error. Please try again."
            else: message = "Request cannot be processed."
            if len(message) > 0: QtGui.QMessageBox.about(self.form, "Sorry", message)
        elif file_type == "Soil Horizon File":
            message = ""
            if len(site_index) > 0:
                init_param = FileReadWrite.readInitialFile(initial_filename)
                if init_param is not None:
                    gis_filename = os.path.join(self.model_directory, init_param.gis_file_name)
                    new_soil_horizon_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "All file (*.txt)")
                    if len(new_soil_horizon_filename) > 0: ret_val = input_package.change_soil_horizon_file(gis_filename, site_index, new_soil_horizon_filename)
                else: message = "File I/O Error. Please try again."
            else: message = "Request cannot be processed."
            if len(message) > 0: QtGui.QMessageBox.about(self.form, "Sorry", message)
        elif file_type == "EPC File":
            message = ""
            if len(site_index) > 0 and veg_no > -1:
                init_param = FileReadWrite.readInitialFile(initial_filename)

                if init_param is not None:
                    veg_filename = os.path.join(self.model_directory, init_param.veg_file_name)
                    new_epc_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "EPC file (*.epc)")
                    if len(new_epc_filename) > 0: ret_val = input_package.change_epc_input_file(veg_filename, site_index, veg_no, new_epc_filename)
                    # else: message = "No file was choosen!"
            else: message = "Unexpected Error!"
            if len(message) > 0: QtGui.QMessageBox.about(self.form, "Sorry", message)

        elif file_type == "Harvest File":
            message = ""
            if len(site_index) > 0 and veg_no > -1:
                init_param = FileReadWrite.readInitialFile(initial_filename)
                if init_param is not None:
                    veg_filename = os.path.join(self.model_directory, init_param.veg_file_name)
                    vegList = FileReadWrite.readVegFile(veg_filename)
                    epc_filename = ""

                    for veg in vegList:
                        if veg.siteIndex == site_index and veg.vegetationNumber == veg_no:
                            epc_filename = veg.epcFileName
                            break

                    if len(epc_filename) > 0:
                        new_harvest_file = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "Harvest file (*.txt)")
                        if len(new_harvest_file) > 0: ret_val = input_package.change_harvest_file(epc_filename, new_harvest_file)
                        # else: message = "No file was chosen!"
                else: message = "Unexpected Error!"
            if len(message) > 0: QtGui.QMessageBox.about(self.form, "Sorry", message)

        if ret_val: self.input_file_validity_check(initial_filename)

    def pushButtonOk_clicked(self):
        self.form.parentWidget().close()
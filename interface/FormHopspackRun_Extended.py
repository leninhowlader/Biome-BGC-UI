from interface.FormHopspackRun import Ui_FormHopspackRun
from application import ApplicationProperty
from PyQt5 import QtGui, QtWidgets
from hopspack.configure import Configure
from interface.DialogShowLog_Extended import DialogLogShow
import os
from file_io import FileReadWrite
from subprocess import call


class FormHopspackRun(Ui_FormHopspackRun):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)

        self.add_socket()

        self.model_directory = ''
        self.model_executable = ''

        self.dialog_show_log = None

    def add_socket(self):
        self.buttonClose.clicked.connect(self.buttonClose_clicked)
        self.buttonBrowseInitialFile.clicked.connect(self.buttonBrowseInitialFile_clicked)
        self.buttonRun.clicked.connect(self.buttonRun_clicked)
        self.buttonBrowseModelExecutable.clicked.connect(self.buttonBrowseModelExecutable_clicked)

    def buttonClose_clicked(self):
        self.form.parentWidget().close()

    def buttonBrowseInitialFile_clicked(self):
        starting_directory = ApplicationProperty.currentModelDirectory
        if starting_directory == "": starting_directory = ApplicationProperty.getScriptPath ()
        init_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', starting_directory, "Text File (*.ini)")

        if init_filename:
            hosp_set = Configure()

            temp = init_filename.split("/")[-1]
            self.lineEditInitialFile.setText(temp)
            hosp_set.initial_filename = temp

            self.model_directory = init_filename.split("/ini/")[0]
            hosp_set.model_directory = self.model_directory
            hosp_set.write_hopspack_setting()

    def buttonRun_clicked(self):
        if self.model_directory and self.lineEditInitialFile.text() and self.model_executable:
            call("hopspack/run_hopspack.sh" , shell=True)

            reply = QtGui.QMessageBox.question(self.form, 'View Log', "Do you want to open the log file?", QtGui.QMessageBox.Yes,
                                                QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                log_file = 'hopspack/hp.log'
                self.dialog_show_log = DialogLogShow()
                self.dialog_show_log.show_log_file(log_file)
                self.dialog_show_log.form.show()

    def buttonBrowseModelExecutable_clicked(self):
        if self.model_directory == '':
            message = 'Please choose model initialization file.'
            QtGui.QMessageBox.about(self.form, 'Input Required', message)
        else:
            executable_filename = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', self.model_directory, "Executable File")
            if executable_filename:
                self.model_executable = executable_filename.split('/')[-1]
                self.lineEditModelExecutable.setText(self.model_executable)
                bash_file_name = os.path.join(self.model_directory, 'bgc_zalf.sh')
                if not FileReadWrite.write_bash_file_for_linux(bash_file_name, self.model_executable):
                    message = "Hash file could not be created. Please create a hash file manually to run the model."
                    QtGui.QMessageBox.about(self.form, "Hash file error", message)
                else: os.chmod(bash_file_name, 0o0744)


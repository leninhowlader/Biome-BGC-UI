from interface.DialogVersionSettings import Ui_DialogVersionSettings
from PyQt5 import QtGui, QtCore, QtWidgets

class DialogVersionSettings(Ui_DialogVersionSettings):
    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        self.add_socket()

        self.model_version = model_version()

        self.add_validator()
        self.initial_setting()



    def add_socket(self):
        self.radioButtonStartNewVersion.toggled.connect(self.radioButtonStartNewVersion_toggled)
        self.checkBoxContinueFromInitFile.toggled.connect(self.checkBoxContinueFromInitFile_toggled)
        self.checkBoxContinueFrom.toggled.connect(self.checkBoxContinueFrom_toggled)
        self.textCurrentVersion.textChanged.connect(self.textCurrentVersion_textChanged)
        self.radioButtonAddVersionNoToFile.toggled.connect(self.radioButtonAddVersionNoToFile_toggled)
        self.buttonCancel.clicked.connect(self.buttonCancel_clicked)

    def add_validator(self):
        rx = QtCore.QRegExp("^[0-9]{2}$")
        versionValidator = QtGui.QRegExpValidator(rx)

        self.textCurrentVersion.setValidator(versionValidator)

    def initial_setting(self):
        if self.model_version.start_from_zero:
            self.radioButtonStartNewVersion.setChecked(True)
            self.checkBoxContinueFromInitFile.setEnabled(False)
            self.checkBoxContinueFrom.setEnabled(False)
            self.textCurrentVersion.setEnabled(False)
        else:
            if self.model_version.continue_from_initial_parameter_version:
                self.checkBoxContinueFromInitFile.setEnabled(True)
                self.checkBoxContinueFromInitFile.setChecked(True)
                self.checkBoxContinueFrom.setEnabled(True)
                self.textCurrentVersion.setEnabled(False)
            else:
                self.checkBoxContinueFromInitFile.setEnabled(True)
                self.checkBoxContinueFrom.setEnabled(True)
                self.checkBoxContinueFrom.setChecked(True)
                self.textCurrentVersion.setEnabled(False)

                if self.model_version.start_version_number_from > 0:
                    self.textCurrentVersion.setEnabled(True)
                    self.textCurrentVersion.setText(str(self.model_version.start_version_number_from))
                else: self.textCurrentVersion.clear()
        if self.model_version.replace_last_two_digit: self.radioButtonReplaceVersionNumberInFile.setChecked(True)
        else: self.radioButtonAddVersionNoToFile.setChecked(True)

    def radioButtonStartNewVersion_toggled(self):
        if self.radioButtonStartNewVersion.isChecked():
            self.model_version.start_from_zero = True
            self.checkBoxContinueFromInitFile.setEnabled(False)
            self.checkBoxContinueFrom.setEnabled(False)
            self.textCurrentVersion.setEnabled(False)
            self.checkBoxContinueFromInitFile.setChecked(False)
            self.checkBoxContinueFrom.setChecked(False)
            self.lblExample.setText(self.model_version.next_initial_filename())
        else:
            self.model_version.start_from_zero = False
            self.checkBoxContinueFromInitFile.setEnabled(True)
            self.checkBoxContinueFrom.setEnabled(True)
            self.textCurrentVersion.setEnabled(False)
            self.checkBoxContinueFromInitFile.setChecked(True)

    def checkBoxContinueFromInitFile_toggled(self):
        if self.checkBoxContinueFromInitFile.isChecked():
            self.model_version.continue_from_initial_parameter_version = True
            self.checkBoxContinueFrom.setChecked(False)
            self.radioButtonReplaceVersionNumberInFile.setChecked(True)
            self.radioButtonAddVersionNoToFile.setEnabled(False)
            self.lblExample.setText(self.model_version.next_initial_filename())
        else:
            self.model_version.continue_from_initial_parameter_version = False
            self.radioButtonAddVersionNoToFile.setChecked(True)
            self.radioButtonAddVersionNoToFile.setEnabled(True)
            if self.radioButtonContinuePreviousVersioning.isChecked(): self.lblExample.clear()

    def checkBoxContinueFrom_toggled(self):
        if self.checkBoxContinueFrom.isChecked():
            self.checkBoxContinueFromInitFile.setChecked(False)
            self.textCurrentVersion.setEnabled(True)
            self.textCurrentVersion.setFocus(True)
        else:
            self.textCurrentVersion.clear()
            self.textCurrentVersion.setEnabled(False)

    def textCurrentVersion_textChanged(self):
        if len(self.textCurrentVersion.text().strip()) > 0:
            version_number = 0
            try: version_number = int(self.textCurrentVersion.text().strip())
            except: pass
            if version_number > 0:
                self.model_version.start_version_number_from = version_number
                self.lblExample.setText(self.model_version.next_initial_filename())
            else: self.textCurrentVersion.clear()

    def radioButtonAddVersionNoToFile_toggled(self):
        if self.radioButtonAddVersionNoToFile.isChecked(): self.model_version.replace_last_two_digit = False
        else: self.model_version.replace_last_two_digit = True
        self.lblExample.setText(self.model_version.next_initial_filename())

    def buttonOk_clicked(self):
        self.form.close()
        return self.model_version

    def buttonCancel_clicked(self):
        self.form.close()


class model_version:
    def __init__(self):
        #start option
        self.start_from_zero = True
        self.continue_from_initial_parameter_version = False
        self.start_version_number_from = -1

        #file naming option
        self.replace_last_two_digit = False  #if false, add version number at the end of filename

        #initial filename
        self.first_initial_filename = ""

    def starting_version_number(self):
        if self.start_from_zero: return 0
        else:
            if len(self.first_initial_filename) > 0:
                if self.continue_from_initial_parameter_version:
                    version_number = self.first_initial_filename.replace(".ini","").split("_")[-1]
                    try: return int(version_number)
                    except: return -1
                else:
                    if self.start_version_number_from > 0: return self.start_version_number_from
                    else: return -2
            else: return -3

    def next_initial_filename(self):
        start_version_number = self.starting_version_number()

        initial_filename = ""
        if start_version_number >= 0 and len(self.first_initial_filename) > 0:
            if self.replace_last_two_digit:
                initial_filename = self.first_initial_filename.lower()[:-6] + str(start_version_number + 1).rjust(2, "0") + ".ini"
            else: initial_filename = self.first_initial_filename.lower()[:-4] + "_" + str(start_version_number + 1).rjust(2, "0") + ".ini"

        return initial_filename
from interface.DialogSoilFileName import Ui_DialogSoilFileName
from PyQt5 import QtGui
from application import ApplicationProperty
from file_io import FileReadWrite

class DialogSoilFileName(Ui_DialogSoilFileName):
    def __init__(self):
        self.dialog = QtGui.QDialog()
        self.setupUi(self.dialog)
        self.add_socket()

        self.listOfSoilProfile = None
        self.modelDirectory = ""

    def add_socket(self):
        self.buttonCancel.clicked.connect(self.buttonCancel_clicked)
        self.buttonOk.clicked.connect(self.buttonOk_clicked)


    def buttonCancel_clicked(self):
        self.dialog.close()

    def buttonOk_clicked(self):
        if self.listOfSoilProfile is not None:
            if not self.txtProfileSaveAsFileName.text().strip():
                message = "Please enter Soil Profile file name."
                QtGui.QMessageBox.about(self.form, "Input Required", message)
                self.txtProfileSaveAsFileName.setFocus(True)
            elif not self.txtHorizonSaveAsFileName.text().strip():
                message = "Please enter Horizon file name."
                QtGui.QMessageBox.about(self.form, "Input Required", message)
                self.txtHorizonSaveAsFileName.setFocus(True)
            else:
                initialDirectory = ""
                if self.modelDirectory: initialDirectory = self.modelDirectory + "/soil/"
                else:
                    #browse model directory folder
                    initialDirectory = str(QtWidgets.QFileDialog.getExistingDirectory(self.form, "Select Directory", ApplicationProperty.getScriptPath()
                                                                                , QtWidgets.QFileDialog.ShowDirsOnly))
                    if len(initialDirectory) == 0: return False
                    else:
                        self.modelDirectory = initialDirectory
                        initialDirectory = initialDirectory + "/soil/"

                profileFileName = initialDirectory + self.txtProfileSaveAsFileName.text().strip()
                if profileFileName[-4:].lower() != ".txt": profileFileName = profileFileName + ".txt"

                horizonFileName = initialDirectory + self.txtHorizonSaveAsFileName.text().strip()
                if horizonFileName[-4:].lower() != ".txt": horizonFileName = horizonFileName + ".txt"

                if len(profileFileName) > 0 and len(horizonFileName) > 0:
                    if FileReadWrite.writeSoilProfile(self.listOfSoilProfile, profileFileName, horizonFileName):
                        message = "Profile and Horizon files have been saved successfully."
                        QtGui.QMessageBox.about(self.dialog, "Saved Successfully", message)
                        self.txtProfileSaveAsFileName.clear()
                        self.txtHorizonSaveAsFileName.clear()
                else:
                    message = "Soil file could not be saved. Please check inputs."
                    QtGui.QMessageBox.about(self.dialog, "Unexpected Error", message)
            self.dialog.close()
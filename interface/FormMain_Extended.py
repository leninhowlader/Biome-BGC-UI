from interface.FormMain import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from interface.FormInitialAndOutputSetting_Extended import FormInitialAndOutputSetting
from interface.FormGisFile_Extended import FormGisFile
from interface.FormVegFile_Extended import FormVegFile
from interface.FormEpcFile_Extended import FormEpcFile
from interface.FormModelRun_Extended import FormModelRun
from interface.FormSoilProfile_Extended import FormSoilProfile
from interface.FormSpssScript_Extended import FormSpssScript
from interface.FormReadOutput_Extended import FormReadOutput
from interface.FormDesignGraph_Extended import FormDesignGraph
from interface.FormShowGraph_Extended import FormShowGraph
from interface.FormInputPackage_extended import FormInputPackage
from interface.FormEvaluatorConfiguration_Extended import FormEvaluatorConfiguration
from interface.FormHopspackRun_Extended import FormHopspackRun
from interface.FormHopspackProblemDefinition_Extended import FormHopspackProblemDefinition
import os

class FormMain(Ui_MainWindow):

    def __init__(self):
        self.form = QtWidgets.QMainWindow()
        self.setupUi(self.form)
        self.mdiArea.setViewMode(QtWidgets.QMdiArea.TabbedView)

        self.addSocket()
        self.initForm = None
        self.gisForm = None
        self.vegForm = None
        self.epcForm = None
        self.modelRunForm = None
        self.soilProfile = None
        self.spssScriptForm = None
        self.outputForm = None
        self.graphDesignForm = None
        self.graphShowForm = None
        self.inputPackageForm = None
        self.hopspackConfigForm = None
        self.hopspackRunForm = None
        self.opt_prob_form = None

        self.list_of_child = []
        # self.form.setParent(self.form)

    def clean_children_list(self):
        for i in reversed(range(len(self.list_of_child))):
            try:
                pseudoObject = self.list_of_child[i].form.parentWidget()
            except:
                self.list_of_child.pop(i)
        pseudoObject = None

    def addSocket(self):
        self.menuExit.triggered.connect(self.menuExit_triggered)
        self.actionInitializationFile.triggered.connect(self.actionInitializationFile_triggered)
        self.actionGIS_File.triggered.connect(self.actionGIS_File_triggered)
        self.actionVegetation_File.triggered.connect(self.actionVegetation_File_triggered)
        self.actionEPC_File.triggered.connect(self.actionEPC_File_triggered)
        self.actionExecute_Run.triggered.connect(self.actionExecute_Run_triggered)
        self.actionSoil_Parameter_File.triggered.connect(self.actionSoil_Parameter_File_triggered)
        self.actionINI_File_SPSS_Script.triggered.connect(self.actionINI_File_SPSS_Script_triggered)
        self.actionOpenOutput.triggered.connect(self.actionOpenOutput_triggered)
        self.actionDesign_Graph.triggered.connect(self.actionDesign_Graph_triggered)
        self.actionView_Graph.triggered.connect(self.actionView_Graph_triggered)
        self.actionWindow_View.triggered.connect(self.actionWindow_View_triggered)
        self.actionTabbed_View.triggered.connect(self.actionTabbed_View_triggered)
        self.actionInput_PACK.triggered.connect(self.actionInput_PACK_triggered)
        self.actionClean_Temp_File.triggered.connect(self.actionClean_Temp_File_triggered)
        self.action_evaluator_Configuration.triggered.connect(self.action_evaluator_Configuration_triggered)
        self.actionRun_HOPSPACK.triggered.connect(self.actionRun_HOPSPACK_triggered)
        self.actionHOPSPACK_Problem_Definition.triggered.connect(self.actionHOPSPACK_Problem_Definition_triggered)

    def actionRun_HOPSPACK_triggered(self):
        self.clean_children_list()
        newChileForm = FormHopspackRun()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def action_evaluator_Configuration_triggered(self):
        self.clean_children_list()
        newChileForm = FormEvaluatorConfiguration()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionClean_Temp_File_triggered(self):
        succeed = True
        directory = "temp"
        fileList = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)) ]
        for item in fileList:
            try: os.remove(os.path.join(directory, item))
            except: succeed = False
        if succeed:
            message = str(len(fileList)) + " files has been deleted from temporary folder."
        else: message = "Files could not be deleted."
        QtGui.QMessageBox.about(self.form, "Temp Files", message)


    def actionINI_File_SPSS_Script_triggered(self):
        self.clean_children_list()
        newChileForm = FormSpssScript()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionSoil_Parameter_File_triggered(self):
        self.clean_children_list()
        newChileForm = FormSoilProfile()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionExecute_Run_triggered(self):
        self.clean_children_list()
        newChileForm = FormModelRun()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionEPC_File_triggered(self):
        self.clean_children_list()
        newChileForm = FormEpcFile()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionVegetation_File_triggered(self):
        self.clean_children_list()
        newChileForm = FormVegFile()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionGIS_File_triggered(self):
        self.clean_children_list()
        newChileForm = FormGisFile()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionInitializationFile_triggered(self):
        self.clean_children_list()
        newChileForm = FormInitialAndOutputSetting()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def menuExit_triggered(self):
        self.form.close()

    def actionOpenOutput_triggered(self):
        self.clean_children_list()
        newChileForm = FormReadOutput()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionDesign_Graph_triggered(self):
        self.clean_children_list()
        newChileForm = FormDesignGraph()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionView_Graph_triggered(self):
        self.clean_children_list()
        newChileForm = FormShowGraph()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionTabbed_View_triggered(self):
        if self.actionWindow_View.isChecked(): self.actionWindow_View.setChecked(False)
        if not self.actionTabbed_View.isChecked(): self.actionTabbed_View.setChecked(True)
        self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)

    def actionWindow_View_triggered(self):
        if self.actionTabbed_View.isChecked(): self.actionTabbed_View.setChecked(False)
        if not self.actionWindow_View.isChecked(): self.actionWindow_View.setChecked(True)
        self.mdiArea.setViewMode(QtGui.QMdiArea.SubWindowView)

    def actionInput_PACK_triggered(self):
        self.clean_children_list()
        newChileForm = FormInputPackage()
        self.mdiArea.addSubWindow(newChileForm.form)
        self.list_of_child.append(newChileForm)
        newChileForm.form.show()

    def actionHOPSPACK_Problem_Definition_triggered(self):
        self.clean_children_list()
        newChildForm = FormHopspackProblemDefinition()
        self.mdiArea.addSubWindow(newChildForm.form)
        self.list_of_child.append(newChildForm)
        newChildForm.form.show()

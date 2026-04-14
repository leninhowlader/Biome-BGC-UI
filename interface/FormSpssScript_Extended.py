from interface.FormSpssScript import Ui_FormSpssScript
from PyQt5 import QtGui, QtWidgets
from application import ApplicationProperty
from file_io import FileReadWrite
from read_output import ReadBinaryOutput
import os

class FormSpssScript(Ui_FormSpssScript):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)
        self.addSocket()

        self.outputDirectory = None
        self.initialParam = None

        self.output_header_var = None
        self.spss_nonveg_var = None
        self.spss_veg_var = None
        self.spss_layer_var = None
        self.spss_unit_conversion_table = None

    def addSocket(self):
        self.buttonBrowseInitFile.clicked.connect(self.buttonBrowseInitFile_clicked)
        self.buttonScriptFileName.clicked.connect(self.buttonScriptFileName_clicked)
        self.buttonCreatScript.clicked.connect(self.buttonCreatScript_clicked)
        self.buttonSpssDataDirectory.clicked.connect(self.buttonSpssDataDirectory_clicked)
        self.buttonClose.clicked.connect(self.buttonClose_click)

    def buttonBrowseInitFile_clicked(self):
        startingDirectory = ApplicationProperty.currentModelDirectory
        if startingDirectory == "": startingDirectory = ApplicationProperty.getScriptPath ()
        initFullPath = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', startingDirectory, "Text File (*.ini)")

        if len(initFullPath) > 0:
            self.txtInitFile.setText(initFullPath.split("/")[-1])

            if len(ApplicationProperty.currentModelDirectory) == 0:
                ApplicationProperty.currentModelDirectory = initFullPath.replace("/ini/" + self.txtInitFile.text(), "")

                #read the ini file to get the output list
                initParam = None
                try:
                    initParam = FileReadWrite.readInitialFile(initFullPath)

                except:
                    message = "The initial file could not be read. Please choose a valid initial file."
                    QtGui.QtMessageBox.about(None, "Not a valid File", message)

                if initParam is not None:
                    if self.spss_nonveg_var is None: self.spss_nonveg_var = ReadBinaryOutput.readSpssVariable_nonveg()
                    if self.spss_veg_var is None: self.spss_veg_var = ReadBinaryOutput.readSpssVariable_veg()
                    if self.spss_layer_var is None: self.spss_layer_var = ReadBinaryOutput.readSpssVariable_layer()
                    if self.output_header_var is None: self.output_header_var = ReadBinaryOutput.readOutputHeaderVaribleList()

                    self.initialParam = initParam
                    self.outputDirectory = initFullPath.replace("ini/" + self.txtInitFile.text(), "") + "outputs/"
    #
    # def findSpssVarDescription(self, category, varid):
    #     if category == "nonveg":
    #         for item in self.spss_nonveg_var:
    #             if item["varid"] == varid: return item
    #     elif category == "veg":
    #         for item in self.spss_veg_var:
    #             if item["varid"] == varid: return item
    #
    #     return None

    def writeSpssScript(self, fileName):
        listOfLine = self.spssScriptForBinaryRead()
        if len(listOfLine) > 0:
            try:
                file = open(fileName, "w")
                for line in listOfLine:
                    file.write(line + "\n")
                file.close()
            except:
                message = "The exporting operation could not be completed."
                QtGui.QMessageBox.about(self.form, "Export Error", message)

    def buttonScriptFileName_clicked(self):
        initialDirectory = ApplicationProperty.currentModelDirectory
        if len(initialDirectory) == 0:
            initialDirectory = ApplicationProperty.getScriptPath()

        initFullPath = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save', initialDirectory, "Text File (*.sps)")
        if len(initFullPath) > 0:
            self.txtScriptFileName.setText(initFullPath)

    def buttonCreatScript_clicked(self):
        if len(self.txtInitFile.text()) == 0:
            message = "Please choose an initial file to proceed."
            QtGui.QMessageBox.about(self.form, "Input Required", message)
            #self.txtInitFile.setFocus(True)
        elif len(self.txtScriptFileName.text()) == 0:
            message = "Please enter destination file name."
            QtGui.QMessageBox.about(self.form, "Input Required", message)
        elif len(self.txtSpssDataDirectory.text()) == 0:
            message = "Please enter SPSS data directory."
            QtGui.QMessageBox.about(self.form, "Input Required", message)
        else:
            try:
                if (self.initialParam is None or self.output_header_var is None
                    or self.spss_veg_var is None or self.spss_nonveg_var is None):
                    self.buttonBrowseInitFile_clicked()
                self.writeSpssScript(self.txtScriptFileName.text())
                message = "SPSS Script has been created successfully."
                QtGui.QMessageBox.about(self.form, "Success!", message)

                #initialize component
                self.txtInitFile.setText("")
                self.txtSpssDataDirectory.setText("")
                self.txtScriptFileName.setText("")
                self.outputDirectory = None
                self.initialParam = None
            except:
                message = "An unexpected error occurred. Please try to input all valid Initial File."
                QtGui.QMessageBox.about(self.form, "Unexpected Error!", message)

    def buttonSpssDataDirectory_clicked(self):
        initDirectory = ApplicationProperty.currentModelDirectory
        if len(initDirectory) == 0:
            initDirectory = ApplicationProperty.getScriptPath()
        dirName = str(QtWidgets.QFileDialog.getExistingDirectory(self.form, "Select Directory", initDirectory, QtWidgets.QFileDialog.ShowDirsOnly))
        if len(dirName) > 0: self.txtSpssDataDirectory.setText(dirName)


    def spssScriptForBinaryRead(self):
        listOfLine = []

        #conversion factor
        if self.spss_unit_conversion_table is None: self.spss_unit_conversion_table = ReadBinaryOutput.readUnitConversionTable()


        #split the output_header_var into header_var, header_var_type and output_files_header_detail
        header_var = self.output_header_var["header_var"]
        header_var_type = self.output_header_var["var_type"]
        output_files_header_detail = {}
        for key, value in self.output_header_var.items():
            if key != "header_var" or key != "var_type": output_files_header_detail[key] = value



        existing_output_files = [f for f in os.listdir(self.outputDirectory) if os.path.isfile(os.path.join(self.outputDirectory,f)) ]
        for fileType in output_files_header_detail:
            for output_file_name in existing_output_files:
                fileExtension = output_file_name.split(".")[-1]
                if fileExtension == fileType:#== fileType:
                    #select input variable list from initial file
                    varList = ReadBinaryOutput.FindOutputVariableList(self.initialParam, fileType)

                    if len(varList) > 0:
                        #script for closing all existing datasets in spss
                        listOfLine.append("DATASET CLOSE all.")

                        #inserting header variables
                        header_var_length_total = 0
                        textLine = "/"
                        file_specific_header_detail = output_files_header_detail[fileType]
                        file_specific_header_variable = []  #This list will be used later on for formatting spss variable
                        for i in range(len(file_specific_header_detail)):
                            if int(file_specific_header_detail[i]) == 1:
                                textLine += header_var[i] + "(" + header_var_type[i] + ") "
                                header_var_length_total += int(header_var_type[i][1:])
                                file_specific_header_variable.append(header_var[i])

                        outputFilePrefix = self.initialParam.output_file_prefix.split("/")[-1]
                        target_binary_file = self.outputDirectory + outputFilePrefix + "." + fileType
                        listOfLine.append("FILE HANDLE  TempFile name = '" + target_binary_file + "' /Mode=image lrecl = "
                                          + str(len(varList) * 4 + header_var_length_total) + ".")
                        listOfLine.append("DATA LIST file = TempFile")

                        #header variable and insert output variable
                        listOfLine.append(textLine)
                        var_name_list = ReadBinaryOutput.FindOutputVariableNameList(self.initialParam, fileType, varList)
                        for var_name in var_name_list:
                            listOfLine.append(var_name + " (rb4)")
                        # #this list will be used for labeling ann_lay and day_lay variables
                        # lay_var_label = []
                        #
                        # #insert output variables
                        # output_var_detail = []
                        # if fileType in ["day", "ann", "monavg", "annavg", "day_veg", "ann_veg", "monavg_veg", "annavg_veg", "day_totlay"]:
                        #
                        #     if fileType in ["day", "ann", "monavg", "annavg"]:
                        #         for var in varList:
                        #             output_var_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, self.spss_nonveg_var))
                        #     elif fileType in ["day_veg", "ann_veg", "monavg_veg", "annavg_veg"]:
                        #         for var in varList:
                        #             output_var_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, self.spss_veg_var))
                        #     elif fileType == "day_totlay":
                        #         for var in varList:
                        #             output_var_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, self.spss_layer_var))
                        #     for var in output_var_detail:
                        #         listOfLine.append(var["varName"] + " (rb4)")
                        # elif fileType in ["day_lay", "ann_lay"]:
                        #     org_depth = self.OrganicLayerDepth()
                        #     if org_depth > 0:
                        #         for item in varList:
                        #             if item["layer"].find("-") > 0:
                        #                 temp = item["layer"].split("-")
                        #                 if int(temp[1]) - org_depth == 0: var_post_fix = "O"
                        #                 else:
                        #                     if int(temp[0]) > 0:
                        #                         var_post_fix = str(int(temp[0]) - org_depth) + "_" + str(int(temp[1]) - org_depth)
                        #                     else: var_post_fix = temp[0] + "_" + str(int(temp[1]) - org_depth)
                        #             else:
                        #                 temp = int(item["layer"]) - org_depth
                        #                 if temp < 0: var_post_fix = "M" + str(temp * -1)
                        #                 else: var_post_fix = str(temp)
                        #
                        #             temp = ReadBinaryOutput.findSpssVariableDetail(item["var"], self.spss_layer_var)
                        #             listOfLine.append(temp["varName"] + var_post_fix + " (rb4)")
                        #             lay_var_label.append(temp["varName"] + var_post_fix + " '" + temp["varTitle"] + " in "
                        #                                 + var_post_fix.replace("_", "-") + " cm, simulated'")
                        #     # return None

                        listOfLine.append(".")
                        listOfLine.append("EXECUTE.")

                        #data formatting and manipulation
                        listOfLine.append("CACHE.")
                        listOfLine.append("DATASET NAME " + fileType + ".")
                        listOfLine.append("DATASET ACTIVATE " + fileType + ".")

                        listOfLine.append("COMPUTE index_str = LTRIM(index_str,'0').")
                        listOfLine.append("Execute.")
                        listOfLine.append("Formats year (f4.0).")

                        if "month_str" in file_specific_header_variable:
                            listOfLine.append("COMPUTE month = NUMBER (month_str,F2.0).")
                            listOfLine.append("COMPUTE MonYr=DATE.MOYR(month,year).")
                            listOfLine.append("IF month=1 MonthDays=31.")
                            listOfLine.append("IF month=2 MonthDays=28.")
                            listOfLine.append("IF month=3 MonthDays=31.")
                            listOfLine.append("IF month=4 MonthDays=30.")
                            listOfLine.append("IF month=5 MonthDays=31.")
                            listOfLine.append("IF month=6 MonthDays=30.")
                            listOfLine.append("IF month=7 MonthDays=31.")
                            listOfLine.append("IF month=8 MonthDays=31.")
                            listOfLine.append("IF month=9 MonthDays=30.")
                            listOfLine.append("IF month=10 MonthDays=31.")
                            listOfLine.append("IF month=11 MonthDays=30.")
                            listOfLine.append("IF month=12 MonthDays=31.")
                            listOfLine.append("EXECUTE.")
                            listOfLine.append("FORMATS MonYr(MoYr8) month(F2.0).")
                            listOfLine.append("DELETE VARIABLES month_str.")
                        if "yrday_str" in file_specific_header_variable:
                            listOfLine.append("COMPUTE yrday = NUMBER (yrday_str,F4.0).")
                            listOfLine.append("COMPUTE #y4=year/4.")
                            listOfLine.append("COMPUTE #y4r=Trunc(#y4).")
                            listOfLine.append("If ((#y4r-#y4)=0 and yrday>59) yrday=yrday+1.")
                            listOfLine.append("COMPUTE date=date.yrday(year, yrday).")
                            listOfLine.append("COMPUTE month=xdate.month(date).")
                            listOfLine.append("COMPUTE week=xdate.week(date).")
                            listOfLine.append("COMPUTE year_week = DATE.WKYR(week,year).")
                            listOfLine.append("EXECUTE.")
                            listOfLine.append("FORMATS yrday week month year (F4.0) date(Edate8) year_week (wkyr8).")
                            listOfLine.append("DELETE VARIABLES yrday_str.")
                        if "epc" in file_specific_header_variable:
                            listOfLine.append("COMPUTE epc = LTRIM(epc,'0').")
                            listOfLine.append("Execute.")
                        if "vegtype_idx_str" in file_specific_header_variable:
                            listOfLine.append("COMPUTE vegtype_idx = NUMBER (vegtype_idx_str,F2.0).")
                            listOfLine.append("Execute.")
                        if "age_str" in file_specific_header_variable:
                            listOfLine.append("COMPUTE age = NUMBER (age_str,F4.0).")
                            listOfLine.append("Execute.")
                        if "layer" in file_specific_header_variable:
                            listOfLine.append("VALUE LABELS layer")
                            listOfLine.append("01 'Of_Oh (8 - 6 cm)'")
                            listOfLine.append("02 'Of_Oh (6 - 4 cm)'")
                            listOfLine.append("03 'Of_Oh (4 - 2 cm)'")
                            listOfLine.append("04 'Of_Oh (2 - 0 cm)'")
                            listOfLine.append("05 'I_Ahe (0 - -5 cm)'")
                            listOfLine.append("06 'I_Ahe (-5 - -10 cm)'")
                            listOfLine.append("07 'I_Bsv (-10 - -15 cm)'")
                            listOfLine.append("08 'I_(Sdw)Al-Bv (-15 - -20 cm)'")
                            listOfLine.append("09 'I_(Sdw)Al-Bv (-20 - -25 cm)'")
                            listOfLine.append("10 'I_(Sdw)Al-Bv (-25 - -30 cm)'")
                            listOfLine.append("11 'I_(Sdw)Al-Bv (-30 - -35 cm)'")
                            listOfLine.append("12 'I_(Sdw)Al-Bv (-35 - -40 cm)'")
                            listOfLine.append("13 'I_II_Btv (-40 - -45 cm)'")
                            listOfLine.append("14 'I_II_Btv (-45 - -50 cm)'")
                            listOfLine.append("15 'I_II_Btv (-50 - -55 cm)'")
                            listOfLine.append("16 'I_II_Btv (-55 - -60 cm)'")
                            listOfLine.append("17 'I_II_Btv (-60 - -65 cm)'")
                            listOfLine.append("18 'I_II_Btv (-65 - -70 cm)'")
                            listOfLine.append("19 'I_II_Btv (-70 - -75 cm)'")
                            listOfLine.append("20 'II_Btv (-75 - -95 cm)'")
                            listOfLine.append("21 'III_Bv-Cv (-95 - -115 cm)'")
                            listOfLine.append("22 'III_Bv-Cv (-115 - -135 cm)'")
                            listOfLine.append("23 'III_Cv (-135 - -155 cm)'")
                            listOfLine.append("24 'III_Cv (-155 - -175 cm)'")
                            listOfLine.append("25 'III_Cv (-175 - -195 cm)'")
                            listOfLine.append("26 'III_Cv (-195 - -215 cm)'")
                            listOfLine.append("27 'III_Cv (-215 - -235 cm)'")
                            listOfLine.append("28 'III_Cv_2 (-235 - -255 cm)'")
                            listOfLine.append("29 'III_Cv_2 (-255 - -275 cm)'")
                            listOfLine.append("30 'IV_Cv (-275 - -295 cm)'")
                            listOfLine.append("31 'V_Cv (-295 - -315 cm)'")
                            listOfLine.append("32 'V_Cv (-315 - -335 cm)'")
                            listOfLine.append("33 'V_Cv (-335 - -355 cm)'")
                            listOfLine.append(".")

                        #unit conversion
                        for item in self.spss_unit_conversion_table:
                            count = 0
                            cftext = ""        #cfValue = conversion factor
                            if fileType.find("day") != -1:
                                cftext = item["cfDaily"]
                            elif fileType.find("monavg") != -1:
                                cftext = item["cfMonthAvg"]
                            elif fileType.find("ann") != -1:
                                cftext = item["cfAnnual"]
                            elif fileType.find("annavg") != -1:
                                cftext = item["cfAnnulaAvg"]

                            if cftext != "":
                                for var_name in var_name_list:
                                    if item["varPFix"] == var_name[:2]:
                                        listOfLine.append("COMPUTE " + var_name + " = " + var_name + " * " + cftext + ".")
                                        count +=1
                            if count > 0: listOfLine.append("Execute.")

                        #insert variable labels
                        var_label_list = ReadBinaryOutput.FindVariableLabelList(self.initialParam, fileType, varList)
                        insert_label = False
                        for label in var_label_list:
                            if len(label) > 0:
                                insert_label = True
                                break
                        if insert_label:
                            listOfLine.append("VARIABLE LABELS")
                            for i in range(len(var_name_list)):
                                var_name = var_name_list[i]
                                var_label = var_label_list[i]
                                if len(var_label) > 0:
                                    listOfLine.append(var_name + " '" + var_label + "'")
                            listOfLine.append(".")

                        # if fileType not in ["day_lay", "ann_lay"]:
                        #     labeledVarList = []
                        #     for var in output_var_detail:
                        #         varName = var["varName"]
                        #         varTitle = var["varTitle"]
                        #         if len(varTitle) > 0:
                        #             labeledVarList.append(varName + " '" + varTitle + "'")
                        #     if len(labeledVarList) > 0:
                        #         listOfLine.append("VARIABLE LABELS")
                        #         for item in labeledVarList: listOfLine.append(item)
                        #         listOfLine.append(".")
                        # else:
                        #     if len(lay_var_label) > 0:
                        #         listOfLine.append("VARIABLE LABELS")
                        #         for item in lay_var_label:
                        #             listOfLine.append(item)
                        #         listOfLine.append(".")


                        #sorting file before output
                        listOfLine.append("SORT CASES BY index_str year.")
                        listOfLine.append("SAVE OUTFILE = '" + self.txtSpssDataDirectory.text() +
                                          self.initialParam.output_file_prefix.replace("outputs","") + "_"+ fileType +".sav'")
                        listOfLine.append("/COMPRESSED.")

        return listOfLine

    # def inputVariableList(self, output_file_type):
    #     varList = None
    #
    #     if self.initialParam is not None:
    #         if output_file_type == "ann":
    #             varList = self.initialParam.output_template.site_specific_annual_output
    #         elif output_file_type == "day":
    #             varList = self.initialParam.output_template.site_specific_daily_output
    #         elif output_file_type == "ann_veg":
    #             varList = self.initialParam.output_template.veg_specific_annual_output
    #         elif output_file_type == "day_veg":
    #             varList = self.initialParam.output_template.veg_specific_daily_output
    #         elif output_file_type == "ann_lay":
    #             varList = []
    #             for item in self.initialParam.output_template.annual_variable_layer_output:
    #                 for i in range(len(item[1])): varList.append({"var":item[0], "layer": item[1][i]})
    #             for item in self.initialParam.output_template.annual_layer_variable_output:
    #                 for i in range(len(item[1])): varList.append({"var": item[1][i], "layer": item[0]})
    #         elif output_file_type == "day_lay":
    #             varList = []
    #             for item in self.initialParam.output_template.daily_variable_layer_output:
    #                 for i in range(len(item[1])): varList.append({"var": item[0], "layer": item[1][i]})
    #             for item in self.initialParam.output_template.daily_layer_variable_output:
    #                 for i in range(len(item[1])): varList.append({"var": item[1][i], "layer": item[0]})
    #         elif output_file_type == "day_totlay":
    #             varList = self.initialParam.output_template.total_layer_output
    #         elif output_file_type == "annavg":
    #             varList = self.initialParam.output_template.site_specific_daily_output
    #         elif output_file_type == "annavg_veg":
    #             varList = self.initialParam.output_template.veg_specific_daily_output
    #         elif output_file_type == "monavg":
    #             varList = self.initialParam.output_template.site_specific_daily_output
    #         elif output_file_type == "monavg_veg":
    #             varList = self.initialParam.output_template.veg_specific_daily_output
    #
    #     return varList

    def OrganicLayerDepth(self):
        org_depth = -999

        #read the gis file
        # temp = self.txtInitFile.text().split("/")[-1]
        targetDir = ApplicationProperty.currentModelDirectory + "/"
        siteList = FileReadWrite.readGisFile(targetDir + self.initialParam.gis_file_name)
        for site in siteList:
            soilProfileList = FileReadWrite.readSoilProfile(targetDir + "soil/" + site.soilProfileFileName,
                                                                targetDir + "soil/" + site.soilHorizonFileName)
            for profile in soilProfileList:
                if profile.profileName == site.profileName:
                    for layer in profile.soilLayerList:
                        if layer.soilTexture == "O": org_depth = layer.depthOfHorizon
                        break
                if org_depth != 999: break
            if org_depth != 999: break

        return org_depth

    def buttonClose_click(self):
        self.form.parentWidget().close()
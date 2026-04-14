# from os import walk
# from os import listdir
# from os.path import isfile, join, exists
import os
#from PyQt5 import QtGui
from application import ApplicationProperty
from parameter import InitialParameter
from parameter import GisParameter
from parameter import VegetationParameter
from parameter import EpcParameter
from parameter import SoilProfile
from parameter import SoilLayer
#from PyQt5 import QtCore


# try:
#     _fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
#     def _fromUtf8(s):
#         return s


class FileReadWrite:
    # def __init__(self):
    #     pass

    # @staticmethod
    # def outputTemplateList():
    #     templateList = []
    #     tarDir = ApplicationProperty().getScriptPath() + "/outputtemplate"
    #
    #     fileList = [f for f in os.listdir(tarDir) if os.path.isfile(os.path.join(tarDir,f)) ]
    #     for item in fileList:
    #         templateList.append(item.replace(".txt",""))
    #
    #     return templateList

    @staticmethod
    def siteSpecificOutputCategoryList():
        categoryList = []
        tarDir = ApplicationProperty().getScriptPath() + "/variablelist/sitespecific/site_variable_list.txt"
        try:
            file = open(tarDir)
            for line in file.readlines():
                temp = line.replace("\n","").split(", ")
                var = {"catid": temp[0], "catname": temp[1]}
                categoryList.append(var)
            #categoryList.append(file.readlines())
            file.close()
        except Exception as ex:
            return None

        return  categoryList

    @staticmethod
    def vegetationSpecificOutputCategoryList():
        categoryList = []
        tarDir = ApplicationProperty().getScriptPath() + "/variablelist/vegspecific/veg_variable_list.txt"

        try:
            file = open(tarDir)
            for line in file.readlines():
                if line:
                    temp = line.replace("\n","").split(",")
                    if temp:
                        var = {"catid": temp[0], "catname": temp[1]}
                        categoryList.append(var)
            file.close()
        except Exception as Ex:
            return None

        return  categoryList

    @staticmethod
    def siteSpecificOutputVariableList(categoryId):
        varList = []
        tarDir = os.path.join(ApplicationProperty().getScriptPath(), "variablelist", "sitespecific", categoryId + ".txt")

        try:
            file = open(tarDir)
            for line in file.readlines():
                if line:
                    temp = line.replace("\n","").split(",")
                    var = {"catid": categoryId, "varid": int(temp[0].strip()),
                           "varname": temp[1].strip(), "vardesc": temp[2].strip()}
                    varList.append(var)
            file.close()
        except Exception as Ex:
            pass
        return varList

    @staticmethod
    def vegetationSpecificOutputVariableList(categoryId):
        varList = []
        tarDir = ApplicationProperty().getScriptPath() + "/variablelist/vegspecific/" + categoryId + ".txt"

        try:
            file = open(tarDir)
            for line in file.readlines():
                if line:
                    temp = line.replace("\n","").split(",")
                    var = {"catid": categoryId, "varid": int(temp[0].strip()),
                           "varname": temp[1].strip(), "vardesc": temp[2].strip()}
                    varList.append(var)
            file.close()
        except Exception as Ex:
            pass
        return varList

    @staticmethod
    def layerSpecificOutputVariableList():
        varList = []
        tarDir = ApplicationProperty().getScriptPath() + "/variablelist/layerspecific/layer_variable_list.txt"

        try:
            file = open(tarDir)
            for line in file.readlines():
                if line:
                    temp = line.replace("\n","").split(",")
                    var = {"varid": temp[0].strip(), "varname": temp[1].strip(), "vardesc": temp[2].strip()}
                    varList.append(var)
        except: pass
        finally:
            try: file.close()
            except: pass

        return varList

    @staticmethod
    def readInitialFile(initFileName):
        init_param = InitialParameter()

        file = None
        try:
            keylist = ["GIS_FILE", "RESTART", "VEG_INI_FILE", "TIME_DEFINE", "CLIM_CHANGE",
                       "CO2_CONTROL", "NDEP_CONTROL", "OUTPUT_CONTROL",
                       "DAILY_OUTPUT", "DAILY_OUTPUT_VEG", "DAILY_OUTPUT_TOTLAY",
                       "DAY_DEPTH_OUTPUT", "DAY_VAR_OUTPUT", "ANNUAL_OUTPUT",
                       "ANNUAL_OUTPUT_VEG", "ANN_DEPTH_OUTPUT", "ANN_VAR_OUTPUT", "END_INIT"]

            keyword = ""
            count = 0

            file = open(initFileName, 'r')

            for line in file.readlines():
                temp = line.strip().split("\t")[0].strip().split(" ")[0]

                if temp:
                    if temp in keylist:
                        keyword = temp
                    else:
                        if keyword:
                            if keyword.upper() == "GIS_FILE":
                                init_param.gis_file_name = temp
                            elif keyword.upper() == "VEG_INI_FILE":
                                init_param.veg_file_name = temp
                            elif keyword.upper() == "RESTART":
                                if count == 0:
                                    init_param.restart_read_flag = int(temp)
                                    count += 1
                                elif count == 1:
                                    init_param.restart_write_flag = int(temp)
                                    count += 1
                                elif count == 2:
                                    init_param.restart_metyear_use_flag = int(temp)
                                    count += 1
                                elif count == 3:
                                    init_param.restart_read_file_name = temp
                                    count += 1
                                elif count == 4:
                                    init_param.restart_write_file_name =temp
                                    count = 0
                            elif keyword.upper() == "TIME_DEFINE":
                                if count == 0:
                                    init_param.no_of_sim_year = int(temp)
                                    count += 1
                                elif count == 1:
                                    init_param.sim_start_year = int(temp)
                                    count += 1
                                elif count == 2:
                                    init_param.sim_spinup_flag = int(temp)
                                    count += 1
                                elif count == 3:
                                    init_param.no_of_spinup_year = int(temp)
                                    count = 0
                            elif keyword.upper() == "CLIM_CHANGE":
                                if count == 0:
                                    init_param.Tmax_offset = float(temp)
                                    count += 1
                                elif count == 1:
                                    init_param.Tmin_offset = float(temp)
                                    count += 1
                                elif  count == 2:
                                    init_param.precipitation_multiplier = float(temp)
                                    count += 1
                                elif count == 3:
                                    init_param.vpd_multiplier = float(temp)
                                    count += 1
                                elif count == 4:
                                    init_param.swave_multiplier = float(temp)
                                    count = 0
                            elif keyword.upper() == "CO2_CONTROL":
                                if count == 0:
                                    init_param.carbon_variability_flag = int(temp)
                                    count += 1
                                elif count == 1:
                                    init_param.air_constant_carbon = float(temp)
                                    count += 1
                                elif count == 2:
                                    init_param.carbon_file = temp
                                    count = 0
                            elif keyword.upper() == "NDEP_CONTROL":
                                if count == 0:
                                    init_param.nitrogen_depo_option_flag = int(temp)
                                    count += 1
                                elif count == 1:
                                    init_param.industrial_ref_year = int(temp)
                                    count = 0
                            elif keyword.upper() == "OUTPUT_CONTROL":
                                if count == 0:
                                    init_param.output_file_prefix = temp
                                    count += 1
                                elif count == 1:
                                    init_param.daily_output_flag = int(temp)
                                    count += 1
                                elif count == 2:
                                    init_param.monthly_average_flag = int(temp)
                                    count += 1
                                elif count == 3:
                                    init_param.annual_average_flag = int(temp)
                                    count += 1
                                elif count == 4:
                                    init_param.annual_output_flag = int(temp)
                                    count += 1
                                elif count == 5:
                                    init_param.display_flag = int(temp)
                                    count = 0
                            elif keyword.upper() == "DAILY_OUTPUT":
                                if count == 0:
                                    count = int(temp)
                                elif count > 0:
                                    # modelParam.output_template.site_specific_daily_output.append(temp)
                                    init_param.output.addVariableToSelectedSiteSpecificList_Daily_ByVarId(int(temp))
                                    count -= 1
                            elif keyword.upper() == "DAILY_OUTPUT_VEG":
                                if count == 0:
                                    count = int(temp)
                                elif count > 0:
                                    # modelParam.output_template.veg_specific_daily_output.append(temp)
                                    init_param.output.addVariableToSelectedVegetationSpecificList_Daily_ByVarId(int(temp))
                                    count -= 1
                            elif keyword.upper() == "DAILY_OUTPUT_TOTLAY":
                                if count == 0: count = int(temp)
                                elif count > 0:
                                    # modelParam.output_template.total_layer_output.append(temp)
                                    init_param.output.addVariableToSelectedTotalLayer_ByVarId(temp)
                                    count -= 1
                            elif keyword.upper() == "DAY_DEPTH_OUTPUT":
                                if count == 0: count = int(temp)
                                elif count > 0:
                                    layer = line.strip().split(":")[0].strip()
                                    varlist = line.strip().split(":")[1].strip().split(" ")
                                    # item = [layer, varlist]
                                    # modelParam.output_template.daily_layer_variable_output.append(item)
                                    for varid in varlist:
                                        init_param.output.addVariableToDailyLayerVarList_VarId(layer, varid)
                                    count -= 1
                            elif keyword.upper() == "DAY_VAR_OUTPUT":
                                if count == 0: count = int(temp)
                                elif count > 0:
                                    var = line.strip().split(":")[0].strip()
                                    laylist = line.strip().split(":")[1].strip().replace("\n","").replace("\t","").split(" ")
                                    # item = [var,laylist]
                                    # modelParam.output_template.daily_variable_layer_output.append(item)
                                    for layer in laylist:
                                        init_param.output.addVariableToDailyVarLayList_VarId(var, layer)
                                    count -= 1
                            elif keyword.upper() == "ANNUAL_OUTPUT":
                                if count == 0: count = int(temp)
                                elif count > 0:
                                    # modelParam.output_template.site_specific_annual_output.append(temp)
                                    init_param.output.addVariableToSelectedSiteSpecificList_Annual_ByVarId(int(temp))
                                    count -= 1
                            elif keyword.upper() == "ANNUAL_OUTPUT_VEG":
                                if count == 0: count = int(temp)
                                elif count > 0:
                                    # modelParam.output_template.veg_specific_annual_output.append(temp)
                                    init_param.output.addVariableToSelectedVegetationSpecificList_Annual_ByVarId(int(temp))
                                    count -= 1
                            elif keyword.upper() == "ANN_DEPTH_OUTPUT":
                                if count == 0: count = int(temp)
                                elif count > 0:
                                    layer = line.strip().split(":")[0].strip()
                                    varlist = line.strip().split(":")[1].strip().split(" ")
                                    # item = [layer, varlist]
                                    # modelParam.output_template.annual_layer_variable_output.append(item)
                                    for varid in varlist:
                                        init_param.output.addVariableToAnnualLayerVarList_VarId(layer, varid)
                                    count -= 1
                            elif keyword.upper() == "ANN_VAR_OUTPUT":
                                if count == 0: count = int(temp)
                                elif count > 0:
                                    var = line.strip().split(":")[0].strip()
                                    laylist = line.strip().split(":")[1].strip().split(" ")
                                    # item = [var, laylist]
                                    # modelParam.output_template.annual_variable_layer_output.append(item)
                                    for layer in laylist:
                                        init_param.output.addVariableToAnnualVarLayList_VarId(var, layer)
                                    count -= 1
        except Exception as ex:
            return None
        finally:
            try: file.close()
            except: pass

        return init_param

    @staticmethod
    def readOutputTemplate(templateName):
        fileName = ApplicationProperty().getScriptPath() + "/outputtemplate/" + templateName + ".txt"
        return FileReadWrite.readInitialFile(fileName).output

    @staticmethod
    def writeInitialFile(init_param, fileName):
        success = True

        file = None
        try:
            file = open(fileName, mode = 'w')

            line = ""
            keyword_note = "(keyword - do not remove)"
            remark = ""

            line = "Biome-BGC-ZALF-Multiveg\n"
            file.write(line)

            #GIS_FILE
            line = "GIS_FILE" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\t(path/file)\tgis-data-file"
            line = init_param.gis_file_name + remark + "\n"
            file.write(line)
            file.write("\n")

            #VEG_INI_FILE
            line = "VEG_INI_FILE" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\t(path/file)\tveg-data-file"
            file.write(init_param.veg_file_name + remark + '\n')
            file.write("\n")

            #RESTART
            line = "RESTART" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\t(flag)\t\t1 = read restart file\t0 = don't read restart file"
            line = str(init_param.restart_read_flag) + remark + "\n"
            file.write(line)

            remark = "\t(flag)\t\t1 = write restart file\t0 = don't write restart file"
            line = str(init_param.restart_write_flag) + remark + "\n"
            file.write(line)

            remark = "\t(flag)\t\t1 = use restart metyear\t0 = reset metyear"
            line = str(init_param.restart_metyear_use_flag) + remark + "\n"
            file.write(line)

            remark = "\t(path/file)\t\tinput restart filename"
            line = init_param.restart_read_file_name + remark + "\n"
            file.write(line)

            remark = "\t(path/file)\t\toutput restart filename"
            line = init_param.restart_write_file_name + remark + "\n"
            file.write(line)
            file.write("\n")

            #TIME_DEFINE
            line = "TIME_DEFINE" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\t(int)\t\tnumber of simulation years"
            line = str(init_param.no_of_sim_year) + remark + "\n"
            file.write(line)

            remark = "\t(int)\t\tfirst simulation year"
            line = str(init_param.sim_start_year) + remark + "\n"
            file.write(line)

            remark = "\t(flag)\t\t1 = spinup simulation\t0 = normal simulation"
            line = str(init_param.sim_spinup_flag) + remark + "\n"
            file.write(line)

            remark = "\t(int)\t\tmaximum number of spinup years (if spinup simulation)"
            line = str(init_param.no_of_spinup_year) + remark + "\n"
            file.write(line)
            file.write("\n")

            #CLIM_CHANGE
            line = "CLIM_CHANGE" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\t(deg C)\t\toffset for Tmax"
            line = str(init_param.Tmax_offset) + remark + "\n"
            file.write(line)

            remark = "\t(deg C)\t\toffset for Tmin"
            line = str(init_param.Tmin_offset) + remark + "\n"
            file.write(line)

            remark = "\t(DIM)\t\tmultiplier for Prcp"
            line = str(init_param.precipitation_multiplier) + remark + "\n"
            file.write(line)

            remark = "\t(DIM)\t\tmultiplier for VPD"
            line = str(init_param.vpd_multiplier) + remark + "\n"
            file.write(line)

            remark = "\t(DIM)\t\tmultiplier for shortwave radiation"
            line = str(init_param.swave_multiplier) + remark + "\n"
            file.write(line)
            file.write("\n")

            #CO2_CONTROL
            line = "CO2_CONTROL" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\t(flag)\t\t0 = constant,\t1 = vary with file"
            line = str(init_param.carbon_variability_flag) + remark + "\n"
            file.write(line)

            remark = "\t(ppm)\t\tconstant atmospheric CO2 concentration"
            line = str(init_param.air_constant_carbon) + remark + "\n"
            file.write(line)

            remark = "\t(path)\t\tfile)annual variable CO2 filename"
            line = init_param.carbon_file + remark + "\n"
            file.write(line)


            file.write("\n")


            #NDEP_CONTROL
            line = "NDEP_CONTROL" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\t(flag)\t\t0 = constant,\t1 = vary with file named in gis-file,\t2 = do a ramped N-deposition run (only with CO2 flag = 1)"
            line = str(init_param.nitrogen_depo_option_flag) + remark + "\n"
            file.write(line)

            remark = "\t(int)\t\treference year for industrial N deposition (not > max. CO2-file yr), ramped N-deposition"
            line = str(init_param.industrial_ref_year) + remark + "\n"
            file.write(line)
            file.write("\n")




            #writing output list
            success = FileReadWrite.writeOutputList(file,init_param)

            #END_INIT
            line = "END_INIT" + "\t\t\t" + keyword_note + "\n"
            file.write(line)
            file.write("\n")
        except Exception as ex:
            success = False
        finally:
            try: file.close()
            except: pass

        # if failed to complete saving, delete the created/modified file
        if not success:
            try: os.remove(fileName)
            except: pass

        if success and len(init_param.output_template_save_fileName) > 0:
            # saving template if applicable
            try:
                appdir = ApplicationProperty.getScriptPath()
                if init_param.output_template_save_flag == 1:
                    template_filename = os.path.join(appdir, "outputtemplate", init_param.output_template_save_fileName + ".txt")
                    file = open(template_filename, mode='w')
                    success = FileReadWrite.writeOutputList(file, init_param)
            except: pass
            finally:
                try: file.close()
                except: pass

            # if failed to complete saving, delete the created/modified file
            if not success:
                try: os.remove(template_filename)
                except: pass

        return success

    @staticmethod
    def writeOutputList(file, init_param):
        try:
            keyword_note = "(keyword - do not remove)"

            #OUTPUT_CONTROL
            line = "OUTPUT_CONTROL" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\t(path/file)\t\tprefix for output files"
            line = init_param.output_file_prefix + remark + "\n"
            file.write(line)

            remark = "\t(flag)\t\t0 = no daily output\t1 = write daily output\t2 = depth+correspondig vars\t3 = var+corresponding depth\t4 = both depth and var"
            line = str(init_param.daily_output_flag) + remark + "\n"
            file.write(line)

            remark = "\t(flag)\t\t1 = monthly avg of daily variables\t0 = no monthly avg"
            line = str(init_param.monthly_average_flag) + remark + "\n"
            file.write(line)

            remark = "\t(flag)\t\t1 = annual avg of daily variables\t0 = no annual avg"
            line = str(init_param.annual_average_flag) + remark + "\n"
            file.write(line)

            remark = "\t(flag)\t\t0 = no annual output\t1 = write annual output\t2 = depth+correspondig vars\t3 = var+corresponding depth\t4 = both depth and var"
            line = str(init_param.annual_output_flag) + remark + "\n"
            file.write(line)

            remark = "\t(flag)\t\tfor on-screen progress indicator"
            line = str(init_param.display_flag) + remark + "\n"
            file.write(line)
            file.write("\n")

            #DAILY_OUTPUT
            line = "DAILY_OUTPUT" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            remark = "\tnumber of site specific daily output variables"
            var_list = init_param.output.getAllSelectedSiteSpecificVariableList(daily=True)
            line = str(len(var_list)) + remark + "\n"
            file.write(line)

            for var in var_list:
                line = str(var["varid"]) + "\t" + var["varname"] + "\n"
                file.write(line)

            file.write("\n")


            #DAILY_OUTPUT_VEG
            line = "DAILY_OUTPUT_VEG" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            var_list = init_param.output.getAllSelectedVegetationSpecificVariableList(daily=True)
            remark = "\tnumber of vegetation specific daily output variables"
            line = str(len(var_list)) + remark + "\n"
            file.write(line)

            for var in var_list:
                line = str(var["varid"]) + "\t" + var["varname"] + "\n"
                file.write(line)
            file.write("\n")

            #DAILY_OUTPUT_TOTLAY
            line = "DAILY_OUTPUT_TOTLAY" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            var_list = init_param.output.getSelectedTotalLayerVariableList()
            remark = "\tnumber of layers pecific output for all layers"
            line = str(len(var_list)) + remark + "\n"
            file.write(line)

            for var in var_list:
                line = str(var["varid"]) + "\t" + var["varname"] + "\n"
                file.write(line)

            file.write("\n")

            if (init_param.daily_output_flag == 2 or init_param.daily_output_flag == 4 or
                init_param.monthly_average_flag == 1 or init_param.annual_average_flag == 1):
                #DAY_DEPTH_OUTPUT
                line = "DAY_DEPTH_OUTPUT" + "\t\t\t" + keyword_note + "\n"
                file.write(line)

                line_list = init_param.output.getTextLinesFromDailyLayerVarList()
                remark = "\tnumber of layers for specified soil depths"
                line = str(len(line_list)) + remark + "\n"
                file.write(line)

                for line in line_list:
                    line = line.replace(",", "")
                    file.write(line + "\n")
                file.write("\n")

            if (init_param.daily_output_flag == 3 or init_param.daily_output_flag == 4 or
                init_param.monthly_average_flag == 1 or init_param.annual_average_flag == 1):
                #DAY_VAR_OUTPUT
                line = "DAY_VAR_OUTPUT" + "\t\t\t" + keyword_note + "\n"
                file.write(line)

                line_list = init_param.output.getTextLinesFromDailyVarLayerList()
                remark = "\tnumber of layerspecific output for specified layers"
                line = str(len(line_list)) + remark + "\n"
                file.write(line)

                for line in line_list:
                    line = line.replace(",","")
                    file.write(line + "\n")

                file.write("\n")

            #ANNUAL_OUTPUT
            line = "ANNUAL_OUTPUT" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            var_list = init_param.output.getAllSelectedSiteSpecificVariableList(annual=True)
            remark = "\tnumber of site specific annual output variables"
            line = str(len(var_list)) + remark + "\n"
            file.write(line)

            for var in var_list:
                line = str(var["varid"]) + "\t" + var["varname"] + "\n"
                file.write(line)
            file.write("\n")

            #ANNUAL_OUTPUT_VEG
            line = "ANNUAL_OUTPUT_VEG" + "\t\t\t" + keyword_note + "\n"
            file.write(line)

            var_list = init_param.output.getAllSelectedVegetationSpecificVariableList(annual=True)
            remark = "\tnumber of vegetation specific annual output variables"
            line = str(len(var_list)) + remark + "\n"
            file.write(line)

            for var in var_list:
                line = str(var["varid"]) + "\t" + var["varname"] + "\n"
                file.write(line)
            file.write("\n")

            if init_param.annual_output_flag == 2 or init_param.annual_output_flag == 4:
                #ANN_DEPTH_OUTPUT
                line = "ANN_DEPTH_OUTPUT" + "\t\t\t" + keyword_note + "\n"
                file.write(line)

                line_list = init_param.output.getTextLinesFromAnnualLayerVarList()
                remark = "\tnumber of layers for specified soil depths"
                line = str(len(line_list)) + remark + "\n"
                file.write(line)

                for line in line_list:
                    line = line.replace(",","")
                    file.write(line + "\n")

                file.write("\n")

            if init_param.annual_output_flag == 3 or init_param.annual_output_flag == 4:
                #ANN_VAR_OUTPUT
                line = "ANN_VAR_OUTPUT" + "\t\t\t" + keyword_note + "\n"
                file.write(line)

                line_list = init_param.output.getTextLinesFromAnnualVarLayerList()
                remark = "\tnumber of layerspecific output for specified layers"
                line = str(len(line_list)) + remark + "\n"
                file.write(line)

                for line in line_list:
                    line = line.replace(",","")
                    file.write(line + "\n")
                file.write("\n")
        except: return False
        return True

    @staticmethod
    def readGisFile(fileName):
        siteList = []

        file = None
        try:
            file = open(fileName)

            #skiping first three lines
            for i in range(4): file.readline()

            for line in file.readlines():
                line = line.strip()
                while line.find("\t\t") != -1:
                    line = line.replace("\t\t", "\t")

                if len(line) > 0:
                    temp = line.split("\t")

                    site = GisParameter()
                    site.siteIndex = temp[0]
                    site.noOfVegetation = int(temp[1])
                    site.soilProfileFileName = temp[2]
                    site.soilHorizonFileName = temp[3]
                    site.profileName = temp[4]
                    site.groundWaterDepth = float(temp[5])
                    site.groundWaterFlag = int(temp[6])
                    site.reductionFactor = float(temp[7])
                    site.zetaParameter = float(temp[8])
                    site.depthOfDehumidification = float(temp[9])
                    site.yearDay = int(temp[10])
                    site.temperatureTimeLag = float(temp[11])
                    site.amplitudeOfSoilTemperature = float(temp[12])
                    site.increaseOfTemperature = float(temp[13])
                    site.siteElevation = float(temp[14])
                    site.siteLatitude = float(temp[15])
                    site.meteorologicalFileName = temp[16]
                    site.noOfMeteorologicalYear = int(temp[17])
                    site.ndepFileName = temp[18]
                    site.ndepRate = float(temp[19])
                    site.industrialNdepRate = float(temp[20])
                    site.snowWaterPool = float(temp[21])
                    site.fastMicrobialFraction = float(temp[22])
                    site.mediumMicrobialFraction = float(temp[23])
                    site.slowMicrobialFraction = float(temp[24])
                    site.recalcitrantSom = float(temp[25])
                    site.soilMineralNitrogenPool = float(temp[26])

                    siteList.append(site)

        except: pass
        finally:
            try: file.close()
            except: pass

        return siteList

    @staticmethod
    def writeGisFile(fileName, siteList):


        try:
            file = open(fileName, mode = 'w')

            line = "GIS-INI-file\n"
            file.write(line)
            line = "A line contains site information\n"
            file.write(line)
            line = "index\tnumber_vegtypes\tprofile_file\thorizon_file\tprofile_name\tgw_depth\tgw_flag\tfact_kf\tzeta_soil\t"
            line += "dehum_depth\tyday_t0\ttemp_time_lag\tA250\ttemp_increase\televat\tlatit\tmet_file\tmetyears\t"
            line += "ndep_file\tNdep\tind_Ndep\tsnow\tfast\tmedium\tslow\trecalc\tsoiln\n"
            file.write(line)
            line = "int\ttxt\ttxt\ttxt\tm\tDIM\tDIM\tDIM\tm\tyday\tDIM\td C\td C/m\tm\tdeg\ttxt\ta\ttxt\tkgN/m2/a\tkgN/m2/a\t"
            line += "DIM\tDIM\tDIM\tDIM\tDIM\tkgN/m2\n"
            file.write(line)
            for site in siteList:
                line = str(site.siteIndex) + "\t"
                line += str(site.noOfVegetation) + "\t"
                line += site.soilProfileFileName + "\t"
                line += site.soilHorizonFileName + "\t"
                line += site.profileName + "\t"
                line += str(site.groundWaterDepth) + "\t"
                line += str(site.groundWaterFlag) + "\t"
                line += str(site.reductionFactor) + "\t"
                line += str(site.zetaParameter) + "\t"
                line += str(site.depthOfDehumidification) + "\t"
                line += str(site.yearDay) + "\t"
                line += str(site.temperatureTimeLag) + "\t"
                line += str(site.amplitudeOfSoilTemperature) + "\t"
                line += str(site.increaseOfTemperature) + "\t"
                line += str(site.siteElevation) + "\t"
                line += str(site.siteLatitude) + "\t"
                line += site.meteorologicalFileName + "\t"
                line += str(site.noOfMeteorologicalYear) + "\t"
                line += site.ndepFileName + "\t"
                line += str(site.ndepRate) + "\t"
                line += str(site.industrialNdepRate) + "\t"
                line += str(site.snowWaterPool) + "\t"
                line += str(site.fastMicrobialFraction) + "\t"
                line += str(site.mediumMicrobialFraction) + "\t"
                line += str(site.slowMicrobialFraction) + "\t"
                line += str(site.recalcitrantSom) + "\t"
                line += str(site.soilMineralNitrogenPool)
                file.write(line + '\n')
            file.close()
            return True
        except Exception as ex:
            return False

    @staticmethod
    def readVegFile(fileName):

        vegList = []

        try:
            file = open(fileName)
            for i in range(4):
                file.readline()

            for line in file.readlines():
                line = line.strip()
                while line.find("\t\t") != -1:
                    line = line.replace("\t\t", "\t")

                if len(line) > 0:
                    temp = line.strip().split("\t")
                    if len(temp) == 17:
                        veg = VegetationParameter()
                        veg.siteIndex = temp[0]
                        veg.vegetationNumber = int(temp[1])
                        veg.epcFileName = temp[2]
                        veg.standDensity = float(temp[3])
                        veg.startingTreeAge = int(temp[4])
                        veg.startingRootDepth = float(temp[5])
                        veg.treeGrowthClass = int(temp[6])
                        veg.treeHeight = float(temp[7])
                        veg.speciesSeqFile = temp[8]
                        veg.leafCarbon = float(temp[9])
                        veg.stemCarbon = float(temp[10])
                        veg.debrisCarbon = float(temp[11])
                        veg.labilePool = float(temp[12])
                        veg.unshieldedCellulosePool = float(temp[13])
                        veg.shieldedCellulosePool = float(temp[14])
                        veg.ligninPool = float(temp[15])
                        veg.nitrogenLabilePool = float(temp[16])
                        
                        vegList.append(veg)
        except Exception as Ex:
            return None

        return  vegList

    @staticmethod
    def writeVegFile(fileName, vegList):
        try:
            file = open(fileName, mode = 'w')

            line = "VEG-INI-file\n"
            file.write(line)
            line = "A line contains a complete dataset of a vegetation type\n"
            file.write(line)
            line = "index\tveg_type_idx\tepc\tsdens\tage\troot_depth\ttgc\tth\tss_file\tleafc\tstemc\tcwdc\tlitrc1\tlitrc2\tlitrc3\tlitrc4\tlitrn1\n"
            file.write(line)
            line = "int\ttxt\tDIM\ta\tm\tDIM\tm\ttxt\tkgC/m2\tkgC/m2\tkgC/m2\tkgC/m2\tkgC/m2\tkgC/m2\tkgC/m2\tkgN/m2\n"
            file.write(line)
            for veg in vegList:
                line = str(veg.siteIndex) + "\t"
                line += str(veg.vegetationNumber) + "\t"
                line += veg.epcFileName + "\t"
                line += str(veg.standDensity) + "\t"
                line += str(veg.startingTreeAge) + "\t"
                line += str(veg.startingRootDepth) + "\t"
                line += str(veg.treeGrowthClass) + "\t"
                line += str(veg.treeHeight) + "\t"
                line += veg.speciesSeqFile + "\t"
                line += str(veg.leafCarbon) + "\t"
                line += str(veg.stemCarbon) + "\t"
                line += str(veg.debrisCarbon) + "\t"
                line += str(veg.labilePool) + "\t"
                line += str(veg.unshieldedCellulosePool) + "\t"
                line += str(veg.shieldedCellulosePool) + "\t"
                line += str(veg.ligninPool) + "\t"
                line += str(veg.nitrogenLabilePool) + "\n"

                file.write(line)

            file.close()
            # QtGui.QMessageBox.about(None, "Save", "The VEG file has been saved successfully.")
            return True
        except Exception as ex:
            # QtGui.QMessageBox.about(None, "Error", "The file could not be saved.")
            return False

    @staticmethod
    def readEpcFile(fileName):
        """

        :rtype : object
        """
        epc = EpcParameter()

        try:
            file = open(fileName)
            file.readline()

            epc.growthForm = int(file.readline().strip().split('\t')[0])
            epc.leafHabit =  int(file.readline().strip().split('\t')[0])
            epc.photosyntheticPathway =  int(file.readline().strip().split('\t')[0])
            epc.phenologicalControlOption =  int(file.readline().strip().split('\t')[0])
            epc.dayOfYearForStartOfNewLeafGrowth =  int(file.readline().strip().split('\t')[0])
            epc.dayOfYearForMaxLitterFall =  int(file.readline().strip().split('\t')[0])
            epc.growthPeriodDurationFraction =  float(file.readline().strip().split('\t')[0])
            epc.litterfallPeriodDurationFraction =  float(file.readline().strip().split('\t')[0])
            epc.offsetValueForParallelShift =  float(file.readline().strip().split('\t')[0])
            epc.interceptConstantForLeafUnfolding =  float(file.readline().strip().split('\t')[0])
            epc.slopeConstantForLeafUnfolding =  float(file.readline().strip().split('\t')[0])
            epc.tempThresholdForChillDay =  float(file.readline().strip().split('\t')[0])
            epc.tempThresholdForThermalTime =  float(file.readline().strip().split('\t')[0])
            epc.criticalDayLengthForLitterfall =  float(file.readline().strip().split('\t')[0])
            epc.soilTempForLitterfall =  float(file.readline().strip().split('\t')[0])
            epc.prolongLitterfallFactor =  float(file.readline().strip().split('\t')[0])
            epc.annualLeafTurnoverFraction =  float(file.readline().strip().split('\t')[0])
            epc.annualFineRootTurnoverFraction =  float(file.readline().strip().split('\t')[0])
            epc.annualCoarseRootTurnoverFraction =  float(file.readline().strip().split('\t')[0])
            epc.annualLiveWoodTurnoverFraction =  float(file.readline().strip().split('\t')[0])
            epc.annualWholePlantMortalityFraction =  float(file.readline().strip().split('\t')[0])
            epc.annualFireMortalityFraction =  float(file.readline().strip().split('\t')[0])
            epc.ratioOfFineRootToLeafGrowth =  float(file.readline().strip().split('\t')[0])
            epc.ratioOfStemToLeafGrowth =  float(file.readline().strip().split('\t')[0])
            epc.ratioOfLiveWoodToTotalWood =  float(file.readline().strip().split('\t')[0])
            epc.ratioOfCoarseRootToStemGrowth =  float(file.readline().strip().split('\t')[0])
            epc.dailyGrowthProportion =  float(file.readline().strip().split('\t')[0])
            epc.leafCarbonNitrogenMassRatio =  float(file.readline().strip().split('\t')[0])
            epc.leafLitterCarbonNitrogenMassRatio =  float(file.readline().strip().split('\t')[0])
            epc.fineRootCarbonNitrogenMassRatio =  float(file.readline().strip().split('\t')[0])
            epc.coarseRootCarbonNitrogenMassRatio =  float(file.readline().strip().split('\t')[0])
            epc.liveWoodCarbonNitrogenMassRatio =  float(file.readline().strip().split('\t')[0])
            epc.deadWoodCarbonNitrogenMassRatio =  float(file.readline().strip().split('\t')[0])
            epc.stemCoarseRootLitterFraction =  float(file.readline().strip().split('\t')[0])
            epc.leafLitterLabileProportion =  float(file.readline().strip().split('\t')[0])
            epc.leafLitterCelluloseProportion =  float(file.readline().strip().split('\t')[0])
            epc.leafLitterLigninProportion =  float(file.readline().strip().split('\t')[0])
            epc.fineRootLabileProportion =  float(file.readline().strip().split('\t')[0])
            epc.fineRootCelluloseProportion =  float(file.readline().strip().split('\t')[0])
            epc.fineRootLigninProportion =  float(file.readline().strip().split('\t')[0])
            epc.deadWoodCelluloseProportion =  float(file.readline().strip().split('\t')[0])
            epc.deadWoodLigninProportion =  float(file.readline().strip().split('\t')[0])
            epc.canopyWaterInterceptionHeight =  float(file.readline().strip().split('\t')[0])
            epc.stemWaterInterceptionHeight =  float(file.readline().strip().split('\t')[0])
            epc.albedo =  float(file.readline().strip().split('\t')[0])
            epc.canopyLightExtinctionCoefficient =  float(file.readline().strip().split('\t')[0])
            epc.allsidedToProjectedLeafAreaRatio =  float(file.readline().strip().split('\t')[0])
            epc.canopyAverageSecificLeafArea =  float(file.readline().strip().split('\t')[0])
            epc.ratioOfShadedToSunlitSLA =  float(file.readline().strip().split('\t')[0])
            epc.maximumTreeHeight =  float(file.readline().strip().split('\t')[0])
            epc.stemWoodMassAtMaxHeight =  float(file.readline().strip().split('\t')[0])
            epc.fractionOfLeafNitrogenInRubisco =  float(file.readline().strip().split('\t')[0])
            epc.startAgeGrowthReduction =  float(file.readline().strip().split('\t')[0])
            epc.endAgeGrowthReduction =  float(file.readline().strip().split('\t')[0])
            epc.growthReductionFactor =  float(file.readline().strip().split('\t')[0])
            epc.allocationReductionFactor =  float(file.readline().strip().split('\t')[0])
            epc.nitrogenFixation =  float(file.readline().strip().split('\t')[0])
            epc.maxStomatalConductance =  float(file.readline().strip().split('\t')[0])
            epc.cuticularConductance =  float(file.readline().strip().split('\t')[0])
            epc.boundaryLayerConductance =  float(file.readline().strip().split('\t')[0])
            epc.availableSoilWaterFactor =  float(file.readline().strip().split('\t')[0])
            epc.wiltingPointFactor =  float(file.readline().strip().split('\t')[0])
            epc.startOfConductanceReductionForVpd =  float(file.readline().strip().split('\t')[0])
            epc.completeConductanceReductionForVpd =  float(file.readline().strip().split('\t')[0])
            epc.thinningRuleOption =  int(float(file.readline().strip().split('\t')[0]))
            epc.thinningRuleFileName =  file.readline().strip().split('\t')[0]
            epc.stemCarbonThresholdFor1stThinning =  float(file.readline().strip().split('\t')[0])
            epc.firstThinningFraction =  float(file.readline().strip().split('\t')[0])
            epc.thinningRuleCoefficientB00 =  float(file.readline().strip().split('\t')[0])
            epc.thinningRuleCoefficientB01 =  float(file.readline().strip().split('\t')[0])
            epc.thinningRuleCoefficientB10 =  float(file.readline().strip().split('\t')[0])
            epc.thinningRuleCoefficientB11 =  float(file.readline().strip().split('\t')[0])
            epc.thinningRuleCoefficientB12 =  float(file.readline().strip().split('\t')[0])
            epc.startHarvestCoefficientIntercept =  float(file.readline().strip().split('\t')[0])
            epc.startHarvestCoefficientSlope =  float(file.readline().strip().split('\t')[0])
            epc.thinningPeriod =  float(file.readline().strip().split('\t')[0])
            epc.ageOfClearCut =  float(file.readline().strip().split('\t')[0])
            epc.harvestCorrectionFactor =  float(file.readline().strip().split('\t')[0])
            epc.exportFractionCoefficientIntercept =  float(file.readline().strip().split('\t')[0])
            epc.exportfractionCoefficientSlope =  float(file.readline().strip().split('\t')[0])
            epc.optimumTempForRootGrowth =  float(file.readline().strip().split('\t')[0])
            epc.minimumTempForRootGrowth =  float(file.readline().strip().split('\t')[0])
            epc.bdCoefForMaxRootGrowth =  float(file.readline().strip().split('\t')[0])
            epc.criticalPorosity =  float(file.readline().strip().split('\t')[0])
            epc.minPhAllowingRootGrowth =  float(file.readline().strip().split('\t')[0])
            epc.maxPhAllowingRootGrowth =  float(file.readline().strip().split('\t')[0])
            epc.minPhForOptimumRootGrowth =  float(file.readline().strip().split('\t')[0])
            epc.maxPhForOptimumRootGrowth =  float(file.readline().strip().split('\t')[0])
            epc.waterSaturationStress =  float(file.readline().strip().split('\t')[0])
            epc.potentialVerticalRootGrowthRate =  float(file.readline().strip().split('\t')[0])
            epc.maxAgeOfRootGrowth =  float(file.readline().strip().split('\t')[0])
            epc.zetaPlantParameter =  float(file.readline().strip().split('\t')[0])
        except Exception as ex:
            pass
        finally:
            try: file.close()
            except: pass

        return epc

    @staticmethod
    def writeEpcFile(fileName, epc):
        try:
            file = open(fileName, mode = 'w')
            file.write("ECOPHYS\tBiomeBGC\n")

            file.write(str(epc.growthForm) + "\t1 = WOODY\t0 = NON-WOODY\n")
            file.write(str(epc.leafHabit) + "\t1 = EVERGREEN\t0 = DECIDUOUS\n")
            file.write(str(epc.photosyntheticPathway) + "\t1 = C3 PSN\t0 = C4 PSN\n")
            file.write(str(epc.phenologicalControlOption) + "\t1 = MODEL PHENOLOGY\t0 = USER-SPECIFIED PHENOLOGY\n")
            file.write(str(epc.dayOfYearForStartOfNewLeafGrowth) + "\tyearday of the middle of transfer (new growth) period  (when phenology flag = 0)\n")
            file.write(str(epc.dayOfYearForMaxLitterFall) + "\tyearday of the middle of litterfall period  (when phenology flag = 0)\n")
            file.write(str(epc.growthPeriodDurationFraction) + "\ttransfer growth period as fraction of growing season\n")
            file.write(str(epc.litterfallPeriodDurationFraction) + "\tlitterfall as fraction of growing season\n")
            file.write(str(epc.offsetValueForParallelShift) + "\toffset value for parallel translation of onset criterium function (model 1 and 2)\n")
            file.write(str(epc.interceptConstantForLeafUnfolding) + "\tconstant a (intercept) for phenology (model 2)\n")
            file.write(str(epc.slopeConstantForLeafUnfolding) + "\tconstant b (slope) for phenology (model 2)\n")
            file.write(str(epc.tempThresholdForChillDay) + "\tChilldays Temperature Threshold\n")
            file.write(str(epc.tempThresholdForThermalTime) + "\tThermal Time Temperature Threshold\n")
            file.write(str(epc.criticalDayLengthForLitterfall) + "\tcritical (first possible) day length for litterfall (middle of period) (seconds)\n")
            file.write(str(epc.soilTempForLitterfall) + "\tSoil Temperature (Lower Limit) Litterfall\n")
            file.write(str(epc.prolongLitterfallFactor) + "\tLitterfall Elongation Factor\n")
            file.write(str(epc.annualLeafTurnoverFraction) + "\tAnnual Leaf Turnover Fraction\n")
            file.write(str(epc.annualFineRootTurnoverFraction) + "\tAnnual Fine Root Turnover Fraction\n")
            file.write(str(epc.annualCoarseRootTurnoverFraction) + "\tAnnual Coarse Root Turnover Fraction\n")
            file.write(str(epc.annualLiveWoodTurnoverFraction) + "\tannual live wood turnover fraction\n")
            file.write(str(epc.annualWholePlantMortalityFraction) + "\tannual whole-plant mortality fraction\n")
            file.write(str(epc.annualFireMortalityFraction) + "\tannual fire mortality fraction\n")
            file.write(str(epc.ratioOfFineRootToLeafGrowth) + "\t(ALLOCATION) new fine root C : new leaf C\n")
            file.write(str(epc.ratioOfStemToLeafGrowth) + "\t(ALLOCATION) new stem C : new leaf C\n")
            file.write(str(epc.ratioOfLiveWoodToTotalWood) + "\t(ALLOCATION) new live wood C : new total wood C\n")
            file.write(str(epc.ratioOfCoarseRootToStemGrowth) + "\t(ALLOCATION) new croot C : new stem C\n")
            file.write(str(epc.dailyGrowthProportion) + "\t(ALLOCATION) current growth proportion\n")
            file.write(str(epc.leafCarbonNitrogenMassRatio) + "\tC:N of leaves\n")
            file.write(str(epc.leafLitterCarbonNitrogenMassRatio) + "\tC:N of leaf litter, after retranslocation\n")
            file.write(str(epc.fineRootCarbonNitrogenMassRatio) + "\tC:N of fine roots\n")
            file.write(str(epc.coarseRootCarbonNitrogenMassRatio) + "\tC:N of Coarse Roots\n")
            file.write(str(epc.liveWoodCarbonNitrogenMassRatio) + "\tC:N of live wood\n")
            file.write(str(epc.deadWoodCarbonNitrogenMassRatio) + "\tC:N of dead wood\n")
            file.write(str(epc.stemCoarseRootLitterFraction) + "\tLitter Fraction of Stem/Coarse Roots (bark, twigs, branches)\n")
            file.write(str(epc.leafLitterLabileProportion) + "\tleaf litter labile proportion\n")
            file.write(str(epc.leafLitterCelluloseProportion) + "\tleaf litter cellulose proportion\n")
            file.write(str(epc.leafLitterLigninProportion) + "\tleaf litter lignin proportion\n")
            file.write(str(epc.fineRootLabileProportion) + "\tfine root labile proportion\n")
            file.write(str(epc.fineRootCelluloseProportion) + "\tfine root cellulose proportion\n")
            file.write(str(epc.fineRootLigninProportion) + "\tfine root lignin proportion\n")
            file.write(str(epc.deadWoodCelluloseProportion)+ "\tdead wood cellulose proportion\n")
            file.write(str(epc.deadWoodLigninProportion) + "\tdead wood lignin proportion\n")
            file.write(str(epc.canopyWaterInterceptionHeight) + "\tCanopy Water Interception Height\n")
            file.write(str(epc.stemWaterInterceptionHeight) + "\tstem water interceptin height [mm / (kg stem C / m2)]\n")
            file.write(str(epc.albedo) + "\tAlbedo\n")
            file.write(str(epc.canopyLightExtinctionCoefficient) + "\tcanopy light extinction coefficient\n")
            file.write(str(epc.allsidedToProjectedLeafAreaRatio) + "\tAll-Sided to Projected Leaf Area Ratio\n")
            file.write(str(epc.canopyAverageSecificLeafArea) + "\tcanopy average specific leaf area (projected area basis)\n")
            file.write(str(epc.ratioOfShadedToSunlitSLA) + "\tRatio of Shaded SLA:Sunlit SLA\n")
            file.write(str(epc.maximumTreeHeight) + "\tMaximum Height [m]\n")
            file.write(str(epc.stemWoodMassAtMaxHeight) + "\tMass at Maximum Height [kg C m-2] \n")
            file.write(str(epc.fractionOfLeafNitrogenInRubisco) + "\tfraction of leaf N in Rubisco\n")
            file.write(str(epc.startAgeGrowthReduction) + "\tStart Age Growth Reduction\n")
            file.write(str(epc.endAgeGrowthReduction) + "\tEnd Age Growth Reduction\n")
            file.write(str(epc.growthReductionFactor) + "\tGrowth Reduction Factor\n")
            file.write(str(epc.allocationReductionFactor) + "\tAllocation Reduction Factor (New Stem C : New Leaf C)\n")
            file.write(str(epc.nitrogenFixation) + "\tN-Fixation [kgN m-2 a-1]\n")
            file.write(str(epc.maxStomatalConductance) + "\tmaximum stomatal conductance (projected area basis)\n")
            file.write(str(epc.cuticularConductance) + "\tcuticular conductance (projected area basis)\n")
            file.write(str(epc.boundaryLayerConductance) + "\tboundary layer conductance (projected area basis)\n")
            file.write(str(epc.availableSoilWaterFactor) + "\tPlant Available Soil Water Factor: Start of Conductance Reduction\n")
            file.write(str(epc.wiltingPointFactor) + "\tPermanent Wilting Point Factor: Complete Conductance Reduction\n")
            file.write(str(epc.startOfConductanceReductionForVpd) + "\tVPD: Start of Conductance Reduction\n")
            file.write(str(epc.completeConductanceReductionForVpd) + "\tVPD: Complete Conductance Reduction\n")
            file.write(str(epc.thinningRuleOption) + "\t[flag] thinning rule, (0 = TABLE, 1 = FUNCTION)\n")
            file.write(str(epc.thinningRuleFileName) + "\tFile Containing Thinning Rule Table\n")
            file.write(str(epc.stemCarbonThresholdFor1stThinning) + "\tFirst Thinning Stem Carbon Threshold\n")
            file.write(str(epc.firstThinningFraction) + "\tfirst thinning fraction (not used if flag=0)\n")
            file.write(str(epc.thinningRuleCoefficientB00) + "\tthinning rule coefficient b00 (kg C/m2) (not used if flag=0)\n")
            file.write(str(epc.thinningRuleCoefficientB01) + "\tthinning rule coefficient b01 (kg C/m2) (not used if flag=0)\n")
            file.write(str(epc.thinningRuleCoefficientB10) + "\tthinning rule coefficient b10 (kg C/m2) (not used if flag=0)\n")
            file.write(str(epc.thinningRuleCoefficientB11) + "\tthinning rule coefficient b11 (kg C/m2) (not used if flag=0)\n")
            file.write(str(epc.thinningRuleCoefficientB12) + "\tthinning rule coefficient b12 (kg C/m2) (not used if flag=0)\n")
            file.write(str(epc.startHarvestCoefficientIntercept) + "\tstart harvest coefficient a (intersect) (not used if flag=0)\n")
            file.write(str(epc.startHarvestCoefficientSlope) + "\tstart harvest coefficient b (slope) (not used if flag=0)\n")
            file.write(str(epc.thinningPeriod) + "\tthinning period (years) (not used if flag=0)\n")
            file.write(str(epc.ageOfClearCut) + "\tage of clear cut (years)\n")
            file.write(str(epc.harvestCorrectionFactor) + "\tharvest correction factor\n")
            file.write(str(epc.exportFractionCoefficientIntercept) + "\texport fraction coefficient a (intersect)\n")
            file.write(str(epc.exportfractionCoefficientSlope) + "\texport fraction coefficient b (slope)\n")
            file.write(str(epc.optimumTempForRootGrowth)+ "\toptimum temperature for root growth   C\n")
            file.write(str(epc.minimumTempForRootGrowth) + "\tminimum temperature for root growth   C\n")
            file.write(str(epc.bdCoefForMaxRootGrowth) + "\tbulk density coefficient for maximum root growth   g/cm3\n")
            file.write(str(epc.criticalPorosity) + "\tcritical value of water-filled porosity\n")
            file.write(str(epc.minPhAllowingRootGrowth) + "\tminimum pH(H2O) allowing root growth\n")
            file.write(str(epc.maxPhAllowingRootGrowth) + "\tmaximum pH allowing root growth\n")
            file.write(str(epc.minPhForOptimumRootGrowth) + "\tminimum pH(H2O) for optimum root growth\n")
            file.write(str(epc.maxPhForOptimumRootGrowth) + "\tmaximum pH for optimum root growth\n")
            file.write(str(epc.waterSaturationStress) + "\twater saturation stress   (from 0 to 1)\n")
            file.write(str(epc.potentialVerticalRootGrowthRate) + "\tpotential vertical root growth rate   m/yr\n")
            file.write(str(epc.maxAgeOfRootGrowth) + "\tmaximum age of root growth   y\n")
            file.write(str(epc.zetaPlantParameter) + "\tZeta-Plant (coefficient for vertical root distribution)\n")

            # QtGui.QMessageBox.about(None, "Save", "The EPC file has been saved successfully.")
            file.close()
            return True
        except Exception as ex:
            # QtGui.QMessageBox.about(None, "Error", "The file could not be saved.")
            return False

    @staticmethod
    def readReferenceData(type):
        tarDir = ApplicationProperty().getScriptPath() + "/refvalue/"

        tempList = []
        if type == "EPC Parameter":
            tarDir += "epcfile"
            fileList = [f for f in os.listdir(tarDir) if os.path.isfile(os.path.join(tarDir,f))]

            for epcFile in fileList:
                item = {"name": epcFile, "epc" : FileReadWrite.readEpcFile(tarDir + "/" + epcFile)}
                tempList.append(item)

            return tempList
        elif type == "VEG Parameter":
            tarDir += "vegfile"

            fileList = [f for f in os.listdir(tarDir) if os.path.isfile(os.path.join(tarDir,f))]

            for vegFile in fileList:
                item = {"name": vegFile, "veg" : FileReadWrite.readVegFile(tarDir + "/" + vegFile)[0]}
                tempList.append(item)

            return tempList
        elif type == "GIS Parameter":
            tarDir += "gisfile"

            fileList = [f for f in os.listdir(tarDir) if os.path.isfile(os.path.join(tarDir,f))]

            for gisFile in fileList:
                item = {"name": gisFile, "gis" : FileReadWrite.readGisFile(tarDir + "/" + gisFile)[0]}
                tempList.append(item)

            return tempList
        elif type == "iniData":
            pass
        pass

    @staticmethod
    def readSoilProfile(soilProfileFilePath, soilHorizonFilePath):
        soilProfileList = []

        file = None
        try:
            f = open(soilProfileFilePath, 'r')
            for i in range(4): f.readline()

            for line in f.readlines():
                temp = line.strip().split("\t")
                for i in reversed(range(len(temp))):
                    temp[i] = temp[i].strip()
                    if not temp[i]: temp.pop(i)

                if len(temp) == 5:
                    profile = None
                    for sp in soilProfileList:
                        if sp.profileName == temp[0]:
                            profile = sp
                            break
                    else:
                        profile = SoilProfile()
                        soilProfileList.append(profile)
                        profile.profileName = temp[0]

                    layer = SoilLayer()
                    layer.horizonName = temp[1]
                    layer.depthOfHorizon = int(temp[2])
                    layer.layerThickness = int(temp[3])
                    layer.correctionFactor = float(temp[4])

                    profile.soilLayerList.append(layer)
        except:
            return None
        finally:
            try: f.close()
            except: pass

        if soilProfileList:
            try:
                file = open(soilHorizonFilePath)
                for i in range(4): file.readline()
                for line in file.readlines():
                    temp = line.strip().split("\t")
                    for i in reversed(range(len(temp))):
                        temp[i] = temp[i].strip()
                        if not temp[i]: temp.pop(i)

                    if len(temp) == 13:
                        layer = None
                        for sp in soilProfileList:
                            for sl in sp.soilLayerList:
                                if sl.horizonName == temp[0]:
                                    layer = sl
                                    # break
                            # if layer is not None: break

                                    if layer is not None:
                                        layer.soilTexture = temp[1]
                                        layer.soilPh = float(temp[2])
                                        layer.organicCarbonContent = float(temp[3])
                                        layer.gravelContent = float(temp[4])
                                        layer.sandContent = float(temp[5])
                                        layer.siltContent = float(temp[6])
                                        layer.clayContent = float(temp[7])
                                        layer.bulkDensity = float(temp[8])
                                        layer.poreVolume = float(temp[9])
                                        layer.waterCapacity = float(temp[10])
                                        layer.permanentWiltingPoint = float(temp[11])
                                        layer.saturatedHydraulicConductivity = float(temp[12])
            except:
                return None
            finally:
                try: file.close()
                except: pass

        return soilProfileList

    @staticmethod
    def writeSoilProfile(listOfSoilProfile, profileFilePath, horizonFilePath):
        file = None

        headerLines = []
        lines = []
        #find if the file exists or not
        if os.path.exists(profileFilePath):
            #because it is not possible to delete lines inside a file, the file will be read first
            #all delete operation will be done inside memory and then the file will rewrite.

            #open the file
            try:
                file = open(profileFilePath, 'r')
                try:
                    for i in range(4): headerLines.append(file.readline().replace("\n","")) #skip first 4 lines
                except: pass

                lines = file.readlines()
                file.close()
            except: pass

            if len(lines) > 0:
                for i in reversed(range(len(lines))):
                    lines[i] = lines[i].replace("\n","").strip()
                    line = lines[i]
                    if len(line) == 0:
                        lines.pop(i)
                    else:
                        temp = line.split("\t")
                        for profile in listOfSoilProfile:
                            if profile.profileName == temp[0].strip():
                                lines.pop(i)
                                break

        #reading profiles and appending new lines for each profile
        for profile in listOfSoilProfile:
            profile.sortSoilProfileByDepth()
            for layer in profile.soilLayerList:
                line = profile.profileName + "\t" +  layer.horizonName + "\t" +  str(layer.depthOfHorizon) + "\t" +\
                       str(layer.layerThickness) + "\t" +  str(layer.correctionFactor)
                lines.append(line)

        if len(lines) > 0:
            try:
                #reopen the file for rewriting
                file = open(profileFilePath, 'w')
                if len(headerLines) == 4:
                    #write header lines
                    for line in headerLines: file.write(line + "\n")
                else:
                    file.write("contains soil profiles information (horizons), header lines=4, no empty lines\n")
                    file.write("[Second Line: You may add information]\n")
                    file.write("ID_plot\thorizon_name\thorizon_depth\thorizon_thickness\tcorg_fact\n")
                    file.write("units:\t--\t[cm]\t[cm]\t--\t--\n")

                #write all lines inside lines
                for line in lines: file.write(line + "\n")
                file.close()
            except: return False

        headerLines = []
        lines = []

        if os.path.exists(horizonFilePath):
            try:
                file = open(horizonFilePath, 'r')
                for i in range(4): headerLines.append(file.readline().replace("\n", ""))

                lines = file.readlines()

                file.close()
            except: pass

            if len(lines) > 0:
                for i in reversed(range(len(lines))):
                    lines[i] = lines[i].replace("\n", "")
                    horizonName = lines[i].split("\t")[0].strip()
                    if len(horizonName) == 0:
                        lines.pop(i)
                    else:
                        exitLoop = False
                        for profile in listOfSoilProfile:
                            for layer in profile.soilLayerList:
                                if layer.horizonName == horizonName:
                                    lines.pop(i)
                                    exitLoop = True
                                    break
                            if exitLoop: break


        #read the horizons from profile list
        tempLayerList = []
        horizonNameList = []
        listOfLayer = []

        for profile in listOfSoilProfile:
            for layer in profile.soilLayerList:
                for lay in tempLayerList:
                    if lay.horizonName == layer.horizonName:
                        break
                else:
                    tempLayerList.append(layer)
                    horizonNameList.append(layer.horizonName)

        # horizonNameList.sort()
        for horizonName in sorted(horizonNameList, key=str.lower):
            for layer in tempLayerList:
                if layer.horizonName == horizonName:
                    listOfLayer.append(layer)
                    break
        tempLayerList = []
        horizonNameList = []

        for layer in listOfLayer:
            line = (layer.horizonName + "\t" + layer.soilTexture + "\t" + str(layer.soilPh) + "\t"
                    + str(layer.organicCarbonContent) + "\t" +
                    str(layer.gravelContent) + "\t" + str(layer.sandContent) + "\t" + str(layer.siltContent) + "\t" +
                    str(layer.clayContent) + "\t" + str(layer.bulkDensity) + "\t" + str(layer.poreVolume) + "\t" +
                    str(layer.waterCapacity) + "\t" + str(layer.permanentWiltingPoint) + "\t" +
                    str(layer.saturatedHydraulicConductivity))
            lines.append(line)

        if len(lines) > 0:
            try:
                file = open(horizonFilePath, 'w')

                if len(headerLines) == 4:
                    for line in headerLines: file.write(line + "\n")
                else:
                    file.write("[1st Line: You can add informaiton]\n")
                    file.write("[2nd Line: You can add informaiton]\n")
                    file.write("[3rd Line: You can add informaiton]\n")
                    file.write("horizon_ name\ttexture\tpH\tcorg\tstones\tsand\tsilt\tclay\tbd\tpv_vol\tfc_vol\tpwp_vol\tkf\n")

                for line in lines: file.write(line + "\n")
                file.close()
            except: return False

        return True

    # @staticmethod
    # def readDynamicInitialParameterList():
    #     paramList = []
    #     fileName = ApplicationProperty.getScriptPath() + "/dynamicparam/" + "initial.prm"
    #     if os.path.exists(fileName):
    #         try:
    #             file = open(fileName, 'r')
    #             for line in file.readlines():
    #                 paramList.append(line.split(",")[-1].strip())
    #             file.close()
    #         except: pass
    #     else: pass
    #     return paramList

    @staticmethod
    def write_bash_file_for_linux(bash_file_name, model_executable_name):
        if bash_file_name and model_executable_name:
            f = None
            try:
                f = open(bash_file_name, 'w')
                f.write("#!/bin/bash\n")
                f.write("\n")
                f.write("#usages: <script name> <initial file> <log option>\n")
                f.write("#log option: n = no log, y = log, any positive integer (excluding 0) = log with version\n")
                f.write("#if a positive number is used, the number will be added to the log file name (e.g. bgc_v3.log)\n")
                f.write("\n")
                f.write("pushd `dirname $0` > /dev/null\n")
                f.write("\n")
                f.write("#clean previous outputs and log\n")
                f.write("#rm outputs/*.*\n")
                f.write("#rm log/*.log\n")
                f.write("\n")
                f.write("args=(\"$@\")\n")
                f.write("\n")
                f.write("if [ $# -gt 0 ]\n")
                f.write("then\n")
                f.write("\tlogFLAG=0\n")
                f.write("\tlogPOSTFIX=""\n")
                f.write("\n")
                f.write("\tif [ $# -gt 1 ]\n")
                f.write("\tthen\n")
                f.write("\t\t{\n")
                f.write("\t\tif [ ${args[1]} = 'y' -o ${args[1]} = 'Y' ]\n")
                f.write("\t\tthen\n")
                f.write("\t\t\tlogFLAG=1\n")
                f.write("\t\tfi\n")
                f.write("\t\t}||\n")
                f.write("\t\t{\n")
                f.write("\t\tif [ ${args[1]} -gt 0 ]\n")
                f.write("\t\tthen\n")
                f.write("\t\t\tlogFLAG=1\n")
                f.write("\t\t\tlogPOSTFIX=\"_v${args[1]}\"\n")
                f.write("\t\tfi\n")
                f.write("\t\t}||\n")
                f.write("\t\t{\n")
                f.write("\t\tlogFLAG=0\n")
                f.write("\t\t}\n")
                f.write("\tfi\n")
                f.write("\n")
                f.write("\tinitfile=\"ini/${args[0]}\"\n")
                f.write("\tif [ ! -f $initfile ]\n")
                f.write("\tthen\n")
                f.write("\t\techo \"Initial file not found!\"\n")
                f.write("\telse\n")
                f.write("\t\tif [ $logFLAG -eq 1 ]\n")
                f.write("\t\tthen\n")
                f.write("\t\t\tmkdir -p log\n")
                f.write("\t\t\t./" + model_executable_name + " $initfile >& \"log/bgc$logPOSTFIX.log\"\n")
                f.write("\t\telse\n")
                f.write("\t\t\t./" + model_executable_name + " $initfile\n")
                f.write("\t\tfi\n")
                f.write("\tfi\n")
                f.write("else\n")
                f.write("\techo \"Usage: <$0> <initial file> <log flag>\"\n")
                f.write("fi")
            except: return False
            finally:
                try: f.close()
                except: pass
            return True
        return False

    @staticmethod
    def write_batch_file_for_windows(batch_file_name, model_executable_name):
        f = None
        try:
            f = open(batch_file_name, mode='w')
            textLine = "pushd \"" + ApplicationProperty.currentModelDirectory + "\""
            f.write(textLine + "\n")
            textLine = model_executable_name + " %1"
            f.write(textLine)
        except: return False
        finally:
            try: f.close()
            except: pass

        return True
        return False


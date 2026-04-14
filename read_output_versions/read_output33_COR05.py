#python 3.3; Biome-BGC v. cor 05

#last modified on: 19-10-2014

from application import ApplicationProperty
from file_io import FileReadWrite
import datetime
import struct
import os
import numpy as np
from copy import deepcopy
import csv
from subprocess import call

class DataReadResult:
    def __init__(self):
        self.header_variable = []
        self.record_list = []

    def get_header_variable(self): return self.header_variable
    def get_record_list(self): return self.record_list

    def add_new_field(self, field_name, field_record):
        if len(field_record) == len(self.record_list):
            for i in range(len(field_record)):
                self.record_list[i].append(field_record[i])
            self.header_variable.append(field_name)
            return True
        return False

class ReadBinaryOutput:
    output_header_variable = None
    spss_non_veg_variable = None
    spss_veg_variable = None
    spss_layer_variable = None
    unit_conversion_table = None

    @staticmethod
    def readSpssVariable_nonveg():
        #List of Spss Variables [{varid: variableId, varName: variableNameInSpss, varTitle: titleInSpss, dUnit: unitName,
                                # mUnit: unitName, aUnit: unitName, vLen: variableLength}, {}, ..]
        varList = []
        fileName = os.path.join(ApplicationProperty.getScriptPath(), "variablelist", "output_file", "spss_nonveg_var.txt")
        temp = None
        try:
            file = open(fileName, 'r')
            line = file.readline()
            for line in file.readlines():
                temp = line.strip().split("\t")
                spssVar = {}

                spssVar["varid"] = temp[0]
                spssVar["varName"] = temp[1]
                spssVar["varTitle"] = temp[2]
                spssVar["varClass"] = temp[3]
                spssVar["dUnit"] = temp[3]
                spssVar["mUnit"] = temp[4]
                spssVar["aUnit"] = temp[5]
                spssVar["vLen"] = temp[6]
                varList.append(spssVar)
            file.close()
        except:
            return None

        return varList

    @staticmethod
    def readSpssVariable_veg():

        #List of Spss Variables [{varid: variableId, varName: variableNameInSpss, varTitle: titleInSpss, dUnit: unitName,
                                # mUnit: unitName, aUnit: unitName, vLen: variableLength}, {}, ..]
        varList = []
        fileName = os.path.join(ApplicationProperty.getScriptPath(), "variablelist", "output_file", "spss_veg_var.txt")
        temp = None
        try:
            file = open(fileName, 'r')
            line = file.readline()
            for line in file.readlines():
                temp = line.strip().split("\t")
                spssVar = {}

                spssVar["varid"] = temp[0]
                spssVar["varName"] = temp[1]
                spssVar["varTitle"] = temp[2]
                spssVar["varClass"] = temp[3]
                spssVar["dUnit"] = temp[3]
                spssVar["mUnit"] = temp[4]
                spssVar["aUnit"] = temp[5]
                spssVar["vLen"] = temp[6]
                varList.append(spssVar)
            file.close()
        except:
            return None
	  
        return varList

    @staticmethod
    def readSpssVariable_layer():
        #List of Spss Variables [{varid: variableId, varName: variableNameInSpss}, {}, ..]
        varList = []
        fileName = os.path.join(ApplicationProperty.getScriptPath(), "variablelist", "output_file", "spss_lay_var.txt")
        temp = None
        try:
            file = open(fileName, 'r')
            for line in file.readlines():
                temp = line.strip().split("\t")
                spssVar = {}

                spssVar["varid"] = temp[0]
                spssVar["varName"] = temp[1]
                spssVar["varTitle"] = temp[2]
                spssVar["vLen"] = temp[3]
                varList.append(spssVar)
            file.close()
        except:
            return None

        return varList

    @staticmethod
    def FindClassVarList(varClass):
        varList = []
        if ReadBinaryOutput.spss_non_veg_variable is None:
            ReadBinaryOutput.spss_non_veg_variable = ReadBinaryOutput.readSpssVariable_nonveg()

        for var in ReadBinaryOutput.spss_non_veg_variable:
            if var["varClass"] == varClass and var not in varList: varList.append(var["varName"])

        if ReadBinaryOutput.spss_veg_variable is None:
            ReadBinaryOutput.spss_veg_variable = ReadBinaryOutput.readSpssVariable_veg()

        for var in ReadBinaryOutput.spss_veg_variable:
            if var["varClass"] == varClass and var not in varList: varList.append(var["varName"])

        return varList

    @staticmethod
    def FindPrecipitationVarList():
        var_list = ["metv_prcp"]

        return var_list

    @staticmethod
    def readOutputHeaderVaribleList():
        #structure: {varNames: [], varType: [], file1:[attrib list], file2: [attrib list], ...}
        varList = {}
        fileName = os.path.join(ApplicationProperty.getScriptPath(),  "variablelist", "output_file", "header_var.txt")
        try:
            file = open(fileName, "r")
            for line in file.readlines():
                temp = line.strip().strip("\n").split("\t")
                varList[temp[0]] = temp[1:]
            file.close()
        except:
            return None

        return varList

    @staticmethod
    def findSpssVariableDetail(varid, spssVarList):
        for var in spssVarList:
            if var["varid"] == str(varid): return var
        return None

    @staticmethod
    def readUnitConversionTable():
        #Structure of the conversion table:
        #[{varPFix: variablePrefix, moUnit: modelOutputUnit, sdUnit: spssDailyUnit, saUnit: spssAnnualUnit,
        # smaUnit: spssMonthlyAverageUnit, saaUnit: spssAnnualAverageUnit, cfDaily: conversionFactorForDailyOutput,
        # cfAnnual: conversionFactorForAnnualOutput, cfMonthAvg: conversionFactorForMonthlyAverageOutput,
        # cfAnnualAvg: conversionFactorForAnnualAverageOutput},{},...]

        conversionTable = []
        fileName = os.path.join(ApplicationProperty.getScriptPath(), "variablelist", "output_file", "spss_unit_conversion.txt")

        try:
            file = open(fileName, "r")
            header = file.readline().strip("\n").split("\t")
            for line in file.readlines():
                temp = line.strip("\n").split("\t")
                item = {}
                for i in range(len(header)):
                    item[header[i]] = temp[i]
                conversionTable.append(item)
            file.close()

        except:
            return None

        return conversionTable

    @staticmethod
    def FindOutputVariableList(initialParam, output_file_type):
        varList = None

        if initialParam is not None:
            if output_file_type == "ann":
                varList = []
                for item in initialParam.output.listOfSelectedSiteSpecificVariable_Annual: varList.append(item["varid"])
            elif output_file_type in ["day", "annavg", "monavg"]:
                varList = []
                for item in initialParam.output.listOfSelectedSiteSpecificVariable_Daily: varList.append(item["varid"])
            elif output_file_type == "ann_veg":
                varList = []
                for item in initialParam.output.listOfSelectedVegSpecificVariable_Annual: varList.append(item["varid"])
            elif output_file_type in ["day_veg", "annavg_veg", "monavg_veg"]:
                varList = []
                for item in initialParam.output.listOfSelectedVegSpecificVariable_Daily: varList.append(item["varid"])
            elif output_file_type == "ann_lay":
                varList = []
                for item in initialParam.output.selectedAnnualVarLayerList:
                    for i in range(len(item["laylist"])): varList.append({"var":item["varid"], "layer": item["laylist"][i]})
                for item in initialParam.output.selectedAnnualLayerVarList:
                    for i in range(len(item["varlist"])): varList.append({"var": item["varlist"][i], "layer": item["layer"]})
            elif output_file_type == "day_lay":
                varList = []
                for item in initialParam.output.selectedDailyVarLayerList:
                    for i in range(len(item["laylist"])): varList.append({"var": item["varid"], "layer": item["laylist"][i]})
                for item in initialParam.output.selectedDailyLayerVarList:
                    for i in range(len(item["varlist"])): varList.append({"var": item["varlist"][i], "layer": item["layer"]})
            elif output_file_type == "day_totlay":
                varList = initialParam.output.listOfSelectedTotalLayerVariable
            # elif output_file_type == "annavg":
            #     varList = initialParam.output_template.site_specific_daily_output
            # elif output_file_type == "annavg_veg":
            #     varList = initialParam.output_template.veg_specific_daily_output
            # elif output_file_type == "monavg":
            #     varList = initialParam.output_template.site_specific_daily_output
            # elif output_file_type == "monavg_veg":
            #     varList = initialParam.output_template.veg_specific_daily_output

        return varList

    @staticmethod
    def FindOutputVariableNameList(init_param, file_type, var_list = None):
        var_name_list = []

        if var_list is None:
            var_list = ReadBinaryOutput.FindOutputVariableList(init_param, file_type)

        if var_list is not None:
            #reading spss variable description from text files (project folder\\variablelist\\output_file\\
            if ReadBinaryOutput.spss_non_veg_variable is None:
                ReadBinaryOutput.spss_non_veg_variable = ReadBinaryOutput.readSpssVariable_nonveg()
            if ReadBinaryOutput.spss_veg_variable is None:
                ReadBinaryOutput.spss_veg_variable = ReadBinaryOutput.readSpssVariable_veg()
            if ReadBinaryOutput.spss_layer_variable is None:
                ReadBinaryOutput.spss_layer_variable = ReadBinaryOutput.readSpssVariable_layer()


            if file_type in ["day", "ann", "monavg", "annavg", "day_veg", "ann_veg", "monavg_veg", "annavg_veg", "day_totlay"]:
                list_variable_detail = []
                if file_type in ["day", "ann", "monavg", "annavg"]:
                    for var in var_list:
                        list_variable_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, ReadBinaryOutput.spss_non_veg_variable))
                elif file_type in ["day_veg", "ann_veg", "monavg_veg", "annavg_veg"]:
                    for var in var_list:
                        list_variable_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, ReadBinaryOutput.spss_veg_variable))
                elif file_type == "day_totlay":
                    for var in var_list:
                        list_variable_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, ReadBinaryOutput.spss_layer_variable))

                for item in list_variable_detail:
                    var_name_list.append(item["varName"])

            elif file_type in ["day_lay", "ann_lay"]:
                org_depth = ReadBinaryOutput.FindOrganicLayerDepth(init_param)

                if org_depth > 0:
                    for item in var_list:
                        if item["layer"].find("-") > 0:
                            temp = item["layer"].split("-")
                            if int(temp[1]) - org_depth == 0: var_post_fix = "O"
                            else:
                                if int(temp[0]) > 0:
                                    var_post_fix = str(int(temp[0]) - org_depth) + "_" + str(int(temp[1]) - org_depth)
                                else: var_post_fix = temp[0] + "_" + str(int(temp[1]) - org_depth)
                        else:
                            temp = int(item["layer"]) - org_depth
                            if temp < 0: var_post_fix = "M" + str(temp * -1)
                            else: var_post_fix = str(temp)

                        temp = ReadBinaryOutput.findSpssVariableDetail(item["var"], ReadBinaryOutput.spss_layer_variable)
                        var_name_list.append(temp["varName"] + var_post_fix)

            if len(var_name_list) == len(var_list):
                return var_name_list

        return None

    @staticmethod
    def FindVariableLabelList(init_param, file_type, var_list = None):
        var_label_list = []

        if var_list is None:
            var_list = ReadBinaryOutput.FindOutputVariableList(init_param, file_type)

        #reading spss variable description from text files (project folder\\variablelist\\output_file\\
        if ReadBinaryOutput.spss_non_veg_variable is None:
            ReadBinaryOutput.spss_non_veg_variable = ReadBinaryOutput.readSpssVariable_nonveg()
        if ReadBinaryOutput.spss_veg_variable is None:
            ReadBinaryOutput.spss_veg_variable = ReadBinaryOutput.readSpssVariable_veg()
        if ReadBinaryOutput.spss_layer_variable is None:
            ReadBinaryOutput.spss_layer_variable = ReadBinaryOutput.readSpssVariable_layer()


        if file_type in ["day", "ann", "monavg", "annavg", "day_veg", "ann_veg", "monavg_veg", "annavg_veg", "day_totlay"]:
            list_variable_detail = []
            if file_type in ["day", "ann", "monavg", "annavg"]:
                for var in var_list:
                    list_variable_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, ReadBinaryOutput.spss_non_veg_variable))
            elif file_type in ["day_veg", "ann_veg", "monavg_veg", "annavg_veg"]:
                for var in var_list:
                    list_variable_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, ReadBinaryOutput.spss_veg_variable))
            elif file_type == "day_totlay":
                for var in var_list:
                    list_variable_detail.append(ReadBinaryOutput.findSpssVariableDetail(var, ReadBinaryOutput.spss_layer_variable))
            for item in list_variable_detail:
                var_label_list.append(item["varTitle"])

        elif file_type in ["day_lay", "ann_lay"]:
            org_depth = ReadBinaryOutput.FindOrganicLayerDepth(init_param)
            if org_depth > 0:
                for item in var_list:
                    if item["layer"].find("-") > 0:
                        temp = item["layer"].split("-")
                        if int(temp[1]) - org_depth == 0: var_post_fix = "O"
                        else:
                            if int(temp[0]) > 0:
                                var_post_fix = str(int(temp[0]) - org_depth) + "_" + str(int(temp[1]) - org_depth)
                            else: var_post_fix = temp[0] + "_" + str(int(temp[1]) - org_depth)
                    else:
                        temp = int(item["layer"]) - org_depth
                        if temp < 0: var_post_fix = "M" + str(temp * -1)
                        else: var_post_fix = str(temp)

                    temp = ReadBinaryOutput.findSpssVariableDetail(item["var"], ReadBinaryOutput.spss_layer_variable)
                    var_label_list.append(temp["varTitle"] + " in " + var_post_fix.replace("_", "-") + " cm, simulated")

        if len(var_label_list) == len(var_list):
            return var_label_list
        else: return None

    @staticmethod
    def FindFileSpecificHeaderVariable(file_type):
        file_specific_header_var = [[],[]] #structure: [[var_name_list],[var_type_list]]; note: the sequence is important

        if ReadBinaryOutput.output_header_variable is None:
            ReadBinaryOutput.output_header_variable = ReadBinaryOutput.readOutputHeaderVaribleList()

        header_var_name_list = ReadBinaryOutput.output_header_variable["header_var"]
        header_var_type = ReadBinaryOutput.output_header_variable["var_type"]
        try:
            file_specific_header_var_temp = ReadBinaryOutput.output_header_variable[file_type]

            for i in range(len(file_specific_header_var_temp)):
                if int(file_specific_header_var_temp[i]) == 1:
                    var_name = header_var_name_list[i]
                    var_type = header_var_type[i]
                    file_specific_header_var[0].append(var_name)
                    file_specific_header_var[1].append(var_type)
        except: pass

        return file_specific_header_var

    @staticmethod
    def FindOrganicLayerDepth(init_param):
        org_depth = 0

        #read the gis file
        targetDir = ApplicationProperty.currentModelDirectory
        siteList = FileReadWrite.readGisFile(os.path.join(targetDir, init_param.gis_file_name))

        if len(siteList) > 0:
            site = siteList[0]
            soilProfileList = FileReadWrite.readSoilProfile(os.path.join(targetDir, "soil", site.soilProfileFileName),
                                                                os.path.join(targetDir,  "soil", site.soilHorizonFileName))
            organic_lower_border = []
            for profile in soilProfileList:
                if profile.profileName == site.profileName:
                    for layer in profile.soilLayerList:
                        if layer.soilTexture == "O": organic_lower_border.append(layer.depthOfHorizon)
            if len(organic_lower_border) > 0: org_depth = max(organic_lower_border)

        return org_depth

    @staticmethod
    def ReadModelOutput(model_directory, initial_filename, file_type, trim=False, post_processing=False, ucf=False):
        read_output = DataReadResult()

        if model_directory and initial_filename and file_type:
            if ApplicationProperty.currentModelDirectory == '': ApplicationProperty.currentModelDirectory = model_directory

            if initial_filename.find('/ini/') == -1: initial_filename = os.path.join(model_directory, "ini", initial_filename)
            initial_parameter = FileReadWrite.readInitialFile(initial_filename)

            list_of_record = []
            if initial_parameter is not None:

                #for version cor_05
                ndx = file_type.find('_')
                if ndx == -1:
                    file_name = os.path.join(model_directory, initial_parameter.output_file_prefix + '.' + file_type + 'out')
                else:
                    file_name = os.path.join(model_directory, initial_parameter.output_file_prefix + '.' + file_type[:ndx] + 'out' + file_type[ndx:])

                #for other version
                # file_name = os.path.join(model_directory, initial_parameter.output_file_prefix + '.' + file_type)

                output_variable_list = ReadBinaryOutput.FindOutputVariableList(initial_parameter, file_type)
                file_specific_header_variable = ReadBinaryOutput.FindFileSpecificHeaderVariable(file_type)

                if os.path.exists(file_name) and output_variable_list is not None and len(file_specific_header_variable) > 0:
                    block_size = 0
                    format_string = "="
                    for i in range(len(file_specific_header_variable[0])):
                        var_name = file_specific_header_variable[0][i]
                        var_type = file_specific_header_variable[1][i]
                        format_string += var_type[1:] + "s"
                        block_size += int(var_type[1:])

                    for i in range(len(output_variable_list)):
                        format_string += "f"

                    block_size += (len(output_variable_list) * 4)

                    f = None

                    try:
                        f = open(file_name, "rb")
                        while True:
                            block = f.read(block_size)
                            if block:
                                b = struct.unpack(format_string, block)
                                list_of_record.append(list(b))
                            else: break

                    except Exception as ex:
                        return None
                    finally:
                        try: f.close()
                        except: pass

                    if len(list_of_record) > 0:
                        read_output.header_variable = file_specific_header_variable[0] + ReadBinaryOutput.FindOutputVariableNameList(initial_parameter,file_type, output_variable_list)
                        read_output.record_list = list_of_record
                        if trim:
                            #trimming strings and trying to make the string as number where possible
                            for j in range(len(file_specific_header_variable[0])):
                                for i in range(len(read_output.record_list)):
                                    temp = str(read_output.record_list[i][j])[1:-1].strip("'").lstrip("0")
                                    try:
                                        temp = int(temp)
                                    except: pass
                                    read_output.record_list[i][j] = temp

                        if post_processing: ReadBinaryOutput.ModelOutputPostProcess(file_type, read_output.record_list, read_output.header_variable, initial_parameter)
                        if ucf: ReadBinaryOutput.UnitConversion(file_type, read_output.header_variable, read_output.record_list)

        return read_output

    @staticmethod
    def ReadModelOutput_binary(model_directory, init_param, file_type):
        list_of_record = []

        if len(model_directory) > 0 and len(file_type) > 0 and init_param is not None:
            #for cor_05
            ndx = file_type.find('_')
            if ndx == -1: temp = file_type + 'out'
            else: temp = file_type[:ndx] + 'out' + file_type[ndx:]
            file_name = os.path.join(model_directory, init_param.output_file_prefix + "." + temp)
            #end
            #file_name = os.path.join(model_directory, init_param.output_file_prefix + "." + file_type)


            output_variable_list = ReadBinaryOutput.FindOutputVariableList(init_param, file_type)
            file_specific_header_variable = ReadBinaryOutput.FindFileSpecificHeaderVariable(file_type)

            if os.path.exists(file_name) and output_variable_list is not None and len(file_specific_header_variable) > 0:
                block_size = 0
                format_string = "="
                for i in range(len(file_specific_header_variable[0])):
                    var_name = file_specific_header_variable[0][i]
                    var_type = file_specific_header_variable[1][i]
                    format_string += var_type[1:] + "s"
                    block_size += int(var_type[1:])

                for i in range(len(output_variable_list)):
                    format_string += "f"

                block_size += (len(output_variable_list) * 4)

                f = None

                try:
                    f = open(file_name, "rb")
                    while True:
                        block = f.read(block_size)
                        if block:
                            b = struct.unpack(format_string, block)
                            list_of_record.append(list(b))
                        else: break
		
                except Exception as ex:
                    return None
                finally:
                    try: f.close()
                    except: pass

        return list_of_record

    @staticmethod
    def ModelOutputPostProcess(file_type, record_list, header_var_list, init_param):
        ReadBinaryOutput.PostProcessing_common(record_list, header_var_list)
        ReadBinaryOutput.PostProcessing_day(record_list, header_var_list)
        ReadBinaryOutput.PostProcessing_month(record_list, header_var_list)
        ReadBinaryOutput.PostProcessing_GroupSum(record_list, header_var_list)
        if file_type in ["day_lay", "ann_lay"]:
            ReadBinaryOutput.PostProcessing_Day_Ann_Lay(record_list, header_var_list, init_param)

    @staticmethod
    def PostProcessing_month(list_of_record, header_var_list):
        index_mon_str = ReadBinaryOutput.FindColumnIndex(header_var_list, "month_str")

        if index_mon_str > -1:
            #the initial value (0) is just to avoid the index-1 operation
            month_day_list = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for record in list_of_record:
                record.append(month_day_list[record[index_mon_str]])
            header_var_list.append("Month Days")

    @staticmethod
    def PostProcessing_day(record_list, header_var_list):
        index_yearday = ReadBinaryOutput.FindColumnIndex(header_var_list, "yrday_str")
        index_year = ReadBinaryOutput.FindColumnIndex(header_var_list, "year")

        if index_yearday > -1 and index_year > -1:
            for record in record_list:
                record[index_yearday] = int(str(record[index_yearday]).strip("b").strip("'").lstrip("0"))
                if record[index_year] % 4 == 0 and record[index_yearday] > 59: record[index_yearday] += 1
                date = datetime.datetime(record[index_year], 1, 1) + datetime.timedelta(record[index_yearday] - 1)
                record.append(date)
                # month = datetime.datetime.month(date)
                record.append(date.month)
                #week_number
                week_number = (record[index_yearday] - 1) // 7 + 1
                record.append(week_number)
                #year week
                record.append(str(week_number) + " WK " + str(record[index_year])[2:])
            header_var_list.append("date")
            header_var_list.append("month")
            header_var_list.append("week")
            header_var_list.append("year_week")

            #cumulated sum for 'wf' and precipitation outputs
            wf_var_list = ReadBinaryOutput.FindClassVarList("wf") + ReadBinaryOutput.FindPrecipitationVarList()
            for var in header_var_list:
                if var in wf_var_list:
                    var_index = ReadBinaryOutput.FindColumnIndex(header_var_list, var)
                    date_index = ReadBinaryOutput.FindColumnIndex(header_var_list, "date")

                    cum_sum = 0
                    for record in record_list:
                        current_date = record[date_index]
                        if current_date.day == 1 and current_date.month == 1: cum_sum = 0

                        var_val = record[var_index]
                        cum_sum += var_val
                        record.append(cum_sum)

                    header_var_list.append("cum_" + var)

    @staticmethod
    def PostProcessing_common(list_of_record, header_var_list):
        index_index_str = ReadBinaryOutput.FindColumnIndex(header_var_list, "index_str")
        index_year = ReadBinaryOutput.FindColumnIndex(header_var_list, "year")
	
        for record in list_of_record:
            record[index_index_str] = str(record[index_index_str])
            record[index_year] = int(record[index_year])
	    

    @staticmethod
    def PostProcessing_GroupSum(list_of_record, header_var_list):
        #summing up cs_soil1, cs_soil2, cs_soil3, cs_soil4
        ndx_cs_soil1 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_soil1")
        ndx_cs_soil2 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_soil2")
        ndx_cs_soil3 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_soil3")
        ndx_cs_soil4 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_soil4")

        if ndx_cs_soil1 > -1 and ndx_cs_soil2 > -1 and ndx_cs_soil3 > -1 and ndx_cs_soil4 > -1:
            for record in list_of_record:
                record[ndx_cs_soil1] = record[ndx_cs_soil1] + record[ndx_cs_soil2] + record[ndx_cs_soil3] + record[ndx_cs_soil4]
                record.pop(ndx_cs_soil4)
                record.pop(ndx_cs_soil3)
                record.pop(ndx_cs_soil2)
            header_var_list.pop(ndx_cs_soil4)
            header_var_list.pop(ndx_cs_soil3)
            header_var_list.pop(ndx_cs_soil2)
            header_var_list[ndx_cs_soil1] = "sum_cs_soil"

        #sum up ns_soil
        ndx_ns_soil1 = ReadBinaryOutput.FindColumnIndex(header_var_list, "ns_soil1")
        ndx_ns_soil2 = ReadBinaryOutput.FindColumnIndex(header_var_list, "ns_soil2")
        ndx_ns_soil3 = ReadBinaryOutput.FindColumnIndex(header_var_list, "ns_soil3")
        ndx_ns_soil4 = ReadBinaryOutput.FindColumnIndex(header_var_list, "ns_soil4")

        if ndx_ns_soil1 > -1 and ndx_ns_soil2 > -1 and ndx_ns_soil3 > -1 and ndx_ns_soil4 > -1:
            for record in list_of_record:
                record[ndx_ns_soil1] = record[ndx_ns_soil1] + record[ndx_ns_soil2] + record[ndx_ns_soil3] + record[ndx_ns_soil4]
                record.pop(ndx_ns_soil4)
                record.pop(ndx_ns_soil3)
                record.pop(ndx_ns_soil2)
            header_var_list.pop(ndx_ns_soil4)
            header_var_list.pop(ndx_ns_soil3)
            header_var_list.pop(ndx_ns_soil2)
            header_var_list[ndx_ns_soil1] = "sum_ns_soil"


        #sum of cs_vegt_l_litr variables
        ndx_cs_vegt_l_litr1 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_vegt_l_litr1")
        ndx_cs_vegt_l_litr2 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_vegt_l_litr2")
        ndx_cs_vegt_l_litr3 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_vegt_l_litr3")
        ndx_cs_vegt_l_litr4 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_vegt_l_litr4")
        if ndx_cs_vegt_l_litr1 > -1 and ndx_cs_vegt_l_litr2 > -1 and ndx_cs_vegt_l_litr3 > -1 and ndx_cs_vegt_l_litr4 > -1:
            for record in list_of_record:
                record[ndx_cs_vegt_l_litr1] = (record[ndx_cs_vegt_l_litr1] + record[ndx_cs_vegt_l_litr2] +
                                               record[ndx_cs_vegt_l_litr3] + record[ndx_cs_vegt_l_litr4])
                record.pop(ndx_cs_vegt_l_litr4)
                record.pop(ndx_cs_vegt_l_litr3)
                record.pop(ndx_cs_vegt_l_litr2)
            header_var_list.pop(ndx_cs_vegt_l_litr4)
            header_var_list.pop(ndx_cs_vegt_l_litr3)
            header_var_list.pop(ndx_cs_vegt_l_litr2)
            header_var_list[ndx_cs_vegt_l_litr1] = "sum_cs_vegt_l_litr"

        #sum of cs_vegt_fr_litr variables
        ndx_cs_vegt_fr_litr1 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_vegt_fr_litr1")
        ndx_cs_vegt_fr_litr2 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_vegt_fr_litr2")
        ndx_cs_vegt_fr_litr3 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_vegt_fr_litr3")
        ndx_cs_vegt_fr_litr4 = ReadBinaryOutput.FindColumnIndex(header_var_list, "cs_vegt_fr_litr4")
        if ndx_cs_vegt_fr_litr1 > -1 and ndx_cs_vegt_fr_litr2 > -1 and ndx_cs_vegt_fr_litr3 > -1 and ndx_cs_vegt_fr_litr4 > -1:
            for record in list_of_record:
                record[ndx_cs_vegt_fr_litr1] = (record[ndx_cs_vegt_fr_litr1] + record[ndx_cs_vegt_fr_litr2] +
                                                record[ndx_cs_vegt_fr_litr3] + record[ndx_cs_vegt_fr_litr4])
                record.pop(ndx_cs_vegt_fr_litr4)
                record.pop(ndx_cs_vegt_fr_litr3)
                record.pop(ndx_cs_vegt_fr_litr2)
            header_var_list.pop(ndx_cs_vegt_fr_litr4)
            header_var_list.pop(ndx_cs_vegt_fr_litr3)
            header_var_list.pop(ndx_cs_vegt_fr_litr2)
            header_var_list[ndx_cs_vegt_fr_litr1] = "sum_cs_vegt_fr_litr"

        # sum of wf_site_evap_tot and wf_site_trans_tot

        '''
        ndx_wf_site_evap_tot = ReadBinaryOutput.FindColumnIndex(header_var_list, "wf_site_evap_tot")
        ndx_wf_site_trans_tot = ReadBinaryOutput.FindColumnIndex(header_var_list, "wf_site_trans_tot")
        if ndx_wf_site_evap_tot > -1 and ndx_wf_site_trans_tot > -1:
            ndx1 = -1
            ndx2 = -1
            if ndx_wf_site_evap_tot < ndx_wf_site_trans_tot:
                ndx1 = ndx_wf_site_evap_tot
                ndx2 = ndx_wf_site_trans_tot
            else:
                ndx2 = ndx_wf_site_evap_tot
                ndx1 = ndx_wf_site_trans_tot

            for record in list_of_record:
                record[ndx1] = record[ndx1] + record[ndx2]
                # record.pop(ndx2)

            # header_var_list.pop(ndx2)
            header_var_list[ndx1] = "wf_site_et_tot"

        pass

        '''

    # @staticmethod
    # def PostProcessing_CumulativeSum(header_var_list, list_of_record, var_name):
    #
    #     var_list = [var_name]
    #
    #     date_index = -1
    #     for var in header_var_list:
    #         if var == "date":
    #             date_index = header_var_list.index(var)
    #             break
    #
    #     if date_index != -1:
    #         for i in range(len(header_var_list)):
    #             var = header_var_list[i]
    #             if var in var_list:
    #
    #                 cum_sum = 0
    #                 for record in list_of_record:
    #                     cum_sum += record[i]
    #                     record.append(sum)
    #
    #                     d = record[date_index]
    #                     if d.day == 1 and d.month == 1: cum_sum = 0


    @staticmethod
    def PostProcessing_Day_Ann_Lay(list_of_record, header_var_list, init_param):
        if ReadBinaryOutput.spss_layer_variable is None:
            ReadBinaryOutput.spss_layer_variable = ReadBinaryOutput.readSpssVariable_layer()

        spss_var_detail = ReadBinaryOutput.findSpssVariableDetail("0", ReadBinaryOutput.spss_layer_variable)
        if spss_var_detail is not None:
            var_name = spss_var_detail["varName"]
            name_length = len(var_name)
            if name_length > 0:
                for i in range(len(header_var_list)):
                    header_var = header_var_list[i]
                    if header_var[:name_length] == var_name:
                        spss_layer_depth_text = header_var[name_length:]
                        grv_content = ReadBinaryOutput.FindGravelContent(init_param, spss_layer_depth_text)

                        ndx_header_var = ReadBinaryOutput.FindColumnIndex(header_var_list, header_var)
                        if ndx_header_var > -1: #grv_content > 0 and ndx_header_var > -1:
                            if grv_content != 0:
                                for record in list_of_record:
                                    fine_soil_wc = (record[ndx_header_var] * 100) / (100 - grv_content)
                                    record.append(fine_soil_wc)
                            else:
                                for record in list_of_record:
                                    record.append(record[ndx_header_var])
                            header_var_list.append(var_name[:name_length] + "_fe_" + spss_layer_depth_text)
    @staticmethod
    def FindGravelContent(init_param, spss_layer_depth_text):
        grv_content = 0

        org_layer_depth = ReadBinaryOutput.FindOrganicLayerDepth(init_param)
        layer_depth = None

        temp = spss_layer_depth_text.split("_")
        if len(temp) == 1:
            try:
                layer_depth = int(temp[0]) + org_layer_depth
            except:
                if temp[0].find("M") > -1:
                    layer_depth = - int(temp[0].strip()[1:]) + org_layer_depth
                if temp[0].find("O") > -1:
                    layer_depth = org_layer_depth
        else:
            try:
                layer_depth = int(temp[1]) + org_layer_depth
            except: pass

        if layer_depth is not None:
            grv_content = ReadBinaryOutput.FindLayerGravelContent(init_param, layer_depth)

        return grv_content

    @staticmethod
    def FindLayerGravelContent(init_param, layer_depth):
        layer_gravel_content = 0

        #read the gis file
        # temp = self.txtInitFile.text().split("/")[-1]
        targetDir = ApplicationProperty.currentModelDirectory + "/"
        siteList = FileReadWrite.readGisFile(targetDir + init_param.gis_file_name)
        for site in siteList:
            soilProfileList = FileReadWrite.readSoilProfile(targetDir + "soil/" + site.soilProfileFileName,
                                                                targetDir + "soil/" + site.soilHorizonFileName)
            for profile in soilProfileList:
                if profile.profileName == site.profileName:
                    for layer in profile.soilLayerList:
                        if layer_depth <= layer.depthOfHorizon:
                            layer_gravel_content = layer.gravelContent
                            break

        return layer_gravel_content



    @staticmethod
    def FindColumnIndex(header_var_list, var):
        for i in range(len(header_var_list)):
            if header_var_list[i].lower() == var.lower(): return i
        return -1

    @staticmethod
    def UnitConversion(file_type, header_var_list, list_of_record):
        if ReadBinaryOutput.unit_conversion_table is None:
            ReadBinaryOutput.unit_conversion_table = ReadBinaryOutput.readUnitConversionTable()
	
        for item in ReadBinaryOutput.unit_conversion_table:
            cftext = ""        #cfValue = conversion factor
            if file_type.find("monavg") == -1:
                if file_type.find("day") != -1:
                    cftext = item["cfDaily"]
                elif file_type.find("annavg") != -1:
                    cftext = item["cfAnnualAvg"]
                elif file_type.find("ann") != -1:
                    cftext = item["cfAnnual"]


                cf_num = 1
                try: cf_num = int(cftext)
                except:
                    try: cf_num = float(cftext)
                    except: pass

                if cf_num != 1:
                    var_list = ReadBinaryOutput.FindClassVarList(item["varPFix"])
                    for var_name in header_var_list:
                        if var_name in var_list: # == item["varPFix"]:
                            index_var = ReadBinaryOutput.FindColumnIndex(header_var_list, var_name)
                            for record in list_of_record:
                                record[index_var] = record[index_var] * cf_num

            else:
                cftext = item["cfMonthAvg"].split("*")[0].strip()

                cf_num = 1
                try: cf_num = int(cftext)
                except:
                    try: cf_num = float(cftext)
                    except: pass

                if cf_num != 1:
                    for var_name in header_var_list:
                        var_list = ReadBinaryOutput.FindClassVarList(item["varPFix"])
                        if var_name in var_list:# [:2] == item["varPFix"]:
                            index_var = ReadBinaryOutput.FindColumnIndex(header_var_list, var_name)
                            index_month_str = ReadBinaryOutput.FindColumnIndex(header_var_list, "Month Days")
                            for record in list_of_record:
                                record[index_var] = record[index_var] * cf_num * record[index_month_str]
        pass

    @staticmethod
    def GenerateListOfOutputFiles(init_param, model_directory):
        output_file_list = []

        if init_param is not None:
            #checking the daily output options
            if len (init_param.output.listOfSelectedSiteSpecificVariable_Daily) > 0:
                output_file_list.append("day")
                if init_param.monthly_average_flag == 1: output_file_list.append("monavg")
                if init_param.annual_average_flag == 1: output_file_list.append("annavg")
            if len(init_param.output.listOfSelectedVegSpecificVariable_Daily) > 0:
                output_file_list.append("day_veg")
                if init_param.monthly_average_flag == 1: output_file_list.append("monavg_veg")
                if init_param.annual_average_flag == 1: output_file_list.append("annavg_veg")
            if len(init_param.output.listOfSelectedTotalLayerVariable) > 0:
                output_file_list.append("day_totlay")
            if len(init_param.output.listOfSelectedSiteSpecificVariable_Annual) > 0:
                output_file_list.append("ann")
            if len(init_param.output.listOfSelectedVegSpecificVariable_Annual) > 0:
                output_file_list.append("ann_veg")
            if (len(init_param.output.selectedDailyLayerVarList) > 0 or
                len(init_param.output.selectedDailyVarLayerList) > 0):
                day_lay = False
                day_lay_veg = False
                for item in init_param.output.selectedDailyLayerVarList:
                    for var in item["varlist"]:
                        if int(var) == 23 or int(var) >= 41:
                            day_lay_veg = True
                        else: day_lay = True

                        if day_lay and day_lay_veg: break
                    if day_lay and day_lay_veg: break

                if (not day_lay) or (not day_lay_veg):
                    for item in init_param.output.selectedDailyVarLayerList:
                        if int(item["varid"]) == 23 or int(item["varid"]) >= 41:
                            day_lay_veg = True
                        else: day_lay = True
                        if day_lay and day_lay_veg: break
                if day_lay: output_file_list.append("day_lay")
                if day_lay_veg: output_file_list.append("day_lay_veg")
            if (len(init_param.output.selectedAnnualLayerVarList) > 0 or
                len(init_param.output.selectedAnnualVarLayerList)> 0):
                ann_lay = False
                ann_lay_veg = False
                for item in init_param.output.selectedAnnualLayerVarList:
                    for var in item["varlist"]:
                        if int(var) == 23 or int(var) >= 41:
                            ann_lay_veg = True
                        else: ann_lay = True
                        if ann_lay and ann_lay_veg: break
                    if ann_lay and ann_lay_veg: break
                if (not ann_lay) or (not ann_lay_veg):
                    for item in init_param.output.selectedAnnualVarLayerList:
                        if int(item["varid"]) == 23 or int(item["varid"]) >= 41:
                            ann_lay_veg = True
                        else: ann_lay = True
                        if ann_lay and ann_lay_veg: break

        for i in reversed(range(len(output_file_list))):
            temp = output_file_list[i]
            ndx = temp.find('_')
            if ndx == -1: temp = temp + 'out'
            else: temp = temp[:ndx] + 'out' + temp[ndx:]
            temp = os.path.join(model_directory, init_param.output_file_prefix + "." + temp)
            if not os.path.exists(temp): output_file_list.pop(i)

        return output_file_list

    @staticmethod
    def ExtractColumnRecord(column_name, header_list,  list_of_record):
        column_record = []
        ndx = ReadBinaryOutput.FindColumnIndex(header_list, column_name)
        if ndx > -1 and len(list_of_record) > 0:
            for record in list_of_record:
                column_record.append(record[ndx])
        return column_record

    @staticmethod
    def Filter(list_of_record_list, comparison_list_index, condition_str, filter_value, filter_2ndValue=None):
        #list_of_record_list: [[RL1],[RL2],[RL3],...]; all RL should have same length
        #comparison_list_index: index of the RL that will be compared
        succeed = True

        #checking the length of record lists
        temp = []
        for rl in list_of_record_list: temp.append(len(rl))
        if min(temp) != max(temp): succeed = False


        if succeed:
            #excluding None values
            for i in range(len(list_of_record_list)):
                rl = list_of_record_list[i]
                for j in reversed(range(len(rl))):
                    if rl[j] is None:
                        for k in range(len(list_of_record_list)):
                            list_of_record_list[k].pop(j)

            #condition_str can be ">", "<", "=", "!=", ">=", "<="
            comparing_list = list_of_record_list[comparison_list_index]
            if condition_str == ">" or condition_str == "greater than":
                for i in reversed(range(len(comparing_list))):
                    if comparing_list[i] <= filter_value:
                        for j in range(len(list_of_record_list)): list_of_record_list[j].pop(i)
            elif condition_str == "<" or condition_str == "less than":
                for i in reversed(range(len(comparing_list))):
                    if comparing_list[i] >= filter_value:
                        for j in range(len(list_of_record_list)): list_of_record_list[j].pop(i)
            elif condition_str == "=" or condition_str == "equals":
                for i in reversed(range(len(comparing_list))):
                    if comparing_list[i] != filter_value:
                        for j in range(len(list_of_record_list)): list_of_record_list[j].pop(i)
            elif condition_str == "!=" or condition_str == "not equal":
                for i in reversed(range(len(comparing_list))):
                    if comparing_list[i] == filter_value:
                        for j in range(len(list_of_record_list)): list_of_record_list[j].pop(i)
            elif condition_str == ">=" or condition_str == "greater than equal":
                for i in reversed(range(len(comparing_list))):
                    if comparing_list[i] < filter_value:
                        for j in range(len(list_of_record_list)): list_of_record_list[j].pop(i)
            elif condition_str == "<=" or condition_str == "less than equal":
                for i in reversed(range(len(comparing_list))):
                    if comparing_list[i] > filter_value:
                        for j in range(len(list_of_record_list)): list_of_record_list[j].pop(i)
            elif condition_str == "between":
                for i in reversed(range(len(comparing_list))):
                    if (comparing_list[i] < filter_value) or (comparing_list[i] > filter_2ndValue):
                        for j in range(len(list_of_record_list)): list_of_record_list[j].pop(i)

        return succeed

    @staticmethod
    def SpecialDataFieldsFromOutputFile(model_directory, initial_filename, file_type, field_list):
        #field_list = [field1, field2,...]
        result_list = []
        output = ReadBinaryOutput.ReadModelOutput(model_directory, initial_filename, file_type, trim=True, post_processing=True, ucf=True)

        for field in field_list:
            temp = ReadBinaryOutput.ExtractColumnRecord(field, output.get_header_variable(), output.get_record_list())
            if temp: result_list.append(temp)
            else: result_list.append([])

        return result_list

    @staticmethod
    def RecalculateStemGrowth(start_year, col_name_list_in, col_data_list_in):
        #col_name_list_in = [col_name1, col_name2,...]
        #con_data_list_in =  [col_data1, col_data2]; col_data = [data, data, data.....]
        if 'year' not in col_name_list_in or 'cf_vegt_harvest_stem_tot' not in col_name_list_in: return None
        else:
            result = [] #[cs_vegt_cum_harvest_stem_tot, cs_vegt_stem_harvest_stem_tot_cum]
            year_index = col_name_list_in.index('year')

            ReadBinaryOutput.Filter(col_data_list_in, year_index, '>=', start_year)
            ndx = col_name_list_in.index('cf_vegt_harvest_stem_tot')
            cf_vegt_harvest_stem_tot = np.array(col_data_list_in[ndx])
            cs_vegt_cum_harvest_stem_tot = np.cumsum(cf_vegt_harvest_stem_tot)

            result.append(cs_vegt_cum_harvest_stem_tot.tolist())

            if 'cs_vegt_sum_stem' in col_name_list_in:
                cs_vegt_sum_stem = np.array(col_data_list_in[col_name_list_in.index('cs_vegt_sum_stem')])
                cs_vegt_stem_harvest_stem_tot_cum = cs_vegt_cum_harvest_stem_tot + cs_vegt_sum_stem
                result.append(cs_vegt_stem_harvest_stem_tot_cum.tolist())
            return result

    @staticmethod
    def FilterRecord(var_record, x_record, condition_str, filter_value, filter_2ndValue=None, numeric_comp_flag=False):
        #excluding None values
        for i in reversed(range(len(var_record))):
            if var_record[i] is None:
                var_record.pop(i)
                x_record.pop(i)

        #conversion for numeric comparison
        if numeric_comp_flag:
            for i in range(len(var_record)):
                try:
                    var_record[i] = float(var_record[i])
                except: pass

            for i in range(len(x_record)):
                try:
                    x_record[i] = float(x_record[i])
                except: pass

        #condition_str can be ">", "<", "=", "!=", ">=", "<="
        if condition_str == ">" or condition_str == "greater than":
            for i in reversed(range(len(var_record))):
                if var_record[i] <= filter_value:
                    var_record.pop(i)
                    x_record.pop(i)
        elif condition_str == "<" or condition_str == "less than":
            for i in reversed(range(len(var_record))):
                if var_record[i] >= filter_value:
                    var_record.pop(i)
                    x_record.pop(i)
        elif condition_str == "=" or condition_str == "equals":
            for i in reversed(range(len(var_record))):
                if var_record[i] != filter_value:
                    var_record.pop(i)
                    x_record.pop(i)
        elif condition_str == "!=" or condition_str == "not equal":
            for i in reversed(range(len(var_record))):
                if var_record[i] == filter_value:
                    var_record.pop(i)
                    x_record.pop(i)
        elif condition_str == ">=" or condition_str == "greater than equal":
            for i in reversed(range(len(var_record))):
                if var_record[i] < filter_value:
                    var_record.pop(i)
                    x_record.pop(i)
        elif condition_str == "<=" or condition_str == "less than equal":
            for i in reversed(range(len(var_record))):
                if var_record[i] > filter_value:
                    var_record.pop(i)
                    x_record.pop(i)
        elif condition_str == "between":
            for i in reversed(range(len(var_record))):
                if (var_record[i] < filter_value) or (var_record[i] > filter_2ndValue):
                    var_record.pop(i)
                    x_record.pop(i)

    @staticmethod
    def FilterRecord_with_groups(var_record, condition_str, condition_value, group_record):
        #condition_str can be ">", "<", "=", "!=", ">=", "<="
        #structure of group_record: [[data list for group1],[data list for group2],..]. in this case
        # length of var_record, and each group list should be the same

        #deleting None values: in respect to the var_record
        for i in reversed(range(len(var_record))):
            if var_record[i] is None:
                var_record.pop(i)
                for grp_rec in group_record: grp_rec.pop(i)

        #deleting None Values: in respect to the group_record
        for grp_rec in group_record:
            for i in reversed(range(len(grp_rec))):
                if grp_rec[i] is None:
                    var_record.pop(i)
                    for gr in group_record: gr.pop(i)



        #filtering data
        pre_check = True
        for grp_rec in group_record:
            if len(var_record) != len(grp_rec): pre_check = False

        if pre_check:
            if condition_str == ">":
                for i in reversed(range(len(var_record))):
                    if var_record[i] <= condition_value:
                        var_record.pop(i)
                        for grp_rec in group_record:
                            grp_rec.pop(i)

            elif condition_str == "<":
                for i in reversed(range(len(var_record))):
                    if var_record[i] >= condition_value:
                        var_record.pop(i)
                        for grp_rec in group_record:
                            grp_rec.pop(i)

            elif condition_str == "=":
                for i in reversed(range(len(var_record))):
                    if var_record[i] != condition_value:
                        var_record.pop(i)
                        for grp_rec in group_record:
                            grp_rec.pop(i)

            elif condition_str == "!=":
                for i in reversed(range(len(var_record))):
                    if var_record[i] == condition_value:
                        var_record.pop(i)
                        for grp_rec in group_record:
                            grp_rec.pop(i)

            elif condition_str == ">=":
                for i in reversed(range(len(var_record))):
                    if var_record[i] < condition_value:
                        var_record.pop(i)
                        for grp_rec in group_record:
                            grp_rec.pop(i)

            elif condition_str == "<=":
                for i in reversed(range(len(var_record))):
                    if var_record[i] > condition_value:
                        var_record.pop(i)
                        for grp_rec in group_record:
                            grp_rec.pop(i)

    @staticmethod
    def FilterXRecord(var_record, x_record, x_filter_condition_str, x_filter_value, x_filter_2ndValue = None, numeric_comp_flag = False):
        ReadBinaryOutput.FilterRecord(x_record, var_record, x_filter_condition_str, x_filter_value,
                                      filter_2ndValue=x_filter_2ndValue, numeric_comp_flag=numeric_comp_flag)

    @staticmethod
    def GroupingVariableValue(var_record, group_record, group_function_str):
        #structure of group_record: [[data list for group1],[data list for group2],..]. in this case
        # length of var_record, and each group list should be the same

        group_label = []
        temp_dic = {}

        #grouping data
        for i in range(len(var_record)):
            temp_str = ""
            for grp_record in group_record:
                temp_str += str(grp_record[i]) + ":"
            temp_str = temp_str[:-1]
            if temp_str in group_label: temp_dic[temp_str].append(var_record[i])
            else:
                temp_dic[temp_str] = [var_record[i]]
                group_label.append(temp_str)

        if group_function_str.lower() == "average":
            for key, value in temp_dic.items():
                l = [x for x in value if x is not None]
                if len(l) > 0: temp_dic[key] = np.mean(l)
                else: temp_dic[key] = None
        elif group_function_str.lower() == "min":
            for key, value in temp_dic.items():
                l = [x for x in value if x is not None]
                if len(l) > 0: temp_dic[key] = np.amin(l)
                else: temp_dic[key] = None
                # if None not in temp_dic[key]: temp_dic[key] = np.amin(value)
                # else: temp_dic[key] = None
        elif group_function_str.lower() == "max":
            for key, value in temp_dic.items():
                l = [x for x in value if x is not None]
                if len(l) > 0: temp_dic[key] = np.amax(l)
                else: temp_dic[key] = None
                # if None not in temp_dic[key]: temp_dic[key] = np.amax(value)
                # else: temp_dic[key] = None
        elif group_function_str.lower() == "std. dev":
            for key, value in temp_dic.items():
                l = [x for x in value if x is not None]
                if len(l) > 0: temp_dic[key] = np.std(l)
                else: temp_dic[key] = None
                # if None not in temp_dic[key]: temp_dic[key] = np.std(value)
                # else: temp_dic[key] = None
        elif group_function_str.lower() == "variance":
            for key, value in temp_dic.items():
                l = [x for x in value if x is not None]
                if len(l) > 0: temp_dic[key] = np.var(l)
                else: temp_dic[key] = None
                # if None not in temp_dic[key]: temp_dic[key] = np.var(value)
                # else: temp_dic[key] = None
        elif group_function_str.lower() == "sum":
            for key, value in temp_dic.items():
                l = [x for x in value if x is not None]
                if len(l) > 0: temp_dic[key] = np.sum(l)
                else: temp_dic[key] = None
                # if None not in temp_dic[key]: temp_dic[key] = np.sum(value)
                # else: temp_dic[key] = None
        elif group_function_str.lower() == "count":
            for key, value in temp_dic.items():
                l = [x for x in value if x is not None]
                if len(l) > 0: temp_dic[key] = len(l)
                else: temp_dic[key] = None
                # if None not in temp_dic[key]: temp_dic[key] = len(value)
                # else: temp_dic[key] = None

        out_list = []   #structure: [[group_title_list],[group_value_list]]
        if len(group_label) == len(temp_dic):
            group_value_list = []
            for i in range(len(group_label)):
                group_value_list.append(temp_dic[group_label[i]])

            return [group_label, group_value_list]

        return None

    @staticmethod
    def FindGroupLabel(group_record):
        #structure of group_record: [[data list for group1],[data list for group2],..]. in this case
        # length of var_record, and each group list should be the same

        group_label = []

        if len(group_record) > 0:
            for i in range(len(group_record[0])):
                temp_str = ""
                for grp_rec in group_record:
                    temp_str += str(grp_rec[i]) + ":"
                temp_str = temp_str[:-1]
                if temp_str not in group_label: group_label.append(temp_str)

        return group_label

    @staticmethod
    def FilterGroupResult(group_result, filter_condition_str, filter_value, try_numeric_comparison=False):
        #structure of group_result: [[group_title_list],[group_value_list]]

        if try_numeric_comparison:
            try:
                filter_value = float(filter_value)

                for i in range(len(group_result[0])):
                    group_result[0][i] = float(group_result[0][i])
            except:
                return None

        if filter_condition_str.lower() == "greater than":
            for i in reversed(range(len(group_result[0]))):
                if group_result[0][i] <= filter_value:
                    group_result[0].pop(i)
                    group_result[1].pop(i)
        elif filter_condition_str.lower() == "equals":
            for i in reversed(range(len(group_result[0]))):
                if group_result[0][i] != filter_value:
                    group_result[0].pop(i)
                    group_result[1].pop(i)
        elif filter_condition_str.lower() == "less than":
            for i in reversed(range(len(group_result[0]))):
                if group_result[0][i] >= filter_value:
                    group_result[0].pop(i)
                    group_result[1].pop(i)
        elif filter_condition_str.lower() == "less than equal":
            for i in reversed(range(len(group_result[0]))):
                if group_result[0][i] > filter_value:
                    group_result[0].pop(i)
                    group_result[1].pop(i)
        elif filter_condition_str.lower() == "greater than equal":
            for i in reversed(range(len(group_result[0]))):
                if group_result[0][i] < filter_value:
                    group_result[0].pop(i)
                    group_result[1].pop(i)

    @staticmethod
    def ReadModelOutput_for_graph(init_file_list, file_type_list_2b_read_in, var_list_2b_picked):
        output_list = deepcopy(var_list_2b_picked)

        for i in range(len(init_file_list)):
            init_file = init_file_list[i]
            init_param = FileReadWrite.readInitialFile(init_file)
            model_directory = init_file.split("/ini/")[0]
            if ApplicationProperty.currentModelDirectory == '': ApplicationProperty.currentModelDirectory = model_directory
            for j in range(len(file_type_list_2b_read_in[i])):
                file_type = file_type_list_2b_read_in[i][j]
                list_of_record = ReadBinaryOutput.ReadModelOutput_binary(model_directory, init_param, file_type)

                #read_result = ReadBinaryOutput.ReadModelOutput(model_directory, init_file, file_type, trim=True, post_processing=True, ucf=True)
                #list_of_record = read_result.get_record_list()
                output_variable_list = ReadBinaryOutput.FindOutputVariableList(init_param, file_type)
                file_specific_header_variable = ReadBinaryOutput.FindFileSpecificHeaderVariable(file_type)
                header_variable_list = file_specific_header_variable[0] + ReadBinaryOutput.FindOutputVariableNameList(init_param, file_type, output_variable_list)

                for k in [0,1]:
                    var_list = var_list_2b_picked[i][j][k]
                    temp_list = []
                    if len(var_list) > 0:
                        ReadBinaryOutput.ModelOutputPostProcess(file_type, list_of_record, header_variable_list, init_param)

                        if k == 0: ReadBinaryOutput.UnitConversion(file_type, header_variable_list, list_of_record)

                        for var in var_list:
                            temp_list.append(ReadBinaryOutput.ExtractColumnRecord(var, header_variable_list, list_of_record))

                    output_list[i][j][k] = temp_list
        return output_list
    
    @staticmethod
    def write_csv(header_list, data, file_name):
        f = None
        try:
            f = open(file_name, 'w', newline="")
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(header_list)
            for d in data:
                wr.writerow(d)
        except: return False
        finally:
            try: f.close()
            except: pass
        return True

class ReadExternalOutput():
    @staticmethod
    def read_csv_file(fileName, delimiter, first_line_as_column_header=True):
        read_result = DataReadResult()

        if os.path.exists(fileName):
            header_row = []
            list_of_record = []

            csv_file = None
            try:
                csv_file = open(fileName, mode='r')
                reader = csv.reader(csv_file, delimiter=delimiter)
                if first_line_as_column_header: header_row = next(reader)
                for row in reader:
                    for i in range(len(row)):
                        try:
                            row[i] = int(row[i])
                        except:
                            try:
                                row[i] = float(row[i])
                            except:
                                if row[i] == " " or row[i] == "": row[i] = None
                                elif row[i].find("/"):
                                    try:
                                        row[i] = datetime.datetime.strptime(row[i], '%m/%d/%Y')
                                    except: pass

                    list_of_record.append(row)

            except:
                return None
            finally:
                try:
                    csv_file.close()
                except: pass

            read_result.header_variable = header_row
            read_result.record_list = list_of_record

        return read_result

    @staticmethod
    def ReadCSV(fileName, delimiter, first_line_as_column_header=True):
        record_list = None  #structure: [[headers],[[row1],[row2],[row3]....]]
        if os.path.exists(fileName):
            header_row = []
            list_of_record = []
            try:
                csv_file = open(fileName, mode='r', encoding='utf-8')
                reader = csv.reader(csv_file, delimiter=delimiter)
                if first_line_as_column_header:
                    header_row = next(reader)
                    # for i in range(len(header_row)): header_row[i] = header_row[i].replace(u'\ufeff', '')

                for row in reader:
                    for i in range(len(row)):
                        try:
                            row[i] = int(row[i])
                        except:
                            try:
                                row[i] = float(row[i])
                            except:
                                if row[i] == " " or row[i] == "": row[i] = None
                                elif row[i].find("/"):
                                    try:
                                        row[i] = datetime.datetime.strptime(row[i], '%m/%d/%Y')
                                    except: pass


                    list_of_record.append(row)
                record_list = [header_row, list_of_record]
            except:
                return None
            finally:
                try:
                    csv_file.close()
                except: pass

        return record_list

    @staticmethod
    def write_csv(header_list, data, file_name):
        f = None

        try:
            f = open(file_name, 'w', newline='')
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(header_list)
            for d in data:
                wr.writerow(d)
        except: return False
        finally:
            try: f.close()
            except: pass
        return True
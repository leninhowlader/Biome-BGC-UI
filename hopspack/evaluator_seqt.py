#!/usr/bin/python

#modified on: 23-10-2014

import sys, os
sys.path.append('..')
from file_io import FileReadWrite
from subprocess import call
from hopspack.configure import Configure, Comparing_Variable, TargetParameter
from parameter_set import BiomeBGCParameterSet
from application import ApplicationProperty
import glob
from hopspack.stat_lm import stat

def read_input_file (input_filename, list_of_parameter):
    succeed = False

    in_file = None
    try:
        in_file = open(input_filename, 'r')

        if in_file:
            temp = in_file.readline().strip()
            if temp == 'F':
                temp = in_file.readline().strip()

                try: temp = int(temp)
                except: temp = 0
                if len(list_of_parameter) == temp:
                    for i in range(temp):
                        try:
                            val = float(in_file.readline())
                            list_of_parameter[i].current_value = val
                        except Exception as ex:
                            print("ERROR: reading parameters\n")
                            break
                    else: succeed = True
    except:
        print("Hopspack-input file is not found!")
    finally:
        try: in_file.close()
        except: pass

    if succeed: return 0
    else: return -2

def write_output_file (out_filename, fun_value_list):
    file = None
    try:
        file = open(out_filename, "w")
        file.write("%d\n" %len(fun_value_list))

        for f in fun_value_list: file.write(str(f) + '\n')
    except:
        print("ERROR opening output file '%s'.\n" % out_filename)
        return -3
    finally:
        try: file.close()
        except: pass

    return 0

def ReadModelParameter_delete(modelDirectory, initialFilename):
    modelParam = None

    initParam = FileReadWrite.readInitialFile(os.path.join(modelDirectory, "ini", initialFilename))
    if initParam is not None:
        #reading gis file
        gisParam = []
        filename = modelDirectory + "/" + initParam.gis_file_name
        gisList = FileReadWrite.readGisFile(filename)
        for gis in gisList:
            gisItem = {"siteIndex": gis.siteIndex, "gis": gis}
            gisParam.append(gisItem)

        if len(gisParam) > 0:
            #reading veg files and epc files
            vegParam = []
            filename = modelDirectory + "/" + initParam.veg_file_name
            vegList = FileReadWrite.readVegFile(filename)

            vegEpc = []             #structure: [{"siteIndex": siteIndex, "epcid": epcid}, {}]
            epcParam = []           #structure: [{"epcid": epcid, "epc": epcObject}, {}]
            temp = []               #structure: [{"epcid": epcid, "fileName": epcFileName}, {}]
            epcid = 0

            for veg in vegList:
                vegItem = {"siteIndex": veg.siteIndex, "vegid": veg.vegetationNumber, "veg": veg}
                vegParam.append(vegItem)

                #because epc parameters were separated from initial parameter in order to
                #allow using the same epc for different sites, here all distinct epc objects
                #will be stored in dictionary and an array of index is used to maintain
                #the relation between site and epc object.

                for i in range(len(temp)):
                    if temp[i]["fileName"] == veg.epcFileName: break
                else:
                    epcid += 1
                    epcFileNameItem = {"epcid": epcid, "fileName": veg.epcFileName}
                    temp.append(epcFileNameItem)

                vegEpcItem = {"siteIndex": veg.siteIndex, "vegid": veg.vegetationNumber, "epcid": epcid}
                vegEpc.append(vegEpcItem)

            for epcFileNameItem in temp:
                filename = modelDirectory + "/epc/" + epcFileNameItem["fileName"]
                epc = FileReadWrite.readEpcFile(filename)
                epcItem = {"epcid": epcFileNameItem["epcid"], "epc": epc, "updateFlag": False}
                epcParam.append(epcItem)

            #read soil profile files and soil horizon files
            temp = []   #structure: [{"siteIndex": profileFileId, "pFileName": profileFileName, "hFileName": horizonFileName,
                        # "profileName": profileName},{}]
            gisSoil = []
            soilParam = []
            for gpo in gisParam:
                for i in range(len(temp)):
                    if temp[i]["siteIndex"] == gpo["gis"].siteIndex: break
                else:
                    gis = gpo["gis"]
                    soilFileItem = {"siteIndex": gis.siteIndex, "pFileName": gis.soilProfileFileName,
                                "hFileName": gis.soilHorizonFileName, "profileName": gis.profileName}
                    temp.append(soilFileItem)

            if len(temp) > 0:
                spfid = 0
                for sp in temp:
                    profileList = FileReadWrite.readSoilProfile(modelDirectory + "/soil/" + sp["pFileName"],
                                            modelDirectory + "/soil/" + sp["hFileName"])
                    for profile in profileList:
                        if profile.profileName == sp["profileName"]:
                            spfid += 1
                            gisSoilItem = {"siteIndex": sp["siteIndex"], "spfid": spfid}
                            gisSoil.append(gisSoilItem)

                            soilParamItem = {"spfid": spfid, "sp": profile}
                            soilParam.append(soilParamItem)

            if (len(vegParam) > 0 and len(vegEpc) > 0 and len(epcParam) > 0 and len(gisSoil) > 0 and len(soilParam) > 0):
                modelParam = BiomeBGCParameterSet()
                modelParam.initParam = initParam
                modelParam.gisParam = gisParam
                modelParam.vegParam = vegParam
                modelParam.vegEpc = vegEpc
                modelParam.epcParam = epcParam
                modelParam.gisSoil = gisSoil
                modelParam.soilParam = soilParam

    return modelParam

def clean_files(model_directory, prefix):
    file_list = []

    folder_list = ['ini', 'epc', 'soil', 'outputs']
    for folder in folder_list:
        file_list += glob.glob(os.path.join(model_directory, folder, '*' + prefix + '*.*'))

    for filename in file_list: os.remove(filename)

def border_penalty(hp_parameter_set, penalty_constant, objective_target='minimize'):
    penalty_sum = 0

    if objective_target.lower() == 'maximize': penalty_constant = 1 / penalty_constant

    for parameter in hp_parameter_set:
        d = 0
        r = parameter.upper_bound - parameter.lower_bound

        if parameter.current_value > parameter.upper_bound:
            d = parameter.current_value - parameter.upper_bound
        elif parameter.current_value < parameter.lower_bound:
            d = parameter.lower_bound - parameter.current_value

        penalty_sum += penalty_constant * (1 + d/r)

    return penalty_sum

def  main (argv):
    if len(argv) != 5:
        print("usage: %s <input file> <output file> <tag> <type>\n" %argv[0])
        return -100

    #step-1: read configuration file
    config = Configure()

    #step-1.1: setting working directory
    bgc_directory = config.model_directory
    initial_filename = os.path.join(bgc_directory, 'ini', config.initial_filename)
    ApplicationProperty.currentModelDirectory = bgc_directory
    #step-1.2: reading parameter information
    hp_parameter_set = []
    if config.parameterMap_file:
        TargetParameter.read_parameter_list(config.parameterMap_file, hp_parameter_set)
        if len(config.parameter_sequence) == len(hp_parameter_set):
            temp = []
            for seq in config.parameter_sequence:
                temp.append(hp_parameter_set[seq])
            hp_parameter_set = temp
    else:
        print('No parameter file specified in Hopspack Setting File.')
        return -3

    #step-1.3: reading comparison file
    Comparing_Variable.objective_function = config.objective_function
    if config.comparisonMap_file:
        comparison_list = Comparing_Variable.read_comparing_variables(config.comparisonMap_file)
    else:
        print('No comparison file specified in Hopspack Setting File.')
        return -3

    #step-2: reading hopspack input file
    nRetStatus = read_input_file (argv[1], hp_parameter_set)
    if nRetStatus != 0: return nRetStatus

    #step-3: saving new parameter value in bgc input files
    bgc_parameter_set = BiomeBGCParameterSet.ReadBBGCParameterSet(bgc_directory, initial_filename)
    
    version_text = ''
    if bgc_parameter_set is not None:
        if config.extension_postfix:
            version_text = config.extension_postfix + str(argv[3])
        else: version_text = 'hp' + str(argv[3])

        if bgc_parameter_set.vegParam is not None:
            if len(bgc_parameter_set.vegParam) == 1:
                site_index = bgc_parameter_set.vegParam[0]["siteIndex"]
                veg_id = bgc_parameter_set.vegParam[0]["vegid"]

                for hp_param in hp_parameter_set:
                    bgc_parameter_set.updateEpcObject(site_index, veg_id, -1, hp_param.parameter_name, hp_param.current_value,
                                                        version_text)

        bgc_parameter_set.initParam.output_file_prefix += version_text
        initial_filename = config.initial_filename.replace('.ini', '_' + version_text + '.ini')
        BiomeBGCParameterSet.save_parameter_set(bgc_parameter_set, bgc_directory, initial_filename, version_text)

        #step-4: run bgc
        call(os.path.join(bgc_directory, "bgc_zalf.sh") + " " + initial_filename + " y", shell=True)

        try:
            #step-5: evaluate model output
            fun_value_list = stat.data_evaluation(bgc_directory, initial_filename, comparison_list, config.normalize_data_by_observed_max,
                                     config.normalize_data_by_observed_mean)

            #step-6: calculate boundary penalty if applicable
            if config.bound_penalty_flag:
                if config.objective_function in ['Index of Agreement','Nash-Sutcliffe Efficiency', 'Coefficient of Determination']: config.objective_target = 'Maximize'
                elif config.objective_function in ['Absolute Average Deviation', 'Mean Absolute Error', 'Mean Square Error', 'Root Mean Square Error', 'RMSE-Observed Stdv. Ratio']: config.objective_target = 'Minimize'
                else: config.objective_target = 'Towards 0'

                bound_penalty = border_penalty(hp_parameter_set, config.penalty_constant, config.objective_target)

                if config.objective_target.lower() == 'maximize': fun_value_list.append(1/bound_penalty)
                else: fun_value_list.append(bound_penalty)

            #step-7: write output file for hopspack
            nRetStatus = write_output_file(argv[2], fun_value_list)
            if nRetStatus != 0: return nRetStatus
        except Exception as ex:
            return -3
        finally:
            #step-8: clean files
            clean_files(bgc_directory, version_text)
    else:
        return -3

    return 0
    
    
main(sys.argv)

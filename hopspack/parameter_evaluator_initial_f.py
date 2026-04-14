#!/usr/bin/python3

#modified on: 23-10-2014

import sys, os
sys.path.append('..')
from subprocess import call
from hopspack.configure import Configure, Comparing_Variable, TargetParameter
from parameter_set import BiomeBGCParameterSet
from application import ApplicationProperty
import glob
from hopspack.stat import stat

def clean_files(model_directory, prefix):
    file_list = []

    folder_list = ['ini', 'epc', 'soil', 'outputs']
    for folder in folder_list:
        file_list += glob.glob(os.path.join(model_directory, folder, '*' + prefix + '*.*'))

    for filename in file_list: 
        try: os.remove(filename)
        except: pass

def border_penalty(hp_parameter_set, penalty_constant):
    penalty_sum = 0

    for parameter in hp_parameter_set:
        d = 0
        r = abs(parameter.upper_bound - parameter.lower_bound)

        if parameter.current_value > parameter.upper_bound:
            d = parameter.current_value - parameter.upper_bound
        elif parameter.current_value < parameter.lower_bound:
            d = parameter.lower_bound - parameter.current_value

        penalty_sum += penalty_constant * (1 + d/r)

    return penalty_sum

def maximum_penalty(parameter_set, penalty_constant):
    maxp = 0
    for parameter in parameter_set:
        d = max(abs(parameter.hard_upper_bound - parameter.upper_bound), abs(parameter.lower_bound - parameter.hard_lower_bound))
        r = abs(parameter.upper_bound - parameter.lower_bound)
        maxp += penalty_constant * (1 + d/r)
    return maxp

def  main ():
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

    #step-3: saving new parameter value in bgc input files
    bgc_parameter_set = BiomeBGCParameterSet.ReadBBGCParameterSet(bgc_directory, initial_filename)
    
    version_text = ''
    if bgc_parameter_set is not None:
        version_text = 'init'

        if bgc_parameter_set.vegParam is not None:
            if len(bgc_parameter_set.vegParam) == 1:
                site_index = bgc_parameter_set.vegParam[0]["siteIndex"]
                veg_id = bgc_parameter_set.vegParam[0]["vegid"]

                for hp_param in hp_parameter_set:
                    hp_param.current_value = hp_param.starting_value
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
                else: config.objective_target = 'Minimize'

                bound_penalty = border_penalty(hp_parameter_set, config.penalty_constant)

                if config.objective_target.lower() == 'maximize':
                    max_penalty = maximum_penalty(hp_parameter_set, config.penalty_constant)
                    fun_value_list.append(max_penalty - bound_penalty)
                else: fun_value_list.append(bound_penalty)

            print('No of Comparison: ' + str(len(comparison_list)))
            print(fun_value_list)
        except Exception as ex:
            return -3
        finally:
            #step-8: clean files
            clean_files(bgc_directory, version_text)
    else:
        return -3

    return 0
    
    
main()

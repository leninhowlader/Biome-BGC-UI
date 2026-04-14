#!/usr/bin/python

#modified on: 23-10-2014

import sys, os
sys.path.append('..')
from subprocess import call
from hopspack.configure import Configure, Comparing_Variable, TargetParameter
from parameter_set import BiomeBGCParameterSet
from application import ApplicationProperty
import glob
from hopspack.stat_ipt import stat

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
        temp = []
        TargetParameter.read_parameter_list(config.parameterMap_file, temp)
        for sname in config.parameter_sequence:
            for p in temp:
                if p.sname == sname:
                    hp_parameter_set.append(p)
                    break
    else:
        print('No parameter file specified in Hopspack Setting File.')
        return -3
    #step-1.3: reading comparison file
    Comparing_Variable.objective_function = config.objective_function
    if config.comparisonMap_file:
        comparison_list = Comparing_Variable.read_comparing_variables(config.comparisonMap_file)
        if config.objective_function:
            for comp in comparison_list: comp.objective_function = config.objective_function
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
                    bgc_parameter_set.updateEpcObject(site_index, veg_id, -1, hp_param.name, hp_param.current_value,
                                                        version_text)

        bgc_parameter_set.initParam.output_file_prefix += version_text
        initial_filename = config.initial_filename.replace('.ini', '_' + version_text + '.ini')
        BiomeBGCParameterSet.save_parameter_set(bgc_parameter_set, bgc_directory, initial_filename, version_text)

        #step-4: run bgc
        call(os.path.join(bgc_directory, "bgc_zalf.sh") + " " + initial_filename + " y", shell=True)

        try:
            norm_obs_max_flag = False
            norm_obs_mean_flag = False

            if config.normalization_option_flag == 0:
                norm_obs_max_flag = True
                norm_obs_mean_flag = False
            elif config.normalization_option_flag == 1:
                norm_obs_max_flag = False
                norm_obs_mean_flag = True
            #step-5: evaluate model output
            fun_value_list = stat.data_evaluation(bgc_directory, initial_filename, comparison_list, norm_obs_max_flag,
                                     norm_obs_mean_flag)

            fit_mode = 'grand sum'
            if fit_mode == 'grand sum':
                r = 0
                for v in fun_value_list:
                    if v == 'DNE':
                        r = 'DNE'
                        break
                    else: r = r + v
                fun_value_list = [r]

            #step-6: calculate boundary penalty if applicable
            if config.penalty_option_flag > -1:
                if config.objective_function in ['Index of Agreement','Nash-Sutcliffe Efficiency', 'Coefficient of Determination']: config.objective_target = 'Maximize'
                else: config.objective_target = 'Minimize'

                bound_penalty = border_penalty(hp_parameter_set, config.penalty_constant)

                if config.objective_target.lower() == 'maximize': fun_value_list.append(-bound_penalty)
                else: fun_value_list.append(bound_penalty)

            #step-7: write output file for hopspack
            nRetStatus = write_output_file(argv[2], fun_value_list)
            
            #__start
            #record the input/output values in a file. This section might be deleted in the final verion
            ff = None
            try:
                ff = open('points_and_funval.txt','a')                                 
                text_line = str(argv[3]) + ';'
                for p in hp_parameter_set: text_line += str(p.current_value) + ';'
                for f in fun_value_list: text_line += str(f) + ';'
                ff.write(text_line + '\n') 
            except: pass
            finally:
                try: ff.close() 
                except: pass
            #__end

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

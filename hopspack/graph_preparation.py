#!/usr/bin/python3

#modified on: 22-10-2014

import sys, os
sys.path.append('..')
from hopspack.configure import Configure, TargetParameter
from application import ApplicationProperty
from parameter_set import BiomeBGCParameterSet
from subprocess import call
from copy import deepcopy

def read_best_points(filename, plot_no, fun):
    bf = None
    try:
        bf = open(filename, 'r')
        bf.readline()
        for line in bf.readlines():
            temp = line.strip('\n').strip('\r').split(',')
            #ff_name = Configure
            if temp[0] == plot_no and temp[1] == fun:
                for i in reversed(range(len(temp))):
                    try:
                        temp[i] = float(temp[i])
                        if temp[i] == -9999: temp.pop(i)
                    except:
                        if temp[i] == '' or temp[i] == ' ': temp.pop(i)
                return temp
    except: return None
    finally:
        try: bf.close()
        except: pass


def  main (argv):
    if len(argv) < 4:
        print('usages: solution_processing.py <plot no.> <Data File> <obj. fun> <Version Text>')
        exit(-1)

    plot_no = argv[1]
    data_file = argv[2]
    obj_fun = argv[3]
    v_text = argv[4]

    initial_run = True
    flag_best_point = True

    #step-1: reading configuration (and saving calibration info)
    if obj_fun != '-': config_file = os.path.join('config',plot_no, 'configuration_' + plot_no + '_' + obj_fun + '.txt')
    else: config_file = os.path.join('config',plot_no, 'configuration_' + plot_no + '_rmse.txt')
    config = Configure(config_file)


    #step-2: reading parameter and solution file (and save parameters)
    #step-2.1: reading parameter file
    hp_parameter_set = []
    if config.parameterMap_file:
        TargetParameter.read_parameter_list(config.parameterMap_file, hp_parameter_set)
    else:
        print('No parameter file specified in Hopspack Setting File.')
        return -3

    #step-2.2: reading solution file
    #best_point = read_best_points('selected_best_parameter.csv', plot_no, obj_fun)[2:]
    best_point = read_best_points(data_file, plot_no, obj_fun.lower())[2:]
    #hubert_point = read_best_points('hubert_parameter_x9.csv', plot_no, obj_fun)[2:]
    # hubert_point = read_best_points('hubert_parameter_x9.csv', plot_no, 'mae')[2:]

    if len(best_point) != len(hp_parameter_set): exit('Parameter count conflict!!')
    #step-3: preparing to run Biome-BGC Model
    #step-3.1: setting working directory
    model_directory = config.model_directory
    initial_filename = os.path.join(model_directory, 'ini', config.initial_filename)
    ApplicationProperty.currentModelDirectory = model_directory

    #step-3.2: reading Biome-BGC input parameter files
    bgc_parameter_set = BiomeBGCParameterSet.ReadBBGCParameterSet(model_directory, initial_filename)

    #step-4: run Biome-BGC with best parameter point(s)
    #step-4.1: assigning starting value as current parameter value
    for i in range(len(hp_parameter_set)):
        hp_param = hp_parameter_set[i]
        hp_param.current_value = best_point[i]

    #step-4.2: saving hp.parameter values in model input files
    bgc_parameter_set_initial = deepcopy(bgc_parameter_set)

    if initial_run:
        if (bgc_parameter_set_initial is not None):
            version_text = v_text
            if bgc_parameter_set_initial.vegParam is not None:
                if len(bgc_parameter_set_initial.vegParam) == 1:
                    site_index = bgc_parameter_set_initial.vegParam[0]["siteIndex"]
                    veg_id = bgc_parameter_set_initial.vegParam[0]["vegid"]

                    for hp_param in hp_parameter_set:
                        bgc_parameter_set_initial.updateEpcObject(site_index, veg_id, -1, hp_param.parameter_name, hp_param.current_value,
                                                            version_text)

            bgc_parameter_set_initial.initParam.output_file_prefix += version_text
            initial_filename = config.initial_filename.replace('.ini', '_' + version_text + '.ini')
            BiomeBGCParameterSet.save_parameter_set(bgc_parameter_set_initial, model_directory, initial_filename, version_text)
            bgc_parameter_set_initial = None

            #step-4.3: executing Biome-BGC model with initial parameter set
            call(os.path.join(model_directory, "bgc_zalf.sh") + " " + initial_filename + " y", shell=True)
        else:
            print('Biome-BGC input files could not be read!')
            exit(-1)


main(sys.argv)


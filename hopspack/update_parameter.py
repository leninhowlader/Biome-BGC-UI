#!/usr/bin/python

#modified on: 23-10-2014

import sys, os
sys.path.append('..')
from hopspack.configure import Configure, TargetParameter, Solution
from parameter_set import BiomeBGCParameterSet
from application import ApplicationProperty

def  main (argv):
    if len(argv) != 4:
        print("usage: %s <plot no.> <objective fun> <calibration no.>\n" %argv[0])
        exit(0)

    plot_no = argv[1]
    fun = argv[2]
    calid = -1
    try: calid = argv[3]
    except: pass

    if calid == -1:
        print('Please enter a valide calibration number.')
        exit(0)

    #step-1: read configuration file
    config_file = os.path.join('config', 'calibration' + str(calid).rjust(4, '0'), plot_no, 'configuration_' + plot_no + '_' + fun + '.txt')
    config = Configure(config_file)


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
        exit(0)

    #read the solution file
    pval_list = Solution.read_solution_file(config.solution_file)
    if len(pval_list) != len(hp_parameter_set):
        print('Parameter count in solution and configuration file does not match.')
        exit(0)

    #step-2: reading hopspack input file
    for i in range(len(hp_parameter_set)):
        param = hp_parameter_set[i]
        param.current_value = pval_list[i]

    #step-3: saving new parameter value in bgc input files
    bgc_parameter_set = BiomeBGCParameterSet.ReadBBGCParameterSet(bgc_directory, initial_filename)

    rt = False
    version_text = 'cal' + str(calid).rjust(2, '0')
    if bgc_parameter_set is not None:
        if bgc_parameter_set.vegParam is not None:
            if len(bgc_parameter_set.vegParam) == 1:
                site_index = bgc_parameter_set.vegParam[0]["siteIndex"]
                veg_id = bgc_parameter_set.vegParam[0]["vegid"]

                for hp_param in hp_parameter_set:
                    bgc_parameter_set.updateEpcObject(site_index, veg_id, -1, hp_param.name, hp_param.current_value, version_text)
        initial_filename = initial_filename.replace('.ini', '_' + version_text + '.ini')
        rt = BiomeBGCParameterSet.save_parameter_set(bgc_parameter_set, bgc_directory, initial_filename, version_text)

    if rt: exit(99)
    else: exit(0)

main(sys.argv)

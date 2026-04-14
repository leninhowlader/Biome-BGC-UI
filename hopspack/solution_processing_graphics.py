#!/usr/bin/python3

#modified on: 22-10-2014

import sys, os
sys.path.append('..')
from hopspack.hpconfigure import HPOutput, HPConfigure, parameter, comparison_policy
from application import ApplicationProperty
from parameter_set import BiomeBGCParameterSet
from subprocess import call
from copy import deepcopy
import glob
from graph import ModelGraph, ModelPlot, DataSeries, DataSource
from draw_graph import BiomeBgcGraphDummy
from hopspack.stat_lm import stat
from hopspack.dbcore import DbCore, DbOperation


def make_graph(model_directory, starting_init_file, optimized_init_file, measured_data_source, save_flag=False, target_directory='', filename_prefix=''):
    #step-1: make a list of graphs to be produced
    graph_list_type1 = ['stand_precipitation', 'canopy_evaporation', 'soil_temperature', 'soil_moisture_TDR', 'soil_moisture_TENS',
                        'leaf_area_index', 'litterfall', 'stem_carbon']

    graph_list_type2 = ['stand_precipitation_R2', 'canopy_evaporation_R2', 'soil_moisture_R2', 'leaf_area_index_R2',
                         'litterfall_R2', 'stem_growth']
    #graph_list_type2 = ['leaf_area_index_R2','stem_growth']

    list_of_type1_graph = []
    list_of_type2_graph = []
    #step-2: load the template for each graph
    # for g_name in graph_list_type1:
    #     temp = ModelGraph.load_template(os.path.join(ApplicationProperty.getScriptPath(), 'graphs', g_name + '.gto'))
    #     if temp: list_of_type1_graph.append(temp)

    for g_name in graph_list_type2:
        temp = ModelGraph.load_binary_template(os.path.join(ApplicationProperty.getScriptPath(), 'graphs', g_name + '.gto'))
        if temp: list_of_type2_graph.append(temp)

    #step-3: change the graph data sources
    #step-3.1: changing model data source i.e. initial filenames
    for g in list_of_type1_graph:
        for p in g.list_of_plot:
            for s in p.list_of_series:
                if s.data_source.source_type == 0:
                    s.data_source.model_directory = model_directory
                    s.data_source.initial_filename = starting_init_file

    for g in list_of_type2_graph:
        for p in g.list_of_plot:
            first_init_file_flag = False
            second_init_file_flag = False
            for s in p.list_of_series:
                if s.data_source.source_type == 0 and (not first_init_file_flag or not second_init_file_flag):
                    if not first_init_file_flag:
                        first_init_file_flag = True
                        s.data_source.model_directory = model_directory
                        s.data_source.initial_filename = starting_init_file
                    elif not second_init_file_flag:
                        second_init_file_flag = True
                        s.data_source.model_directory = model_directory
                        s.data_source.initial_filename = optimized_init_file

    #step-3.2: changing measured data sources (to be done...)
    #this section should be improved. Data filename should not be used for changing data source
    for g in list_of_type1_graph: pass

    for g in list_of_type2_graph:
        for p in g.list_of_plot:
            for s in p.list_of_series:
                temp = s.data_source.data_filename_csv.split('/')[-1][:9]
                if len(temp) > 0:
                    for i in range(len(measured_data_source)):
                        df = measured_data_source[i].split('/')[-1]
                        if df.find(temp) >= 0:
                            s.data_source.data_filename_csv = measured_data_source[i]
                            break

    #step-4: read data from new sources
    # for g in list_of_type1_graph:
    #     ModelGraph.read_data_from_source_file(g)

    for g in list_of_type2_graph:
        ModelGraph.read_data_from_source_file(g)

    #step-5: produce graphs
    # for i in range(len(list_of_type1_graph)):
    #     g = list_of_type1_graph[i]
    #     print(g.graph_title)
    #     if save_flag:
    #         filename = os.path.join(target_directory, filename_prefix + str(i + 1) + '.png')
    #         BiomeBgcGraphDummy.ShowGraph(g, i+1, display=False, save_file_filename=filename)
    #     else: BiomeBgcGraphDummy.ShowGraph(g, i+1, display=True)

    for i in range(len(list_of_type2_graph)):
        g = list_of_type2_graph[i]
        print(g.graph_title)
        if save_flag:
            filename = os.path.join(target_directory, filename_prefix + str(i + 1) + '.png')
            BiomeBgcGraphDummy.ShowGraph(g, i+1, display=False, save_file_filename=filename)
        else: BiomeBgcGraphDummy.ShowGraph(g, i+1, display=True)

def clean_files(model_directory, prefix):
    file_list = []

    folder_list = ['ini', 'epc', 'soil', 'outputs']
    for folder in folder_list:
        file_list += glob.glob(os.path.join(model_directory, folder, '*' + prefix + '*.*'))

    for filename in file_list: os.remove(filename)

def write_stat_result_into_file(plot_no, fun_name, cal_normalized_by, comparison_list, fun_list, result, filename, is_init):
    #plot,cal_fun,cal_norm,is_init,Root Mean Square Error,Coefficient of Determination,Absolute Average Deviation,
    # Index of Agreement,Mean Absolute Error,Mean Square Error,Percentage Bias,RMSE-Observed Stdv. Ratio,Nash-Sutcliffe Efficiency
    rf = None
    try:
        rf = open(filename, 'a')
        line = plot_no + ';' + fun_name + ';' + cal_normalized_by + ';' + str(is_init)

        for i in range(len(comparison_list)):
            comparison = comparison_list[i]
            sim_var = comparison.output_variable_name
            var_type = comparison.output_file_type
            obs_var = comparison.observation_variable_name
            category = comparison.group
            if comparison.output_file_type.find('monavg') >= 0 and obs_var.find('cum') >= 0: obs_var = obs_var.replace('_cum', '')

            txt = line + ';' + sim_var + ';' + var_type + ';' + obs_var + ';' + category
            for j in range(len(fun_list)): txt += ';' + str(result[i][j])
            rf.write(txt +'\n')
    except Exception as ex:
        pass
    finally:
        try: rf.close()
        except: pass

def write_parameter_value(filename, parameter_set, new_param_value):
    f = None
    try:
        f = open(filename, 'a')
        f.write('parameter name, initial value, optimized value\n')
        for i in range(len(parameter_set)):
            param = parameter_set[i]
            f.write(param.parameter_name + ', ' + str(param.starting_value) + ', ' + str(new_param_value[i]) + '\n')
    except Exception as ex:
        return False
    finally:
        try: f.close()
        except: pass
    return True

def  main (argv):
    if len(argv) < 2:
        print('usages: solution_processing.py <plot no.> <obj. fun>')
        exit(-1)

    plot_no = argv[1]
    obj_fun = argv[2]
    call( os.path.join(ApplicationProperty.getScriptPath(), 'hopspack') + "/prepare.sh " + str(plot_no) + " " + str(obj_fun), shell=True)

    initial_run = True

    #step-1: reading configuration (and saving calibration info)
    config = HPConfigure()
    normalization_type = 'No normalization'
    if config.normalize_data_by_observed_max: normalization_type = 'Using Observed Maximum'
    elif config.normalize_data_by_observed_mean: normalization_type = 'Using Observed Mean'

    #step-2: reading parameter and solution file (and save parameters)
    #step-2.1: reading parameter file
    hp_parameter_set = []
    if config.parameter_file:
        parameter.read_parameter_list(config.parameter_file, hp_parameter_set)
    else:
        print('No parameter file specified in Hopspack Setting File.')
        return -3

    #step-2.2: reading solution file
    param_opt_val = []
    if config.solution_file:
        param_opt_val = HPOutput.read_solution_file(config.solution_file)

    #step-3: preparing to run Biome-BGC Model
    #step-3.1: setting working directory
    model_directory = config.model_directory
    initial_filename = os.path.join(model_directory, 'ini', config.initial_filename)
    ApplicationProperty.currentModelDirectory = model_directory

    #step-3.2: reading Biome-BGC input parameter files
    bgc_parameter_set = BiomeBGCParameterSet.ReadBBGCParameterSet(model_directory, initial_filename)

    #step-4: run Biome-BGC with starting parameter value(s)
    #step-4.1: assigning starting value as current parameter value
    for hp_param in hp_parameter_set:
        hp_param.current_value = hp_param.starting_value

    #step-4.2: saving hp.parameter values in model input files
    bgc_parameter_set_initial = deepcopy(bgc_parameter_set)

    if initial_run:
        if (bgc_parameter_set_initial is not None):
            version_text = 'initial'
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

    #step-5: running the model with optimized parameter values
    #step-5.1: obtaining Biome-BGC model input parameters
    bgc_parameter_set_optimized = deepcopy(bgc_parameter_set)
    initial_filename_optimized = ''

    #step-5.2: assigning optimized value to hp.parameters
    if len(param_opt_val) == len(hp_parameter_set):
        for i in range(len(param_opt_val)):
            hp_param = hp_parameter_set[i]
            hp_param.current_value = param_opt_val[i]
    else:
        print('No. of optimum values are not the same as no. of total parameters.')
        exit(-1)
    #step-5.3: saving hp_parameter values in model input files
    if bgc_parameter_set_optimized is not None:
        version_text = 'optimized'
        if bgc_parameter_set_optimized.vegParam is not None:
            if len(bgc_parameter_set_optimized.vegParam) == 1:
                site_index = bgc_parameter_set_optimized.vegParam[0]["siteIndex"]
                veg_id = bgc_parameter_set_optimized.vegParam[0]["vegid"]

                for hp_param in hp_parameter_set:
                    bgc_parameter_set_optimized.updateEpcObject(site_index, veg_id, -1, hp_param.parameter_name, hp_param.current_value,
                                                        version_text)

        bgc_parameter_set_optimized.initParam.output_file_prefix += version_text
        initial_filename_optimized = config.initial_filename.replace('.ini', '_' + version_text + '.ini')
        BiomeBGCParameterSet.save_parameter_set(bgc_parameter_set_optimized, model_directory, initial_filename_optimized, version_text)

        #step-5.4: executing bgc model with optimized parameter set
        call(os.path.join(model_directory, "bgc_zalf.sh") + " " + initial_filename_optimized + " y", shell=True)
        bgc_parameter_set_optimized = None
    else:
        print('Biome-BGC model cannot be run!')
        exit(-1)

    #step-6: reading comparison file (and saving comparisons into database)
    comparison_list = []
    comparison_policy.cost_function = config.cost_function
    if config.comparison_file:
        comparison_list = comparison_policy.read_policy(config.comparison_file)
    else:
        print('No comparison file specified in Hopspack Setting File.')
        return -100

    #step-7: producing graphs
    config.graph_flag = True
    if config.graph_flag:
        measured_data_source = []
        for comparison in comparison_list:
            if comparison.observation_data_file not in measured_data_source:
                measured_data_source.append(comparison.observation_data_file)

        try:
            make_graph(model_directory, initial_filename, initial_filename_optimized, measured_data_source, save_flag=False, target_directory=os.path.join(model_directory, 'graph'), filename_prefix='test')
        except Exception as ex:
            pass
        # make_graph(model_directory, initial_filename, initial_filename_optimized, measured_data_source, save_flag=False, target_directory=os.path.join(model_directory, 'graph'), filename_prefix='test')

    #step-5: cleaning temporary parameter files, output and/or graphs
    if initial_run: clean_files(model_directory, 'initial')
    clean_files(model_directory, 'optimized')

main(sys.argv)


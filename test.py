import os
from graph import ModelGraph, DataSeries
from read_output import ReadExternalOutput, DataReadResult
from hopspack.configure import Comparing_Variable, Configure, TargetParameter
from copy import deepcopy
from application import ApplicationProperty
from parameter_set import BiomeBGCParameterSet
from subprocess import call
from draw_graph import BiomeBgcGraphDummy


def read_parameter_data(filename):
    dt = DataReadResult()
    try:
        dt = ReadExternalOutput.read_csv_file(filename, ',')
    except: return None
    return dt

def does_var_exists(csv_filename, variable_name):
    dt = DataReadResult()
    try:
        dt = ReadExternalOutput.read_csv_file(csv_filename, ',')
    except: return None

    ndx = -1
    try: ndx = dt.header_variable.index(variable_name)
    except: pass

    if ndx == -1: return False
    else: return True


def select_paramset(dataset, plot_no, fun=''):
    paramset = []

    pndx, fndx = -1, -1
    try:
        if not fun:
            pndx = dataset.header_variable.index('plot')
            for d in dataset.record_list:
                if d[pndx] == plot_no:
                    paramset = d[pndx + 2:]
                    break
        else:
            pndx = dataset.header_variable.index('plot')
            fndx = dataset.header_variable.index('fun')
            for d in dataset.record_list:
                if d[pndx] == plot_no and d[fndx] == fun:
                    paramset = d[fndx + 1:]
                    break
    except: return []

    return paramset

def collect_parameter_set(solution_type_list, plot_no):
    parameter_set = []

    #for sol in solution_type_list:
    sol = solution_type_list.lower()

    data_filename, fun = '', ''
    if sol == 'hopspack solution':
        data_filename = 'best_paramset.csv'
    elif sol == 'hopspack 2nd best solution':
        data_filename = 'second_best_paramset.csv'
    elif sol == 'hopspack 3rd best solution':
        data_filename = 'third_best_paramset.csv'
    elif sol == 'jochheim et. al., 2011':
        data_filename = 'jochheim_etal_2011_paramset.csv'
    elif sol in ['solution using nse', 'solution using rmse', 'solution using mse', 'solution using r2',
                 'solution using pbias', 'solution using rsr', 'solution using ioa', 'Solution using mape',
                 'Solution using mae']:
        fun = sol.split(' ')[-1].strip()
        data_filename = 'hopspack_solution_set.csv'

    ds = read_parameter_data(os.path.join('hopspack', data_filename))
    parameter_set = select_paramset(ds, plot_no, fun)


    return parameter_set

def find_obs_varname(comparison_var_list, sim_varname, sim_datatype):
    obs_varname_list = []
    obs_filename_list = []

    for cvar in comparison_var_list:
        if cvar.model_file_type == sim_datatype and cvar.model_variable_name == sim_varname:
            obs_varname_list.append(cvar.observation_variable_name)
            obs_filename_list.append(cvar.observation_filename)

    return obs_varname_list, obs_filename_list

def find_obs_datafile(comparison_var_list, datafile_type):
    df = ''
    for cvar in comparison_var_list:
        if cvar.model_file_type.find(datafile_type) > -1:
            df = cvar.observation_filename
            break
    return df

def generate_init_file_version(parameterset_type):
    version_text = ''

    parameterset_type = parameterset_type.lower()
    if parameterset_type == 'hopspack solution':
        version_text = 'hp_bst'
    elif parameterset_type == 'hopspack 2nd best solution':
        version_text = 'hp_bst2nd'
    elif parameterset_type == 'hopspack 3rd best solution':
        version_text = 'hp_bst3rd'
    elif parameterset_type == 'jochheim et. al., 2011':
        version_text = 'jcm2011'
    elif parameterset_type in ['solution using nse', 'solution using rmse', 'solution using mse', 'solution using r2',
                 'solution using pbias', 'solution using rsr', 'solution using ioa', 'Solution using mape',
                 'Solution using mae']:
        fun = parameterset_type.split(' ')[-1].strip()
        version_text = 'hp_sol_' + fun

    return version_text


#'Solution using NSE', 'Solution using RMSE', 'Solution using MSE', 'Solution using R2', 'Solution using PBIAS',
#'Solution using RSR', 'Solution using IOA, 'Solution using MAPE', 'Solution using MAE'

observation_color_list = ['#0000FF', '#01DF01', '#5858FA']
simulation_color_list = ['#FE2E64', '#FA58F4', '#FFBF00', '#A901DB', '#81F7F3', '#0B4C5F', '#A9D0F5', '#E2A9F3', '#848484']
app_path = ApplicationProperty.getScriptPath()

#, 'HOPSPACK Solution', 'HOPSPACK 2nd Best Solution',  'HOPSPACK 3rd Best Solution', 'Jochheim et. al., 2011'
include_list = [ 'HOPSPACK Solution', 'HOPSPACK 2nd Best Solution', 'HOPSPACK 3rd Best Solution', 'Jochheim et. al., 2011']

graph_name_list = ['canopy_evaporation_ann', 'canopy_evaporation_day', 'lai_ann', 'lai_day',
                   'leaf_litterfall', 'stem_litterfall', 'stand_throughfall', 'stem_carbon', 'stem_growth']

plot_list = ['DE0301', 'DE0302', 'DE0303', 'DE0304', 'DE0305', 'DE0307', 'DE0308',
             'DE0901', 'DE0908', 'DE0919', 'DE1201', 'DE1202', 'DE1203', 'DE1204', 'DE1205', 'DE1206',
             'IT0001', 'IT0006', 'IT0008', 'IT0009', 'IT0010', 'IT0012', 'IT0017',
             'SK0206', 'SK0209', 'GR0002','AT0016']
#plot_list = ['DE0301']
for plot in plot_list:
    #plot = plot_list[1]
    #reading the comparison map file required for finding observation variable names
    filename = os.path.join('hopspack', 'comparison', 'comparison_' + plot + '.txt')
    comp_var_list = Comparing_Variable.read_comparing_variables(filename)

    #reading the configuration file required for finding initial filename of the model and model directory
    filename = os.path.join('hopspack', 'config', 'start_value', 'configuration_' + plot + '.txt')
    config = Configure(filename)
    initial_filename = config.initial_filename
    model_directory = ApplicationProperty.get_absolute_path(config.model_directory, os.path.join(app_path, 'hopspack'))

    #running the model
    succeed = False
    if succeed:
        for item in include_list:
            paramset = collect_parameter_set(item, plot)

            target_param_set = []
            TargetParameter.read_parameter_list(os.path.join('hopspack', config.parameterMap_file), target_param_set)
            if target_param_set and paramset:
                if len(target_param_set) == 10: paramset = paramset[1:]
                if len(target_param_set) == len(paramset):
                    for i in range(len(target_param_set)):
                        tp = target_param_set[i]
                        tp.current_value = paramset[i]
                else: succeed = False
            else: succeed = False

            bgc_parameter_set = BiomeBGCParameterSet.ReadBBGCParameterSet(model_directory, config.initial_filename)

            version_text = generate_init_file_version(item)
            if bgc_parameter_set is not None:
                if bgc_parameter_set.vegParam is not None:
                    if len(bgc_parameter_set.vegParam) == 1:
                        site_index = bgc_parameter_set.vegParam[0]["siteIndex"]
                        veg_id = bgc_parameter_set.vegParam[0]["vegid"]

                        for hp_param in target_param_set:
                            bgc_parameter_set.updateEpcObject(site_index, veg_id, -1, hp_param.name, hp_param.current_value,
                                                                version_text)

                bgc_parameter_set.initParam.output_file_prefix += version_text
                initial_filename = config.initial_filename.replace('.ini', '_' + version_text + '.ini')
                BiomeBGCParameterSet.save_parameter_set(bgc_parameter_set, model_directory, initial_filename, version_text)

                #step-4: run bgc
                print('running model with ' + initial_filename + '...')
                call(os.path.join(model_directory, "bgc_zalf.sh") + " " + initial_filename + " y", shell=True)
            else: succeed = False

    succeed = True
    if succeed:
        for graph_name in graph_name_list:
            #graph_name = graph_name_list[0]
            if graph_name in ['canopy_evaporation_ann', 'canopy_evaporation_day', 'lai_ann', 'lai_day', 'leaf_litterfall', 'stem_litterfall',
                              'stand_cumulative_precipitation', 'stand_throughfall', 'stem_carbon', 'stem_growth']:
                template_filename = os.path.join('graphs', 'sample_template', graph_name + '.txt')
                gtmp = ModelGraph.read_graph_template(template_filename)

                #x. creating original graph object from template
                grp = deepcopy(gtmp)

                #x. find the observation variable names
                for i in range(len(gtmp.list_of_plot)):
                    p = gtmp.list_of_plot[i]
                    sim_series, obs_series = None, None

                    for s in p.list_of_series:              #template plots must contain only one observation series and one simulated series
                        if s.data_source.source_type == 0: sim_series = deepcopy(s)
                        elif s.data_source.source_type == 1: obs_series = deepcopy(s)

                    new_data_series_list = []

                    if sim_series and obs_series:
                        sim_varname = obs_series.attribute_name
                        sim_datatype = obs_series.data_source.output_file_type

                        #copy simulated data series, modify values and adding them to the new series list
                        for j in range(len(include_list)):
                            item = include_list[j]
                            series_title = sim_series.series_title + ' (' + item + ')'
                            version_text = generate_init_file_version(item)
                            init_file = config.initial_filename.replace('.ini', '_' + version_text + '.ini')
                            if item.lower().find('jochheim') > -1:
                                html_colcode = '#000000'
                            else: html_colcode = simulation_color_list[j%len(simulation_color_list)]

                            s = deepcopy(sim_series)
                            s.series_title = series_title
                            s.data_source.initial_filename = init_file
                            s.data_source.model_directory = model_directory
                            try: s.edit_feature.color = html_colcode
                            except: pass

                            new_data_series_list.append(s)

                        #copy the observation data series and modify values of the new data series
                        obs_var_list, obs_file_list = find_obs_varname(comp_var_list, sim_series.attribute_name, sim_series.data_source.output_file_type)

                        if obs_var_list and obs_file_list and len(obs_var_list) == len(obs_file_list):
                            for j in range(len(obs_var_list)):
                                html_colcode = observation_color_list[j%len(observation_color_list)] #only 3 colours has been assigned for observation
                                data_filename = ApplicationProperty.get_absolute_path(obs_file_list[j],
                                                                                      os.path.join(app_path, 'hopspack'))
                                obs_variable = obs_var_list[j]

                                s = deepcopy(obs_series)
                                s.data_source.data_filename_csv = data_filename
                                s.attribute_name = obs_variable
                                if obs_variable.find('dw_vTI') > -1: s.series_title += ', dw vTI'
                                elif obs_variable.find('dd_vTI') > -1: s.series_title += ', dd vTI'
                                elif obs_variable.find('vTI')> -1: s.series_title += ', vTI'
                                elif obs_variable.find('dw') > -1: s.series_title += ', dw'
                                elif obs_variable.find('dd') > -1: s.series_title += ', dd'

                                try: s.edit_feature.color = html_colcode
                                except: pass

                                new_data_series_list.append(s)

                        elif len(obs_var_list)==len(obs_file_list)==0:
                            data_filetype = 'day'
                            if obs_series.data_source.data_filename_csv.find('ann') > -1: data_filetype = 'ann'
                            data_file = find_obs_datafile(comp_var_list, data_filetype)
                            data_file = ApplicationProperty.get_absolute_path(data_file, os.path.join(app_path, 'hopspack'))
                            if os.path.exists(data_file):
                                if does_var_exists(data_file, obs_series.attribute_name):
                                    s = deepcopy(obs_series)
                                    s.data_source.data_filename_csv = data_file
                                    new_data_series_list.append(s)

                    #add the new series list to the graph plot
                    grp.list_of_plot[i].list_of_series = new_data_series_list


                filename = os.path.join('graphs', plot)
                os.makedirs(filename, mode=0o777, exist_ok=True)
                filename = os.path.join(filename, graph_name + '.txt')
                ModelGraph.write_graph_template(grp, filename)
                # ModelGraph.read_data_from_source_file(grp)
                # BiomeBgcGraphDummy.ShowGraph(grp, 1)

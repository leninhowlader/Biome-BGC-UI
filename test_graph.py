import os
from graph import ModelGraph, ModelPlot, DataSource, DataSeries
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
simulation_color_list = ['#F7D358', '#F7FE2E', '#FA58F4', '#A901DB', '#81F7F3', '#0B4C5F', '#A9D0F5', '#E2A9F3', '#848484']
app_path = ApplicationProperty.getScriptPath()

#, 'HOPSPACK Solution', 'HOPSPACK 2nd Best Solution',  'HOPSPACK 3rd Best Solution', 'Jochheim et. al., 2011'
include_list = [ 'HOPSPACK Solution', 'HOPSPACK 2nd Best Solution', 'HOPSPACK 3rd Best Solution', 'Jochheim et. al., 2011']

graph_name_list = ['canopy_evaporation_ann', 'canopy_evaporation_day', 'lai_ann', 'lai_day',
                   'leaf_litterfall', 'stem_litterfall', 'stand_throughfall', 'stem_carbon', 'stem_growth']
#graph_name_list = ['canopy_evaporation_day']
#
# plot_list = ['DE0301', 'DE0302', 'DE0303', 'DE0304', 'DE0305', 'DE0307', 'DE0308',
#              'DE0901', 'DE0908', 'DE0919', 'DE1201', 'DE1202', 'DE1203', 'DE1204', 'DE1205', 'DE1206',
#              'IT0001', 'IT0006', 'IT0008', 'IT0009', 'IT0010', 'IT0012', 'IT0017',
#              'SK0206', 'SK0209', 'GR0002','AT0016']
plot_list = ['DE1202', 'DE1203', 'DE1204', 'DE1205', 'DE1206']
for plot in plot_list:
    print(plot)
    for graph_name in graph_name_list:
        print('\t'+graph_name)
        #graph_name = graph_name_list[0]
        if graph_name in ['canopy_evaporation_ann', 'canopy_evaporation_day', 'lai_ann', 'lai_day', 'leaf_litterfall', 'stem_litterfall',
                          'stand_cumulative_precipitation', 'stand_throughfall', 'stem_carbon', 'stem_growth']:
            template_filename = os.path.join('graphs', plot, graph_name + '.txt')
            grp = ModelGraph.read_graph_template(template_filename)

            ModelGraph.read_data_from_source_file(grp)
            for p in grp.list_of_plot: p.calculate_axes_limit()
            #ModelGraph.write_graph_template(grp, template_filename)
            try: BiomeBgcGraphDummy.ShowGraph(grp, 1)
            except: pass

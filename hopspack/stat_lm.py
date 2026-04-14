#modified on: 13-Nov-2014

import numpy as np
import sys, os
sys.path.append('..')
from read_output import ReadBinaryOutput, ReadExternalOutput

class readdata:
    @staticmethod
    def read_external_data(datafilename):
        observ_output = None

        if os.path.exists(datafilename): observ_output = ReadExternalOutput.read_csv_file(datafilename, ",", True)

        return observ_output

    @staticmethod
    def read_model_data(model_directory, file_type, in_initial_filename):
        model_output = None

        if os.path.exists(model_directory): model_output = ReadBinaryOutput.ReadModelOutput(model_directory, in_initial_filename, file_type, True, True, True)

        return model_output

class stat:
    fun_list = ['Root Mean Square Error', 'Coefficient of Determination', 'Absolute Average Deviation',
                    'Index of Agreement', 'Mean Absolute Error', 'Mean Square Error', 'Percentage Bias',
                    'RMSE-Observed Stdv. Ratio', 'Nash-Sutcliffe Efficiency']

    @staticmethod
    def root_mean_square_error(sim, obs):
        return np.sqrt(np.mean((obs - sim) ** 2))

    @staticmethod
    def coefficient_of_determination(sim, obs):
        obs_mean = np.mean(obs)
        return  1 - (np.sum((sim-obs)**2)/np.sum((obs-obs_mean)**2))

    @staticmethod
    def coefficient_of_determination2(sim, obs):
        obs_mean = np.mean(obs)
        sim_mean = np.mean(sim)

        r2 = (np.sum((obs - obs_mean)*(sim-sim_mean)))**2/(np.sum((obs-obs_mean)**2)*(np.sum((sim-sim_mean)**2)))

        return r2

    @staticmethod
    def mean_square_error(sim, obs):
        return np.mean((sim - obs) ** 2)

    @staticmethod
    def absolute_average_deviation(sim, obs):
        return np.mean(abs(sim-obs)/obs)*100

    @staticmethod
    def index_of_agreement(sim, obs):
        pe = stat.potential_error(sim, obs)

        if pe != 0: return 1-(np.sum((sim-obs)**2)/pe)
        else: return None

    @staticmethod
    def nash_sutcliffe_efficiency(sim, obs):
        obs_mean = np.mean(obs)
        return 1 - (np.sum((obs-sim)**2)/np.sum((obs-obs_mean)**2))

    @staticmethod
    def mean_absolute_error(sim, obs):
        return np.mean(abs(sim-obs))

    @staticmethod
    def potential_error(sim, obs):
        obs_mean = np.mean(obs)
        return np.sum((abs(sim-obs_mean)+abs(obs-obs_mean))**2)

    @staticmethod
    def percentage_bias(sim, obs):
        return abs(np.sum(obs-sim)*100/np.sum(obs))

    @staticmethod
    def rmse_stdv_ratio(sim, obs):
        rmse = stat.root_mean_square_error(sim, obs)
        return rmse/np.std(obs)

    @staticmethod
    def objective_function(fun_name, sim, obs, normalize_by_obs_max=False, normalize_by_obs_mean=False):
        result = 0
        sim = np.array(sim)
        obs = np.array(obs)
        if fun_name == 'Root Mean Square Error':
            if normalize_by_obs_max or normalize_by_obs_mean:
                sim, obs = stat.normalize_data(sim, obs, normalize_by_obs_max, normalize_by_obs_mean)
            result = stat.root_mean_square_error(sim, obs)
        elif fun_name == 'Coefficient of Determination':
            result = stat.coefficient_of_determination2(sim, obs)
        elif fun_name == 'Absolute Average Deviation':
            if normalize_by_obs_max or normalize_by_obs_mean:
                sim, obs = stat.normalize_data(sim, obs, normalize_by_obs_max, normalize_by_obs_mean)
            result = stat.absolute_average_deviation(sim, obs)
        elif fun_name == 'Index of Agreement':
            result = stat.index_of_agreement(sim, obs)
        elif fun_name == 'Mean Absolute Error':
            if normalize_by_obs_max or normalize_by_obs_mean:
                sim, obs = stat.normalize_data(sim, obs, normalize_by_obs_max, normalize_by_obs_mean)
            result = stat.mean_absolute_error(sim, obs)
        elif fun_name == 'Mean Square Error':
            if normalize_by_obs_max or normalize_by_obs_mean:
                sim, obs = stat.normalize_data(sim, obs, normalize_by_obs_max, normalize_by_obs_mean)
            result = stat.mean_square_error(sim, obs)
        elif fun_name == 'Percentage Bias':
            result = stat.percentage_bias(sim, obs)
        elif fun_name == 'RMSE-Observed Stdv. Ratio':
            result = stat.rmse_stdv_ratio(sim, obs)
        elif fun_name == 'Nash-Sutcliffe Efficiency':
            result = stat.nash_sutcliffe_efficiency(sim, obs)
        return result

    @staticmethod
    def normalize_data(sim, obs, by_max=True, by_mean=False):
        norm_value = None
        if by_max: norm_value = np.max(obs)
        elif by_mean: norm_value = np.mean(obs)

        if norm_value:
            sim = sim / norm_value
            obs = obs / norm_value

        return sim, obs

    @staticmethod
    def pairing_variables(first_value_list, first_key_list, second_value_list, second_key_list):

        a = np.array(first_key_list)
        b = np.array(first_value_list)

        p = np.array(second_key_list)
        q = np.array(second_value_list)

        for i in reversed(range(len(first_value_list))): first_value_list.pop(i)
        for i in reversed(range(len(first_key_list))): first_key_list.pop(i)
        for i in reversed(range(len(second_value_list))): second_value_list.pop(i)
        for i in reversed(range(len(second_key_list))): second_key_list.pop(i)

        ndx = a.argsort()
        a = a[ndx]
        b = b[ndx]

        ndx = p.argsort()
        p = p[ndx]
        q = q[ndx]

        i = 0
        j = 0
        while i < len(a) and j < len(p):
            if a[i] == p[j]:
                if b[i] and q[j]:
                    first_value_list.append(b[i])
                    second_value_list.append(q[j])
                i += 1
                j += 1
            elif a[i] > p[j]:
                while j < len(p) and p[j] < a[i]: j += 1
            else:
                while i < len(a) and a[i] < p[j]: i += 1

    @staticmethod
    def data_evaluation(bgc_directory, bgc_init_filename, comparison_list, normby_obsmax=False, normby_obsmean=False,
                        model_output_dic=None, observ_data_dic=None, ob_file_list=None):
        group_list = []
        group_result = []

        #initializing group list and group result
        for comparison in comparison_list:
            if comparison.group not in group_list:
                group_list.append(comparison.group)
                group_result.append(0)

        try:
            if len(comparison_list) > 0:
                #step-1: collect all required data. (dictionary structure = {'file_type': model_output, 'file_type2': model_output2})
                if (model_output_dic==None) or (observ_data_dic==None) or (ob_file_list==None):
                    model_output_dic, observ_data_dic, ob_file_list = stat.collection_of_data(bgc_directory, bgc_init_filename, comparison_list)

                for comparison in comparison_list:
                    r = 0

                    bgc_output = model_output_dic[comparison.output_file_type]
                    observed_dataset = observ_data_dic[ob_file_list.index(comparison.observation_data_file)]

                    #step-2: from collection (of data) select data for required variables
                    sim, obs = stat.comparison_specific_data_processing(comparison, bgc_output, observed_dataset)
                    #step-3: calculate output of objective function

                    if sim and obs:
                        r = stat.objective_function(comparison.cost_function, sim, obs, normby_obsmax, normby_obsmean)
                        if comparison.weighing_factor not in [0, 1]: r *= comparison.weighing_factor

                        ndx = group_list.index(comparison.group)
                        group_result[ndx] += r
                        
                    else: raise Exception
        except Exception as ex:
            for i in range(len(group_list)): group_result[i] = 'DNE'

        return group_result

    @staticmethod
    def collection_of_data(bgc_directory, bgc_init_filename, comparison_list):
        model_output_dic = {} #structure = {'file_type': model_output, 'file_type2': model_output2}
        observ_data_dic = {} #structure = do
        ob_file_list = []

        for rule in comparison_list:
            file_type = rule.output_file_type
            observ_dfile = rule.observation_data_file

            if file_type not in model_output_dic.keys():
                model_output = readdata.read_model_data(bgc_directory, file_type, bgc_init_filename)
                if model_output is not None: model_output_dic[file_type] = model_output
            if observ_dfile not in ob_file_list:
                observ_data = readdata.read_external_data(observ_dfile)

                if observ_data is not None:
                    ob_file_list.append(observ_dfile)
                    observ_data_dic[ob_file_list.index(observ_dfile)] = observ_data

        return model_output_dic, observ_data_dic, ob_file_list

    @staticmethod
    def comparison_specific_data_processing(comparison, bgc_output, observed_data):
        sim, obs, psim, pobs = [], [], [], []

        #step-1: from dataset read specific columns (variables); some variable needs specific pre-processing steps
        if comparison.pairing_model_variable: psim = ReadBinaryOutput.ExtractColumnRecord(comparison.pairing_model_variable, bgc_output.header_variable, bgc_output.record_list)
        if comparison.pairing_observation_variable: pobs = ReadBinaryOutput.ExtractColumnRecord(comparison.pairing_observation_variable, observed_data.header_variable, observed_data.record_list)

        if comparison.output_variable_name in ['cf_site_hr_rr']:
            cf_site_hr = ReadBinaryOutput.ExtractColumnRecord('cf_site_hr', bgc_output.header_variable, bgc_output.record_list)
            cf_site_rr = ReadBinaryOutput.ExtractColumnRecord('cf_site_rr', bgc_output.header_variable, bgc_output.record_list)
            sim = (np.array(cf_site_hr) + np.array(cf_site_rr)).tolist()
            obs = ReadBinaryOutput.ExtractColumnRecord(comparison.observation_variable_name, observed_data.header_variable, observed_data.record_list)
            comparison.pairing_flag = True
        elif comparison.output_variable_name in ['epv_vegt_proj_lai']:
            sim = ReadBinaryOutput.ExtractColumnRecord(comparison.output_variable_name, bgc_output.header_variable, bgc_output.record_list)
            obs = ReadBinaryOutput.ExtractColumnRecord(comparison.observation_variable_name, observed_data.header_variable, observed_data.record_list)
            sim_year = ReadBinaryOutput.ExtractColumnRecord('year', bgc_output.header_variable, bgc_output.record_list)
            obs_year = ReadBinaryOutput.ExtractColumnRecord('year', observed_data.header_variable, observed_data.record_list)

            #if year column is not available
            if not obs_year:
                obs_date = ReadBinaryOutput.ExtractColumnRecord('date', observed_data.header_variable, observed_data.record_list)
                for d in obs_date: obs_year.append(d.year)

            sim, psim, obs, pobs = stat.sm_leaf_area_index(sim, sim_year, obs, obs_year)
            comparison.pairing_flag = True
        #Following elif condition in needed to process observed data if it is a cumulative daily variable
        #but its counterpart is a simulated monthly average variable
        elif comparison.output_file_type.lower().find('monavg') >= 0 and comparison.observation_variable_name.lower().find('cum') >= 0:
            sim = ReadBinaryOutput.ExtractColumnRecord(comparison.output_variable_name, bgc_output.header_variable, bgc_output.record_list)
            obs = ReadBinaryOutput.ExtractColumnRecord(comparison.observation_variable_name, observed_data.header_variable, observed_data.record_list)

            obs_date = ReadBinaryOutput.ExtractColumnRecord('date', observed_data.header_variable, observed_data.record_list)
            obs, pobs = stat.daily_cumulative_to_monthly_averages(obs, obs_date)

            #year-month from simulation data
            year = ReadBinaryOutput.ExtractColumnRecord('year', bgc_output.header_variable, bgc_output.record_list)
            month = ReadBinaryOutput.ExtractColumnRecord('month_str', bgc_output.header_variable, bgc_output.record_list)
            psim = stat.year_month(year, month)
            comparison.pairing_flag = True
        else:
            sim = ReadBinaryOutput.ExtractColumnRecord(comparison.output_variable_name, bgc_output.header_variable, bgc_output.record_list)
            obs = ReadBinaryOutput.ExtractColumnRecord(comparison.observation_variable_name, observed_data.header_variable, observed_data.record_list)

        #step-2: process data for comparison
        pair_flag = comparison.pairing_flag
        if pair_flag: stat.pairing_variables(sim, psim, obs, pobs)



        return sim, obs

    @staticmethod
    def sm_leaf_area_index(sim, sim_year, obs, obs_year):
        #special method for leaf area index

        #step-1: filter sim, along with its corresponding year, for non-zero values
        ReadBinaryOutput.Filter([sim, sim_year], 0, '>', 0)
        #step-2: apply group by function for simulation data (group sim by sim_year)
        sp, s = ReadBinaryOutput.GroupingVariableValue(sim, [sim_year], 'average')

        #step-3: apply group by function observation data (group obs by obs_year)
        op, o = ReadBinaryOutput.GroupingVariableValue(obs, [obs_year], 'average')

        return s, sp, o, op

    @staticmethod
    def daily_cumulative_to_monthly_averages(cum_data, date):
        if len(cum_data) == len(date):
            #step-1: removing Null values
            for i in reversed(range(len(cum_data))):
                if cum_data[i] == None or date[i] == None:
                    cum_data.pop(i)
                    date.pop(i)

            cum_data = np.array(cum_data)
            date = np.array(date)

            #step-2: sort observation data according to date
            ndx = date.argsort()
            date = date[ndx]
            cum_data = cum_data[ndx]

            #step-3: extract month and year from date
            month = []
            year =[]
            for d in date:
                month.append(d.month)
                year.append(d.year)

            #step-4: extract daily data (i.e., increment in each step) from cumulative data for individual year
            distinct_year = np.unique(year)
            dlen = len(year)
            for i in range(len(distinct_year)):
                ndx_strt = year.index(distinct_year[i])
                ndx_end = -1
                if i < len(distinct_year) - 1: ndx_end = year.index(distinct_year[i+1])
                else: ndx_end = dlen

                for i in reversed(range(ndx_strt + 1, ndx_end)):
                    cum_data[i] -= cum_data[i-1]

            #step-5: split data according to year and month
            data_yr_mon = []    #structure [[[data for Jan],[data for Feb], ...],[],]
            yr_mon = []         #contains year-month

            for i in range(len(distinct_year)):
                data_yr = []
                ndx_strt = year.index(distinct_year[i])
                ndx_end = -1
                if i < len(distinct_year) - 1: ndx_end = year.index(distinct_year[i+1])
                else: ndx_end = dlen

                j = ndx_strt
                m = -1
                data_mn = []
                ym = ''
                while j < ndx_end:
                    if m == month[j]:
                        data_mn.append(cum_data[j])
                        j += 1
                    else:
                        if data_mn:
                            data_yr.append(data_mn)
                            yr_mon.append(ym)
                        ym = str(distinct_year[i]) + '-' + str(month[j]).rjust(2, '0')
                        data_mn = []
                        m = month[j]
                if data_mn:
                    data_yr.append(data_mn)
                    yr_mon.append(ym)

                data_yr_mon.append(data_yr)

            #step-6: calculate average for each month
            avg_list = []
            for data_yr in data_yr_mon:
                for data_mn in data_yr:
                    avg_list.append(np.mean(data_mn))

            return avg_list, yr_mon
        else: return [],[]

    @staticmethod
    def year_month(year, month):
        yr_mn = []
        if len(year) == len(month):
            for i in range(len(year)):
                yr_mn.append(str(year[i]) + '-' + str(month[i]).rjust(2,'0'))
        return yr_mn

    @staticmethod
    def calculate_statistics_all(bgc_directory, bgc_initial_filename, comparison_list, normby_obsmax=False, normby_obsmean=False):
        result =  []
        if len(comparison_list) > 0:
            try:
                #step-1: collect all required data. (dictionary structure = {'file_type': model_output, 'file_type2': model_output2})
                model_output_dic, observ_data_dic, ob_file_list = stat.collection_of_data(bgc_directory, bgc_initial_filename, comparison_list)

                for comparison in comparison_list:
                    bgc_output = model_output_dic[comparison.output_file_type]
                    observed_dataset = observ_data_dic[ob_file_list.index(comparison.observation_data_file)]

                    #step-2: from collection (of data) select data for required variables
                    sim, obs = stat.comparison_specific_data_processing(comparison, bgc_output, observed_dataset)

                    #step-3: calculate output of all objective functions
                    r = []
                    for fun in stat.fun_list:
                        f = 'None'
                        try:
                            f = stat.objective_function(fun, sim, obs, normby_obsmax, normby_obsmean)
                            if comparison.weighing_factor not in [0, 1]: f *= comparison.weighing_factor
                            if f == 'DNE': f = 'None'
                        except Exception as ex: f = 'None'
                        r.append(f)
                    result.append(r)
            except Exception as ex:
                return None, None, None
        return stat.fun_list, result

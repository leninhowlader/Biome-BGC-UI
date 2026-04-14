#!/usr/bin/python

import random, sys, os
sys.path.append('..')
from hopspack.configure import OptimizationProblem, Configure, TargetParameter, HopspackCitizen

def random_seq(no_of_paramter, no_of_trail):
    if no_of_trail <= 0: no_of_trail = 1

    seq_list = []
    for i in range(no_of_trail):
        temp = []

        while True:
            for j in range(no_of_paramter):
                while True:
                    random.seed()
                    x = random.randint(0, no_of_paramter - 1)
                    if x not in temp:
                        temp.append(x)
                        break

            if temp not in seq_list:
                seq_list.append(temp)
                break

    return seq_list

def write_seq_list(filename, sequence_list):
    file = None
    try:
        file = open(filename, 'w')
        for i in range(len(sequence_list)):
            seq = sequence_list[i]
            l = str(i + 1)
            for s in seq: l += ';' + str(s)
            file.write(l + '\n')
    except: return False
    finally:
        try: file.close()
        except: pass

    return True

def find_upper_bound(parameter_list):
    upper_bound = []
    for param in parameter_list: upper_bound.append(param.hard_upper_bound)
    return upper_bound

def find_lower_bound(parameter_list):
    lower_bound = []
    for param in parameter_list: lower_bound.append(param.hard_lower_bound)
    return lower_bound

def find_initial_value(parameter_list):
    initial_value = []
    for param in parameter_list: initial_value.append(param.starting_value)
    return initial_value

def change_parameter_sequence(seq, parameter_list):
    temp = []
    for s in seq: temp.append(parameter_list[s])
    return temp

def main(argv):
    if len(argv) < 3: exit("usage: %s <Plot Number> <No. of Trials> <Output Filename>" % argv[0])

    plot_no = argv[1].strip()
    if len(plot_no) == 0: exit('Please provide arguments in proper order and format.')

    trial_count = 0
    try: trial_count = int(argv[2])
    except: exit('Please provide arguments in proper order and format.')
    if trial_count == 0: exit('No. of trials cannot be zero')

    output_filename = ''
    try: output_filename = argv[3]
    except: pass
    if len(output_filename) == 0: output_filename = 'sequence_list_' + plot_no + '.txt'

    #reading configuration file
    filename = 'config/configuration_' + plot_no + '.txt'
    config = None
    if os.path.exists(filename): config = Configure(filename)
    else: exit('Configuration file not found!')

    #reading parameter file
    param_list = []
    if os.path.exists(config.parameterMap_file): TargetParameter.read_parameter_list(config.parameterMap_file, param_list)
    else: exit('Parameter file is not found!')

    param_count = len(param_list)
    if param_count == 0: exit('Parameter file is empty or is not properly formatted!')


    fun_list = ['rmse', 'r2', 'aad', 'ioa', 'mae', 'pbias', 'rsr', 'nse', 'mse']

    seq_list = random_seq(param_count, trial_count * len(fun_list))
    write_seq_list(output_filename, seq_list)

    seq_count = 0
    comparison_file = config.comparisonMap_file
    for fun in fun_list:
        if fun == 'rmse': config.objective_function = 'Root Mean Square Error'
        elif fun == 'r2': config.objective_function = 'Coefficient of Determination'
        elif fun == 'aad': config.objective_function = 'Absolute Average Deviation'
        elif fun == 'ioa': config.objective_function == 'Index of Agreement'
        elif fun == 'mae': config.objective_function = 'Mean Absolute Error'
        elif fun == 'mse': config.objective_function = 'Mean Square Error'
        elif fun == 'pbias': config.objective_function = 'Percentage Bias'
        elif fun == 'rsr': config.objective_function = 'RMSE-Observed Stdv. Ratio'
        elif fun == 'nse': config.objective_function = 'Nash-Sutcliffe Efficiency'
        if fun in ['nse', 'r2', 'rsr']: config.comparisonMap_file = comparison_file[:-4] + '_nse_rsr_r2.txt'
        config.extension_postfix = plot_no[-4:] + fun

        objective = ''
        if fun in ['ioa', 'nse', 'r2']: objective = 'Maximize'
        else: objective = 'Minimize'

        prob = OptimizationProblem()
        prob.citizen_list.append(HopspackCitizen())
        prob.no_of_parameters = param_count
        prob.optimization_objective = objective
        prob.executable_name = './evaluator_seqt.py'
        prob.input_prefix = fun + '_in'
        prob.output_prefix = fun + '_out'
        prob.processor_count = 41
        prob.thread_count = 41
        for i in range(trial_count):
            #update and save saving config file
            seq = seq_list[seq_count]

            filename = plot_no + '_' + fun + '_' + str(i + 1) + '.txt'
            config.parameter_sequence = seq

            config.solution_file = 'output/seqtest/' + filename



            config.write_configuration_file('config/seqtest/' + filename)

            #change parameter sequence in parameter list
            param_list = change_parameter_sequence(seq, param_list)

            #update and save problem definition
            prob.upper_bound = find_upper_bound(param_list)
            prob.lower_bound = find_lower_bound(param_list)
            prob.initial_value = find_initial_value(param_list)
            prob.solution_filename = config.solution_file

            prob.write_problem_definition_file('definition/seqtest/' + filename)

            seq_count += 1


    #writing definition files


main(sys.argv)
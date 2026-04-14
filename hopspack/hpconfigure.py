#modified on: 23-10-2014

import os
import numpy as np

class comparison_policy:
    cost_function = ''
    def __init__(self):
        self.output_file_type = ""
        self.output_variable_name = ""
        self.observation_data_type = 1  #0 = Model Output, 1 = Observation Data
        self.observation_data_file = ""
        self.observation_variable_name = ""
        self.pairing_flag = True
        self.pairing_model_variable = ""
        self.pairing_observation_variable = ""
        self.model_data_conversion_factor = 1
        self.observation_data_conversion_factor = 1
        self.weighing_factor = 1
        #self.cost_function = ""
        self.group = ''

    def set_cost_function(self, cost_function):
        comparison_policy.cost_function = cost_function

    def is_complete(self):
        if len(self.output_file_type) == 0 or len(self.output_variable_name) == 0 or len(self.observation_data_file) == 0 or len(self.observation_variable_name) == 0: return False
        elif self.pairing_flag and (len(self.pairing_model_variable) == 0 or len(self.pairing_observation_variable) == 0 ): return False
        elif len(self.cost_function) == 0: return False
        elif len(self.group) == 0: return False
        else: return True

    @staticmethod
    def read_policy(policy_file_name):
        policy_list = []

        pfile = None
        if os.path.exists(policy_file_name):
            try:
                pfile = open(policy_file_name, 'r')

                policy = None

                block_start = False

                for line in pfile.readlines():
                    temp = line.strip().strip('\n').strip('\t')

                    if temp:
                        if not block_start and temp == '@':
                            policy = comparison_policy()
                            block_start = True
                        elif block_start and temp == '@@':
                            if policy is not None:
                                if policy.is_complete():
                                    policy_list.append(policy)
                                    policy = None
                                    block_start = False
                        else:
                            if block_start:
                                temp = temp.split('=')
                                if temp and len(temp) >= 2:
                                    arg = temp[0].strip()
                                    val = temp[1].strip()

                                    if len(arg) > 0 and len(val) > 0:
                                        temp = arg.lower()
                                        if temp in ["output file type"]: policy.output_file_type = val
                                        elif temp in ["output variable name"]: policy.output_variable_name = val
                                        elif temp in ["observation data type"]: policy.observation_data_type = int(val)
                                        elif temp in ["observation data file"]: policy.observation_data_file = val
                                        elif temp in ["observation variable"]: policy.observation_variable_name = val
                                        elif temp in ["pair flag"]:
                                            if val.lower() in ['true', 't', '1']: policy.pairing_flag = True
                                            else: policy.pairing_flag = False
                                        elif temp in ["pairing variable [model]"]: policy.pairing_model_variable = val
                                        elif temp in ["pairing variable [observation]"]: policy.pairing_observation_variable = val
                                        elif temp in ["conversion factor [model]"]:
                                            try:
                                                policy.model_data_conversion_factor = float(val)
                                                if policy.model_data_conversion_factor == 0: policy.model_data_conversion_factor = 1.0
                                            except: policy.model_data_conversion_factor = 1.0
                                        elif temp in ["conversion factor [observation]"]:
                                            try:
                                                policy.observation_data_conversion_factor = float(val)
                                                if policy.observation_data_conversion_factor == 0: policy.observation_data_conversion_factor = 1.0
                                            except: policy.observation_data_conversion_factor = 1.0
                                        elif temp in ["weighing factor"]:
                                            try:
                                                policy.weighing_factor = float(val)
                                                if policy.weighing_factor == 0: policy.weighing_factor = 1.0
                                            except: policy.weighing_factor = 1.0
                                        #elif temp in ['cost function']: Comparing_Variable.cost_function = val
                                        elif temp.lower() in ['group']: policy.group = val

            except Exception as ex:
                return None
            finally:
                try: pfile.close()
                except: pass
        return policy_list

    @staticmethod
    def write_policy_file(list_of_policy, policy_file_name):
        if list_of_policy and policy_file_name:
            pf = None
            try:
                pf = open(policy_file_name, 'w')
                text_line = "This file specifies the variables that will be used for comparing model output with " \
                            "observation data. Each block of definition start with '@' and ends with double '@' (@@) " \
                            "(please note that no other text is allowed on the same line with @ and @@ except white " \
                            "spaces). Four arguments are mandatory for each block: model output file type, output " \
                            "variable name, observation data file and variable. (Observation data file must be in " \
                            "CSV format). In addition to these arguments, there are other optional arguments for specific tasks.\n"
                pf.write(text_line)

                text_line = "If \"pair flag\" is set true, the model data and observation data will be paired using " \
                            "specified pairing fields. Otherwise, a positional comparison of model output and " \
                            "observation will be perfored. The null values will not be used in either cases. " \
                            "Data (model output or observation) can be manipulated using conversion factors.\n"
                pf.write(text_line)

                text_line = "If more than one comparing block is used, the effect will be additive not multiplicative." \
                            " In that case a weighing factor can be used.\n"
                pf.write(text_line)

                text_line = "Cost function defines which method should be applied during data comparison. Cost function defines " \
                            "which method should be applied during data comparison. Cost function should be defined only once, in " \
                            "case of multiple declaration, the last one will be taken.\n"
                pf.write(text_line)

                for policy in list_of_policy:
                    if policy.is_complete():
                        pf.write("@\n")
                        pf.write("output file type = " + policy.output_file_type + "\n")
                        pf.write("output variable name = " + policy.output_variable_name + "\n")
                        pf.write("observation data type = " + str(policy.observation_data_type) + "\n")
                        pf.write("observation data file = " + policy.observation_data_file + "\n")
                        pf.write("observation variable = " + policy.observation_variable_name + "\n")
                        pf.write("pair flag = " + str(policy.pairing_flag) + "\n")
                        pf.write("pairing variable [model] = " + policy.pairing_model_variable + "\n")
                        pf.write("pairing variable [observation] = " + policy.pairing_observation_variable + "\n")
                        pf.write("conversion factor [model] = " + str(policy.model_data_conversion_factor) + "\n")
                        pf.write("conversion factor [observation] = " + str(policy.observation_data_conversion_factor) + "\n")
                        pf.write("weighing factor = " + str(policy.weighing_factor) + "\n")
                        #pf.write("cost function = " + str(Comparing_Variable.cost_function) + "\n")
                        pf.write("@@\n")
            except: return False
            finally:
                try: pf.close()
                except: pass
            return True
        else: return False

class parameter:
    def __init__(self):
        self.parameter_name = ""
        self.current_value = None
        self.upper_bound = None
        self.lower_bound = None
        self.starting_value = None
        self.hard_upper_bound = None
        self.hard_lower_bound = None

    def is_complete(self):
        if self.parameter_name and (self.upper_bound != None) and (self.lower_bound != None) and (self.starting_value != None): return True
        else: return False

    @staticmethod
    def read_parameter_list(parameter_file_name, parameter_list_out):
        if os.path.exists(parameter_file_name):
            pf = None
            try:
                pf = open(parameter_file_name, 'r')

                param = None
                block_start = False
                for line in pf.readlines():
                    temp = line.strip().strip('\n').strip('\t')

                    if not block_start and temp == '@PARAMETER':
                        param = parameter()
                        block_start = True
                    elif block_start and temp == '@@':
                        if param is not None:
                            if param.is_complete():
                                parameter_list_out.append(param)
                                param = None
                                block_start = False
                    else:
                        if block_start:
                            temp = temp.split(':')
                            arg = temp[0].strip()
                            val = temp[1].strip()

                            if len(arg) > 0 and len(val) > 0:
                                temp = arg.lower()
                                if temp in ["parameter name"]: param.parameter_name = val
                                elif temp in ["upper bound"]: param.upper_bound = float(val)
                                elif temp in ["lower bound"]: param.lower_bound = float(val)
                                elif temp in ["starting value"]: param.starting_value = float(val)
                                elif temp in ['hard upper bound']: param.hard_upper_bound = float(val)
                                elif temp in ['hard lower bound']: param.hard_lower_bound = float(val)
            except: return False
            finally:
                try: pf.close()
                except: pass
            return True
        else: return False

    @staticmethod
    def write_parameter_file(list_of_parameter, parameter_file_name):
        if list_of_parameter and parameter_file_name:
            pf = None
            try:
                pf = open(parameter_file_name, 'w')

                text_line = "This file contains the list of parameters to be used in parameterization process. "
                text_line += "Each parameter starts with a key word @PARAMETER and ends with @@ and each parameter "
                text_line += "has four attributes (name, upper and lower bounds, and starting value). The names must "
                text_line += "comply with the names used in interface module (..interface/paramdomain/epc.prm).\n"
                pf.write(text_line)

                for param in list_of_parameter:
                    if param.is_complete():
                        pf.write("@PARAMETER\n")
                        pf.write("Parameter Name: " + param.parameter_name + "\n")
                        pf.write("Upper Bound: " + str(param.upper_bound) + "\n")
                        pf.write("Lower Bound: " + str(param.lower_bound) + "\n")
                        pf.write("Starting Value: " + str(param.starting_value) + "\n")
                        pf.write("@@\n")
            except: return False
            finally:
                try: pf.close()
                except: pass
            return True
        else: return False

class HPConfigure:
    def __init__(self):
        self.model_directory = ''
        self.initial_filename = ''
        self.parameter_file = ''
        self.comparison_file = ''
        self.version_prefix = ''
        self.solution_file = ''
        self.stat_filename = ''
        self.graph_flag = False
        self.normalize_data_by_observed_max = False
        self.normalize_data_by_observed_mean = False
        self.cost_function = ''
        self.objective_target = ''
        self.bound_penalty_flag = False
        self.penalty_constant = 0


        self.read_configuration_file()

    def read_configuration_file(self):
        hf = None
        filename = 'configuration.txt'
        try:
            hf = open(filename, 'r')
            begin = False
            for line in hf.readlines():
                temp = line.strip().strip('\n')
                if begin:
                    if temp == '@@': break
                    else:
                        temp = temp.split("=")
                        opt_name = temp[0].strip().strip('\t')
                        opt_value = temp[1].strip().strip('\t')
                        if opt_name and opt_value:
                            if opt_name == 'model_directory': self.model_directory = opt_value
                            elif opt_name == 'initial_file': self.initial_filename = opt_value
                            elif opt_name == 'parameter_file': self.parameter_file = opt_value
                            elif opt_name == 'comparison_file': self.comparison_file = opt_value
                            elif opt_name == 'version_prefix': self.version_prefix = opt_value
                            elif opt_name == 'solution_file': self.solution_file = opt_value
                            elif opt_name == 'stat_filename': self.stat_filename = opt_value
                            elif opt_name == 'cost_function': self.cost_function = opt_value
                            elif opt_name == 'objective_target':
                                self.objective_target = opt_value
                            elif opt_name == 'graph_flag':
                                if opt_value.lower() in ['true', '1']: self.graph_flag = True
                                else: self.graph_flag = False
                            elif opt_name == 'normalize_data_by_observed_max':
                                if opt_value.lower() in ['true', '1']: self.normalize_data_by_observed_max = True
                                else: self.normalize_data_by_observed_max = False
                            elif opt_name == 'normalize_data_by_observed_mean':
                                if opt_value.lower() in ['true', '1']: self.normalize_data_by_observed_mean = True
                                else: self.normalize_data_by_observed_mean = False
                            elif opt_name == 'bound_penalty_flag':
                                if opt_value.lower() in ['true', '1']: self.bound_penalty_flag = True
                                else: self.bound_penalty_flag = False
                            elif opt_name == 'penalty_constant':
                                try: self.penalty_constant = float(opt_value)
                                except: pass
                elif temp == '@': begin = True
        except: return False
        finally:
            try: hf.close()
            except: pass

    def write_configuration_file(self, filename='hopspack/configuration.txt'):
        hf = None

        try:
            hf = open(filename, 'w')
            hf.write('@\n')
            hf.write('model_directory = ' + self.model_directory + '\n')
            hf.write('initial_file = ' + self.initial_filename + '\n')
            hf.write('parameter_file = ' + self.parameter_file + '\n')
            hf.write('comparison_file = ' + self.comparison_file + '\n')
            hf.write('version_prefix = ' + self.version_prefix + '\n')
            hf.write('solution_file = ' + self.solution_file + '\n')
            hf.write('stat_filename = ' + self.stat_filename + '\n')
            if self.graph_flag: hf.write('graph_flag = TRUE\n')
            else: hf.write('graph_flag = FALSE\n')
            hf.write('cost_function = ' + self.cost_function + '\n')
            hf.write('objective_target = ' + self.objective_target + '\n')
            if self.normalize_data_by_observed_max: hf.write('normalize_data_by_observed_max = True\n')
            else: hf.write('normalize_data_by_observed_max = False\n')
            if self.normalize_data_by_observed_mean: hf.write('normalize_data_by_observed_mean = True\n')
            else: hf.write('normalize_data_by_observed_mean = False\n')
            if self.bound_penalty_flag: hf.write('bound_penalty_flag = True\n')
            else:  hf.write('bound_penalty_flag = False\n')
            hf.write('penalty_constant = ' + str(self.penalty_constant) + '\n')
            hf.write('@@')
        except: return False
        finally:
            try: hf.close()
            except: pass

    @staticmethod
    def write_problem_definition_file(list_of_parameter, filename):
        upper_bound = []
        lower_bound = []
        initial_value = []

        parameter_count = len(list_of_parameter)

        for parameter in list_of_parameter:
            upper_bound.append(parameter.upper_bound)
            lower_bound.append(parameter.lower_bound)
            initial_value.append(parameter.starting_value)

        df = None
        try:
            df = open(filename, 'w')

            line_text = '# ************************************************************************\n'
            line_text += '#         HOPSPACK: Hybrid Optimization Parallel Search Package\n'
            line_text += '#                Copyright 2009-2010 Sandia Corporation\n'
            line_text += '#\n'
            line_text += '#   Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,\n'
            line_text += '#   the U.S. Government retains certain rights in this software.\n'
            line_text += '# ************************************************************************\n\n'
            df.write(line_text)

            line_text = '@ \"Problem Definition\"\n'
            df.write(line_text)
            line_text = '  \"Number Unknowns\" int ' + str(parameter_count) + '\n'
            df.write(line_text)
            line_text = '  \"Upper Bounds\" vector ' + str(parameter_count) + ' ' + str(upper_bound).replace('[','').replace(']','').replace(',',' ') + '\n'
            df.write(line_text)
            line_text = '  \"Lower Bounds\" vector ' + str(parameter_count) + ' ' + str(lower_bound).replace('[','').replace(']','').replace(',',' ') +'\n'
            df.write(line_text)
            line_text = '  \"Objective Type\" string \"Minimize\"\n'
            df.write(line_text)
            #line_text = ' \"Objective Target\" double 1e-8 \n'
            #df.write(line_text)
            line_text = '  \"Display\" int 2\n'
            df.write(line_text)
            line_text = '  \"Initial X\" vector ' + str(parameter_count) + ' ' + str(initial_value).replace('[','').replace(']','').replace(',',' ') + '\n'
            df.write(line_text)
            line_text = '@@\n\n'
            df.write(line_text)

            line_text = '@ \"Evaluator\"\n'
            df.write(line_text)
            line_text = '  \"Evaluator Type\"  string \"System Call\"\n'
            df.write(line_text)
            line_text = '  \"Executable Name\" string \"./parameter_evaluator.py\"\n'
            df.write(line_text)
            line_text = '  \"Input Prefix\"    string \"bgc_in\"\n'
            df.write(line_text)
            line_text = '  \"Output Prefix\"   string \"bgc_out\"\n'
            df.write(line_text)
            line_text = '  \"Debug Eval Worker\" bool false \n'
            df.write(line_text)
            line_text = '  \"Save IO Files\" bool False true\n'
            df.write(line_text)
            line_text = '@@\n\n'
            df.write(line_text)

            line_text = '@ \"Mediator\" \n'
            df.write(line_text)
            line_text = '  \"Citizen Count\" int 1 \n'
            df.write(line_text)
            line_text = '  \"Number Processors\" int 1 \n'
            df.write(line_text)
            line_text = '  \"Number Threads\" int 1 \n'
            df.write(line_text)
            line_text = '  \"Maximum Evaluations\" int -1 \n'
            df.write(line_text)
            line_text = '  \"Display\" int 3 \n'
            df.write(line_text)
            line_text = '@@\n\n'
            df.write(line_text)

            line_text = '@ \"Citizen 1\" \n'
            df.write(line_text)
            line_text = '  \"Type\" string \"GSS\"\n'
            df.write(line_text)
            line_text = '  \"Step Tolerance\" double 0.001\n'
            df.write(line_text)
            line_text = '  \"Display\" int 1 \n'
            df.write(line_text)
            line_text = '@@'
            df.write(line_text)

        except: return False
        finally:
            try: df.close()
            except: pass

        return True

class HPOutput:
    @staticmethod
    def read_output(log_filename):
        best_points = []

        points_scan_start = False

        lf = None
        try:
            lf = open(log_filename, 'r')
            for line in lf.readlines():
                if points_scan_start:
                    if line.strip('\n').strip():
                        temp = line.split(',')[1][3:-1].strip().split(' ')
                        for p in temp:
                            try: best_points.append(float(p))
                            except: pass
                        break
                else:
                    if line.strip().strip('\n') == 'Mediator best point found:':
                        points_scan_start = True
        except:
            best_points = []
        finally:
            try: lf.close()
            except: pass

        return best_points

    @staticmethod
    def read_solution_file(filename):
        plist = []

        sf = None
        try:
            sf = open(filename, 'r')
            line = sf.readlines()[-1].strip()
            if line:
                ndx = line.find('x')
                if ndx >= 0:
                    temp = line[ndx + 4: -1].strip().split(' ')
                    for p in temp:
                        try:
                            p = float(p)
                            plist.append(p)
                        except: pass
        except Exception as ex:
            pass
        finally:
            try: sf.close()
            except: pass

        return plist

    @staticmethod
    def inspect_logfile(logfile):
        total_iteration = 0
        unsuccess = 0
        failed = 0

        lf = None
        try:
            lf = open(logfile, 'r')
            for line in lf.readlines():
                if line.find('F=[ DNE') >= 0: unsuccess += 1
                elif line.find('F=(empty)') >= 0: failed += 1
                elif line.find('Number executed by workers') >=0:
                    try:
                        total_iteration = int(line.split('=')[1].strip().strip('\n'))
                    except: pass
        except Exception as ex:
            pass
        finally:
            try: lf.close()
            except: pass
        success_ratio = 0.0
        if total_iteration > 0: success_ratio = (total_iteration - unsuccess - failed) * 100 / total_iteration

        return total_iteration, failed, unsuccess, success_ratio
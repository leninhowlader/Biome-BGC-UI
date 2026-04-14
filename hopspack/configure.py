#modified on: 23-10-2014

import os, random

class Comparing_Variable:
    objective_function = ''
    def __init__(self):
        self.model_file_type = ''
        self.model_variable_name = ''
        self.observation_type = 1  #0 = Model Output, 1 = Observation Data
        self.observation_filename = ''
        self.observation_variable_name = ''
        self.pairing_flag = True
        self.pairing_model_variable = ''
        self.pairing_observation_variable = ''
        self.model_data_conversion_factor = 1
        self.observation_data_conversion_factor = 1
        self.weighing_factor = 1
        self.objective_function = ''     #if objective functioin is not defined for individual object, class objected
                                         #function will be over taken
        self.group_name = ''

    def set_objective_function(self, cost_function):
        Comparing_Variable.objective_function = cost_function

    def is_complete(self):
        if len(self.model_file_type) == 0 or len(self.model_variable_name) == 0 or len(self.observation_filename) == 0 or len(self.observation_variable_name) == 0: return False
        elif self.pairing_flag and (len(self.pairing_model_variable) == 0 or len(self.pairing_observation_variable) == 0 ): return False
        #elif self.objective_function or Comparing_Variable.objective_function: return False
        #elif len(self.group_name) == 0: return False
        else: return True

    @staticmethod
    def read_comparing_variables(compmap_file_name):
        compvar_list = []

        pfile = None
        if os.path.exists(compmap_file_name):
            try:
                pfile = open(compmap_file_name, 'r')

                comp_var = None

                block_start = False

                for line in pfile.readlines():
                    temp = line.strip().strip('\n').strip('\t')

                    if temp:
                        if not block_start and temp == '@':
                            comp_var = Comparing_Variable()
                            block_start = True
                        elif block_start and temp == '@@':
                            if comp_var is not None:
                                if comp_var.is_complete():
                                    compvar_list.append(comp_var)
                                    comp_var = None
                                    block_start = False
                        else:
                            if block_start:
                                temp = temp.split('=')
                                if temp and len(temp) >= 2:
                                    arg = temp[0].strip()
                                    val = temp[1].strip()

                                    if len(arg) > 0 and len(val) > 0:
                                        temp = arg.lower()
                                        if temp in ["output file type", 'model output file type']: comp_var.model_file_type = val
                                        elif temp in ["output variable name", 'model variable name']: comp_var.model_variable_name = val
                                        elif temp in ["observation data type", 'observation type']: comp_var.observation_type = int(val)
                                        elif temp in ["observation data file", 'observation filename']: comp_var.observation_filename = val
                                        elif temp in ["observation variable"]: comp_var.observation_variable_name = val
                                        elif temp in ["pair flag"]:
                                            if val.lower() in ['true', 't', '1']: comp_var.pairing_flag = True
                                            else: comp_var.pairing_flag = False
                                        elif temp in ["pairing variable [model]", 'pairing variable [sim]']: comp_var.pairing_model_variable = val
                                        elif temp in ["pairing variable [observation]", 'pairing variable [obs]']: comp_var.pairing_observation_variable = val
                                        elif temp in ["conversion factor [model]", 'conversion factor [sim]']:
                                            try:
                                                comp_var.model_data_conversion_factor = float(val)
                                                if comp_var.model_data_conversion_factor == 0: comp_var.model_data_conversion_factor = 1.0
                                            except: comp_var.model_data_conversion_factor = 1.0
                                        elif temp in ["conversion factor [observation]", 'conversion factor [obs]']:
                                            try:
                                                comp_var.observation_data_conversion_factor = float(val)
                                                if comp_var.observation_data_conversion_factor == 0: comp_var.observation_data_conversion_factor = 1.0
                                            except: comp_var.observation_data_conversion_factor = 1.0
                                        elif temp in ["weighing factor", 'weighting factor']:
                                            try:
                                                comp_var.weighing_factor = float(val)
                                                if comp_var.weighing_factor == 0: comp_var.weighing_factor = 1.0
                                            except: comp_var.weighing_factor = 1.0
                                        elif temp in ['cost function', 'objective function']: Comparing_Variable.cost_function = val
                                        elif temp.lower() in ['group', 'group name']: comp_var.group_name = val

            except Exception as ex:
                return None
            finally:
                try: pfile.close()
                except: pass
        return compvar_list

    @staticmethod
    def write_compmap_file(list_of_compvar, compmap_filename):
        if list_of_compvar and compmap_filename:
            pf = None
            try:
                pf = open(compmap_filename, 'w')
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

                for compvar in list_of_compvar:
                    if compvar.is_complete():
                        pf.write("@\n")
                        pf.write("Model Output File Type = " + compvar.model_file_type + "\n")
                        pf.write("Model Variable Name = " + compvar.model_variable_name + "\n")
                        pf.write("Observation Type = " + str(compvar.observation_type) + "\n")
                        pf.write("Observation Filename = " + compvar.observation_filename + "\n")
                        pf.write("Observation Variable = " + compvar.observation_variable_name + "\n")
                        pf.write("Pair Flag = " + str(compvar.pairing_flag) + "\n")
                        pf.write("Pairing Variable [sim] = " + compvar.pairing_model_variable + "\n")
                        pf.write("Pairing Variable [obs] = " + compvar.pairing_observation_variable + "\n")
                        pf.write("Conversion Factor [sim] = " + str(compvar.model_data_conversion_factor) + "\n")
                        pf.write("Conversion Factor [obs] = " + str(compvar.observation_data_conversion_factor) + "\n")
                        pf.write("Weighting Factor = " + str(compvar.weighing_factor) + "\n")
                        if compvar.objective_function:
                            pf.write("Objective Function = " + compvar.objective_function + "\n")
                        pf.write('Group Name = ' + compvar.group_name + '\n')
                        pf.write("@@\n")
            except: return False
            finally:
                try: pf.close()
                except: pass
            return True
        else: return False

class TargetParameter:
    def __init__(self):
        self.name = ""
        self.sname = ''
        self.type = ''
        self.has_index = False  #if has_index is false, default indexing will be used
        self.site_index = ''
        self.veg_no = -1
        self.profile_name = ''
        self.horizon_name = ''
        self.current_value = None
        self.has_preferred_boundary = False
        self.upper_bound = None
        self.lower_bound = None
        self.starting_value = None
        self.hard_upper_bound = None
        self.hard_lower_bound = None
        self.sequence = -1

    def is_complete(self):
        ret_val = True
        if not self.name or not self.type: ret_val = False
        if ret_val:
            if self.has_index and not self.get_index_text(): ret_val = False
        if ret_val:
            if self.has_preferred_boundary:
                if self.hard_lower_bound is None or self.lower_bound is None or self.upper_bound is None or self.hard_upper_bound is None:
                    ret_val = False
                else: ret_val = (self.hard_lower_bound<=self.lower_bound<=self.starting_value<=self.upper_bound<=self.hard_upper_bound)
            else:
                if self.lower_bound is None or self.upper_bound is None or self.starting_value is None: ret_val = False
                else: ret_val = (self.lower_bound<=self.starting_value<=self.upper_bound)
        return ret_val

    def get_index_text(self):
        index_text = ''
        if self.has_index:
            if self.type.lower() in ['gis parameter', 'vegetation parameter']: index_text = 'Site Index: ' + self.site_index
            elif self.type.lower() == 'epc parameter': index_text = 'Site Index: ' + self.site_index + ', Veg No.: ' + str(self.veg_no)
            elif self.type.lower() == 'soil parameter': index_text = 'Site Index: ' + self.site_index + ', Profile: ' + self.profile_name + ', Horizon: ' + self.horizon_name
        return index_text

    @staticmethod
    def ParameterSequence(parameter_list):
        seq = []
        for param in parameter_list: seq.append(param.sequence)
        return seq

    @staticmethod
    def GenerateRandomSequence(param_count):
        seq_list = []

        for j in range(param_count):
            while True:
                random.seed()
                x = random.randint(0, param_count - 1)
                if x not in seq_list:
                    seq_list.append(x)
                    break
        return seq_list

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
                        param = TargetParameter()
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
                                try:
                                    if temp in ['parameter name']: param.name = val
                                    elif temp in ['short name']: param.sname = val
                                    elif temp in ['type']: param.type = val
                                    elif temp in ['upper bound', 'upper bound (p)']: param.upper_bound = float(val)
                                    elif temp in ['lower bound', 'lower bound (h)']: param.lower_bound = float(val)
                                    elif temp in ['starting value']: param.starting_value = float(val)
                                    elif temp in ['hard upper bound']: param.hard_upper_bound = float(val)
                                    elif temp in ['hard lower bound']: param.hard_lower_bound = float(val)
                                    elif temp in ['indexed', 'has index']:
                                        if val.lower in ['true']: param.has_index = True
                                    elif temp in ['site index', '1']: param.site_index = val
                                    elif temp in ['veg no.', 'veg no', 'veg number', 'vegetation no', 'vegetation no.',
                                                  'vegetation number']: param.veg_no = int(val)
                                    elif temp in ['profile name', 'soil profile', 'profile']: param.profile_name = val
                                    elif temp in ['horizon name', 'soil horizon', 'horizon']: param.horizon_name = val
                                    elif temp in ['preferred boundary']:
                                        if val.lower() in ['true','1']: param.has_preferred_boundary = True
                                    elif temp in ['upper bound (h)']: param.hard_upper_bound = float(val)
                                    elif temp in ['lower bound (h)']: param.hard_lower_bound = float(val)
                                    elif temp in ['parameter sequence', 'sequence']: param.sequence = int(val)

                                except: pass
            except: return False
            finally:
                try: pf.close()
                except: pass
            if len(parameter_list_out) == 0: return False
            else: return True
        else: return False

    @staticmethod
    def write_parameter_file(list_of_parameter, parameter_file_name):
        if list_of_parameter and parameter_file_name:
            pf = None
            try:
                pf = open(parameter_file_name, 'w')

                text_line = "This file contains the list of selected parameters to be used in optimization. "
                text_line += "Each parameter starts with a key word @PARAMETER and ends with @@. The names must "
                text_line += "comply with the names used in interface module (..interface/paramdomain/epc.prm).\n"
                pf.write(text_line)

                for param in list_of_parameter:
                    if param.is_complete():
                        pf.write('@PARAMETER\n')
                        pf.write('Parameter Name: ' + param.name + '\n')
                        pf.write('Type: ' + str(param.type) + '\n')
                        if param.has_index:
                            pf.write('Indexed: True\n')
                            if param.type.lower() in ['gis', 'gis parameter', 'veg', 'veg parameter', 'vegetation parameter']:
                                pf.write('Site Index: ' + param.site_index + '\n')
                            elif param.type.lower() in ['epc', 'epc parameter']:
                                pf.write('Site Index: ' + param.site_index + '\n')
                                pf.write('Veg No.: ' + str(param.veg_no) + '\n')
                            elif param.type.lower() in ['soil', 'soil parameter']:
                                pf.write("Site Index: " + param.site_index + "\n")
                                pf.write("Profile Name: " + param.profile_name + "\n")
                                pf.write("Horizon Name: " + param.horizon_name + "\n")
                        if param.has_preferred_boundary:
                            pf.write("Preferred Boundary: True\n")
                            pf.write("Lower Bound (H): " + str(param.hard_lower_bound) + "\n")
                            pf.write("Lower Bound (P): " + str(param.lower_bound) + "\n")
                            pf.write("Upper Bound (P): " + str(param.upper_bound) + "\n")
                            pf.write("Upper Bound (H): " + str(param.hard_upper_bound) + "\n")
                        else:
                            pf.write("Upper Bound: " + str(param.upper_bound) + "\n")
                            pf.write("Lower Bound: " + str(param.lower_bound) + "\n")
                        pf.write("Starting Value: " + str(param.starting_value) + "\n")
                        pf.write("Parameter Sequence: " + str(param.sequence) + "\n")
                        pf.write("@@\n")
            except: return False
            finally:
                try: pf.close()
                except: pass
            return True
        else: return False

class Configure:
    def __init__(self, filename='configuration.txt'):
        self.model_directory = ''
        self.initial_filename = ''
        self.parameterMap_file = ''
        self.comparisonMap_file = ''
        self.extension_postfix = ''

        self.stat_filename = ''
        self.solution_file = ''
        self.objective_target = ''
        self.objective_function = ''
        self.normalization_option_flag = -1 #-1 = No Normalization
                                            # 0 = 'Normalize data using Observation Max',
                                            # 1 = 'Normalize data using Observation Mean',
                                            # 2 = 'Normalize data using Predicted Max',
                                            # 3 = 'Normalize data using Predicted Mean'
        self.penalty_option_flag = -1   #-1 = None 0 = Linear Distance 1 = Squared Distance 2 = Cubic Distance 3 = Logistic Function'
        self.penalty_constant = 0
        self.parameter_sequence = []

        self.relative_path_flag = False
        self.reference_directory = ''
        self.graph_flag = False

        self.read_configuration_file(filename)


    def get_normalization_option(self):
        if self.normalization_option_flag == 0: return 'Normalize data using Observation Max'
        elif self.normalization_option_flag == 1: return 'Normalize data using Observation Mean'
        elif self.normalization_option_flag == 2: return 'Normalize data using Predicted Max'
        elif self.normalization_option_flag == 3: return 'Normalize data using Predicted Mean'
        else: return 'No Normalization'

    def get_normalization_flag(self, norm_option):
        norm_option = norm_option.lower()
        if norm_option in ['normalize data using observation max', 'observation max', 'observed max']: return 0
        elif norm_option in ['normalize data using observation mean', 'observation mean', 'observed mean']: return 1
        elif norm_option in ['normalize data using predicted max', 'prediction max', 'predicted max']: return 2
        elif norm_option in ['normalize data using predicted mean', 'prediction mean', 'predicted mean']: return 3
        else: return -1

    def get_penalty_option(self):
        if self.penalty_option_flag == 0: return 'Linear Distance'
        elif self.penalty_option_flag == 1: return 'Squared Distance'
        elif self.penalty_option_flag == 2: return 'Cubic Distance'
        elif self.penalty_option_flag == 3: return  'Logistic Function'
        else: return 'None'

    def get_penalty_flag(self, penalty_option):
        if penalty_option == 'Linear Distance': return 0
        elif penalty_option == 'Squared Distance': return 1
        elif penalty_option == 'Cubic Distance': return 2
        elif penalty_option == 'Logistic Function': return 3
        else: return -1

    def is_relative_address_used(self):
        if not os.path.isabs(self.model_directory): return True
        elif not os.path.isabs(self.initial_filename): return True
        elif not os.path.isabs(self.parameterMap_file):return True
        elif not os.path.isabs(self.comparisonMap_file): return True
        else: return False

    def read_configuration_file(self, filename='configuration.txt'):
        hf = None

        try:
            hf = open(filename, 'r')
            begin = False
            for line in hf.readlines():
                temp = line.strip().strip('\n')
                if begin:
                    if temp == '@@': break
                    else:
                        temp = temp.split("=")
                        opt_name = temp[0].strip().strip('\t').lower()
                        opt_value = temp[1].strip().strip('\t')
                        if opt_name and opt_value:
                            if opt_name in ['model directory', 'model_directory', 'model home directory']: self.model_directory = opt_value
                            elif opt_name in ['initial file', 'initial_file', 'initialization file']: self.initial_filename = opt_value
                            elif opt_name in ['parameter file', 'parameter_file']: self.parameterMap_file = opt_value
                            elif opt_name in ['comparison file', 'comparison_file']: self.comparisonMap_file = opt_value
                            elif opt_name in ['extension postfix', 'version_prefix', 'extention postfix']: self.extension_postfix = opt_value
                            elif opt_name in ['solution file', 'solution_file']: self.solution_file = opt_value
                            elif opt_name in ['stat filename', 'stat_filename', 'stat file']: self.stat_filename = opt_value
                            elif opt_name == 'objective function': self.objective_function = opt_value
                            elif opt_name == 'objective target': self.objective_target = opt_value
                            elif opt_name in ['normalization option']: self.normalization_option_flag = self.get_normalization_flag(opt_value)
                            elif opt_name in ['penalty option']: self.penalty_option_flag = self.get_penalty_flag(opt_value)
                            elif opt_name in ['penalty option']: self.penalty_option_flag = self.get_penalty_flag(opt_value)
                            elif opt_name in ['penalty_constant', 'penalty constant']:
                                try: self.penalty_constant = float(opt_value)
                                except: pass
                            elif opt_name in ['parameter_sequence', 'parameter sequence']:
                                temp = opt_value.split(',')

                                for i in range(len(temp)):
                                    try: temp[i] = temp[i].strip()
                                    except:
                                        temp = []
                                        break
                                self.parameter_sequence = temp
                            elif opt_name in ['relative path flag']:
                                if opt_value.lower() in ['true', '1']: self.relative_path_flag = True
                                else: self.relative_path_flag = False
                            elif opt_name == 'reference directory': self.reference_directory = opt_value
                            elif opt_name == 'graph flag':
                                if opt_value.lower() in ['true', '1']: self.graph_flag = True
                                else: self.graph_flag = False

                elif temp == '@': begin = True
        except: return False
        finally:
            try: hf.close()
            except: pass
        return True

    def write_configuration_file(self, filename='hopspack/configuration.txt'):
        hf = None

        try:
            hf = open(filename, 'w')
            hf.write('@\n')
            hf.write('Model Home Directory = ' + self.model_directory + '\n')
            hf.write('Initialization File = ' + self.initial_filename + '\n')
            hf.write('Parameter File = ' + self.parameterMap_file + '\n')
            hf.write('Comparison File = ' + self.comparisonMap_file + '\n')
            hf.write('Extention Postfix = ' + self.extension_postfix + '\n')
            hf.write('Solution File = ' + self.solution_file + '\n')
            hf.write('Stat File = ' + self.stat_filename + '\n')
            hf.write('Objective Function = ' + self.objective_function + '\n')
            hf.write('Objective Target = ' + self.objective_target + '\n')
            hf.write('Normalization Option = ' + self.get_normalization_option() + '\n')
            hf.write('Penalty Option = ' + self.get_penalty_option() + '\n')
            hf.write('Penalty Constant = ' + str(self.penalty_constant) + '\n')
            hf.write('Parameter Sequence = ' + str(self.parameter_sequence)[1:-1].replace('\'','').strip() + '\n')
            hf.write('Relative Path Flag =' + str(self.relative_path_flag) + '\n')
            hf.write('Reference Directory = ' + self.reference_directory + '\n')
            if self.graph_flag: hf.write('Graph Flag = TRUE\n')
            else: hf.write('Graph Flag = FALSE \n')
            hf.write('@@')
        except: return False
        finally:
            try: hf.close()
            except: pass

        return True

    @staticmethod
    def function_short_name(fun):
        if fun == 'Absolute Average Deviation': return 'aad'
        elif fun == 'Coefficient of Determination': return 'r2'
        elif fun == 'Index of Agreement': return 'ioa'
        elif fun == 'Mean Absolute Error': return 'mae'
        elif fun == 'Mean Square Error': return 'mse'
        elif fun == 'Nash-Sutcliffe Efficiency': return 'nse'
        elif fun == 'Percentage Bias': return 'pbias'
        elif fun == 'RMSE-Observed Stdv. Ratio': return 'rsr'
        elif fun == 'Root Mean Square Error': return 'rmse'
        else: return ''

    @staticmethod
    def function_full_name(function):
        if function == 'aad': return 'Absolute Average Deviation'
        elif function == 'r2': return 'Coefficient of Determination'
        elif function == 'ioa': return 'Index of Agreement'
        elif function == 'mae': return 'Mean Absolute Error'
        elif function == 'mse': return 'Mean Square Error'
        elif function == 'nse': return 'Nash-Sutcliffe Efficiency'
        elif function == 'pbias': return 'Percentage Bias'
        elif function == 'rsr': return 'RMSE-Observed Stdv. Ratio'
        elif function == 'rmse': return 'Root Mean Square Error'
        else: return ''


class OptimizationProblem:
    def __init__(self):
        #variables for problem definition section
        self.no_of_parameters = 0
        self.upper_bound = []
        self.lower_bound = []
        self.initial_value = []
        self.initial_fvalue = []
        self.optimization_objective = ''
        self.definition_display_option = 1

        #variables for evaluator section
        self.evaluator_type = 'System Call'
        self.executable_name = ''
        self.file_precision = 0
        self.input_prefix = ''
        self.output_prefix = ''
        self.display_debug_info_flag = False
        self.save_io_file_flag = False

        #variables for mediator section
        self.citizen_count = 1
        self.processor_count = 1
        self.thread_count = 1
        self.maximum_evaluations = -1
        self.synchronize_evaluation_flag = True
        self.solution_filename = ''
        self.solution_file_precision = 6
        self.mediator_display_option = 3

        #variables for citizen section
        self.citizen_list = []      #must contain Hopspack Citizen objects

    def check_completeness(self):
        if (len(self.upper_bound) != self.no_of_parameters or len(self.lower_bound) != self.no_of_parameters
            or len(self.initial_value) != self.no_of_parameters): return False
        elif len(self.citizen_list) != self.citizen_count: return False
        else: return True

    @staticmethod
    def read_problem_definition_file(filename):
        prob_def = OptimizationProblem()

        df = None
        try:
            df = open(filename, 'r')

            segment = ''
            citizen = None
            for text_line in df.readlines():
                text_line = text_line.strip()
                if text_line.find('#') > -1: text_line = text_line.split('#')[0].strip()
                if text_line:
                    if text_line == "@@":
                        if segment == 'Citizen':
                            prob_def.citizen_list.append(citizen)
                            citizen = None
                        segment = ''
                    else:
                        if segment:

                            while text_line.find('\t') > -1: text_line = text_line.replace('\t', ' ')
                            while text_line.find('  ') > -1: text_line = text_line.replace('  ', ' ')

                            temp = text_line.split('\"')
                            for i in reversed(range(len(temp))):
                                if not temp[i].strip(): temp.pop(i)

                            if temp[1].strip().lower() in ['string']:
                                val = [temp[-1]]
                            else:
                                val = temp[-1].strip().split(' ')
                                for i in reversed(range(len(val))):
                                    if not val[i].strip(): val.pop(i)

                            if temp[0] == 'Number Unknowns':
                                try: prob_def.no_of_parameters = int(val[-1])
                                except: return None
                            elif temp[0] == 'Upper Bounds':
                                ub = []
                                for i in range(len(val)):
                                    try: ub.append(float(val[i]))
                                    except: pass
                                if ub: prob_def.upper_bound = ub[1:]
                            elif temp[0] == 'Lower Bounds':
                                lb = []
                                for i in range(len(val)):
                                    try: lb.append(float(val[i]))
                                    except: pass
                                if lb: prob_def.lower_bound = lb[1:]
                            elif temp[0] == 'Initial X':
                                ix = []
                                for i in range(len(val)):
                                    try: ix.append(float(val[i]))
                                    except: pass
                                if ix: prob_def.initial_value = ix[1:]
                            elif temp[0] == 'Initial F':
                                fv = []
                                for i in range(len(val)):
                                    try: fv.append(float(val[i]))
                                    except: pass
                                if fv: prob_def.initial_fvalue = fv[1:]
                            elif temp[0] == 'Objective Type': prob_def.optimization_objective = val[-1]
                            elif temp[0] == 'Display':
                                if segment == 'Problem Definition':
                                    try: prob_def.definition_display_option = int(val[-1])
                                    except: pass
                                elif segment == 'Mediator':
                                    try: prob_def.mediator_display_option = int(val[-1])
                                    except: pass
                                elif segment == 'Citizen':
                                    try: citizen.citizen_display_option = int(val[-1])
                                    except: pass
                            elif temp[0] == 'Evaluator Type': prob_def.evaluator_type = val[-1]
                            elif temp[0] == 'Executable Name': prob_def.executable_name = val[-1]
                            elif temp[0] == 'Input Prefix': prob_def.input_prefix = val[-1]
                            elif temp[0] == 'Output Prefix': prob_def.output_prefix = val[-1]
                            elif temp[0] == 'Debug Eval Worker':
                                if val[-1].lower() == 'true': prob_def.display_debug_info_flag = True
                                else: prob_def.display_debug_info_flag = False
                            elif temp[0] == 'Save IO Files':
                                if val[-1].lower() == 'true': prob_def.save_io_file_flag = True
                                else: prob_def.save_io_file_flag = False
                            elif temp[0] == 'Citizen Count':
                                try: prob_def.citizen_count = int(val[-1])
                                except: return None
                            elif temp[0] == 'Number Processors':
                                try: prob_def.processor_count = int(val[-1])
                                except: pass
                            elif temp[0] == 'Number Threads':
                                try: prob_def.thread_count = int(val[-1])
                                except: pass
                            elif temp[0] == 'Maximum Evaluations':
                                try: prob_def.maximum_evaluations = int(val[-1])
                                except: pass
                            elif temp[0] == 'Synchronous Evaluations':
                                if val[-1].lower() == 'true': prob_def.synchronize_evaluation_flag = True
                                else: prob_def.synchronize_evaluation_flag = False
                            elif temp[0] == 'Solution File': prob_def.solution_filename = val[-1]
                            elif temp[0] == 'Solution File Precision':
                                try: prob_def.solution_file_precision = int(val[-1])
                                except: pass
                            elif temp[0] == 'Type': citizen.citizen_type = val[-1]
                            elif temp[0] == 'Step Tolerance':
                                try: citizen.step_tolerence = float(val[-1])
                                except: pass
                        else:
                            if text_line[0] == '@':
                                temp = text_line[1:].strip().split('\"')
                                if temp[1] in ['Problem Definition', 'Evaluator', 'Mediator', 'Citizen']:
                                    segment = temp[1]
                                elif temp[1].split(' ')[0] == 'Citizen':
                                    segment = temp[1].split(' ')[0]
                                    citizen = HopspackCitizen()
        except: return None
        finally:
            try: df.close()
            except: pass

        return prob_def

    def write_problem_definition_file(self, filename):
        if self.check_completeness():

            df = None
            try:
                df = open(filename, 'w')
                list_of_text_lines = []

                #file heading
                list_of_text_lines.append('# ************************************************************************')
                list_of_text_lines.append('#         HOPSPACK: Hybrid Optimization Parallel Search Package')
                list_of_text_lines.append('#                Copyright 2009-2010 Sandia Corporation')
                list_of_text_lines.append('#')
                list_of_text_lines.append('#   Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,')
                list_of_text_lines.append('#   the U.S. Government retains certain rights in this software.')
                list_of_text_lines.append('# ************************************************************************\n')

                #problem definition section
                list_of_text_lines.append('@ \"Problem Definition\"')
                list_of_text_lines.append('  \"Number Unknowns\" int ' + str(self.no_of_parameters))

                if self.upper_bound:
                    l = ''
                    for x in self.upper_bound: l += str(x) + ' '
                    list_of_text_lines.append('  \"Upper Bounds\" vector ' + str(self.no_of_parameters) + ' ' + l)

                if self.lower_bound:
                    l = ''
                    for x in self.lower_bound: l += str(x) + ' '
                    list_of_text_lines.append('  \"Lower Bounds\" vector ' + str(self.no_of_parameters) + ' ' + l)

                if self.initial_value:
                    l = ''
                    for x in self.initial_value: l += str(x) + ' '
                    list_of_text_lines.append('  \"Initial X\" vector ' + str(self.no_of_parameters) + ' ' + l)

                if self.initial_fvalue:
                    l = ''
                    for x in self.initial_fvalue: l += str(x) + ' '
                    list_of_text_lines.append('  \"Initial F\" vector ' + str(len(self.initial_fvalue)) + ' ' + l.strip())

                list_of_text_lines.append('  \"Objective Type\" string \"' + self.optimization_objective + '\"')
                list_of_text_lines.append('  \"Display\" int ' + str(self.definition_display_option))
                list_of_text_lines.append('@@\n')

                #evaluator section
                list_of_text_lines.append('@ \"Evaluator\"')
                list_of_text_lines.append('  \"Evaluator Type\"  string \"' + self.evaluator_type + '\"')
                list_of_text_lines.append('  \"Executable Name\" string \"' + self.executable_name + '\"')
                list_of_text_lines.append('  \"Input Prefix\"    string \"' + self.input_prefix + '\"')
                list_of_text_lines.append('  \"Output Prefix\"   string \"' + self.output_prefix + '\"')
                list_of_text_lines.append('  \"Debug Eval Worker\" bool ' + str(self.display_debug_info_flag))
                list_of_text_lines.append('  \"Save IO Files\" bool ' + str(self.save_io_file_flag))
                list_of_text_lines.append('@@\n')

                #mediator section
                list_of_text_lines.append('@ \"Mediator\"')
                list_of_text_lines.append('  \"Citizen Count\" int ' + str(self.citizen_count))
                list_of_text_lines.append('  \"Number Processors\" int ' + str(self.processor_count))
                list_of_text_lines.append('  \"Number Threads\" int ' + str(self.thread_count))
                list_of_text_lines.append('  \"Maximum Evaluations\" int ' + str(self.maximum_evaluations))
                list_of_text_lines.append('  \"Synchronous Evaluations\" bool ' + str(self.synchronize_evaluation_flag))
                list_of_text_lines.append('  \"Solution File\" string \"' + self.solution_filename + '\"')
                list_of_text_lines.append('  \"Solution File Precision\" int ' + str(self.solution_file_precision))
                list_of_text_lines.append('  \"Display\" int ' + str(self.mediator_display_option))
                list_of_text_lines.append('@@\n')

                #citizen section
                for i in range(len(self.citizen_list)):
                    citizen = self.citizen_list[i]
                    list_of_text_lines.append('@ \"Citizen ' + str(i + 1) + '\"')
                    list_of_text_lines.append('  \"Type\" string \"' + citizen.citizen_type + '\"')
                    list_of_text_lines.append('  \"Step Tolerance\" double ' + str(citizen.step_tolerence))
                    list_of_text_lines.append('  \"Display\" int ' + str(citizen.citizen_display_option))
                    list_of_text_lines.append('@@')

                for text_line in list_of_text_lines: df.write(text_line + '\n')

            except: return False
            finally:
                try: df.close()
                except: pass

            return True
        else:
            # print('Problem(s) detected in problem definition. Please check the definition.')
            return False

class HopspackCitizen:
    def __init__(self):
        self.citizen_type = 'GSS'
        self.step_tolerence = 0.001
        self.citizen_display_option = 2



class Solution:
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
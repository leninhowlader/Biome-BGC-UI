import mysql.connector
from mysql.connector.constants import ClientFlag

class DbCore:
    server_name = ''
    database_name = ''
    user_name = ''
    password = ''

    @staticmethod
    def read_password_file(passfile):
        pf = None
        try:
            pf = open(passfile, 'r')

            for line in pf.readlines():
                temp = line.split('=')
                if len(temp) == 2:
                    var_name = temp[0].strip().lower()
                    value = temp[1].strip().strip('\n')
                    if var_name == 'server name':
                        DbCore.server_name = value
                    elif var_name == 'database name':
                        DbCore.database_name = value
                    elif var_name == 'user name':
                        DbCore.user_name = value
                    elif var_name == 'password':
                        DbCore.password = value
        except Exception as ex:
            return False
        finally:
            try: pf.close()
            except: pass
        return DbCore.is_ready()

    @staticmethod
    def is_ready():
        if (not DbCore.server_name) or (not DbCore.database_name) or (not DbCore.user_name) or (not DbCore.password):
            return False
        else: return True

    @staticmethod
    def execute_query(sql, commit=False, password_file='hpresult.pwd'):
        if not DbCore.is_ready():
            if not DbCore.read_password_file(password_file): return None

        result = None
        dbcon = None
        try:
            dbcon = mysql.connector.connect(user=DbCore.user_name, password=DbCore.password,
                                            database=DbCore.database_name, host=DbCore.server_name)
            cur = dbcon.cursor()
            cur.execute(sql)

            result = cur.fetchall()
            if commit: dbcon.commit()
            dbcon.close()
        except Exception as ex:
            return None
        finally:
            try: dbcon.close()
            except: pass

        return result

    @staticmethod
    def execute_parameter_query(sql, parameter_set_tuple, commit=False, password_file='hpresult.pwd'):
        if not DbCore.is_ready():
            if not DbCore.read_password_file(password_file): return None

        result = None
        dbcon = None
        try:
            dbcon = mysql.connector.connect(user=DbCore.user_name, password=DbCore.password,
                                            database=DbCore.database_name, host=DbCore.server_name,
                                            client_flags=[ClientFlag.LOCAL_FILES])
            cur = dbcon.cursor()

            cur.execute(sql, parameter_set_tuple)
            result = cur.fetchall()
            if commit: dbcon.commit()
        except Exception as ex:
            return None
        finally:
            try: dbcon.close()
            except: pass

        return result

class DbOperation:
    #database functions:
    #save_calibration(plot_no_str varchar(20), fun_name_str varchar(50), norm_type_str varchar(50), iteration_int int)
    #save_comparison(sim_var_name_str varchar(50), sim_var_category_str varchar(50), obs_var_name_str varchar(50), weigh_factor_float float)
    #save_observed_variable(var_name_str varchar(50))
    #save_parameter(param_name_str varchar(100), param_type_str varchar(30))
    #save_parameter_summary(cal_id_int int, param_name_str varchar(100), param_category_str varchar(30), param_max_float float,
	#                       param_min_float float, start_val_float float, opt_val_float float)
    #save_simulation_variable(var_name_str varchar(50), var_category_str varchar(50))
    #save_statistics(cal_id_int int, init_flag_bol bool, fun_name_str varchar(50), comparision_id_int int, comparison_value_float float)

    @staticmethod
    def save_into_database(config, list_of_parameter, list_of_comparison, stat_result, no_of_iteration=-1):
        #step -1: save calibration
        plot_no = ''
        temp = config.parameter_file.split('.')[0].split('_')[-1]
        if temp: plot_no = temp

        normalization_type = 'No normalization'
        if config.normalize_data_by_observed_max: normalization_type = 'Using Observed Maximum'
        elif config.normalize_data_by_observed_mean: normalization_type = 'Using Observed Mean'

        # sql = 'select save_calibration(' + plot_no + ', ' + config.cost_function + ', ' + normalization_type + ', ' + str(no_of_iteration) + ');'
        sql = "select save_calibration(%s, %s, %s, %s);"

        cal_id = DbCore.execute_parameter_query(sql, ('301', 'Mean Square Error', 'No Normalization', 200), commit=True)
        return cal_id

    @staticmethod
    def save_calibration(plot_no, function_name, normalization_type, iteration, success_rate):
        sql = 'select save_calibration(%s, %s, %s, %s, %s) as result;'
        result = DbCore.execute_parameter_query(sql, (plot_no, function_name, normalization_type, iteration, success_rate), commit=True)
        return result[0][0]

    @staticmethod
    def save_parameter(calibration_id, parameter_name, parameter_category, max_val, min_val, start_val, opt_val):
        sql = 'select save_parameter_summary(%s, %s, %s, %s, %s, %s, %s) as result;'
        result = DbCore.execute_parameter_query(sql, (calibration_id, parameter_name, parameter_category, max_val,
                                                    min_val, start_val, opt_val), commit=True)
        return result[0][0]

    @staticmethod
    def save_comparison(comparison_group, sim_variable, sim_var_cat, obs_var, weight):
        sql = 'select save_comparison(%s, %s, %s, %s, %s) as result;'
        result = DbCore.execute_parameter_query(sql, (comparison_group, sim_variable, sim_var_cat, obs_var, weight), commit=True)
        return result[0][0]

    @staticmethod
    def save_statistics(calibration_id, is_initial, cost_function, comparison_id, value):
        sql = 'select save_statistics(%s, %s, %s, %s, %s) as result;'
        result = DbCore.execute_parameter_query(sql, (calibration_id, is_initial, cost_function, comparison_id, str(value)), commit=True)
        return result[0][0]
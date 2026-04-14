#!/usr/bin/python3

import os

def inspect_logfile(logfile):
    total_iteration = 0
    unsuccess = 0
    failed = 0

    lf = None
    try:
        lf = open(logfile, 'r')
        for line in lf.readlines():
            if line.find('Step') == -1:
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



wf = None
try:
    directory_name = 'log'

    plot_list = ['301', '302', '303', '304', '305', '307', '308', '901', '908', '919', '1201', '1202', '1203', '1204', '1205', '1206',
                 'IT01', 'IT06', 'IT08', 'IT09', 'IT10', 'IT12', 'IT17', 'GR02', 'AT16', 'SK206', 'SK209']
    norm_list = ['wt_nmax']
    fun_list = ['rmse', 'mse', 'mae', 'aad', 'r2', 'rsr', 'ioa', 'pbias', 'nse']

    wf = open('inspect.txt', 'w')
    for norm in norm_list:
        wf.write(norm + ':\n')
        for plot in plot_list:
            wf.write('\t\t' + plot + ':\n')
            for fun in fun_list:
                log_file = os.path.join(directory_name, norm, 'plot' + plot, fun + '.log')
                #print(log_file)
                total_iteration, failed, unsuccess, success_ratio = inspect_logfile(log_file)
                temp = 'iteration = ' + str(total_iteration).ljust(10, ' ') + ' Failed: ' + str(failed).ljust(10, ' ') + ' Unsuccessful = ' + str(unsuccess).ljust(10, ' ') + ' success ratio = ' + (str(round(success_ratio, 2)) + '%').ljust(10, ' ')
                text_line = '\t\t\t\t' + fun.ljust(5, ' ') + ': ' + temp

                wf.write(text_line + '\n')

    plot_list = ['301', '302', '303', '304', '305', '307', '308', '901', '908', '919', '1201', '1202', '1203', '1204', '1205', '1206',
                 'IT01', 'IT06', 'IT08', 'IT09', 'IT10', 'IT12', 'IT17', 'GR02', 'AT16', 'SK206', 'SK209']
    norm_list = ['wt_nmean']
    fun_list = ['rmse', 'mse', 'mae', 'aad']
    for norm in norm_list:
        wf.write(norm + ':\n')
        for plot in plot_list:
            wf.write('\t\t' + plot + ':\n')
            for fun in fun_list:
                log_file = os.path.join(directory_name, norm, 'plot' + plot, fun + '.log')
                #print(log_file)
                total_iteration, failed, unsuccess, success_ratio = inspect_logfile(log_file)
                temp = 'iteration = ' + str(total_iteration).ljust(10, ' ') + ' Failed: ' + str(failed).ljust(10, ' ') + ' Unsuccessful = ' + str(unsuccess).ljust(10, ' ') + ' success ratio = ' + (str(round(success_ratio, 2)) + '%').ljust(10, ' ')
                text_line = '\t\t\t\t' + fun.ljust(5, ' ') + ': ' + temp

                wf.write(text_line + '\n')
except Exception as ex: pass
finally:
    try: wf.close()
    except: pass


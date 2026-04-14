import numpy as np
import pickle
from read_output import ReadBinaryOutput, ReadExternalOutput
from copy import deepcopy
import os
from dateutil import parser

# from PyQt5 import QtGui
from application import ApplicationProperty

class printable_graph():
    model_graph = None

class ModelGraph():
    def __init__(self, title):
        self.graph_title = title
        self.no_of_plot = 1
        self.plot_orientation_col = 1
        self.plot_orientation_row = 1
        self.list_of_plot = []

        self.edit_feature = FigureEditFeature()


    def max_plot_number(self):
        return self.plot_orientation_col * self.plot_orientation_row

    def add_plot(self, plot):
        if plot is not None:
            for p in self.list_of_plot:
                if p.plot_title == plot.plot_title:
                    return False
            else:
                self.list_of_plot.append(plot)
                return True
        return False

    def plot_exists(self, title):
        for plot in self.list_of_plot:
            if plot.plot_title == title:
                return True
        else:
            return False

    def remove_plot(self, plot_index=-1, plot_title=""):
        if plot_index > -1 or plot_title != "":
            if plot_index > -1:
                self.list_of_plot.pop(plot_index)
            elif plot_title != "":
                plot_index = self.find_plot_index(plot_title)
                if plot_index > -1: self.list_of_plot.pop(plot_index)

    def find_plot_index(self, plot_title):
        for i in range(len(self.list_of_plot)):
            plot = self.list_of_plot[i]
            if plot.plot_title == plot_title:
                return i
        return -1

    def find_number_of_existing_plot(self):
        return len(self.list_of_plot)

    def find_plot_by_index(self, plot_index):
        return self.list_of_plot[plot_index]

    def find_plot_by_title(self, title):
        plot_index = self.find_plot_index(title)
        if plot_index > -1: return self.find_plot_by_index(plot_index)
        else: return None

    def find_free_plot_position(self):
        free_position = 0
        for i in range(self.no_of_plot):
            for j in range(len(self.list_of_plot)):
                plot = self.list_of_plot[j]
                if plot.plot_position == i + 1: break
            else:
                free_position = i + 1
                break
        return free_position

    def check_missing_data(self):
        data_missing = False
        for plot in self.list_of_plot:
            for series in plot.list_of_series:
                if series.series_data is None:
                    data_missing = True
                    break
            if data_missing: break
        return data_missing

    @staticmethod
    def write_graph_template(model_graph, filename):
        f = None
        try:
            f = open(filename, 'w')
            f.write('@@model_graph\n')
            f.write('graph_title = ' + model_graph.graph_title + '\n')
            f.write('no_of_plot = ' + str(model_graph.no_of_plot) + '\n')
            f.write('plot_orientation_col = ' + str(model_graph.plot_orientation_col) + '\n')
            f.write('plot_orientation_row = ' + str(model_graph.plot_orientation_row) + '\n')
            f.write('@@edit_feature = FigureEditFeature\n')
            f.write('window_text = ' + model_graph.edit_feature.window_text + '\n')
            f.write('faceColor = ' + model_graph.edit_feature.faceColor + '\n')
            f.write('width = ' + str(model_graph.edit_feature.width) + '\n')
            f.write('height = ' + str(model_graph.edit_feature.height) + '\n')
            f.write('showMaximized = ' + str(model_graph.edit_feature.showMaximized) + '\n')
            f.write('show_figure_title = ' + str(model_graph.edit_feature.show_figure_title) + '\n')
            f.write('font_size = ' + str(model_graph.edit_feature.font_size) + '\n')
            f.write('font_color = ' + model_graph.edit_feature.font_color + '\n')
            f.write('show_bold = ' + str(model_graph.edit_feature.show_bold) + '\n')
            f.write('horizontal_alignment = ' + model_graph.edit_feature.horizontal_alignment + '\n')
            f.write('@edit_feature\n')
            for p in model_graph.list_of_plot:
                f.write('@@plot\n')
                f.write('plot_title = ' + p.plot_title + '\n')
                f.write('plot_position = ' + str(p.plot_position) + '\n')
                f.write('show_x_label = ' + str(p.show_x_label) + '\n')
                f.write('show_y_label = ' + str(p.show_y_label) + '\n')
                f.write('x_label = ' + p.x_label + '\n')
                f.write('y_label = ' + p.y_label + '\n')
                f.write('show_x_ticks = ' + str(p.show_x_ticks) + '\n')
                f.write('x_ticks_rotation = ' + str(p.x_ticks_rotation) + '\n')
                f.write('show_legend = ' + str(p.show_legend) + '\n')
                f.write('legend_vertical_position = ' + str(p.legend_vertical_position) + '\n')
                f.write('legend_horizontal_position = ' + str(p.legend_horizontal_position) + '\n')
                f.write('@@edit_feature = PlotEditFeature\n')
                f.write('backgroundColor = ' + p.edit_feature.backgroundColor + '\n')
                f.write('x_lim_max = ' + str(p.edit_feature.x_lim_max) + '\n')
                f.write('x_lim_min = ' + str(p.edit_feature.x_lim_min) + '\n')
                f.write('y_lim_max = ' + str(p.edit_feature.y_lim_max) + '\n')
                f.write('y_lim_min = ' + str(p.edit_feature.y_lim_min) + '\n')

                f.write('x_axis_major_interval = ' + str(p.edit_feature.x_axis_major_interval) + '\n')
                f.write('x_axis_minor_interval = ' + str(p.edit_feature.x_axis_minor_interval) + '\n')
                f.write('y_axis_major_interval = ' + str(p.edit_feature.y_axis_major_interval) + '\n')
                f.write('y_axis_minor_interval = ' + str(p.edit_feature.y_axis_minor_interval) + '\n')

                f.write('grid_show = ' + str(p.edit_feature.grid_show) + '\n')
                f.write('grid_axis_option = ' + p.edit_feature.grid_axis_option + '\n')
                f.write('grid_which_option = ' + p.edit_feature.grid_which_option + '\n')

                f.write('show_plot_title = ' + str(p.edit_feature.show_plot_title) + '\n')
                f.write('title_font_size = ' + str(p.edit_feature.title_font_size) + '\n')
                f.write('title_font_color = ' + p.edit_feature.title_font_color + '\n')
                f.write('title_show_bold = ' + str(p.edit_feature.title_show_bold) + '\n')
                f.write('horizontal_alignment = ' + p.edit_feature.horizontal_alignment + '\n')
                f.write('@edit_feature\n')

                for s in p.list_of_series:
                    f.write('@@series\n')
                    f.write('attribute_name = ' + s.attribute_name + '\n')
                    f.write('series_title = ' + s.series_title + '\n')
                    f.write('x_axis_variable = ' + s.x_axis_variable + '\n')
                    f.write('filter_variable = ' + s.filter_variable + '\n')
                    f.write('filter_condition = ' + s.filter_condition + '\n')
                    f.write('filter_first_value = ' + str(s.filter_first_value) + '\n')
                    f.write('filter_second_value = ' + str(s.filter_second_value) + '\n')

                    f.write('plotting_option = ' + s.plotting_option + '\n')

                    f.write('@@data_source = DataSource\n')
                    f.write('source_type = ' + str(s.data_source.source_type) + '\n')
                    f.write('model_directory = ' + s.data_source.model_directory + '\n')
                    f.write('initial_filename = ' + s.data_source.initial_filename + '\n')
                    f.write('output_file_type = ' + s.data_source.output_file_type + '\n')
                    f.write('unit_conversion_flag = ' + str(s.data_source.unit_conversion_flag) + '\n')
                    f.write('data_filename_csv = ' + s.data_source.data_filename_csv + '\n')
                    f.write('@data_source\n')
                    if isinstance(s.edit_feature, BarEditFeature):
                        f.write('@@edit_feature = BarEditFeature\n')
                        f.write('color = ' + s.edit_feature.color + '\n')
                        f.write('edge_color = ' + s.edit_feature.edge_color + '\n')
                        f.write('line_style = ' + s.edit_feature.line_style + '\n')
                        f.write('line_width = ' + str(s.edit_feature.line_width) + '\n')
                        f.write('hatch = ' + s.edit_feature.hatch + '\n')
                        f.write('@edit_feature\n')
                    elif isinstance(s.edit_feature, LineEditFeature):
                        f.write('@@edit_feature = LineEditFeature\n')
                        f.write('style = ' + s.edit_feature.style + '\n')
                        f.write('color = ' + s.edit_feature.color + '\n')
                        f.write('line_width = ' + str(s.edit_feature.line_width) + '\n')
                        f.write('show_marker = ' + str(s.edit_feature.show_marker) + '\n')
                        f.write('marker = ' + s.edit_feature.marker + '\n')
                        f.write('marker_size = ' + str(s.edit_feature.marker_size) + '\n')
                        f.write('@edit_feature\n')
                    elif isinstance(s.edit_feature, PointEditFeature):
                        f.write('@@edit_feature = PointEditFeature\n')
                        f.write('point_style = ' + s.edit_feature.point_style + '\n')
                        f.write('face_color = ' + s.edit_feature.face_color + '\n')
                        f.write('size = ' + str(s.edit_feature.size) + '\n')
                        f.write('edge_color = ' + s.edit_feature.edge_color + '\n')
                        f.write('edge_line_width = ' + str(s.edit_feature.edge_line_width) + '\n')
                        f.write('@edit_feature\n')
                    elif isinstance(s.edit_feature, PieEditFeature):
                        f.write('@@edit_feature = PieEditFeature\n')
                        temp = str(s.edit_feature.color).replace('[','').replace(']','')
                        f.write('color = ' + temp + '\n')
                        f.write('start_angle = ' + str(s.edit_feature.start_angle) + '\n')
                        f.write('shadow = ' + str(s.edit_feature.shadow) + '\n')
                        f.write('radius = ' + str(s.edit_feature.radius) + '\n')
                        f.write('explode = ' + str(s.edit_feature.explode) + '\n')
                        f.write('explode_maximum = ' + str(s.edit_feature.explode_maximum) + '\n')
                        f.write('label_distance = ' + str(s.edit_feature.label_distance) + '\n')
                        f.write('show_value_label = ' + str(s.edit_feature.show_value_label) + '\n')
                        f.write('@edit_feature\n')
                    f.write('@series\n')
                f.write('@plot\n')
            f.write('@model_graph\n')
        except Exception as ex:
            print(ex)
            return False
        finally:
            try:f.close()
            except:pass
        return True

    @staticmethod
    def read_graph_template(filename):
        f = None
        try:
            f = open(filename, 'r')

            for line in f:
                line = line.strip().strip('\t').strip('\n').strip('\r')
                if line == '@@model_graph':
                    mg = ModelGraph('')
                    for line in f:
                        temp = line.strip().strip('\t').strip('\n').strip('\r')
                        temp = temp.split(' = ')

                        key, val = '', ''
                        if len(temp) == 2:
                            key = temp[0].strip()
                            val = temp[1].strip()
                        elif len(temp) == 1:
                            key = temp[0].strip()

                        if key == '@model_graph':
                            return mg
                        elif key == 'graph_title': mg.graph_title = val
                        elif key == 'no_of_plot': mg.no_of_plot = int(val)
                        elif key == 'plot_orientation_col': mg.plot_orientation_col = int(val)
                        elif key == 'plot_orientation_row': mg.plot_orientation_row = int(val)
                        elif key == '@@edit_feature' and val == 'FigureEditFeature':
                            ef = FigureEditFeature()
                            for line in f:
                                temp = line.strip().strip('\t').strip('\n').strip('\r')
                                temp = temp.split(' = ')

                                key, val = '', ''
                                if len(temp) == 2:
                                    key = temp[0].strip()
                                    val = temp[1].strip()
                                elif len(temp) == 1:
                                    key = temp[0].strip()

                                if key == '@edit_feature':
                                    mg.edit_feature = ef
                                    break
                                elif key == 'window_text': ef.window_text = val
                                elif key == 'faceColor': ef.faceColor = val
                                elif key == 'width': ef.width = int(val)
                                elif key == 'height': ef.height = int(val)
                                elif key == 'showMaximized':
                                    if val.lower() == 'true': ef.showMaximized = True
                                    else: ef.showMaximized = False
                                elif key == 'show_figure_title':
                                    if val.lower() == 'true': ef.show_figure_title = True
                                    else: ef.show_figure_title = False
                                elif key == 'font_size': ef.font_size = float(val)
                                elif key == 'font_color': ef.font_color = val
                                elif key == 'show_bold':
                                    if val.lower() == 'true': ef.show_bold = True
                                    else: ef.show_bold = False
                                elif key == 'horizontal_alignment': ef.horizontal_alignment = val
                        elif key == '@@plot':
                            p = ModelPlot('', -1)
                            for line in f:
                                temp = line.strip().strip('\t').strip('\n').strip('\r')
                                temp = temp.split(' = ')

                                key, val = '', ''
                                if len(temp) == 2:
                                    key = temp[0].strip()
                                    val = temp[1].strip()
                                elif len(temp) == 1:
                                    key = temp[0].strip()

                                if key == '@plot':
                                    mg.list_of_plot.append(p)
                                    break
                                elif key == 'plot_title': p.plot_title = val
                                elif key == 'plot_position': p.plot_position = int(val)
                                elif key == 'show_x_label':
                                    if val.lower() == 'true': p.show_x_label = True
                                    else: p.show_x_label = False
                                elif key == 'show_y_label':
                                    if val.lower() == 'true': p.show_y_label = True
                                    else: p.show_y_label = False
                                elif key == 'x_label': p.x_label = val
                                elif key == 'y_label': p.y_label = val
                                elif key == 'show_x_ticks':
                                    if val.lower() == 'true': p.show_x_ticks = True
                                    else: p.show_x_ticks = False
                                elif key == 'x_ticks_rotation': p.x_ticks_rotation = float(val)
                                elif key ==  'show_legend':
                                    if val.lower() == 'true': p.show_legend = True
                                    else: p.show_legend = False
                                elif key == 'legend_vertical_position': p.legend_vertical_position = int(val)
                                elif key == 'legend_horizontal_position': p.legend_horizontal_position = int(val)
                                elif key == '@@edit_feature':
                                    ef = PlotEditFeature()
                                    for line in f:
                                        temp = line.strip().strip('\t').strip('\n').strip('\r')
                                        temp = temp.split(' = ')

                                        key, val = '', ''
                                        if len(temp) == 2:
                                            key = temp[0].strip()
                                            val = temp[1].strip()
                                        elif len(temp) == 1:
                                            key = temp[0].strip()
                                        if key == '@edit_feature':
                                            p.edit_feature = ef
                                            break
                                        elif key == 'backgroundColor': ef.backgroundColor = val
                                        elif key == 'x_lim_max':
                                            try: ef.x_lim_max = float(val)
                                            except: ef.x_lim_max = parser.parse(val)
                                        elif key == 'x_lim_min':
                                            try: ef.x_lim_min = float(val)
                                            except: ef.x_lim_min = parser.parse(val)
                                        elif key == 'y_lim_max': ef.y_lim_max = float(val)
                                        elif key == 'y_lim_min': ef.y_lim_min = float(val)
                                        elif key == 'x_axis_major_interval': ef.x_axis_major_interval = float(val)
                                        elif key == 'x_axis_minor_interval': ef.x_axis_minor_interval = float(val)
                                        elif key == 'y_axis_major_interval': ef.y_axis_major_interval = float(val)
                                        elif key == 'y_axis_minor_interval': ef.y_axis_minor_interval = float(val)
                                        elif key == 'grid_show':
                                            if val.lower() == 'true': ef.grid_show = True
                                            else: ef.grid_show = False
                                        elif key == 'grid_axis_option': ef.grid_axis_option = val
                                        elif key == 'grid_which_option': ef.grid_which_option = val
                                        elif key == 'show_plot_title':
                                            if val.lower() == 'true': ef.show_plot_title = True
                                            else: ef.show_plot_title = False
                                        elif key == 'title_font_size': ef.title_font_size = float(val)
                                        elif key ==  'title_font_color': ef.title_font_color = val
                                        elif key == 'title_show_bold':
                                            if val.lower() == 'true': ef.title_show_bold = True
                                            else: ef.title_show_bold = False
                                        elif key == 'horizontal_alignment': ef.horizontal_alignment = val
                                elif key == '@@series':
                                    s = DataSeries('')
                                    for line in f:
                                        temp = line.strip().strip('\t').strip('\n').strip('\r')
                                        temp = temp.split(' = ')

                                        key, val = '', ''
                                        if len(temp) == 2:
                                            key = temp[0].strip()
                                            val = temp[1].strip()
                                        elif len(temp) == 1:
                                            key = temp[0].strip()

                                        if key == '@series':
                                            p.list_of_series.append(s)
                                            break
                                        elif key == 'attribute_name': s.attribute_name = val
                                        elif key == 'series_title': s.series_title = val
                                        elif key == 'x_axis_variable': s.x_axis_variable = val
                                        elif key == 'filter_variable': s.filter_variable = val
                                        elif key == 'filter_condition': s.filter_condition = val
                                        elif key == 'filter_first_value':
                                            if val.lower() == 'none': s.filter_first_value = None
                                            else:
                                                try: s.filter_first_value = float(val)
                                                except: s.filter_first_value = parser.parse(val)
                                        elif key == 'filter_second_value':
                                            if val.lower() == 'none': s.filter_second_value = None
                                            else:
                                                try: s.filter_second_value = float(val)
                                                except: s.filter_second_value = parser.parse(val)
                                        elif key == 'plotting_option': s.plotting_option = val
                                        elif key == '@@data_source':
                                            ds = DataSource()
                                            for line in f:
                                                temp = line.strip().strip('\t').strip('\n').strip('\r')
                                                temp = temp.split(' = ')

                                                key, val = '', ''
                                                if len(temp) == 2:
                                                    key = temp[0].strip()
                                                    val = temp[1].strip()
                                                elif len(temp) == 1:
                                                    key = temp[0].strip()

                                                if key == '@data_source':
                                                    s.data_source = ds
                                                    break
                                                elif key == 'source_type': ds.source_type = int(val)
                                                elif key == 'model_directory': ds.model_directory = val
                                                elif key == 'initial_filename': ds.initial_filename = val
                                                elif key == 'output_file_type': ds.output_file_type = val
                                                elif key == 'unit_conversion_flag':
                                                    if val.lower() == 'true': ds.unit_conversion_flag = True
                                                    else: ds.unit_conversion_flag = False
                                                elif 'data_filename_csv': ds.data_filename_csv = val
                                        elif key == '@@edit_feature' and val == 'BarEditFeature':
                                            ef = BarEditFeature()
                                            for line in f:
                                                temp = line.strip().strip('\t').strip('\n').strip('\r')
                                                temp = temp.split(' = ')

                                                key, val = '', ''
                                                if len(temp) == 2:
                                                    key = temp[0].strip()
                                                    val = temp[1].strip()
                                                elif len(temp) == 1:
                                                    key = temp[0].strip()

                                                if key == '@edit_feature':
                                                    s.edit_feature = ef
                                                    break
                                                elif key == 'color': ef.color = val
                                                elif key == 'edge_color': ef.edge_color = val
                                                elif key == 'line_style': ef.line_style = val
                                                elif key == 'line_width': ef.line_width = float(val)
                                                elif key == 'hatch': ef.hatch = val
                                        elif key == '@@edit_feature' and val == 'LineEditFeature':
                                            ef = LineEditFeature()
                                            for line in f:
                                                temp = line.strip().strip('\t').strip('\n').strip('\r')
                                                temp = temp.split(' = ')

                                                key, val = '', ''
                                                if len(temp) == 2:
                                                    key = temp[0].strip()
                                                    val = temp[1].strip()
                                                elif len(temp) == 1:
                                                    key = temp[0].strip()

                                                if key == '@edit_feature':
                                                    s.edit_feature = ef
                                                    break
                                                elif key == 'style': ef.style = val
                                                elif key == 'color': ef.color = val
                                                elif key == 'line_width': ef.line_width = float(val)
                                                elif key == 'show_marker':
                                                    if val.lower() == 'true': ef.show_marker = True
                                                    else: ef.show_marker = False
                                                elif key == 'marker': ef.marker = val
                                                elif key == 'marker_size': ef.marker_size = float(val)
                                        elif key == '@@edit_feature' and val == 'PointEditFeature':
                                            ef = PointEditFeature()
                                            for line in f:
                                                temp = line.strip().strip('\t').strip('\n').strip('\r')
                                                temp = temp.split(' = ')

                                                key, val = '', ''
                                                if len(temp) == 2:
                                                    key = temp[0].strip()
                                                    val = temp[1].strip()
                                                elif len(temp) == 1:
                                                    key = temp[0].strip()

                                                if key == '@edit_feature':
                                                    s.edit_feature = ef
                                                    break
                                                elif key == 'point_style': ef.point_style = val
                                                elif key == 'face_color': ef.face_color = val
                                                elif key == 'size': ef.size = float(val)
                                                elif key == 'edge_color': ef.edge_color = val
                                                elif key == 'edge_line_width': ef.edge_line_width = float(val)
                                        elif key == '@@edit_feature' and val == 'PieEditFeature':
                                            ef = PieEditFeature()
                                            for line in f:
                                                temp = line.strip().strip('\t').strip('\n').strip('\r')
                                                temp = temp.split(' = ')

                                                key, val = '', ''
                                                if len(temp) == 2:
                                                    key = temp[0].strip()
                                                    val = temp[1].strip()
                                                elif len(temp) == 1:
                                                    key = temp[0].strip()

                                                if key == '@edit_feature':
                                                    s.edit_feature = ef
                                                    break
                                                elif key == 'color':
                                                    temp = val.split(',')
                                                    for t in temp: t = t.strip()
                                                    ef.color = temp
                                                elif key == 'start_angle': ef.start_angle = float(val)
                                                elif key == 'shadow':
                                                    if val.lower() == 'true': ef.shadow = True
                                                    else: ef.shadow = False
                                                elif key == 'radius': ef.radius = float(val)
                                                elif key ==  'explode': efexplode = float(val)
                                                elif key == 'explode_maximum':
                                                    if val.lower() == 'true': ef.explode_maximum = True
                                                    else: ef.explode_maximum = False
                                                elif key == 'label_distance': ef.label_distance = float(val)
                                                elif key == 'show_value_label':
                                                    if val.lower() == 'true': ef.show_value_label = True
                                                    else: ef.show_value_label = False
        except Exception as ex:
            print(ex)
        finally:
            try:f.close()
            except:pass

        return None

    @staticmethod
    def save_as_binary_template(model_graph, file_name, save_no_series_data=False):
        succeed = False

        if save_no_series_data:
            for plot in model_graph.list_of_plot:
                for series in plot.list_of_series:
                    series.series_data = None
                    series.x_axis_data = None

        if len(file_name) > 0:
            output = None
            try:
                output = open(file_name, 'wb')
                pickle.dump(model_graph, output, pickle.HIGHEST_PROTOCOL)
                succeed = True
            except: pass
            finally:
                try:
                    output.close()
                except: pass
        return succeed

    @staticmethod
    def read_binary_template_list():
        target_directory = os.path.join(ApplicationProperty.getScriptPath(), "graphs")
        template_list = [f for f in os.listdir(target_directory) if f.lower().find(".gtm") != -1 and os.path.isfile(os.path.join(target_directory,f)) ]
        if len(template_list) > 0: return template_list
        else: return []

    @staticmethod
    def load_binary_template(file_name):
        model_obj = None

        if len(file_name) > 0:
            model_obj_file = None
            try:
                model_obj_file = open(file_name, 'rb')
                model_obj = pickle.load(model_obj_file)
            except Exception as ex: print(ex.args)
            finally:
                try:
                    model_obj_file.close()
                except: pass

        return model_obj

    @staticmethod
    def data_source_file_names(model_graph):
        source_file_list = []

        if model_graph is not None:
            for plot in model_graph.list_of_plot:
                for series in plot.list_of_series:
                    file_name = ""
                    if series.data_source.get_source_type() == 0:
                        file_name = series.data_source.get_initial_filepath()
                    else: file_name = series.data_source.get_csv_filename()

                    if len(file_name) > 0:
                        if file_name not in source_file_list: source_file_list.append(file_name)
        return source_file_list

    @staticmethod
    def change_data_source(model_graph, old_file_name, new_file_name):
        succeed = False
        if model_graph and old_file_name and new_file_name:
            for plot in model_graph.list_of_plot:
                for series in plot.list_of_series:
                    if series.data_source.change_data_source(old_file_name, new_file_name):
                        succeed = True
        return succeed

    @staticmethod
    def read_data_from_source_file(model_graph):
        '''
        Because the data reading and processing is time consuming, specially in case of model output, it is required
        to limit reading time as low as possible. That means when multiple data series use the same source file,
        the file should only be read once. For this purpose, first a list of file will be generated along with the
        variables to be read in, and then each file will be read and data will be assigned to data series.

        '''

        #reading model output files
        #step-1: collecting required information (initial file names, file type to be read in, unit conversion info etc)
        init_file_list = []              #structure: 1D [init file1, init file2]
        file_type_list_2b_read_in = []   #structure: 2D [[output file list for init file1], [output file list for init file2],..]
        var_list_2b_picked = []          #structure: 4D [[[[var list if ucf=True], [var list if ucf=False]]],[[[]]],..]

        for plot in model_graph.list_of_plot:
            for series in plot.list_of_series:

                if series.data_source.get_source_type() == 0:
                    init_file = series.data_source.get_initial_filepath()
                    if init_file not in init_file_list: init_file_list.append(init_file)

                    ndx_init_file = init_file_list.index(init_file)
                    file_type = series.data_source.get_output_filetype()
                    if len(file_type_list_2b_read_in) == ndx_init_file: file_type_list_2b_read_in.append([file_type])
                    else:
                        if file_type not in file_type_list_2b_read_in[ndx_init_file]:
                            file_type_list_2b_read_in[ndx_init_file].append(file_type)

                    ndx_file_type = file_type_list_2b_read_in[ndx_init_file].index(file_type)
                    ucf = series.data_source.get_unit_conversion_flag()

                    var_list = []
                    var_list.append(series.attribute_name)
                    if len(series.x_axis_variable) > 0:
                        if series.x_axis_variable not in var_list: var_list.append(series.x_axis_variable)
                    if len(series.filter_variable):
                        if series.filter_variable not in var_list: var_list.append(series.filter_variable)

                    if len(var_list_2b_picked) == ndx_init_file:
                        if ucf: var_list_2b_picked.append([[var_list,[]]])
                        else: var_list_2b_picked.append([[[],var_list]])
                    elif len(var_list_2b_picked[ndx_init_file]) == ndx_file_type:
                        if ucf: var_list_2b_picked[ndx_init_file].append([var_list, []])
                        else: var_list_2b_picked[ndx_init_file].append([],var_list)
                    else:
                        if ucf:
                            for var_name in var_list:
                                if var_name not in var_list_2b_picked[ndx_init_file][ndx_file_type][0]:
                                    var_list_2b_picked[ndx_init_file][ndx_file_type][0].append(var_name)
                        else:
                            for var_name in var_list:
                                if var_name not in var_list_2b_picked[ndx_init_file][ndx_file_type][1]:
                                    var_list_2b_picked[ndx_init_file][ndx_file_type][1].append(var_name)

        #step-2: reading model output
        data = ReadBinaryOutput.ReadModelOutput_for_graph(init_file_list, file_type_list_2b_read_in, var_list_2b_picked)
        #remarks: structure of data is exactly the same as var_list_2b_picked, only the difference is instead of variable
        #name the data list is saved inside data

        #step-3: assigning data to appropriate data series
        for plot in model_graph.list_of_plot:
            for series in plot.list_of_series:
                if series.data_source.get_source_type() == 0:
                    init_file = series.data_source.get_initial_filepath()
                    file_type = series.data_source.get_output_filetype()

                    ucf = series.data_source.get_unit_conversion_flag()

                    ndx_init_file = init_file_list.index(init_file)
                    ndx_file_type = file_type_list_2b_read_in[ndx_init_file].index(file_type)

                    if ucf: ndx_ufc = 0
                    else: ndx_ufc = 1

                    ndx_var_name = var_list_2b_picked[ndx_init_file][ndx_file_type][ndx_ufc].index(series.attribute_name)
                    series.series_data = deepcopy(data[ndx_init_file][ndx_file_type][ndx_ufc][ndx_var_name])

                    if len(series.x_axis_variable) > 0:
                        ndx_var_name = var_list_2b_picked[ndx_init_file][ndx_file_type][ndx_ufc].index(series.x_axis_variable)
                        series.x_axis_data = deepcopy(data[ndx_init_file][ndx_file_type][ndx_ufc][ndx_var_name])

                    if len(series.filter_variable) > 0:
                        if series.filter_variable != series.x_axis_variable:
                            ndx_var_name = var_list_2b_picked[ndx_init_file][ndx_file_type][ndx_ufc].index(series.filter_variable)
                            filtering_RL = deepcopy(data[ndx_init_file][ndx_file_type][ndx_ufc][ndx_var_name])

                            if len(series.x_axis_variable) > 0:
                                ReadBinaryOutput.Filter([series.series_data, series.x_axis_data, filtering_RL], 2, series.filter_condition, series.filter_first_value, series.filter_second_value)
                            else: ReadBinaryOutput.Filter([series.series_data, filtering_RL], 1, series.filter_condition, series.filter_first_value, series.filter_second_value)
                        else:
                            ReadBinaryOutput.Filter([series.series_data, series.x_axis_data], 1, series.filter_condition, series.filter_first_value, series.filter_second_value)

                    #special case for stem carbon
                    #Attention!!
                    #this code block has been used in ''. any modification should be carried out both the places
                    if series.attribute_name in ['cs_vegt_cum_harvest_stem_tot', 'cs_vegt_stem_harvest_stem_tot_cum']:
                        model_directory = series.data_source.get_model_directory()
                        init_filename = series.data_source.get_initial_filename()
                        rc_list = ['cf_vegt_harvest_stem_tot', 'year']
                        rc = ReadBinaryOutput.SpecialDataFieldsFromOutputFile(model_directory, init_filename, 'annavg_veg', rc_list)

                        start_year = min(series.x_axis_data)
                        if series.attribute_name == 'cs_vegt_stem_harvest_stem_tot_cum':
                            rc_list.append('cs_vegt_sum_stem')
                            if 'cs_vegt_sum_stem' in var_list_2b_picked[ndx_init_file][ndx_file_type][ndx_ufc]:
                                ndx_var_name = var_list_2b_picked[ndx_init_file][ndx_file_type][ndx_ufc].index(series.attribute_name)
                                rc.append(deepcopy(data[ndx_init_file][ndx_file_type][ndx_ufc][ndx_var_name]))
                            else:
                                rc.append(ReadBinaryOutput.SpecialDataFieldsFromOutputFile(model_directory, init_filename, 'annavg', 'cs_vegt_sum_stem'))
                            series.series_data = ReadBinaryOutput.RecalculateStemGrowth(start_year, rc_list, rc)[1]
                        else: series.series_data = ReadBinaryOutput.RecalculateStemGrowth(start_year, rc_list, rc)[0]

        #reading external files (csv)
        #step-1: collecting required information
        list_of_ext_file = []
        list_of_var_ext = []
        for plot in model_graph.list_of_plot:
            for series in plot.list_of_series:
                if series.data_source.get_source_type() == 1:
                    source_file = series.data_source.get_csv_filename()
                    if source_file not in list_of_ext_file: list_of_ext_file.append(source_file)

                    ndx_ext_file = list_of_ext_file.index(source_file)

                    # var_list = []
                    # var_list.append(series.attribute_name)
                    # if len(series.x_axis_variable) > 0:
                    #     if series.x_axis_variable not in var_list: var_list.append(series.x_axis_variable)
                    # if series.group_flag:
                    #     for grp_var in series.group_variables:
                    #         if grp_var not in var_list: var_list.append(grp_var)
                    #
                    if len(list_of_var_ext) == ndx_ext_file:
                        list_of_var_ext.append([series.attribute_name])
                    else:
                        if series.attribute_name not in list_of_var_ext[ndx_ext_file]:
                            list_of_var_ext[ndx_ext_file].append(series.attribute_name)

                    if len(series.x_axis_variable) > 0:
                        if series.x_axis_variable not in list_of_var_ext[ndx_ext_file]:
                            list_of_var_ext[ndx_ext_file].append(series.x_axis_variable)

                    if len(series.filter_variable) > 0:
                        if series.filter_variable not in list_of_var_ext[ndx_ext_file]:
                            list_of_var_ext[ndx_ext_file].append(series.filter_variable)

        #epecial processing if required
        # for plot in model_graph.list_of_plot:
        #     for series in plot.list_of_series:
        #         if series.attribute_name == 'epv_vegt_proj_lai' and series.data_source.output_file_type == ''


        #step-2: reading external files
        data_ext = deepcopy(list_of_var_ext)
        for i in range(len(list_of_ext_file)):
            ext_file = list_of_ext_file[i]
            result_lit_ext = ReadExternalOutput.ReadCSV(ext_file,",")
            header_variable_ext = result_lit_ext[0]
            record_list_ext = result_lit_ext[1]
            for j in range(len(list_of_var_ext[i])):
                var_name = list_of_var_ext[i][j]

                data_ext[i][j] = ReadBinaryOutput.ExtractColumnRecord(var_name, header_variable_ext, record_list_ext)

        #step-3: assigning data to series data
        for plot in model_graph.list_of_plot:
            for series in plot.list_of_series:
                if series.data_source.get_source_type() == 1:
                    source_file = series.data_source.get_csv_filename()
                    ndx_ext_file = list_of_ext_file.index(source_file)

                    var_ndx = list_of_var_ext[ndx_ext_file].index(series.attribute_name)
                    series.series_data = deepcopy(data_ext[ndx_ext_file][var_ndx])

                    if len(series.x_axis_variable) > 0:
                        var_ndx = list_of_var_ext[ndx_ext_file].index(series.x_axis_variable)
                        series.x_axis_data = deepcopy(data_ext[ndx_ext_file][var_ndx])

                    if len(series.filter_variable) > 0:
                        if series.filter_variable != series.x_axis_variable: # and series.filter_variable != series.attribute_name:
                            var_ndx = list_of_var_ext[ndx_ext_file].index(series.filter_variable)
                            filtering_RL = deepcopy(data_ext[ndx_ext_file][var_ndx])

                            if len(series.x_axis_variable) > 0:
                                ReadBinaryOutput.Filter([series.series_data, series.x_axis_data, filtering_RL], 2, series.filter_condition, series.filter_first_value, series.filter_second_value)
                            else: ReadBinaryOutput.Filter([series.series_data, filtering_RL], 1, series.filter_condition, series.filter_first_value, series.filter_second_value)
                        else:
                            ReadBinaryOutput.Filter([series.series_data, series.x_axis_data], 1, series.filter_condition, series.filter_first_value, series.filter_second_value)



    @staticmethod
    def read_data_from_specific_model_output(model_graph, model_directory, initial_filename):

        #collecting information from graph object
        list_of_output_filetype = []
        list_of_ucf_for_each_file = []

        for plot in model_graph.list_of_plot:
            for series in plot.list_of_series:
                if series.data_source.initial_filename == initial_filename:
                    output_filetype = series.data_source.get_output_filetype()
                    ucf = series.data_source.get_unit_conversion_flag()
                    if output_filetype in list_of_output_filetype:
                        file_type_index = list_of_output_filetype.index(output_filetype)
                        if not (list_of_ucf_for_each_file[file_type_index] == ucf):
                            list_of_output_filetype.append(output_filetype)
                            list_of_ucf_for_each_file.append(ucf)
                    else:
                        list_of_output_filetype.append(output_filetype)
                        list_of_ucf_for_each_file.append(ucf)

        count = 0
        #reading data from output files and assigning data
        for i in range(len(list_of_output_filetype)):
            file_type = list_of_output_filetype[i]
            ucf = list_of_ucf_for_each_file[i]

            output_data = ReadBinaryOutput.ReadModelOutput(model_directory, initial_filename, file_type, trim=True, post_processing=True, ucf=ucf)
            for plot in model_graph.list_of_plot:
                for series in plot.list_of_series:
                    if (series.data_source.initial_filename == initial_filename and
                        series.data_source.get_output_filetype() == file_type and
                        series.data_source.get_unit_conversion_flag() == ucf):
                        count += 1

                        series.series_data = ReadBinaryOutput.ExtractColumnRecord(series.attribute_name, output_data.get_header_variable(), output_data.get_record_list())
                        if series.x_axis_variable:
                            series.x_axis_data = ReadBinaryOutput.ExtractColumnRecord(series.x_axis_variable, output_data.get_header_variable(), output_data.get_record_list())

                        if series.filter_variable:
                            filter_data = ReadBinaryOutput.ExtractColumnRecord(series.filter_variable, output_data.get_header_variable(), output_data.get_record_list())

                            if series.x_axis_variable:
                                ReadBinaryOutput.Filter([series.series_data, series.x_axis_data, filter_data], 2, series.filter_condition, series.filter_first_value, series.filter_second_value)
                            else: ReadBinaryOutput.Filter([series.series_data, filter_data], 1, series.filter_condition, series.filter_first_value, series.filter_second_value)

        if count > 0: return True
        else: return False



class ModelPlot():
    def __init__(self, title, position):
        self.plot_title = title
        self.plot_position = position

        self.show_x_label = False
        self.show_y_label = False
        self.x_label = ""
        self.y_label = ""

        # self.x_min = 0
        # self.x_max = 20
        # self.y_min = 0
        # self.y_max = 2

        self.show_x_ticks = False
        self.x_ticks_rotation = 0

        self.show_legend = False
        self.legend_vertical_position = 1       #position: -1=Low 0=Mid 1 = top
        self.legend_horizontal_position = 1     #position: -1=Left 0=Mid 1 = Right

        self.list_of_series = []

        self.edit_feature = PlotEditFeature()

    def add_series(self, series):
        #when a new series is added few things need to be checked. (i) if the series attribute name is the same as one of the
        #existing series, if so (a) whether the data source is the same for these series, or (b) if the plotting option is the same.
        #if both the series come from same source, but plotting options are different, the program can accept but in that case the title of
        #the newly added title should have a suffix like "_P02"; if they come from different sources but the attribute names are the same;
        #the program also accept the new series with giving a suffix at the end of tile like "_S02". But the program cannot accept
        #two series coming from the same source, with same attribute (field name) and having same plotting option.
        accept = False

        if series is not None:
            index_list = []
            for i in range(len(self.list_of_series)):
                if self.list_of_series[i].attribute_name == series.attribute_name: index_list.append(i)

            count = len(index_list)

            if len(index_list) > 0:
                #check data source
                for i in reversed(range(len(index_list))):
                    if not DataSource.compare_data_source(self.list_of_series[index_list[i]].data_source, series.data_source): index_list.pop(i)

                if len(index_list) > 0:
                    #check plotting option
                    for i in reversed(range(len(index_list))):
                        if self.list_of_series[index_list[i]].plotting_option != series.plotting_option: index_list.pop(i)

                    if len(index_list) > 0: accept = False
                    else:
                        for sr in self.list_of_series:
                            if (sr.attribute_name == series.attribute_name) and (sr.series_title == series.series_title):
                                series.series_title = series.series_title + "_P" + str(count + 1)
                                break
                        accept = True
                else:
                    for sr in self.list_of_series:
                            if (sr.attribute_name == series.attribute_name) and (sr.series_title == series.series_title):
                                series.series_title = series.series_title + "_S" + str(count + 1)
                                break
                    accept = True
            else: accept = True

            if accept:
                self.list_of_series.append(series)
                self.calculate_axes_limit()
        return accept


    def delete_series(self, series):
        if series is not None:
            for i in range(len(self.list_of_series)):
                if self.list_of_series[i].attribute_name == series.attribute_name:
                    self.list_of_series.pop(i)
                    return True
        return False

    def calculate_axes_limit(self):
        # y-axis values are always numeric, therefore min and max functions can be used to find the limit of that axis. But
        # x-axis values can be of type numeric or string, moreover different series can have different value types. so special
        # care is needed to find the x-axis limit.
        if len(self.list_of_series) > 0:
            y_max = None
            y_min = None

            x_max = None
            x_min = None

            is_numeric_x_data = True
            max_len_x_data = 0
            for series in self.list_of_series:
                temp = None
                if series.series_data:
                    temp_list = [y for y in series.series_data if y is not None]

                    temp = np.amax(temp_list)
                    if y_max is None or temp > y_max: y_max = temp

                    temp = np.amin(temp_list)
                    if y_min is None or temp < y_min: y_min = temp


                temp = None
                if series.x_axis_data:
                    if is_numeric_x_data:
                        temp_list = [y for y in series.x_axis_data if y is not None]
                        try: temp = np.amax(temp_list)
                        except:
                            is_numeric_x_data = False
                            max_len_x_data = len(series.x_axis_data)

                        if is_numeric_x_data and temp is not None:
                            if x_max is None or temp > x_max: x_max = temp
                            temp = np.amin(temp_list)
                            if x_min is None or temp < x_min: x_min = temp

            if y_max is not None and y_min is not None:
                self.edit_feature.setYAxisMinimumLimit(y_min - (y_max - y_min) * 0.2)
                self.edit_feature.setYAxisMaximumLimit(y_max + (y_max - y_min) * 0.4)

            if not is_numeric_x_data:
                self.edit_feature.setXAxisMaximumLimit(max_len_x_data)
                self.edit_feature.setXAxisMinimumLimit(0)
            elif x_max is not None and x_min is not None:
                self.edit_feature.setXAxisMaximumLimit(x_max)
                self.edit_feature.setXAxisMinimumLimit(x_min)

    def find_series_index(self, var_name):
        for i in range(len(self.list_of_series)):
            if self.list_of_series[i].attribute_name == var_name:
                return i
        return -1

    def find_series_by_var_name(self, var_name):
        if len(var_name) > 0:
            for series in self.list_of_series:
                if series.attribute_name == var_name:
                    return series
        return None

    def find_series_by_title(self, series_title):
        if series_title:
            for series in self.list_of_series:
                if series.series_title == series_title: return series
        return None

    def find_series_by_index(self, sr_index):
        if (sr_index > -1) and sr_index < len(self.list_of_series):
            return self.list_of_series[sr_index]
        else: return None

    def find_bar_series(self):
        bar_series = []
        for series in self.list_of_series:
            if series.plotting_option.lower() in ["bar", "stacked bar"]:
                bar_series.append(series)
        return bar_series

    def find_stacked_bar_option(self):
        stacked = False

        for series in self.list_of_series:
            if series.plotting_option.lower() == "stacked bar": stacked = True

        return stacked

    def find_line_series(self):
        line_series = []
        for series in self.list_of_series:
            if series.plotting_option.lower() == "line":
                line_series.append(series)
        return line_series

    def find_point_series(self):
        point_series = []
        for series in self.list_of_series:
            if series.plotting_option.lower() == "point":
                point_series.append(series)
        return point_series

    def find_pie_series(self):
        pie_series = []
        for series in self.list_of_series:
            if series.plotting_option.lower() == "pie":
                pie_series.append(series)
        return pie_series

    def find_scatter_plot_series(self):
        scatter_series = []
        for series in self.list_of_series:
            if series.plotting_option.lower() == "scatter plot":
                scatter_series.append(series)
        return scatter_series

    def legend_position_text(self):
        position_str = ""
        if self.legend_vertical_position == 1:
            position_str = "upper"
        elif self.legend_vertical_position == -1:
            position_str = "lower"
        else:
            pass

        if len(position_str) > 0:
            if self.legend_horizontal_position == 1:
                position_str += " right"
            elif self.legend_horizontal_position == 0:
                position_str += " center"
            else: position_str += " left"

        if len(position_str) > 0:
            return position_str
        else: return "upper right"

    # def add_series(self, series_data, graph_type, label=""):
    #     series = BgcDataSeries(series_data, graph_type)
    #     self.list_of_series.append(series)
    #     if self.sp is not None:
    #         if graph_type == 0:
    #             self.sp.plot(series_data, label=label)
    #         if graph_type == 1:
    #             x = np.arange(len(series_data))
    #             self.sp.bar(x,series_data, label=label)

class DataSeries():
    def __init__(self, field_name):
        self.attribute_name = field_name
        self.series_title = ""
        self.series_data = None

        self.x_axis_variable = ""
        self.x_axis_data = None

        self.filter_variable = ""
        self.filter_condition = ""
        self.filter_first_value = None
        self.filter_second_value = None

        self.plotting_option = ""
        self.data_source = DataSource()
        self.edit_feature = None

    def initializeEditFeature(self):
        plot_option = self.plotting_option.lower()

        if plot_option == "line":
            self.edit_feature = LineEditFeature()
        elif plot_option in ["bar", "histogram"]:
            self.edit_feature = BarEditFeature()
        elif plot_option in ["point", "scatter plot"]:
            self.edit_feature = PointEditFeature()
        elif plot_option == "pie":
            self.edit_feature = PieEditFeature()

    def setEditFeature(self, edit_feature):
        self.edit_feature = edit_feature

    def read_source_datafile(self):
        if self.data_source.source_type == 0:
            return ReadBinaryOutput.ReadModelOutput(self.data_source.model_directory, self.data_source.initial_filename, self.data_source.output_file_type, True, True, True)
        else:
            return ReadExternalOutput.read_csv_file(self.data_source.get_csv_filename(), ',')


    # @staticmethod
    # def series_comparison(series_1, series_2):
    #     result = False
    #     series_1 = DataSeries()
    #     attribute_1 = [series_1.attribute_name, series_1.series_title, series_1.series_data]

class DataSource():
    def __init__(self):
        self.source_type = 0  #source type: 0=Model output, 1=External Output

        #for model output
        self.model_directory = ""
        self.initial_filename = ""
        self.output_file_type = ""
        self.unit_conversion_flag = True

        #for external data
        self.data_filename_csv = ""

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



    def set_data_source(self, source_type, model_directory="", initial_filename="", output_filetype="", ucf=True, data_filename=""):
        self.source_type = source_type
        self.model_directory = model_directory
        self.initial_filename = initial_filename
        self.output_file_type = output_filetype
        self.unit_conversion_flag = ucf
        self.data_filename_csv = data_filename

    def get_source_type(self): return self.source_type
    def get_model_directory(self): return self.model_directory
    def get_initial_filename(self): return self.initial_filename
    def get_initial_filepath(self): return os.path.join(self.model_directory, "ini", self.initial_filename).replace("\\", "/")
    def get_output_filetype(self): return self.output_file_type
    def get_unit_conversion_flag(self): return self.unit_conversion_flag
    def get_csv_filename(self): return self.data_filename_csv.replace("\\", "/")

    def change_data_source(self, old_file_name, new_file_name):
        succeed = False
        if self.source_type == 0:
            if self.get_initial_filepath().lower() == old_file_name.lower():
                self.initial_filename = new_file_name
                succeed = True
        else:
            if self.get_csv_filename().lower() == old_file_name.lower():
                self.data_filename_csv = new_file_name
                succeed = True
        return succeed

    @staticmethod
    def compare_data_source(first_data_source, second_data_source):
        #returns true if both source is the same, otherwise false
        if first_data_source.source_type != second_data_source.source_type: return False
        else:
            if first_data_source.source_type == 0:
                if first_data_source.model_directory != second_data_source.model_directory: return False
                elif first_data_source.initial_filename != second_data_source.initial_filename: return False
                elif first_data_source.output_file_type != second_data_source.output_file_type: return False
                elif first_data_source.unit_conversion_flag != second_data_source.unit_conversion_flag: return False
                else: return True
            else:
                if first_data_source.data_filename_csv != second_data_source.data_filename_csv: return False
                else: return True

class PlotEditFeature:
    def __init__(self):
        self.backgroundColor = "#ffffff"

        self.x_lim_max = 20
        self.x_lim_min = 0
        self.y_lim_max = 2
        self.y_lim_min = 0

        self.x_axis_major_interval = 5
        self.x_axis_minor_interval = 1
        self.y_axis_major_interval = 0.5
        self.y_axis_minor_interval = 0.1

        self.grid_show = True
        self.grid_axis_option = "both"          #options: "x", "y", "both"
        self.grid_which_option = "major"        #options: "major", "minor", "both"

        #title
        self.show_plot_title = True
        self.title_font_size = 10
        self.title_font_color = "#000000"
        self.title_show_bold = False
        self.horizontal_alignment = "center"

    def getShowPlotTitle(self): return self.show_plot_title
    def getTitleFontSize(self): return self.title_font_size
    def getTitleFontColor(self): return self.title_font_color
    def getTitleBold(self): return self.title_show_bold
    def getTitleHorizontalAlignment(self): return self.horizontal_alignment


    def getBackgroundColor(self): return self.backgroundColor
    def getXAxisMaximumLimit(self): return self.x_lim_max
    def getXAxisMinimumLimit(self): return self.x_lim_min
    def getYAxisMaximumLimit(self): return self.y_lim_max
    def getYAxisMinimumLimit(self): return self.y_lim_min
    def getXAxisMajorInterval(self): return self.x_axis_major_interval
    def getXAxisMinorInterval(self): return self.x_axis_minor_interval
    def getYAxisMajorInterval(self): return self.y_axis_major_interval
    def getYAxisMinorInterval(self): return self.y_axis_minor_interval
    def getGridShowOption(self): return self.grid_show
    def getGridAxisOption(self): return self.grid_axis_option
    def getGridWhichOption(self): return self.grid_which_option

    def setBackgroundColor(self, htmlColorCode_str): self.backgroundColor = htmlColorCode_str
    def setXAxisMaximumLimit(self, lim_max): self.x_lim_max = lim_max
    def setXAxisMinimumLimit(self, lim_min): self.x_lim_min = lim_min
    def setYAxisMaximumLimit(self, lim_max):
        self.y_lim_max = lim_max
        self.y_axis_minor_interval = round((self.y_lim_max - self.y_lim_min) / 25, 2)
        self.y_axis_major_interval =  self.y_axis_minor_interval * 5

    def setYAxisMinimumLimit(self, lim_min): self.y_lim_min = lim_min
    def setXAxisMajorInterval(self, interval): self.x_axis_major_interval = interval
    def setXAxisMinorInterval(self, interval): self.x_axis_minor_interval = interval
    def setYAxisMajorInterval(self, interval): self.y_axis_major_interval = interval
    def setYAxisMinorInterval(self, interval): self.y_axis_minor_interval = interval
    def setGridShowOption(self, option_str): self.grid_show = option_str
    def setGridAxisOption(self, option_str): self.grid_axis_option = option_str
    def setGridWhichOption(self, option_str): self.grid_which_option = option_str

    def setShowPlotTitle(self, show_title_bol): self.show_plot_title = show_title_bol
    def setTitleFontSize(self, font_size_float): self.title_font_size = font_size_float
    def setTitleFontColor(self, htmlColor_str): self.title_font_color = htmlColor_str
    def setTitleBold(self, show_bold_bol): self.title_show_bold = show_bold_bol
    def setTitleHorizontalAlignment(self, alignment_str): self.horizontal_alignment = alignment_str

class FigureEditFeature:
    def __init__(self):
        self.window_text = "Biome BGC Graph"
        self.faceColor = "#ffffff"
        self.width = int(ApplicationProperty.getScreenWidth() * 0.8)         #in pixel
        self.height = int(ApplicationProperty.getScreenHeight() * 0.8)       #in pixel
        self.showMaximized = True

        self.show_figure_title = True
        self.font_size = 15
        self.font_color = "#000000"
        self.show_bold = True
        self.horizontal_alignment = "center"


    def setTitle(self, title): self.window_text = title
    def setFaceColor(self, htmlColorCode_str): self.faceColor = htmlColorCode_str
    def setWidth(self, width_pixel): self.width = width_pixel
    def setHeight(self, height_pixel): self.height = height_pixel
    def setShowFigureTitle(self, show_title_bol): self.show_figure_title = show_title_bol
    def setFontSize(self, font_size_float): self.font_size = font_size_float
    def setFontColor(self, htmlColor_str): self.font_color = htmlColor_str
    def setShowBold(self, bold_bol): self.show_bold = bold_bol
    def setHorizontalAlignment(self, alignment_str): self.horizontal_alignment = alignment_str

    def getTitle(self): return self.window_text
    def getFaceColor(self): return self.faceColor
    def getWidth(self): return self.width
    def getHeight(self): return self.height
    def getShowFigureTitle(self): return self.show_figure_title
    def getFontSize(self): return self.font_size
    def getFontColor(self): return self.font_color
    def getShowBold(self): return self.show_bold
    def getHorizontalAlignment(self): return self.horizontal_alignment

class PointEditFeature:
    def __init__(self):
        self.point_style = "o"
        self.face_color = "#ffffff"
        self.size = 5
        self.edge_color= "#000000"
        self.edge_line_width = 1


    def getPointStyle(self): return self.point_style
    def getFaceColor(self): return self.face_color
    def getSize(self): return self.size
    def getEdgeColor(self): return self.edge_color
    def getEdgeLineWidth(self): return self.edge_line_width


    def setPointStyle(self, style_str): self.point_style = style_str
    def setFaceColor(self, htmlColor_str): self.face_color = htmlColor_str
    def setSize(self, size_float): self.size = size_float
    def setEdgeColor(self, htmlColor_str): self.edge_color = htmlColor_str
    def setEdgeLineWidth(self, width_float): self.edge_line_width = width_float

class LineEditFeature:
    def __init__(self):
        self.style = "-"
        self.color = "#000000"
        self.line_width = 1
        self.show_marker = True
        self.marker = "o"
        self.marker_size = 3

    def getStyle(self): return self.style
    def getColor(self): return self.color
    def getLineWidth(self): return self.line_width
    def getShowMarker(self): return self.show_marker
    def getMarker(self): return self.marker
    def getMarkerSize(self): return self.marker_size

    def setStyle(self, line_style_str): self.style = line_style_str
    def setColor(self, htmlColor_str): self.color = htmlColor_str
    def setLineWidth(self, width_float): self.line_width = width_float
    def setShowMarker(self, show_marker_bol): self.show_marker = show_marker_bol
    def setMarker(self, marker_str): self.marker = marker_str
    def setMarkerSize(self, marker_size_int): self.marker_size = marker_size_int

class BarEditFeature:
    def __init__(self):
        self.color = "#ffffff"
        self.edge_color = "#000000"
        self.line_style = "solid"           #[solid | dashed | dashdot | dotted]
        self.line_width = 1
        self.hatch = ""                     #['/' | '\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*']

    def getColor(self): return self.color
    def getEdgeColor(self): return self.edge_color
    def getLineStyle(self): return self.line_style
    def getLineWidth(self): return self.line_width
    def getHatch(self): return self.hatch

    def setColor(self, htmlColor_str): self.color = htmlColor_str
    def setEdgeColor(self, htmlColor_str): self.edge_color = htmlColor_str
    def setLineStyle(self, line_style_str): self.line_style = line_style_str
    def setLineWidth(self, line_width_float): self.line_width = line_width_float
    def setHatch(self, hatch_str): self.hatch = hatch_str

class PieEditFeature:
    def __init__(self):
        self.color = []
        self.start_angle = 90
        self.shadow = False
        self.radius = 10
        self.explode = 0.1
        self.explode_maximum = True
        self.label_distance = 1.1
        self.show_value_label = False

    def getColor(self): return self.color
    def getStartAngel(self): return self.start_angle
    def getShadow(self): return self.shadow
    def getRadius(self): return self.radius
    def getExplodeDistance(self): return  self.explode
    def getExplodeMaximum(self): return self.explode_maximum
    def getLabelDistance(self): return self.label_distance
    def getShowValueLabel(self): return self.show_value_label

    def setColor(self, htmlColor_str_array): self.color = htmlColor_str_array
    def setStartAngel(self, angle_degree): self.start_angle = angle_degree
    def setShadow(self, shadow_bol): self.shadow = shadow_bol
    def setRadius(self, radius_float): self.radius = radius_float
    def setExplodeDistance(self, explode_distance_float): self.explode = explode_distance_float
    def setExplodeMaximum(self, explode_only_max_bol): self.explode_maximum = explode_only_max_bol
    def setLabelDistance(self, distance_float): self.label_distance = distance_float
    def setShowValueLabel(self, show_bol): self.show_value_label = show_bol

class BgcDataSeries():
    def __init__(self, series_data=[], graph_type=0):
        self.series_data = series_data
        self.graph_type = graph_type



class X_bar():
    def __init__(self, lim_min = 0, lim_max = 999, bar_title= "", tick_interval = 5, bar_tick_labels = None, tick_color = "black"):
        self.x_lim_min = lim_min
        self.x_lim_max = lim_max
        self.x_bar_title = bar_title
        self.x_bar_tick_interval = tick_interval
        self.x_bar_tick_labels = bar_tick_labels
        self.x_bar_tick_color = tick_color

    def set_bar(self, plot):
        if plot is not None:
            plot.xlim(self.x_lim_min, self.x_lim_max)
            bar_ticks = []
            if self.x_bar_tick_interval != 0:
                bar_ticks = np.arange(self.x_lim_min, self.x_lim_max, self.x_bar_tick_interval)
            else:
                bar_ticks = np.arange(self.x_lim_min, self.x_lim_max)

            if self.x_bar_tick_labels is not None and len(self.x_bar_tick_labels) == len(bar_ticks):
                plot.xticks(bar_ticks, self.x_bar_tick_labels, color=self.x_bar_tick_color)
            else:
                plot.xaxis.set_ticks(bar_ticks)

class Y_bar():
    def __init__(self, lim_min = 0, lim_max = 999, bar_title= "", tick_interval = 0, bar_tick_labels = None, tick_color = "black"):
        self.y_lim_min = lim_min
        self.y_lim_max = lim_max
        self.y_bar_title = bar_title
        self.y_bar_tick_interval = tick_interval
        self.y_bar_tick_labels = bar_tick_labels
        self.y_bar_tick_color = tick_color

    def set_bar(self, plot):
        if plot is not None:
            plot.xlim(self.y_lim_min, self.y_lim_max)
            bar_ticks = []
            if self.y_bar_tick_interval != 0:
                bar_ticks = np.arange(self.y_lim_min, self.y_lim_max, self.y_bar_tick_interval)
            else:
                bar_ticks = np.arange(self.y_lim_min, self.y_lim_max)

            if self.y_bar_tick_labels is not None and len(self.y_bar_tick_labels) == len(bar_ticks):
                plot.xticks(bar_ticks, self.y_bar_tick_labels, color=self.y_bar_tick_color)
            else:
                plot.xaxis.set_ticks(bar_ticks)


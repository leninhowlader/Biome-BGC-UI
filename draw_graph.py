import numpy as np
from application import ApplicationProperty
from copy import deepcopy
from datetime import datetime
from  matplotlib import pyplot

class BiomeBgcGraphDummy():
    @staticmethod
    def ShowGraph(model_graph, figure_no, display=True, save_file_filename=""):
        if model_graph is not None:
            fig = pyplot.figure(figure_no)
            # fig.setFacecolor("#ffffff")

            #set window title
            fig.canvas.set_window_title(model_graph.edit_feature.getTitle())
            #set figure face color
            fig.set_facecolor(model_graph.edit_feature.getFaceColor())

            #setting width and height
            mng = pyplot.get_current_fig_manager()
            size_format_str = str(model_graph.edit_feature.getWidth()) + "x" + str(model_graph.edit_feature.getHeight())
            fig_x_pos = (ApplicationProperty.getScreenWidth() - model_graph.edit_feature.getWidth())//2
            fig_y_pos = (ApplicationProperty.getScreenHeight() - model_graph.edit_feature.getHeight())//2
            mng.window.wm_geometry(size_format_str + "+" + str(fig_x_pos) + "+" + str(fig_y_pos))

            ef = model_graph.edit_feature
            if ef.getShowFigureTitle():
                if ef.getShowBold():
                    fig.suptitle(model_graph.graph_title, fontsize=ef.getFontSize(), color=ef.getFontColor(), fontweight='bold',
                                 horizontalalignment=ef.getHorizontalAlignment())
                else:
                    fig.suptitle(model_graph.graph_title, fontsize=ef.getFontSize(), color=ef.getFontColor(),
                                 horizontalalignment=ef.getHorizontalAlignment())

            for plot in model_graph.list_of_plot:
                ax = fig.add_subplot(model_graph.plot_orientation_col, model_graph.plot_orientation_row, plot.plot_position)

                ef = plot.edit_feature
                if ef.getShowPlotTitle():
                    if ef.getTitleBold():
                        ax.set_title(plot.plot_title, fontsize=ef.getTitleFontSize(), color=ef.getTitleFontColor(),
                                     fontweight='bold', horizontalalignment=ef.getTitleHorizontalAlignment())
                    else: ax.set_title(plot.plot_title, fontsize=ef.getTitleFontSize(), color=ef.getTitleFontColor(),
                                       horizontalalignment=ef.getTitleHorizontalAlignment())


                #drawing pie if there is any
                pie_series = plot.find_pie_series()
                if len(pie_series) > 0:
                    series = pie_series[0]
                    pie_size = deepcopy(series.series_data)
                    pie_label = deepcopy(series.x_axis_data)

                    #delete None values
                    if pie_label is not None and len(pie_size) == len(pie_label):
                        for i in reversed(range(len(pie_size))):
                            if pie_size[i] is None:
                                pie_size.pop(i)
                                pie_label.pop(i)
                    else:
                        for i in reversed(range(len(pie_size))):
                            if pie_size[i] is None: pie_size.pop(i)
                        pie_label = np.arange(1, len(pie_size) + 1)

                    ef = series.edit_feature

                    if ef is not None:
                        color = ef.getColor()
                        if len(color) != len(pie_size):
                            color = []
                            while len(color) <= len(pie_size): color.append(np.random.rand(3,1))
                            ef.setColor(color)

                        if ef.getShowValueLabel():
                            explode = None
                            if ef.getExplodeMaximum():
                                max_val = max(pie_size)
                                max_index = pie_size.index(max_val)

                                explode = [0] * len(pie_size)
                                explode[max_index] = ef.getExplodeDistance()
                            else:
                                explode = [ef.getExplodeDistance()] * len(pie_size)

                            ax.pie(pie_size, labels=pie_label, color=ef.getColor(), autopct='%1.1f%%', shadow=ef.getShadow(),
                                   startangle=ef.getStartAngel(), radius=ef.getRadius(), labeldistance=ef.getLabelDistance(),
                                   explode=explode)
                        else:
                            ax.pie(pie_size, labels=pie_label, shadow=True, startangle=90)
                    else: ax.pie(pie_size, labels=pie_label, shadow=True, startangle=90)
                    ax.axis('equal')
                ########################################################
                else:
                    #plot background color
                    ax.set_axis_bgcolor(plot.edit_feature.getBackgroundColor())

                    #axes limit
                    ax.set_xlim(plot.edit_feature.getXAxisMinimumLimit(), plot.edit_feature.getXAxisMaximumLimit())
                    ax.set_ylim(plot.edit_feature.getYAxisMinimumLimit(), plot.edit_feature.getYAxisMaximumLimit())

                    # print(plot.edit_feature.getXAxisMinimumLimit(), plot.edit_feature.getXAxisMaximumLimit())
                    #major and minor axis
                    # major_locator   = MultipleLocator(plot.edit_feature.getXAxisMajorInterval())
                    # ax.xaxis.set_major_locator(major_locator)
                    # minor_locator   = MultipleLocator(plot.edit_feature.getXAxisMinorInterval())
                    # ax.xaxis.set_minor_locator(minor_locator)
                    #
                    # major_locator   = MultipleLocator(plot.edit_feature.getYAxisMajorInterval())
                    # ax.yaxis.set_major_locator(major_locator)
                    # minor_locator   = MultipleLocator(plot.edit_feature.getYAxisMinorInterval())
                    # ax.yaxis.set_minor_locator(minor_locator)

                    if plot.show_x_label: ax.set_xlabel(plot.x_label)
                    if plot.show_y_label: ax.set_ylabel(plot.y_label, fontsize=9)

                    # grid show
                    if plot.edit_feature.getGridShowOption():
                        ax.grid(which=plot.edit_feature.getGridWhichOption(), axis=plot.edit_feature.getGridAxisOption())

                    #drawing scatter plot
                    scatter_series = plot.find_scatter_plot_series()
                    if len(scatter_series) > 0:
                        for series in scatter_series:
                            x = series.x_axis_data
                            y = series.series_data

                            ef = series.edit_feature
                            if ef is not None:
                                ax.plot(x, y, ef.getPointStyle(), label=series.series_title, mfc=ef.getFaceColor(),
                                        ms=ef.getSize(), mec=ef.getEdgeColor(), mew=ef.getEdgeLineWidth())
                            else: ax.plot(x, y, "ro", label=series.series_title)
                    else:
                        #generating x-axis data
                        #In perfect situation all the series have same x-axis both in values and length. But there might be
                        #situation when a series can have x-axis values or some may have x-values while other do not. Furthermore
                        #the x-value can be different for different data series.

                        #Algorithm:
                        #step-1: collect all unique x-values in all series
                        #step-2: if number of x-values are greater than zero, if the x-values are numeric sort them
                        #step-3: check whether the length of x-value collection is either less than or equal to individual
                        #        series y-value lengths. If not, add blank spaces at the beginning of the collection
                        #step-4: generate "false" x-series
                        #step-5: if the length of new x-value collection is greater than zero, distribute y-values for all
                        #        series in right order according to x-value collection. During this redistribution be careful
                        #        about the graph-option (type of graph). In case of line and points, the empty spaces in the
                        #        y-value list should be none, while in case of bars the empty spaces should be zero.

                        #remarks: Because all series data is stored inside list, modification of data will cause permanent
                        #changes in the original series data. To avoid the changes in data, all data must be copied first
                        #using deepcopy. This is also to be noted that for scattered plots this algorithm must be changed
                        #if this function is used.

                        #step-1: collecting unique x-values from all series
                        x_value_collection = []
                        for series in plot.list_of_series:
                            x_value = series.x_axis_data
                            if x_value is not None:
                                for i in range(len(x_value)):
                                    if (x_value[i] is not None) and (x_value[i] not in x_value_collection): x_value_collection.append(x_value[i])
                        #step-2: sorting the items in x-value collection if the values are numeric
                        is_string = False
                        for x_val in x_value_collection:
                            if type(x_val) is type(""):
                                is_string = True
                                break

                        if not is_string:
                            if len(x_value_collection) > 0: x_value_collection.sort()

                        #step-3: adjusting x-value length for all series
                        max_len = 0
                        for series in plot.list_of_series:
                            y_value = series.series_data
                            if y_value is not None:
                                if len(y_value) > max_len: max_len = len(y_value)

                        if max_len > len(x_value_collection):
                            empty_list = [i for i in range(1, (max_len - len(x_value_collection) + 1))]
                            x_value_collection = empty_list + x_value_collection
                        #step-5: generating false x-axis
                        if not is_string: x = np.array(x_value_collection)
                        else: x = np.arange(0, len(x_value_collection))
                        # print("x:", x)
                        # print("x collection",x_value_collection)



                        # x_axis_series = None
                        # if plot.series_index_referring_x_axis != -1:
                        #     x_axis_series = plot.find_series_by_index(plot.series_index_referring_x_axis)
                        # else: x_axis_series = plot.find_series_by_index(0)
                        # x_ticks = x_axis_series.x_axis_data
                        #
                        # x = None
                        # if len(x_ticks) > 0: x = np.arange(0, len(x_ticks))



                        #drawing bars
                        bar_series = plot.find_bar_series()
                        if len(bar_series) > 0:
                            stacked_option = plot.find_stacked_bar_option()
                            if not stacked_option:
                                b_width = (1/len(bar_series)) - (0.15/len(bar_series))

                                for i in range(len(bar_series)):
                                    series = bar_series[i]
                                    y = BiomeBgcGraphDummy.arrange_series_value(series.series_data, series.x_axis_data,
                                                                                x_value_collection, replaceNone=True)
                                    ef = series.edit_feature


                                    if ef is not None:
                                        #if x values are datetime objects, there is no need for adding b_width
                                        if type(x[0]) is not datetime:
                                            ax.bar(x + i * b_width, y, width=b_width, label=series.series_title, color=ef.getColor(),
                                                   edgecolor=ef.getEdgeColor(), linestyle=ef.getLineStyle(), linewidth=ef.getLineWidth(),
                                                   hatch=ef.getHatch())
                                        else:
                                            pass
                                    else:
                                        if type(x[0]) is not datetime:
                                            ax.bar(x + i * b_width, y, width=b_width, color=np.random.rand(3,1), label=series.series_title)
                                        else: pass
                                    # if None in series.series_data:
                                    #
                                    # else:
                                    #     ax.bar(x + i * b_width, series.series_data,width=b_width, color=np.random.rand(3,1),
                                    #            label=series.series_title)
                                if type(x[0]) is not datetime:
                                    x = x + (b_width / 2 * len(bar_series))

                            else:
                                b_width = 0.75 #(1/len(bar_series)) - (0.15/len(bar_series))

                                bottom_y = np.array([0] * len(x))
                                for i in range(len(bar_series)):
                                    series = bar_series[i]
                                    y = BiomeBgcGraphDummy.arrange_series_value(series.series_data, series.x_axis_data,
                                                                                x_value_collection, replaceNone=True)
                                    ef = series.edit_feature
                                    if ef is not None:
                                        if bottom_y is not None:
                                            ax.bar(x, y, width=b_width, bottom=bottom_y, label=series.series_title, color=ef.getColor(),
                                                   edgecolor=ef.getEdgeColor(), linestyle=ef.getLineStyle(), linewidth=ef.getLineWidth(),
                                                   hatch=ef.getHatch())
                                        else:
                                            ax.bar(x, y, width=b_width, label=series.series_title, color=ef.getColor(),
                                                   edgecolor=ef.getEdgeColor(), linestyle=ef.getLineStyle(), linewidth=ef.getLineWidth(),
                                                   hatch=ef.getHatch())
                                    else:
                                        if bottom_y is not None:
                                            ax.bar(x, y, width=b_width, bottom=bottom_y, color=np.random.rand(3,1), label=series.series_title)
                                        else: ax.bar(x + i * b_width, y, width=b_width, color=np.random.rand(3,1), label=series.series_title)
                                    bottom_y += y

                                    # if None in series.series_data:
                                    #
                                    # else:
                                    #     ax.bar(x + i * b_width, series.series_data,width=b_width, color=np.random.rand(3,1),
                                    #            label=series.series_title)
                                x = x + (b_width / 2 * len(bar_series))


                        #drawing lines
                        line_series = plot.find_line_series()
                        for series in line_series:
                            if series.series_data:
                                y = BiomeBgcGraphDummy.arrange_series_value(series.series_data, series.x_axis_data, x_value_collection)
                                if series.edit_feature is not None:
                                    ef = series.edit_feature
                                    if ef.getShowMarker():
                                        # print(ef.getLineWidth(), type(ef.getLineWidth()))
                                        # print(ef.getMarkerSize(), type(ef.getMarkerSize()))
                                        # print(ef.getMarker(), type(ef.getMarker()))
                                        # print(ef.getStyle(), type(ef.getStyle()))
                                        # print(ef.getColor(), type(ef.getColor()))
                                        # print("x: ", x)
                                        # print("y: ", y)
                                        ax.plot(x, y, label=series.series_title, linestyle=ef.getStyle(), color=ef.getColor(),
                                                linewidth=ef.getLineWidth(), marker=ef.getMarker(), markersize=ef.getMarkerSize())
                                    else: ax.plot(x, y, label=series.series_title, linestyle=ef.getStyle(), color=ef.getColor(),
                                                linewidth=ef.getLineWidth())
                                else: ax.plot(x, y, linestyle="solid", label=series.series_title)

                        #drawing points
                        point_series = plot.find_point_series()
                        for series in point_series:
                            y = BiomeBgcGraphDummy.arrange_series_value(series.series_data, series.x_axis_data, x_value_collection)
                            ef = series.edit_feature
                            if ef is not None:
                                ax.plot(x, y, ef.getPointStyle(), label=series.series_title, mfc=ef.getFaceColor(),
                                        ms=ef.getSize(), mec=ef.getEdgeColor(), mew=ef.getEdgeLineWidth())
                            else: ax.plot(x, y, "ro", label=series.series_title)


                        #putting x_ticks
                        if plot.show_x_ticks:
                            pyplot.xticks(x, x_value_collection, rotation=plot.x_ticks_rotation)
                            ax.xaxis.set_ticks_position('none')
                            ax.yaxis.set_ticks_position('left')
                            # pyplot.locator_params(axis="x", nbins=4)





                        #drawing bars

                        # no_of_series = len(plot.list_of_series)
                        # for i in range(no_of_series):
                        #     series = plot.list_of_series[i]
                        #     if series.plotting_option.lower() == "line":
                        #         # if series.x_axis_flag:
                        #         if x is None: x = np.arange(1, len(series.series_data) + 1)
                        #         pyplot.xticks(x,np.array(series.x_axis_data), rotation=90)
                        #         ax.plot(x, series.series_data, linestyle="solid", label=series.series_title)
                        #
                        #             # print(series.x_axis_data)
                        #             # x = np.array(series.x_axis_data)
                        #         # else:
                        #         #     x = np.arange(1, len(series.series_data) + 1)
                        #         #     pyplot.xticks(x,np.array(series.x_axis_data), rotation=90)
                        #         #     ax.plot(x, series.series_data, linestyle="solid", label=series.series_title)
                        #             #
                        #     elif series.plotting_option.lower() == "bar":
                        #
                        #         if x is None: x = np.arange(1, len(series.series_data) + 1)
                        #         b_width = (1/no_of_series) - (0.15/no_of_series)
                        #         pyplot.xticks(x + (b_width / 2 * no_of_series), np.array(series.x_axis_data), rotation=90)
                        #
                        #
                        #         # xt = x + b_width
                        #         # ax.bar(xt, series.series_data)
                        #         ax.bar(x + i * b_width, series.series_data,width=b_width, color=np.random.rand(3,1),
                        #                label=series.series_title)
                        #
                        #
                        #         # ax.spines['top'].set_visible(False)
                        #         # ax.spines['right'].set_visible(False)
                        #         #
                        #
                        #         ax.xaxis.set_ticks_position('none')
                        #         ax.yaxis.set_ticks_position('left')
                        #         print(b_width)
                        #
                        #     elif series.plotting_option.lower() == "pie":
                        #         pass

                        #adding legend
                    if plot.show_legend:
                        legend = ax.legend(loc=plot.legend_position_text(), shadow=True, prop={'size':8})
                        frame  = legend.get_frame()
                        frame.set_facecolor('0.90')

                        # for label in legend.get_texts():
                        #     label.set_fontsize('large')
                        #
                        # for label in legend.get_lines():
                        #     label.set_linewidth(1.5)  # the legend line width


            if display: pyplot.show()
            if len(save_file_filename):
                try:
                    fig.savefig(save_file_filename)
                    fig = None
                    return True
                except: return False

    @staticmethod
    def arrange_series_value(series_data, series_x_value, x_value_collection, replaceNone=False):
        y = None
        #replace None to Zero
        if replaceNone: y = [0] * len(x_value_collection)
        else: y = [None] * len(x_value_collection)

        if series_x_value is not None:
            for i in range(len(x_value_collection)):
                x_val = x_value_collection[i]
                x_index = -1
                if x_val in series_x_value: x_index = series_x_value.index(x_val)
                if x_index != -1:
                    if series_data[x_index] is not None and i < len(y): y[i] = series_data[x_index]
        else:
            for i in range(len(series_data)):
                if series_data[i] is not None and i < len(y): y[i] = series_data[i]

        return y

    # def add_plot(self, plot_position, list_of_series, list_series_type, list_series_label=None):
    #     if plot_position <= self.model_graph.max_plot_number():
    #         sp = self.plot.subplot(self.plot_column, self.plot_rows, plot_position)
    #         self.new_plot = ModelPlot(sp)
    #
    #         if len(list_of_series) == len(list_series_type):
    #             for i in range(len(list_of_series)):
    #                 series_label = ""
    #                 if list_series_label is not None:
    #                     try:
    #                         series_label = list_series_label[i]
    #                     except: pass
    #                     if series_label == "": series_label = "series number " + str(i)
    #                 self.new_plot.add_series(list_of_series[i], list_series_type[i], label=series_label)
    #
    # def edit_plot(self, plot_position, x_min, x_max):
    #     sp = self.plot.subplot(self.plot_column, self.plot_rows, plot_position)
    #     sp.set_xlim(x_min, x_max)
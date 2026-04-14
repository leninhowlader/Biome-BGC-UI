from interface.FormDesignGraph import Ui_FormDesignGraph
from PyQt5 import QtGui, QtCore, QtWidgets
from graph import ModelGraph, ModelPlot, printable_graph
from interface.DialogGraphData_Extended import DialogGraphData
from draw_graph import BiomeBgcGraphDummy
from application import ApplicationProperty
import os
from datetime import datetime
from interface.DialogPlotProperties_Extended import DialogPlotProperties
from interface.DialogGraphProperties_Extended import DialogGraphProperties

class FormDesignGraph(Ui_FormDesignGraph):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)

        self.add_validator()
        self.initial_setting()

        self.add_socket()

        #form variable
        self.model_graph = ModelGraph("")
        self.data_series_form = None

        self.dialog_graph_properties = DialogGraphProperties()
        self.dialog_plot_properties = DialogPlotProperties()


    def add_validator(self):
        rx = QtCore.QRegExp("^[0-9]*$")
        integerValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)

        self.txtNumberOfSubplot.setValidator(integerValidator)
        self.txtXMin.setValidator(decimalValidator)
        self.txtXMax.setValidator(decimalValidator)
        self.txtYMin.setValidator(decimalValidator)
        self.txtYMax.setValidator(decimalValidator)
        self.txtXTickRotation.setValidator(integerValidator)

    def initial_setting(self):
        self.txtNumberOfSubplot.setText("1")
        self.comboOrientationColumnNo.addItem("1")
        self.comboOrientationColumnNo.setCurrentIndex(0)
        self.comboOrientationRowNo.addItem("1")
        self.comboOrientationRowNo.setCurrentIndex(0)
        self.comboSubplotPosition.addItem("1")
        self.comboSubplotPosition.setCurrentIndex(-1)

    def add_socket(self):
        self.txtGraphTitle.textChanged.connect(self.txtGraphTitle_textChanged)
        self.txtNumberOfSubplot.textChanged.connect(self.txtNumberOfSubplot_textChanged)
        self.comboOrientationColumnNo.currentIndexChanged.connect(self.comboOrientationColumnNo_currentIndexChanged)
        self.comboOrientationRowNo.currentIndexChanged.connect(self.comboOrientationRowNo_currentIndexChanged)
        self.buttonAddSubplot.clicked.connect(self.buttonAddSubplot_clicked)
        self.listSubplot.itemSelectionChanged.connect(self.listSubplot_itemSelectionChanged)
        self.txtPlotTitle.textChanged.connect(self.txtPlotTitle_textChanged)
        self.buttonDeleteSubplot.clicked.connect(self.buttonDeleteSubplot_clicked)
        self.txtXAxisLabel.textChanged.connect(self.txtXAxisLabel_textChanged)
        self.txtYAxisLabel.textChanged.connect(self.txtYAxisLabel_textChanged)
        self.checkBoxShowXLabel.toggled.connect(self.checkBoxShowXLabel_toggled)
        self.checkBoxShowYLabel.toggled.connect(self.checkBoxShowYLabel_toggled)
        self.txtXMin.textChanged.connect(self.txtXMin_textChanged)
        self.txtXMax.textChanged.connect(self.txtXMax_textChanged)
        self.txtYMin.textChanged.connect(self.txtYMin_textChanged)
        self.txtYMax.textChanged.connect(self.txtYMax_textChanged)
        self.radioButtonSLYes.toggled.connect(self.radioButtonShowLegend_toggled)
        self.radioButtonHLPLeft.toggled.connect(self.radioButtonLegendHorizontalPosition_toggled)
        self.radioButtonHLPCenter.toggled.connect(self.radioButtonLegendHorizontalPosition_toggled)
        self.radioButtonHLPRight.toggled.connect(self.radioButtonLegendHorizontalPosition_toggled)
        self.radioButtonVLPTop.toggled.connect(self.radioButtonLegendVerticalPosition_toggled)
        self.radioButtonVLPMiddle.toggled.connect(self.radioButtonLegendVerticalPosition_toggled)
        self.radioButtonVLPBottom.toggled.connect(self.radioButtonLegendVerticalPosition_toggled)
        self.buttonAddDataSeries.clicked.connect(self.buttonAddDataSeries_clicked)
        self.ButtonClose.clicked.connect(self.ButtonClose_clicked)
        self.listDataSeries.itemSelectionChanged.connect(self.listDataSeries_itemSelectionChanged)
        self.ButtonCreateGraph.clicked.connect(self.ButtonCreateGraph_clicked)
        self.comboSubplotPosition.currentIndexChanged.connect(self.comboSubplotPosition_currentIndexChanged)
        self.buttonDeleteDataSeries.clicked.connect(self.buttonDeleteDataSeries_clicked)
        self.checkBoxShowXTicks.toggled.connect(self.checkBoxShowXTicks_toggled)
        self.txtXTickRotation.textChanged.connect(self.txtXTickRotation_textChanged)
        self.ButtonSaveTemplate.clicked.connect(self.ButtonSaveTemplate_clicked)
        self.ButtonOpenTemplate.clicked.connect(self.ButtonOpenTemplate_clicked)
        self.txtSeriesTitle.textChanged.connect(self.txtSeriesTitle_textChanged)
        self.buttonPlotProperties.clicked.connect(self.buttonPlotProperties_clicked)
        self.buttonGraphProperties.clicked.connect(self.buttonGraphProperties_clicked)
        self.buttonEditSeries.clicked.connect(self.buttonEditSeries_clicked)
        self.pushButtonRefreshPreview.clicked.connect(self.pushButtonRefreshPreview_clicked)

    def ButtonCreateGraph_clicked(self):
        message = ""
        if len(self.model_graph.list_of_plot) > 0:
            try: BiomeBgcGraphDummy.ShowGraph(self.model_graph, 1)
            except: pass
            # BiomeBgcGraphDummy.ShowGraph(self.model_graph, 2, display=False, save_file_filename="graphs/test2.png")
            # p = threading.Thread(target=self.create_separate_app())
            # p.start()

        else:
            message = "There is no data to plot."
        if message != "": QtGui.QMessageBox.about(self.form, "No data", message)


    def create_separate_app(self):
        BiomeBgcGraphDummy.ShowGraph(self.model_graph, 1)



    def txtGraphTitle_textChanged(self):
        self.model_graph.graph_title = self.txtGraphTitle.text()

    def txtNumberOfSubplot_textChanged(self):
        self.combo_row_column_event_deactivate_flag = True

        if len(self.txtNumberOfSubplot.text()) > 0:
            no_of_subplot = int(self.txtNumberOfSubplot.text())

            if no_of_subplot > 0:
                if no_of_subplot < self.model_graph.find_number_of_existing_plot():
                    no_of_subplot = self.model_graph.find_number_of_existing_plot()
                    self.txtNumberOfSubplot.setText(str(no_of_subplot))

                if no_of_subplot != self.model_graph.no_of_plot:
                    self.model_graph.no_of_plot = no_of_subplot
                    self.comboOrientationColumnNo.clear()
                    self.comboOrientationRowNo.clear()
                    self.comboSubplotPosition.clear()
                    for i in range(1, no_of_subplot + 1):
                        itemText = str(i)
                        self.comboOrientationColumnNo.addItem(itemText)
                        self.comboOrientationRowNo.addItem(itemText)
                        self.comboSubplotPosition.addItem(itemText)
                    self.comboOrientationColumnNo.setCurrentIndex(no_of_subplot - 1)
                    self.comboOrientationRowNo.setCurrentIndex(0)
                    self.comboSubplotPosition.setCurrentIndex(-1)

                    self.model_graph.plot_orientation_col = no_of_subplot

            else:
                if self.model_graph.find_number_of_existing_plot() == 0:
                    self.comboOrientationColumnNo.clear()
                    self.comboOrientationRowNo.clear()
                    self.comboSubplotPosition.clear()

                    self.txtNumberOfSubplot.setText("1")
                    self.comboOrientationColumnNo.addItem("1")
                    self.comboOrientationColumnNo.setCurrentIndex(0)
                    self.comboOrientationRowNo.addItem("1")
                    self.comboOrientationRowNo.setCurrentIndex(0)
                else:
                    self.txtNumberOfSubplot.setText(str(self.model_graph.no_of_plot))
        else:
            if self.model_graph.find_number_of_existing_plot() == 0:
                self.comboOrientationColumnNo.clear()
                self.comboOrientationRowNo.clear()
                self.comboSubplotPosition.clear()

                self.txtNumberOfSubplot.setText("1")
                self.comboOrientationColumnNo.addItem("1")
                self.comboOrientationColumnNo.setCurrentIndex(0)
                self.comboOrientationRowNo.addItem("1")
                self.comboOrientationRowNo.setCurrentIndex(0)
            else:
                self.txtNumberOfSubplot.setText(str(self.model_graph.no_of_plot))

        self.combo_row_column_event_deactivate_flag = False

    def comboOrientationColumnNo_currentIndexChanged(self):
        if not self.combo_row_column_event_deactivate_flag:
            no_of_column = int(self.comboOrientationColumnNo.currentText())

            no_of_subplot = int(self.txtNumberOfSubplot.text())
            no_of_row = (no_of_subplot - 1) // no_of_column + 1

            self.comboOrientationRowNo.setCurrentIndex(no_of_row - 1)

            self.model_graph.plot_orientation_col = no_of_column

    def comboOrientationRowNo_currentIndexChanged(self):
        if not self.combo_row_column_event_deactivate_flag:
            no_of_row = int(self.comboOrientationRowNo.currentText())
            no_of_subplot = int(self.txtNumberOfSubplot.text())
            no_of_column = (no_of_subplot - 1) // no_of_row + 1

            self.comboOrientationColumnNo.setCurrentIndex(no_of_column - 1)

            self.model_graph.plot_orientation_row = no_of_row

    def buttonAddSubplot_clicked(self):
        t = self.model_graph.no_of_plot
        n = len(self.model_graph.list_of_plot)
        if n < t:
            plot_position = self.model_graph.find_free_plot_position()

            i = 0
            while True:
                plot_title = "Sub-plot " + str(plot_position + i)
                if not self.model_graph.plot_exists(plot_title): break
                i += 1

            plot = ModelPlot(plot_title, plot_position)
            if self.model_graph.add_plot(plot):
                item = QtGui.QListWidgetItem(plot_title)
                self.listSubplot.addItem(item)
                item.setSelected(True)
                self.comboSubplotPosition.setCurrentIndex(plot.plot_position - 1)
                self.show_preview()
        # self.txtPlotTitle.setText(item.text())

    def buttonDeleteSubplot_clicked(self):
        ndx = -1
        for i in range(self.listSubplot.count()):
            item = self.listSubplot.item(i)
            if item.isSelected():
                ndx = i
                break
        if ndx > -1:
            self.listSubplot.takeItem(ndx)
            self.model_graph.remove_plot(plot_index=ndx)
            self.show_preview()
            if self.listSubplot.count() == 0:
                self.listDataSeries.clear()
                self.txtSeriesTitle.clear()


    def listSubplot_itemSelectionChanged(self):
        for i in range(self.listSubplot.count()):
            item = self.listSubplot.item(i)
            if item.isSelected():
                plot = self.model_graph.find_plot_by_index(i)
                self.txtPlotTitle.setText(plot.plot_title)
                self.comboSubplotPosition.setCurrentIndex(plot.plot_position - 1)
                self.txtXAxisLabel.setText(plot.x_label)
                self.txtYAxisLabel.setText(plot.y_label)
                self.checkBoxShowXLabel.setChecked(plot.show_x_label)
                self.checkBoxShowYLabel.setChecked(plot.show_y_label)

                if type(plot.edit_feature.getXAxisMinimumLimit()) is int or type(plot.edit_feature.getXAxisMinimumLimit()) is float:
                    self.txtXMin.setText(str(round(plot.edit_feature.getXAxisMinimumLimit(), 0)))
                    self.txtXMax.setText(str(round(plot.edit_feature.getXAxisMaximumLimit(), 0)))
                else:
                    self.txtXMin.setText(str(plot.edit_feature.getXAxisMinimumLimit()))
                    self.txtXMax.setText(str(plot.edit_feature.getXAxisMaximumLimit()))
                if type(plot.edit_feature.getYAxisMinimumLimit()) is int or type(plot.edit_feature.getYAxisMinimumLimit()) is float:
                    self.txtYMin.setText(str(round(plot.edit_feature.getYAxisMinimumLimit(), 0)))
                    self.txtYMax.setText(str(round(plot.edit_feature.getYAxisMaximumLimit(), 0)))
                else:
                    self.txtYMin.setText(str(plot.edit_feature.getYAxisMinimumLimit()))
                    self.txtYMax.setText(str(plot.edit_feature.getYAxisMaximumLimit()))

                # self.txtXMin.setText(str(plot.edit_feature.getXAxisMinimumLimit()))
                # self.txtXMax.setText(str(plot.edit_feature.getXAxisMaximumLimit()))
                # self.txtYMin.setText(str(round(plot.edit_feature.getYAxisMinimumLimit(), 0)))
                # self.txtYMax.setText(str(round(plot.edit_feature.getYAxisMaximumLimit, 0)))


                if plot.show_x_ticks: self.checkBoxShowXTicks.setChecked(True)
                else: self.checkBoxShowXTicks.setChecked(False)
                self.txtXTickRotation.setText(str(plot.x_ticks_rotation))

                if plot.show_legend: self.radioButtonSLYes.setChecked(True)
                else: self.radioButtonSLNo.setChecked(True)
                if plot.legend_horizontal_position == 1: self.radioButtonHLPRight.setChecked(True)
                elif plot.legend_horizontal_position == 0: self.radioButtonHLPCenter.setChecked(True)
                else: self.radioButtonHLPLeft.setChecked(True)
                if plot.legend_vertical_position == 1: self.radioButtonVLPTop.setChecked(True)
                elif plot.legend_vertical_position == 0: self.radioButtonVLPMiddle.setChecked(True)
                else: self.radioButtonVLPBottom.setChecked(True)


                self.listDataSeries.clear()
                self.txtSeriesTitle.clear()
                if len(plot.list_of_series) > 0:
                    for series in plot.list_of_series:
                        self.listDataSeries.addItem(series.attribute_name)
                    self.listDataSeries.item(0).setSelected(True)
                break
        else:
            self.txtPlotTitle.setText("")
            self.comboSubplotPosition.setCurrentIndex(-1)
            self.txtXAxisLabel.clear()
            self.txtYAxisLabel.clear()
            self.checkBoxShowXLabel.setChecked(False)
            self.checkBoxShowYLabel.setChecked(False)
            self.txtXMin.clear()
            self.txtXMax.clear()
            self.txtYMin.clear()
            self.txtYMax.clear()
            self.radioButtonHLPRight.setChecked(True)
            self.radioButtonVLPTop.setChecked(True)

    def txtPlotTitle_textChanged(self):
        for i in range(self.listSubplot.count()):
            item = self.listSubplot.item(i)
            if item.isSelected():
                plot = self.model_graph.list_of_plot[i]
                plot.plot_title = self.txtPlotTitle.text()
                item.setText(plot.plot_title)
                break
        else:
            self.txtPlotTitle.setText("")

    def txtXAxisLabel_textChanged(self):
        plot = self.find_selected_plot()

        if plot is not None:
            plot.x_label = self.txtXAxisLabel.text()

    def txtYAxisLabel_textChanged(self):
        plot = self.find_selected_plot()

        if plot is not None:
            plot.y_label = self.txtYAxisLabel.text()

    def find_selected_plot(self):
        plot = None
        for i in range(self.listSubplot.count()):
            item = self.listSubplot.item(i)
            if item.isSelected():
                plot = self.model_graph.find_plot_by_index(i)
                break
        return plot

    def checkBoxShowXLabel_toggled(self):
        plot = self.find_selected_plot()
        if plot is not None: plot.show_x_label = self.checkBoxShowXLabel.isChecked()

    def checkBoxShowYLabel_toggled(self):
        plot = self.find_selected_plot()
        if plot is not None: plot.show_y_label = self.checkBoxShowYLabel.isChecked()

    def txtXMin_textChanged(self):
        if len(self.txtXMin.text().strip()) > 0:
            plot = self.find_selected_plot()
            if plot is not None:
                try:
                    plot.edit_feature.setXAxisMinimumLimit(float(self.txtXMin.text()))
                except:
                    try:
                        plot.edit_feature.setXAxisMinimumLimit(datetime.strptime(self.txtXMin.text(), "%Y-%m-%d %H:%M:%S"))
                    except: pass

    def txtXMax_textChanged(self):
        if len(self.txtXMax.text().strip()) > 0:
            plot = self.find_selected_plot()
            if plot is not None:
                try:
                    plot.edit_feature.setXAxisMaximumLimit(float(self.txtXMax.text()))
                except:
                    try:
                        plot.edit_feature.setXAxisMaximumLimit(datetime.strptime(self.txtXMax.text(), "%Y-%m-%d %H:%M:%S"))
                    except: pass

    def txtYMin_textChanged(self):
        if len(self.txtYMin.text().strip()) > 0:
            plot = self.find_selected_plot()
            if plot is not None:
                try:
                    plot.edit_feature.setYAxisMinimumLimit(float(self.txtYMin.text()))
                except: pass

    def txtYMax_textChanged(self):
        if len(self.txtYMax.text().strip()) > 0:
            plot = self.find_selected_plot()
            if plot is not None:
                try:
                    plot.edit_feature.setYAxisMaximumLimit(float(self.txtYMax.text()))
                except: pass

    def radioButtonShowLegend_toggled(self):
        plot = self.find_selected_plot()
        if plot is not None: plot.show_legend = self.radioButtonSLYes.isChecked()

    def radioButtonLegendHorizontalPosition_toggled(self):
        plot = self.find_selected_plot()
        if plot is not None:
            if self.radioButtonHLPLeft.isChecked(): plot.legend_horizontal_position = -1
            elif self.radioButtonHLPCenter.isChecked(): plot.legend_horizontal_position = 0
            else: plot.legend_horizontal_position = 1

    def radioButtonLegendVerticalPosition_toggled(self):
        plot = self.find_selected_plot()
        if plot is not None:
            if self.radioButtonVLPTop.isChecked(): plot.legend_vertical_position = 1
            elif self.radioButtonVLPMiddle.isChecked(): plot.legend_vertical_position = 0
            else: plot.legend_vertical_position = -1

    def buttonAddDataSeries_clicked(self):
        # self.data_series_form.exec_()
        plot = self.find_selected_plot()
        if plot is not None:
            if self.data_series_form is None:
                self.data_series_form = DialogGraphData()
                self.data_series_form.model_plot = plot
                self.data_series_form.current_series_index = -1
                self.data_series_form.buttonOk.clicked.connect(self.DataSeriesDialogReturn)
                self.data_series_form.form.show()
            else:
                self.data_series_form.model_plot = plot
                self.data_series_form.current_series_index = -1
                self.data_series_form.clear_field()
                self.data_series_form.form.show()
                self.data_series_form.form.activateWindow()
        else:
            message = "There is no plot selected. Please select one plot."
            QtGui.QMessageBox.about(self.form, "No plot active", message)


    def DataSeriesDialogReturn(self):
        data_series = self.data_series_form.buttonOk_clicked()
        if data_series is not None:
            plot = self.find_selected_plot()
            if plot is not None and len(plot.list_of_series) > 0:
                self.listDataSeries.clear()
                for data_series in plot.list_of_series:
                    item = QtGui.QListWidgetItem(data_series.attribute_name)
                    self.listDataSeries.addItem(item)
                    item.setSelected(True)

                if type(plot.edit_feature.getXAxisMinimumLimit()) is int or type(plot.edit_feature.getXAxisMinimumLimit()) is float:
                    self.txtXMin.setText(str(round(plot.edit_feature.getXAxisMinimumLimit(), 0)))
                    self.txtXMax.setText(str(round(plot.edit_feature.getXAxisMaximumLimit(), 0)))
                else:
                    self.txtXMin.setText(str(plot.edit_feature.getXAxisMinimumLimit()))
                    self.txtXMax.setText(str(plot.edit_feature.getXAxisMaximumLimit()))
                if type(plot.edit_feature.getYAxisMinimumLimit()) is int or type(plot.edit_feature.getYAxisMinimumLimit()) is float:
                    self.txtYMin.setText(str(round(plot.edit_feature.getYAxisMinimumLimit(), 0)))
                    self.txtYMax.setText(str(round(plot.edit_feature.getYAxisMaximumLimit(), 0)))
                else:
                    self.txtYMin.setText(str(plot.edit_feature.getYAxisMinimumLimit()))
                    self.txtYMax.setText(str(plot.edit_feature.getYAxisMaximumLimit()))

            # self.show_preview()

    def ButtonClose_clicked(self):
        self.form.parentWidget().close()

    def listDataSeries_itemSelectionChanged(self):
        series = self.find_selected_series()
        if series is not None:
            self.txtSeriesTitle.setText(series.series_title)

    def find_selected_series(self):
        series_index = -1
        for i in range(self.listDataSeries.count()):
            item =  self.listDataSeries.item(i)
            if item.isSelected():
                series_index = i
                break

        if series_index >= 0:
            plot = self.find_selected_plot()
            series = plot.find_series_by_index(series_index)
            return series
        return None

    def find_current_series_index(self):
        for i in range(self.listDataSeries.count()):
            item =  self.listDataSeries.item(i)
            if item.isSelected():
                return i

        return -1

    def comboSubplotPosition_currentIndexChanged(self):
        if self.comboSubplotPosition.currentIndex() != -1:
            plot = self.find_selected_plot()
            if plot is not None:
                current_position = plot.plot_position
                expected_position = int(self.comboSubplotPosition.currentText())
                for p in self.model_graph.list_of_plot:
                    if p.plot_position == expected_position:
                        free_position = self.model_graph.find_free_plot_position()
                        if free_position != 0:
                            p.plot_position = free_position
                        else:
                            p.plot_position = current_position
                        break

                plot.plot_position = int(self.comboSubplotPosition.currentText())

    def buttonDeleteDataSeries_clicked(self):
        plot = self.find_selected_plot()
        series = self.find_selected_series()
        if series is not None:
            s_name = series.attribute_name
            if plot.delete_series(series):
                for i in range(self.listDataSeries.count()):
                    item = self.listDataSeries.item(i)
                    if item.text() == s_name:
                        self.listDataSeries.takeItem(i)
                        if self.listDataSeries.count() == 0:
                            self.txtSeriesTitle.clear()
                        # if i > 0:
                        #     item = self.listDataSeries.item(i-1)
                        #     item.setSelected(True)
                        # self.txtSeriesTitle.clear()
                        break
                self.show_preview()

    def checkBoxShowXTicks_toggled(self):
        plot = self.find_selected_plot()
        if plot is not None:
            plot.show_x_ticks = self.checkBoxShowXTicks.isChecked()

    def txtXTickRotation_textChanged(self):
        deg_str = self.txtXTickRotation.text()
        if len(deg_str) > 0:
            deg = 0
            try: deg = float(self.txtXTickRotation.text())
            except: pass

            plot = self.find_selected_plot()
            if plot is not None:
                plot.x_ticks_rotation = deg
        # else: self.txtXTickRotation.setText("0")

    def ButtonSaveTemplate_clicked(self):
        if len(self.model_graph.list_of_plot) > 0:
            series_count = 0
            for plot in self.model_graph.list_of_plot:
                series_count += len(plot.list_of_series)

            if series_count > 0:
                initial_directory = os.path.join(ApplicationProperty.getScriptPath(), "graphs")
                file_name = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save Graph Template', initial_directory, "Graph Template (*.txt)")

                if len(file_name) > 0:
                    file_name = file_name.strip()
                    if file_name.lower().find('.gtm') == -1 or file_name.lower().find('.gtm') != len(file_name) - 5:
                        file_name += '.gtm'
                    if ModelGraph.write_graph_template(self.model_graph, file_name):
                        message = "The graph has been saved as a template successfully"
                        QtGui.QMessageBox.about(self.form, "Template Saved", message)
                    else:
                        message = "An unknown error occurred. The template could not be saved."
                        QtGui.QMessageBox.about(self.form, "Error", message)
            else:
                message = "There is no data series in model plot(s). No template can be saved."
                QtGui.QMessageBox.about(self.form, "No data", message)
        else:
            message = "There is no plot. No template can be saved."
            QtGui.QMessageBox.about(self.form, "No plot", message)

    def ButtonOpenTemplate_clicked(self):
        initial_directory = os.path.join(ApplicationProperty.getScriptPath(), "graphs")
        file_name = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open Graph Template', initial_directory, "Graph Template (*.txt)")

        if len(file_name) > 0:
            model_graph =  ModelGraph.read_graph_template(file_name)
            if model_graph is not None:
                try: ModelGraph.read_data_from_source_file(model_graph)
                except: pass
                self.model_graph = model_graph
                self.txtGraphTitle.setText(self.model_graph.graph_title)
                self.txtNumberOfSubplot.setText(str(self.model_graph.no_of_plot))
                self.listSubplot.clear()
                for plot in self.model_graph.list_of_plot:
                    self.listSubplot.addItem(plot.plot_title)
                if self.listSubplot.count() > 0: self.listSubplot.item(0).setSelected(True)
                #self.show_preview()
            else:
                message = "An unknown error occurred. The template could not be Loaded."
                QtGui.QMessageBox.about(self.form, "Error", message)

    def txtSeriesTitle_textChanged(self):
        if self.txtSeriesTitle.text() != "":
            series = self.find_selected_series()
            if series is not None:
                series.series_title = self.txtSeriesTitle.text()

    def buttonPlotProperties_clicked(self):
        plot = self.find_selected_plot()
        if plot is not None:
            self.dialog_plot_properties.plot = plot
            self.dialog_plot_properties.set_values()
            self.dialog_plot_properties.form.setModal(True)
            self.dialog_plot_properties.form.show()


    def buttonGraphProperties_clicked(self):
        if self.model_graph is not None:
            self.dialog_graph_properties.model_graph = self.model_graph
            self.dialog_graph_properties.form.setModal(True)
            self.dialog_graph_properties.set_values()
            self.dialog_graph_properties.form.show()

    def buttonEditSeries_clicked(self):
        plot = self.find_selected_plot()
        if plot is not None:
            current_series_index = self.find_current_series_index()
            if current_series_index >= 0:
                if self.data_series_form is None:
                    self.data_series_form = DialogGraphData()
                    self.data_series_form.buttonOk.clicked.connect(self.DataSeriesDialogReturn)

                self.data_series_form.model_plot = plot
                self.data_series_form.current_series_index = current_series_index
                self.data_series_form.clear_field()

                self.data_series_form.load_series()
                self.data_series_form.form.show()
                self.data_series_form.form.activateWindow()

    def show_preview(self):
        if len(self.model_graph.list_of_plot) > 0:
            if BiomeBgcGraphDummy.ShowGraph(self.model_graph, 1, display=False, save_file_filename="temp/design_preview.png"):
                scene = QtGui.QGraphicsScene()
                pix_map = QtGui.QPixmap('temp/design_preview.png')
                w = pix_map.width()
                h = pix_map.height()
                scene.addPixmap(pix_map)
                self.graphicsView.setScene(scene)
                self.graphicsView.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
            else: self.graphicsView.setScene(None)
        else: self.graphicsView.setScene(None)

        self.graphicsView.show()

    def pushButtonRefreshPreview_clicked(self):
        try: self.show_preview()
        except: pass

    def insert_preview(self, image_path):
        scene = QtGui.QGraphicsScene()
        pix_map = QtGui.QPixmap(image_path)
        w = pix_map.width()
        h = pix_map.height()
        scene.addPixmap(pix_map)
        self.graphicsView.setScene(scene)
        self.graphicsView.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
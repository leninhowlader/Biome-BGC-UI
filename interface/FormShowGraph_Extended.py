from interface.FormShowGraph import Ui_FormShowGraph
from PyQt5 import QtGui, QtCore, QtWidgets
from application import ApplicationProperty
import os
from graph import ModelGraph
import threading
from draw_graph import BiomeBgcGraphDummy
from interface.FormDesignGraph_Extended import FormDesignGraph

class FormShowGraph(Ui_FormShowGraph):
    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.setupUi(self.form)

        self.add_socket()
        self.initial_setting()

        self.signalMapper = QtCore.QSignalMapper(self.form)
        #self.signalMapper.mapped[QtWidgets.QWidget].connect(self.dynamicButton_clicked)

        #form variables
        self.template_dir =  ""
        self.model_graph = None
        self.data_source_changed_flag = False


        self.ReadTemplate()
        self.design_form = FormDesignGraph()


    def add_socket(self):
        # self.buttonBrowseTemplate.clicked.connect(self.buttonBrowseTemplate_clicked)
        self.tableTemplate.cellClicked.connect(self.tableTemplate_cellClicked)
        self.buttonClose.clicked.connect(self.buttonClose_clicked)
        self.buttonShowGraph.clicked.connect(self.buttonShowGraph_clicked)
        self.buttonEditGraph.clicked.connect(self.buttonEditGraph_clicked)
        self.buttonSaveAsNewTemplate.clicked.connect(self.buttonSaveAsNewTemplate_clicked)

    def initial_setting(self):
        self.tableTemplate.setColumnCount(1)
        self.tableTemplate.setHorizontalHeaderLabels(["Graph Template Name"])
        self.tableTemplate.setColumnWidth(0, 300)
        self.tableDataSource.setColumnCount(4)
        self.tableDataSource.setHorizontalHeaderLabels(["Source Data File", "File Type", "", "New Data Source"])
        self.tableDataSource.setColumnWidth(0, 230)
        self.tableDataSource.setColumnWidth(1, 60)
        self.tableDataSource.setColumnWidth(2, 90)
        self.tableDataSource.setColumnWidth(3, 230)

    def ReadTemplate(self):
        target_directory = os.path.join(ApplicationProperty.getScriptPath(), "graphs")
        template_list = [f for f in os.listdir(target_directory) if f.lower().find(".gto") != -1 and os.path.isfile(os.path.join(target_directory,f)) ]
        if len(template_list) > 0:
            self.template_dir = target_directory
            self.clear_table_template()

            for tmp in template_list:
                item = QtWidgets.QTableWidgetItem(tmp.replace(".gto", ""))
                row_index = self.tableTemplate.rowCount()
                self.tableTemplate.insertRow(row_index)
                self.tableTemplate.setItem(row_index, 0, item)
                self.tableTemplate.setRowHeight(0, 20)

    def clear_field(self):
        self.lineEditGraphTitle.clear()
        self.clear_table_data_source()

    def tableTemplate_cellClicked(self):
        self.model_graph = None
        self.clear_field()
        cur_item = self.tableTemplate.currentItem()
        if cur_item is not None:
            file_name = os.path.join(self.template_dir, cur_item.text() + ".gto")
            if os.path.exists(file_name):
                model_graph = ModelGraph.load_binary_template(file_name)
                if model_graph is not None:
                    self.model_graph = model_graph
                    self.lineEditGraphTitle.setText(self.model_graph.graph_title)

                    source_file_list = ModelGraph.data_source_file_names(self.model_graph)

                    if len(source_file_list) > 0:
                        for i in range(len(source_file_list)):
                            source_file_name = source_file_list[i]

                            row_index = self.tableDataSource.rowCount()
                            self.tableDataSource.insertRow(row_index)
                            self.tableDataSource.setRowHeight(row_index, 24)

                            item = QtWidgets.QTableWidgetItem(source_file_name)
                            self.tableDataSource.setItem(row_index, 0, item)

                            item = QtWidgets.QTableWidgetItem(source_file_name.split(".")[-1])
                            self.tableDataSource.setItem(row_index, 1, item)

                            buttonCell = QtGui.QPushButton()
                            buttonCell.setText("change")
                            buttonCell.clicked.connect(self.signalMapper.map)
                            self.tableDataSource.setCellWidget(row_index, 2, buttonCell)
                            buttonCell.row_index = i
                            self.signalMapper.setMapping(buttonCell, buttonCell)
            #draw preview
            self.show_preview()

    def show_preview(self):
        if self.model_graph is not None and len(self.model_graph.list_of_plot) > 0:
            if BiomeBgcGraphDummy.ShowGraph(self.model_graph, 1, display=False, save_file_filename="temp/template_preview.png"):
                scene = QtGui.QGraphicsScene()
                pix_map = QtGui.QPixmap('temp/template_preview.png')
                w = pix_map.width()
                h = pix_map.height()
                scene.addPixmap(pix_map)
                self.graphicsView.setScene(scene)
                self.graphicsView.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
            else: self.graphicsView.setScene(None)
        else: self.graphicsView.setScene(None)
        self.graphicsView.show()

    @QtCore.pyqtSlot(QtWidgets.QWidget)
    def dynamicButton_clicked(self, buttonCell):
        old_file_name = self.tableDataSource.item(buttonCell.row_index, 0).text()
        file_extension = self.tableDataSource.item(buttonCell.row_index, 1).text()
        if len(old_file_name) > 0 and len(file_extension) > 0:
            init_directory = ApplicationProperty.currentModelDirectory
            if len(init_directory) == 0: init_directory = ApplicationProperty.getScriptPath()

            file_type = ""
            if file_extension.lower() == "ini": file_type = "Model Initial File (*.ini)"
            elif file_extension.lower() == "csv": file_type = "CSV File (*.csv)"
            new_file_name = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', init_directory, file_type)
            if len(new_file_name) > 0:
                if new_file_name.lower() != old_file_name.lower():
                    cellItem = QtWidgets.QTableWidgetItem(new_file_name)
                    self.tableDataSource.setItem(buttonCell.row_index, 3, cellItem)
                    ModelGraph.change_data_source(self.model_graph, old_file_name, new_file_name)
                    self.data_source_changed_flag = True
                else:
                    message = "The new data source and the old data source are the same."
                    QtGui.QMessageBox.about(self.form,"Same Source", message)


    def clear_table_data_source(self):
        for i in reversed(range(self.tableDataSource.rowCount())):
            self.tableDataSource.removeRow(i)

    def clear_table_template(self):
        for i in reversed(range(self.tableTemplate.rowCount())):
            self.tableTemplate.removeRow(i)

    def buttonShowGraph_clicked(self):
        if self.model_graph is not None and len(self.model_graph.list_of_plot) > 0:
            if self.data_source_changed_flag:
                ModelGraph.read_data_from_source_file(self.model_graph)
            p = threading.Thread(target=BiomeBgcGraphDummy.ShowGraph(self.model_graph, 1))
            p.daemon = True
            p.start()

    def buttonSaveAsNewTemplate_clicked(self):
        if self.model_graph is not None and len(self.model_graph.list_of_plot) > 0:
            initial_directory = os.path.join(ApplicationProperty.getScriptPath(), "graphs")
            if self.data_source_changed_flag:
                ModelGraph.read_data_from_source_file(self.model_graph)

            file_name = QtWidgets.QFileDialog.getSaveFileName(self.form, 'Save Graph Template', initial_directory, "Graph Template Object (*.gto)")

            if len(file_name) > 0:
                if ModelGraph.save_as_binary_template(self.model_graph, file_name):
                    message = "The graph has been saved as a template successfully"
                    QtGui.QMessageBox.about(self.form, "Template Saved", message)
                    self.ReadTemplate()
                else:
                    message = "An unknown error occurred. The template could not be saved."
                    QtGui.QMessageBox.about(self.form, "Error", message)
        else:
            message = "There is no graph to save."
            QtGui.QMessageBox.about(self.form, "No data", message)


    def buttonClose_clicked(self):
        try:
            if self.design_form.form.parentWidget(): self.design_form.form.parentWidget().close()
        except: pass
        self.form.parentWidget().close()

    def buttonEditGraph_clicked(self):
        if self.model_graph is not None:
            self.design_form = FormDesignGraph()
            self.parentForm.mdiArea.addSubWindow(self.design_form.form)
            self.design_form.model_graph = self.model_graph
            if len(self.model_graph.list_of_plot) > 0:
                self.design_form.txtGraphTitle.setText(self.model_graph.graph_title)
                self.design_form.txtNumberOfSubplot.setText(str(len(self.model_graph.list_of_plot)))
                for plot in self.model_graph.list_of_plot:
                    self.design_form.listSubplot.addItem(plot.plot_title)
                self.design_form.listSubplot.item(0).setSelected(True)
                self.design_form.form.show()
                self.design_form.insert_preview("temp/template_preview.png")

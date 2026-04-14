from interface.DialogGraphData import Ui_dialogAddSeries
from PyQt5 import QtGui, QtCore, QtWidgets
from application import ApplicationProperty
from file_io import FileReadWrite
from read_output import ReadBinaryOutput, ReadExternalOutput
from graph import DataSeries, PointEditFeature, LineEditFeature, BarEditFeature, PieEditFeature, DataSource
from datetime import datetime
import copy

class DialogGraphData(Ui_dialogAddSeries):
    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        self.add_socket()

        self.set_validator()


        #form variable
        self.model_plot = None
        self.current_series_index = -1

        self.point_feature = PointEditFeature()
        self.line_feature = LineEditFeature()
        self.bar_feature = BarEditFeature()
        self.pie_feature = PieEditFeature()
        self.line_style = {"Solid": "-", "Dashed": "--", "Dotted": ".", "Dash Dot": "-.", "No Line": ""}
        self.bar_edge_style = {"Solid": "solid", "Dashed": "dashed", "Dotted": "dotted", "Dash Dot": "dashdot", "No Line": ""}
        self.point_style = {"None": None, "Circle": "o", "Square": "s", "Diamond": "D", "Thin Diamond": "d", "Point": ".",
                            "Star": "*", "Plus": "+", "Pentagon": "p", "Hexagon1": "h", "Hexagon2": "H", "Octagon": "8",
                            "Triangle Up": "^", "Triangle Down": "v", "Triangle Left": ">", "Triangle Right": "<",
                            "Tick Left": 0, "Tick Right": 1 , "Tick Up": 2, "Tick Down": 3, "Verlicle Line": "|"}
        self.hatch_option = {"None": "", "///////": "/", "\\\\\\\\\\\\\\": "\\", "|||||||": "|", "-------": "-", "+++++++": "+",
                             "xxxxxxx": "x", "ooooooo": "o", "OOOOOOO": "O", ".......": ".", "*******": "*"}

        self.initial_setting()

        # self.model_data_form = FormReadOutput()

        self.data_source = None

        self.read_result = None

    def initial_setting(self):
        self.frameOpenModelData.setVisible(False)
        self.comboFilterCondition.addItems(["None", ">","<","=", ">=", "<=", "between"])
        self.comboFilterCondition.setCurrentIndex(-1)
        self.txtSeriesTitle.setEnabled(False)
        self.comboPlotingOption.addItems(["Point","Line","Bar","Pie", "Scatter Plot", "Stacked Bar"])
        self.comboPlotingOption.setCurrentIndex(1)

        style_point = ["None", "Circle", "Square", "Diamond", "Thin Diamond", "Point", "Star", "Plus", "Pentagon",
                       "Hexagon1", "Hexagon2", "Octagon", "Triangle Up", "Triangle Down", "Triangle Left",
                       "Triangle Right", "Tick Left", "Tick Right", "Tick Up", "Tick Down", "Verlicle Line"]
        style_line = ["Solid", "Dashed", "Dotted", "Dash Dot", "No Line"]

        list_hatch = ["None", "///////", "\\\\\\\\\\\\\\", "|||||||", "-------", "+++++++", "xxxxxxx", "ooooooo", "OOOOOOO",
                      ".......", "*******"]

        self.comboBoxLineStyle.addItems(style_line)
        self.comboBoxLineMarkerStyle.addItems(style_point)
        self.comboBoxPointStyle.addItems(style_point)
        self.comboBoxBarEdgeStyle.addItems(style_line)
        self.comboBoxBarHatch.addItems(list_hatch)

        self.comboBoxLineStyle.setCurrentIndex(0)
        self.comboBoxLineMarkerStyle.setCurrentIndex(1)
        self.comboBoxPointStyle.setCurrentIndex(1)
        self.comboBoxBarEdgeStyle.setCurrentIndex(0)
        self.comboBoxBarHatch.setCurrentIndex(0)


        self.pushButtonPieColor.setEnabled(False)
        self.pushButtonAddPieColor.setEnabled(False)
        self.pushButtonRemovePieColor.setEnabled(False)
        self.frameEditOption.setVisible(False)

        self.show_point_edit_option()
        self.show_line_edit_option()
        self.show_bar_edit_option()
        self.show_pie_edit_option()

    def show_point_edit_option(self):
        if self.point_feature is not None:
            key_str = None
            for key, value in self.point_style.items():
                if value == self.point_feature.getPointStyle(): key_str = key

            key_str_index = self.comboBoxPointStyle.findText(key_str)
            self.comboBoxPointStyle.setCurrentIndex(key_str_index)
            self.pushButtonPointFaceColor.setStyleSheet("QWidget { background-color: %s }" %
                                                        self.point_feature.getFaceColor())
            self.lineEditPointSize.setText(str(self.point_feature.getSize()))
            self.pushButtonPointEdgeColor.setStyleSheet("QWidget { background-color: %s }" %
                                                        self.point_feature.getEdgeColor())
            self.lineEditPointEdgeWidth.setText(str(self.point_feature.getEdgeLineWidth()))

    def show_line_edit_option(self):
        if self.line_feature is not None:
            key_str = None
            for key, value in self.line_style.items():
                if value == self.line_feature.getStyle(): key_str = key
            key_index = self.comboBoxLineStyle.findText(key_str)
            self.comboBoxLineStyle.setCurrentIndex(key_index)
            self.pushButtonLineColor.setStyleSheet("QWidget {background-color: %s}" % self.line_feature.getColor())
            self.lineEditLineWidth.setText(str(self.line_feature.getLineWidth()))
            self.checkBoxLineShowMarker.setChecked(self.line_feature.getShowMarker())

            for key, value in self.point_style.items():
                if value == self.line_feature.getMarker(): key_str = key
            key_index = self.comboBoxLineMarkerStyle.findText(key_str)
            self.comboBoxLineMarkerStyle.setCurrentIndex(key_index)
            self.lineEditLineMarkerSize.setText(str(self.line_feature.getMarkerSize()))

    def show_bar_edit_option(self):
        if self.bar_feature is not None:
            self.pushButtonBarFillColor.setStyleSheet("QWidget{background-color:%s}" % self.bar_feature.getColor())
            self.pushButtonBarEdgeColor.setStyleSheet("QWidget{background-color:%s}" % self.bar_feature.getEdgeColor())

            key_str = None
            for key, value in self.bar_edge_style.items():
                if value == self.bar_feature.getLineStyle(): key_str = key
            key_index = self.comboBoxBarEdgeStyle.findText(key_str)
            self.comboBoxBarEdgeStyle.setCurrentIndex(key_index)
            self.lineEditBarEdgeWidth.setText(str(self.bar_feature.getLineWidth()))

            for key, value in self.hatch_option.items():
                if value == self.bar_feature.getHatch(): key_str = key
            key_index = self.comboBoxBarHatch.findText(key_str)
            self.comboBoxBarHatch.setCurrentIndex(key_index)

    def show_pie_edit_option(self):
        if self.pie_feature is not None:
            self.lineEditPieRadius.setText(str(self.pie_feature.getRadius()))
            self.lineEditPieStartAngle.setText(str(self.pie_feature.getStartAngel()))
            self.lineEditPieLabelDistance.setText(str(self.pie_feature.getLabelDistance()))
            self.lineEditExplodeDistance.setText(str(self.pie_feature.getExplodeDistance()))
            self.checkBoxExplodeMaxSize.setChecked(self.pie_feature.getExplodeMaximum())
            self.checkBoxShowValueLabel.setChecked(self.pie_feature.getShowValueLabel())
            self.checkBoxShadow.setChecked(self.pie_feature.getShadow())

    def set_validator(self):
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)

        # self.txtSeriesFilterValue.setValidator(decimalValidator)

    def add_socket(self):
        self.buttonOpen.clicked.connect(self.buttonOpen_clicked)
        self.buttonModelDataCancel.clicked.connect(self.buttonModelDataCancel_clicked)
        self.buttonBrowseInitFile.clicked.connect(self.buttonBrowseInitFile_clicked)
        self.buttonModelDataOk.clicked.connect(self.buttonModelDataOk_clicked)
        self.buttonGraphVarIn.clicked.connect(self.buttonGraphVarIn_clicked)
        # self.buttonGrpVarOut.clicked.connect(self.buttonGrpVarOut_clicked)
        # self.buttonOk.clicked.connect(self.buttonOk_clicked)
        self.buttonCancel.clicked.connect(self.buttonCancel_clicked)
        #self.checkGroupLabel.clicked.connect(self.checkGroupLabel_toggled)
        self.buttonXAxisIn.clicked.connect(self.buttonXAxisIn_clicked)
        # self.buttonXAxisOut.clicked.connect(self.buttonXAxisOut_clicked)
        self.pushButtonFeatureEdit.clicked.connect(self.pushButtonFeatureEdit_clicked)
        self.pushButtonStyleCancel.clicked.connect(self.pushButtonStyleCancel_clicked)
        self.pushButtonStyleOk.clicked.connect(self.pushButtonStyleOk_clicked)
        self.comboBoxLineStyle.currentIndexChanged.connect(self.comboBoxLineStyle_currentIndexChanged)
        self.pushButtonLineColor.clicked.connect(self.pushButtonLineColor_clicked)
        self.lineEditLineWidth.textChanged.connect(self.lineEditLineWidth_textChanged)
        self.checkBoxLineShowMarker.toggled.connect(self.checkBoxLineShowMarker_toggled)
        self.comboBoxLineMarkerStyle.currentIndexChanged.connect(self.comboBoxLineMarkerStyle_currentIndexChanged)
        self.lineEditLineMarkerSize.textChanged.connect(self.lineEditLineMarkerSize_textChanged)
        self.comboBoxPointStyle.currentIndexChanged.connect(self.comboBoxPointStyle_currentIndexChanged)
        self.pushButtonPointFaceColor.clicked.connect(self.pushButtonPointFaceColor_clicked)
        self.lineEditPointSize.textChanged.connect(self.lineEditPointSize_textChanged)
        self.pushButtonPointEdgeColor.clicked.connect(self.pushButtonPointEdgeColor_clicked)
        self.lineEditPointEdgeWidth.textChanged.connect(self.lineEditPointEdgeWidth_textChanged)
        self.pushButtonBarFillColor.clicked.connect(self.pushButtonBarFillColor_clicked)
        self.pushButtonBarEdgeColor.clicked.connect(self.pushButtonBarEdgeColor_clicked)
        self.comboBoxBarEdgeStyle.currentIndexChanged.connect(self.comboBoxBarEdgeStyle_currentIndexChanged)
        self.lineEditBarEdgeWidth.textChanged.connect(self.lineEditBarEdgeWidth_textChanged)
        self.comboBoxBarHatch.currentIndexChanged.connect(self.comboBoxBarHatch_currentIndexChanged)
        self.comboFilterCondition.currentIndexChanged.connect(self.comboFilterCondition_indexChanged)
        self.buttonFilterVarIn.clicked.connect(self.buttonFilterVarIn_clicked)
        self.radioButtonSetDataSource.toggled.connect(self.radioButtonDataSource_toggle)
        self.radioButtonModelData.toggled.connect(self.radioButtonSource_toggled)

    def radioButtonSource_toggled(self):
        self.comboOutputFileType.clear()

        file_types = []
        cur_ndx = -1

        if self.radioButtonModelData.isChecked():
            self.checkBoxUnitConversion.setEnabled(True)
            self.lineEditModelDirectory.setEnabled(True)
            if self.radioButtonEditDataSource.isChecked():
                file_types = ['day', 'day_veg', 'day_lay', 'day_lay_veg', 'day_totlay',
                              'ann', 'ann_veg', 'ann_lay', 'ann_lay_veg', 'monavg',
                              'monavg_veg', 'annavg', 'annavg_veg']
                if self.data_source is not None:
                    self.lineEditModelDirectory.setText(self.data_source.get_model_directory())
                    self.txtInitFileName.setText(self.data_source.get_initial_filename())
                    self.checkBoxUnitConversion.setChecked(self.data_source.get_unit_conversion_flag())
                    for i in range(len(file_types)):
                        if self.data_source.get_output_filetype() == file_types[i]:
                            cur_ndx = i
                            break
            self.labelInitialFile.setText('Initial File')
        else:
            self.checkBoxUnitConversion.setChecked(False)
            self.checkBoxUnitConversion.setEnabled(False)
            self.lineEditModelDirectory.setEnabled(False)
            self.lineEditModelDirectory.clear()

            file_types = ['csv']
            cur_ndx = 0
            self.labelInitialFile.setText('Obs. (csv) File')
            if self.radioButtonEditDataSource.isChecked():
                if self.data_source is not None:
                    self.txtInitFileName.setText(self.data_source.get_csv_filename())

        self.comboOutputFileType.addItems(file_types)
        self.comboOutputFileType.setCurrentIndex(cur_ndx)

    def radioButtonDataSource_toggle(self):
        if self.radioButtonSetDataSource.isChecked(): self.buttonOpen.setText('Open')
        else: self.buttonOpen.setText('Edit')

    def comboFilterCondition_indexChanged(self):
        #options: ["None", ">","<","=", ">=", "<=", "between"]
        if self.comboFilterCondition.currentIndex() in [1, 2, 3, 4, 5]:
            self.txtFilterValue.setEnabled(True)
            self.txtFilterAndValue.clear()
            self.txtFilterAndValue.setEnabled(False)
        elif self.comboFilterCondition.currentIndex() == 6:
            self.txtFilterValue.setEnabled(True)
            self.txtFilterAndValue.setEnabled(True)
        else:
            self.txtFilterValue.clear()
            self.txtFilterValue.setEnabled(False)
            self.txtFilterAndValue.clear()
            self.txtFilterAndValue.setEnabled(False)


    def comboBoxBarHatch_currentIndexChanged(self):
        if self.comboBoxBarHatch.currentIndex() != -1:
            self.bar_feature.setHatch(self.hatch_option[self.comboBoxBarHatch.currentText()])

    def lineEditBarEdgeWidth_textChanged(self):
        if len(self.lineEditBarEdgeWidth.text()) > 0:
            self.bar_feature.setLineWidth(float(self.lineEditBarEdgeWidth.text()))

    def comboBoxBarEdgeStyle_currentIndexChanged(self):
        if self.comboBoxBarEdgeStyle.currentIndex() != -1:
            self.bar_feature.setLineStyle(self.bar_edge_style[self.comboBoxBarEdgeStyle.currentText()])

    def pushButtonBarEdgeColor_clicked(self):
        col = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.bar_feature.setEdgeColor(col.name())
            self.pushButtonBarEdgeColor.setStyleSheet("QWidget{background-color:%s}" % col.name())

    def pushButtonBarFillColor_clicked(self):
        col = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.bar_feature.setColor(col.name())
            self.pushButtonBarFillColor.setStyleSheet("QWidget{background-color:%s}" % col.name())

    def lineEditPointEdgeWidth_textChanged(self):
        if len(self.lineEditPointEdgeWidth.text()) > 0:
            self.point_feature.setEdgeLineWidth(float(self.lineEditPointEdgeWidth.text()))

    def pushButtonPointEdgeColor_clicked(self):
        col = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.point_feature.setEdgeColor(col.name())
            self.pushButtonPointEdgeColor.setStyleSheet("QWidget{background-color:%s}" % col.name())

    def lineEditPointSize_textChanged(self):
        if len(self.lineEditPointSize.text()) > 0:
            self.point_feature.setSize(float(self.lineEditPointSize.text()))

    def pushButtonPointFaceColor_clicked(self):
        col = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.point_feature.setFaceColor(col.name())
            self.pushButtonPointFaceColor.setStyleSheet("QWidget{background-color:%s}" % col.name())

    def comboBoxPointStyle_currentIndexChanged(self):
        if self.comboBoxPointStyle.currentIndex() != -1:
            self.point_feature.setPointStyle(self.point_style[self.comboBoxPointStyle.currentText()])

    def comboBoxLineStyle_currentIndexChanged(self):
        if self.comboBoxLineStyle.currentIndex() != -1:
            self.line_feature.setStyle(self.line_style[self.comboBoxLineStyle.currentText()])

    def pushButtonLineColor_clicked(self):
        col = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.line_feature.setColor(col.name())
            self.pushButtonLineColor.setStyleSheet("QWidget{background-color:%s}" % col.name())

    def lineEditLineWidth_textChanged(self):
        if len(self.lineEditLineWidth.text()) > 0:
            self.line_feature.setLineWidth(float(self.lineEditLineWidth.text()))

    def checkBoxLineShowMarker_toggled(self):
        if self.line_feature is not None:
            self.line_feature.setShowMarker(self.checkBoxLineShowMarker.isChecked())
            self.comboBoxLineMarkerStyle.setEnabled(self.checkBoxLineShowMarker.isChecked())
            self.lineEditLineMarkerSize.setEnabled(self.checkBoxLineShowMarker.isChecked())

    def comboBoxLineMarkerStyle_currentIndexChanged(self):
        if self.comboBoxLineMarkerStyle.currentIndex != -1:
            self.line_feature.setMarker(self.point_style[self.comboBoxLineMarkerStyle.currentText()])

    def lineEditLineMarkerSize_textChanged(self):
        if len(self.lineEditLineMarkerSize.text()) > 0:
            marker_size = -1
            try: marker_size = int(float(self.lineEditLineMarkerSize.text()))
            except: marker_size = 3

            self.line_feature.setMarkerSize(marker_size)

    def pushButtonStyleCancel_clicked(self):
        self.frameEditOption.setVisible(False)

        self.frameSeriesVariable.setEnabled(True)
        self.listAttributeList.setEnabled(True)
        self.buttonOk.setEnabled(True)
        self.buttonCancel.setEnabled(True)
        self.radioButtonModelData.setEnabled(True)
        self.radioButtonExternalData.setEnabled(True)
        self.buttonOpen.setEnabled(True)

    def pushButtonStyleOk_clicked(self):
        self.frameEditOption.setVisible(False)

        self.frameSeriesVariable.setEnabled(True)
        self.listAttributeList.setEnabled(True)
        self.buttonOk.setEnabled(True)
        self.buttonCancel.setEnabled(True)
        self.radioButtonModelData.setEnabled(True)
        self.radioButtonExternalData.setEnabled(True)
        self.buttonOpen.setEnabled(True)

    def pushButtonFeatureEdit_clicked(self):
        plotting_option = self.comboPlotingOption.currentText().lower()
        if plotting_option == "line":
            self.framePointEdit.setVisible(False)
            self.frameBarEdit.setVisible(False)
            self.framePieEdit.setVisible(False)
            self.frameLineEdit.setVisible(True)
            self.frameLineEdit.setGeometry(10,10, 351, 125)
            self.pushButtonStyleOk.setGeometry(210, 145, 75, 23)
            self.pushButtonStyleCancel.setGeometry(290, 145, 75, 23)
            self.frameEditOption.setGeometry(190,28, 371, 178)
            self.frameEditOption.setVisible(True)
        elif plotting_option in ["bar", "stacked bar"]:
            self.framePointEdit.setVisible(False)
            self.frameBarEdit.setVisible(True)
            self.framePieEdit.setVisible(False)
            self.frameLineEdit.setVisible(False)
            self.frameBarEdit.setGeometry(10,10, 351, 102)
            self.pushButtonStyleOk.setGeometry(210, 122, 75, 23)
            self.pushButtonStyleCancel.setGeometry(290, 122, 75, 23)
            self.frameEditOption.setGeometry(190,28, 371, 155)
            self.frameEditOption.setVisible(True)
        elif plotting_option in ["point", "scatter plot"]:
            self.framePointEdit.setVisible(True)
            self.frameBarEdit.setVisible(False)
            self.framePieEdit.setVisible(False)
            self.frameLineEdit.setVisible(False)
            self.framePointEdit.setGeometry(10,10, 351, 102)
            self.pushButtonStyleOk.setGeometry(210, 122, 75, 23)
            self.pushButtonStyleCancel.setGeometry(290, 122, 75, 23)
            self.frameEditOption.setGeometry(190,28, 371, 155)
            self.frameEditOption.setVisible(True)
        elif plotting_option == "pie":
            self.framePointEdit.setVisible(False)
            self.frameBarEdit.setVisible(False)
            self.framePieEdit.setVisible(True)
            self.frameLineEdit.setVisible(False)
            self.framePieEdit.setGeometry(10,10, 351, 112)
            self.pushButtonStyleOk.setGeometry(210, 132, 75, 23)
            self.pushButtonStyleCancel.setGeometry(290, 132, 75, 23)
            self.frameEditOption.setGeometry(190,28, 371, 165)
            self.frameEditOption.setVisible(True)

        self.frameSeriesVariable.setEnabled(False)
        self.listAttributeList.setEnabled(False)
        self.buttonOk.setEnabled(False)
        self.buttonCancel.setEnabled(False)
        self.radioButtonModelData.setEnabled(False)
        self.radioButtonExternalData.setEnabled(False)
        self.buttonOpen.setEnabled(False)

    def buttonOpen_clicked(self):
        if self.radioButtonSetDataSource.isChecked():
            self.checkBoxUnitConversion.setChecked(True)
            self.txtInitFileName.clear()
            self.comboOutputFileType.clear()
            self.txtInitFileName.clear()
            self.lineEditModelDirectory.clear()
            self.radioButtonModelData.setChecked(True)
        else:
            if self.data_source is not None:
                if self.data_source.source_type == 0:
                    self.radioButtonModelData.setChecked(True)
                else: self.radioButtonExternalData.setChecked(True)
            else: self.radioButtonModelData.setChecked(True)


        self.radioButtonSource_toggled()
        # if self.radioButtonExternalData.isChecked():
        #     self.comboOutputFileType.addItems(["csv"])
        #     self.comboOutputFileType.setCurrentIndex(0)

        self.frameOpenModelData.setVisible(True)
        self.frameSeriesVariable.setEnabled(False)
        self.listAttributeList.setEnabled(False)
        self.buttonOk.setEnabled(False)
        self.buttonCancel.setEnabled(False)
        self.radioButtonSetDataSource.setEnabled(False)
        self.radioButtonEditDataSource.setEnabled(False)
        self.buttonOpen.setEnabled(False)
        self.frameGraphType.setEnabled(False)


    def buttonBrowseInitFile_clicked(self):
        init_dir = ApplicationProperty.currentModelDirectory
        if len(init_dir) == 0: init_dir = ApplicationProperty.getScriptPath()

        if self.radioButtonModelData.isChecked():
            file_name = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', init_dir, "Initial File (*.ini)")

            if len(file_name) > 0:
                initial_parameter = FileReadWrite.readInitialFile(file_name)
                if initial_parameter is not None:
                    temp = file_name.split("/")[-1]
                    self.txtInitFileName.setText(temp)
                    ApplicationProperty.currentModelDirectory = file_name.replace("ini/" + temp, "")
                    self.lineEditModelDirectory.setText(ApplicationProperty.currentModelDirectory)

                    #generating list of output files and check their availability
                    self.output_file_list = ReadBinaryOutput.GenerateListOfOutputFiles(initial_parameter, ApplicationProperty.currentModelDirectory)

                    #inserting output file names in combo box
                    if len(self.output_file_list) > 0:

                        self.comboOutputFileType.addItems(self.output_file_list)
                        self.comboOutputFileType.setCurrentIndex(-1)

                else:
                    message = "The initial file could not be opened. Please choose a valid initial file."
                    QtGui.QMessageBox.about(self.form, "Invalid Initial File", message)
        else:
            file_name = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Open File', init_dir, "CSV File (*.csv)")
            if len(file_name) > 0:
                self.txtInitFileName.setText(file_name)



    def buttonModelDataCancel_clicked(self):
        self.txtInitFileName.clear()
        self.frameOpenModelData.setVisible(False)

        self.frameSeriesVariable.setEnabled(True)
        self.listAttributeList.setEnabled(True)
        self.buttonOk.setEnabled(True)
        self.buttonCancel.setEnabled(True)
        self.radioButtonSetDataSource.setEnabled(True)
        self.radioButtonEditDataSource.setEnabled(True)
        self.buttonOpen.setEnabled(True)
        self.frameGraphType.setEnabled(True)

    def buttonModelDataOk_clicked(self):
        filename = ''
        source_type = -1
        file_type = ''
        if self.radioButtonModelData.isChecked():
            if self.comboOutputFileType.currentIndex() != -1:
                filename =  self.txtInitFileName.text()
                file_type = self.comboOutputFileType.currentText()

                self.read_result = ReadBinaryOutput.ReadModelOutput(ApplicationProperty.currentModelDirectory, filename,
                                                                    file_type, trim=True, post_processing=True, ucf=True)
                source_type = 0
        else:
            filename = self.txtInitFileName.text()
            self.read_result = ReadExternalOutput.read_csv_file(filename, ",")
            source_type = 1

        if source_type != -1:
            if self.data_source is None: self.data_source = DataSource()
            self.data_source.source_type = source_type
            if source_type == 0:
                self.data_source.initial_filename = filename
                self.data_source.model_directory = self.lineEditModelDirectory.text()
                self.data_source.output_file_type = file_type
                if self.checkBoxUnitConversion.isChecked(): self.data_source.unit_conversion_flag = True
                else: self.data_source.unit_conversion_flag = False
            else:
                self.data_source.source_type = 1
                self.data_source.data_filename_csv = filename

            if len(self.read_result.record_list) > 0:
                self.listAttributeList.clear()
                self.listAttributeList.addItems(self.read_result.header_variable)
                #self.clear_field()

            self.frameOpenModelData.setVisible(False)

            self.frameSeriesVariable.setEnabled(True)
            self.listAttributeList.setEnabled(True)
            self.buttonOk.setEnabled(True)
            self.buttonCancel.setEnabled(True)
            self.radioButtonSetDataSource.setEnabled(True)
            self.radioButtonEditDataSource.setEnabled(True)
            self.buttonOpen.setEnabled(True)
            self.frameGraphType.setEnabled(True)

    def buttonGraphVarIn_clicked(self):
        if self.buttonGraphVarIn.text() == ">":
            if self.listGraphVariable.count() == 0:
                for i in range(self.listAttributeList.count()):
                    item = self.listAttributeList.item(i)
                    if item.isSelected():
                        self.listGraphVariable.addItem(item.text())
                        self.buttonGraphVarIn.setText("<")
                        self.txtSeriesTitle.setEnabled(True)
                        break
        else:
            self.listGraphVariable.clear()
            self.txtSeriesTitle.clear()
            self.buttonGraphVarIn.setText(">")
            self.txtSeriesTitle.clear()
            self.txtSeriesTitle.setEnabled(False)


    def buttonCancel_clicked(self):
        self.form.close()

    def buttonOk_clicked(self):
        # if self.model_plot is not None:
        if self.listGraphVariable.count() == 0:
            message = "No data has been selected. Please select data."
            QtGui.QMessageBox.about(self.form, "Nothing Selected", message)
        elif self.comboPlotingOption.currentIndex() == -1:
            message = "Please choose plotting option."
            QtGui.QMessageBox.about(self.form, "Required Field", message)
            self.comboPlotingOption.setFocus(True)
        elif self.listFilterVar.count() > 0 and (self.comboFilterCondition.currentIndex() <= 0):
            message = "Please choose a filtering condition."
            QtGui.QMessageBox.about(self.form, "Select Condition", message)
            self.comboFilterCondition.setFocus(True)
        elif self.comboFilterCondition.currentIndex() > 0 and len(self.txtFilterValue.text()) == 0:
            message = "Please enter filter value."
            QtGui.QMessageBox.about(self.form, "Required Field", message)
            self.txtFilterValue.setFocus(True)
        elif self.comboFilterCondition.currentIndex() == 6 and len(self.txtFilterAndValue.text()) == 0:
            message = "Please enter the second value"
            QtGui.QMessageBox.about(self.form, "Required Field", message)
            self.txtFilterAndValue.setFocus(True)
        elif self.comboPlotingOption.currentIndex() == 3 and len(self.model_plot.list_of_series) > 0:
            message = "You cannot more than one series in Pie Plot."
            QtGui.QMessageBox.about(self.form, "No more series allowed", message)
        else:
            succeed = False
            series = self.create_new_series()
            if series is not None and self.model_plot is not None:
                if self.current_series_index >= 0:
                    self.model_plot.list_of_series[self.current_series_index] = series
                    self.model_plot.calculate_axes_limit()
                    succeed = True
                else:
                    succeed = self.model_plot.add_series(series)
                    if not succeed:
                        message = "A series with same attribute is already present."
                        QtGui.QMessageBox.about(self.form, "Duplicate Series", message)
                        return None
            if succeed:
                self.form.close()
                return series
            else:
                message = "An unexpected error occur! Please Close the utility and try again."
                QtGui.QMessageBox.about(self.form, "Unexpected Error", message)

    def clear_field(self):
        self.listGraphVariable.clear()
        self.buttonGraphVarIn.setText(">")
        self.txtSeriesTitle.clear()
        self.comboPlotingOption.setCurrentIndex(1)
        self.listXAxisVariable.clear()
        self.buttonXAxisIn.setText(">")
        self.buttonXAxisIn.setEnabled(True)
        self.listXAxisVariable.setEnabled(True)
        self.buttonFilterVarIn.setText(">")
        self.listFilterVar.clear()
        self.comboFilterCondition.setEnabled(False)
        self.comboFilterCondition.setCurrentIndex(-1)
        self.frameEditOption.setVisible(False)

        self.point_feature = PointEditFeature()
        self.line_feature = LineEditFeature()
        self.bar_feature = BarEditFeature()
        self.pie_feature = PieEditFeature()

        self.show_line_edit_option()
        self.show_point_edit_option()
        self.show_bar_edit_option()
        self.show_pie_edit_option()



    def buttonXAxisIn_clicked(self):
        if self.buttonXAxisIn.text() == ">":
            if self.listXAxisVariable.count() == 0:
                for i in range(self.listAttributeList.count()):
                    item = self.listAttributeList.item(i)
                    if item.isSelected():
                        self.listXAxisVariable.addItem(item.text())
                        self.buttonXAxisIn.setText("<")


        else:
            self.listXAxisVariable.clear()
            self.buttonXAxisIn.setText(">")

    # def x_axis_settings(self):
    #     if self.model_plot.series_index_referring_x_axis != -1:
    #         self.buttonXAxisIn.setEnabled(False)
    #         self.listXAxisVariable.setEnabled(False)
    #
    #         x_axis_series = self.model_plot.find_series_by_index(self.model_plot.series_index_referring_x_axis)
    #         if x_axis_series.group_flag:
    #
    #             #data source must be checked.......
    #             similar_source = True
    #             for grp_var in x_axis_series.group_variables:
    #                 for i in range(self.listAttributeList.count()):
    #                     if self.listAttributeList.item(i).text() == grp_var: break
    #                 else:
    #                     similar_source = False
    #                     break
    #
    #             for grp_var in x_axis_series.group_variables:
    #                 if not similar_source: grp_var += " [unknown]"
    #                 item = QtGui.QListWidgetItem(grp_var)
    #                 self.listGroupVariable.addItem(item)
    #
    #             for i in range(self.comboGroupFunction.count()):
    #                 if self.comboGroupFunction.itemText(i) == x_axis_series.group_function:
    #                     self.comboGroupFunction.setCurrentIndex(i)
    #                     break
    #             if x_axis_series.group_filter_flag:
    #                 for i in range(self.comboGroupFilterCondition.count()):
    #                     if self.comboGroupFilterCondition.itemText(i) == x_axis_series.group_filter_condition:
    #                         self.comboGroupFilterCondition.setCurrentIndex(i)
    #                         break
    #                 self.txtGroupFilterValue.setText(str(x_axis_series.group_filter_value))
    #                 self.checkNumericComparison.setChecked(x_axis_series.group_filtering_numeric_comparison)
    #         else:
    #             similar_source = True
    #             for i in range(self.listAttributeList.count()):
    #                 if self.listAttributeList.item(i).text() == x_axis_series.x_axis_variable:
    #                     item = QtGui.QListWidgetItem(x_axis_series.x_axis_variable)
    #                     self.listXAxisVariable.addItem(item)
    #             else:
    #                 item = QtGui.QListWidgetItem(x_axis_series.x_axis_variable + "[unknown]")
    #                 self.listXAxisVariable.addItem(item)
    #                 self.buttonXAxisIn.setText("<")

    def load_series(self):
        series = None

        if self.model_plot is not None and self.current_series_index >= 0:
            series = self.model_plot.list_of_series[self.current_series_index]

        if series is not None:
            self.listGraphVariable.addItem(series.attribute_name)
            self.buttonGraphVarIn.setText("<")
            self.txtSeriesTitle.setText(series.series_title)

            if len(series.x_axis_variable) > 0:
                self.listXAxisVariable.addItem(series.x_axis_variable)
                self.buttonXAxisIn.setText("<")

            if len(series.filter_variable) > 0:
                self.listFilterVar.addItem(series.filter_variable)
                self.buttonFilterVarIn.setText("<")
                ndx = self.comboFilterCondition.findText(series.filter_condition)
                self.comboFilterCondition.setCurrentIndex(ndx)
                if series.filter_first_value is not None: self.txtFilterValue.setText(str(series.filter_first_value))
                if series.filter_second_value is not None: self.txtFilterAndValue.setText(str(series.filter_second_value))

            if series.plotting_option.lower() in ["point", "scatter plot"]:
                self.point_feature = series.edit_feature
                self.show_point_edit_option()
            elif series.plotting_option.lower() == "line":
                self.line_feature = series.edit_feature
                self.show_line_edit_option()
            elif series.plotting_option.lower() in ["bar", "stacked bar"]:
                self.bar_feature = series.edit_feature
                self.show_bar_edit_option()
            elif series.plotting_option.lower() == "pie":
                self.pie_feature = series.edit_feature
                self.show_pie_edit_option()
            option_index = self.comboPlotingOption.findText(series.plotting_option)
            self.comboPlotingOption.setCurrentIndex(option_index)

            #check if the series data source is the same as current data source. If they are not the same
            #load data from the series data source. (Note: it could be a bit time consuming but would be
            #very user friendly.

            if (self.data_source is None) or (self.data_source != series.data_source):
                self.data_source = copy.deepcopy(series.data_source)
                self.read_result = series.read_source_datafile()

                if len(self.read_result.header_variable) > 0:
                    self.listAttributeList.clear()
                    self.listAttributeList.addItems(self.read_result.header_variable)



    def create_new_series(self):
        series = None
        if self.data_source is not None:
            var_name = self.listGraphVariable.item(0).text()

            series = DataSeries(var_name)
            series.series_title = self.txtSeriesTitle.text()
            if series.series_title == "": series.series_title = series.attribute_name

            series.data_source = copy.deepcopy(self.data_source)
            series.plotting_option = self.comboPlotingOption.currentText()

            if series.plotting_option.lower() == "line":
                series.setEditFeature(self.line_feature)
            elif series.plotting_option.lower() in ["point", "scatter plot"]:
                series.setEditFeature(self.point_feature)
            elif series.plotting_option.lower() in ["bar", "stacked bar"]:
                series.setEditFeature(self.bar_feature)
            elif series.plotting_option.lower() == "pie":
                series.setEditFeature(self.pie_feature)

            if self.listXAxisVariable.count() > 0:
                series.x_axis_variable = self.listXAxisVariable.item(0).text()

            if self.listFilterVar.count() > 0:
                series.filter_variable = self.listFilterVar.item(0).text()
                series.filter_condition = self.comboFilterCondition.currentText()
                first_value = self.txtFilterValue.text().strip()
                if len(first_value) > 0:
                    try: series.filter_first_value = int(first_value)
                    except:
                        try: series.filter_first_value = float(first_value)
                        except:
                            try: series.filter_first_value = datetime.strptime(first_value, "%d-%m-%Y").date()
                            except: series.filter_first_value = first_value

                second_value = self.txtFilterAndValue.text().strip()
                if len(second_value) > 0:
                    try: series.filter_second_value = int(second_value)
                    except:
                        try: series.filter_second_value = float(second_value)
                        except:
                            try: series.filter_second_value = datetime.strptime(second_value, "%d-%m-%Y").date()
                            except: series.filter_second_value = second_value

            #collecting data
            var_data = ReadBinaryOutput.ExtractColumnRecord(var_name, self.read_result.header_variable, self.read_result.record_list)
            x_data = None
            if series.x_axis_variable:
                x_data = ReadBinaryOutput.ExtractColumnRecord(series.x_axis_variable, self.read_result.header_variable, self.read_result.record_list)

            if series.filter_variable:
                filter_var_data = ReadBinaryOutput.ExtractColumnRecord(series.filter_variable, self.read_result.header_variable, self.read_result.record_list)

                if series.x_axis_variable:
                    ReadBinaryOutput.Filter([var_data, x_data, filter_var_data], 2, series.filter_condition, series.filter_first_value, series.filter_second_value)
                else:
                    ReadBinaryOutput.Filter([var_data, filter_var_data], 1, series.filter_condition, series.filter_first_value, series.filter_second_value)

            series.series_data = var_data
            series.x_axis_data = x_data

            #special case for stem carbon
            #Attention!!
            #this code block has been used in 'graph.py' (ModelGraph.read_data_from_source_file). any modification should be carried out both the places
            if series.attribute_name in ['cs_vegt_cum_harvest_stem_tot', 'cs_vegt_stem_harvest_stem_tot_cum']:
                model_directory = series.data_source.get_model_directory()
                init_filename = series.data_source.get_initial_filename()
                rc_list = ['cf_vegt_harvest_stem_tot', 'year']
                rc = ReadBinaryOutput.SpecialDataFieldsFromOutputFile(model_directory, init_filename, 'annavg_veg', rc_list)

                start_year = min(series.x_axis_data)
                if series.attribute_name == 'cs_vegt_stem_harvest_stem_tot_cum':
                    rc_list.append('cs_vegt_sum_stem')
                    rc.append(ReadBinaryOutput.ExtractColumnRecord('cs_vegt_sum_stem', self.read_result.header_variable, self.read_result.record_list))
                    series.series_data = ReadBinaryOutput.RecalStemCarbonField(start_year, rc_list, rc)[1]
                else: series.series_data = ReadBinaryOutput.RecalStemCarbonField(start_year, rc_list, rc)[0]
        return series

    def buttonFilterVarIn_clicked(self):
        if self.buttonFilterVarIn.text() == ">":
            if self.listFilterVar.count() == 0:
                for i in range(self.listAttributeList.count()):
                    item = self.listAttributeList.item(i)
                    if item.isSelected():
                        self.listFilterVar.addItem(item.text())
                        self.buttonFilterVarIn.setText("<")
                        self.comboFilterCondition.setEnabled(True)
                        break
        else:
            self.listFilterVar.clear()
            self.buttonFilterVarIn.setText(">")
            self.comboFilterCondition.setCurrentIndex(-1)
            self.comboFilterCondition.setEnabled(False)
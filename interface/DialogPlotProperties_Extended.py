from interface.DialogPlotProperties import Ui_DialogPlotProperties
from PyQt5 import QtGui, QtCore, QtWidgets


class DialogPlotProperties(Ui_DialogPlotProperties):
    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)
        self.add_socket()
        self.plot = None

        self.initial_settings()




    def add_socket(self):
        self.checkBoxShowPlotTitle.toggled.connect(self.checkBoxShowPlotTitle_toggled)
        self.lineEditFontSize.textChanged.connect(self.lineEditFontSize_textChanged)
        self.pushButtonPlotFontColor.clicked.connect(self.pushButtonPlotFontColor_clicked)
        self.comboBoxPlotHorizontalAlignment.currentIndexChanged.connect(self.comboBoxPlotHorizontalAlignment_currentIndexChanged)
        self.lineEditXAxisMajorInterval.textChanged.connect(self.lineEditXAxisMajorInterval_textChanged)
        self.lineEditXAxisMinorInterval.textChanged.connect(self.lineEditXAxisMinorInterval_textChanged)
        self.lineEditYAxisMajorInterval.textChanged.connect(self.lineEditYAxisMajorInterval_textChanged)
        self.lineEditYAxisMinorInterval.textChanged.connect(self.lineEditYAxisMinorInterval_textChanged)
        self.checkBoxShowGridLine.toggled.connect(self.checkBoxShowGridLine_toggled)
        self.checkBoxPlotTitleBold.toggled.connect(self.checkBoxPlotTitleBold_toggled)
        self.comboBoxAxisOption.currentIndexChanged.connect(self.comboBoxAxisOption_currentIndexChanged)
        self.comboBoxGridType.currentIndexChanged.connect(self.comboBoxGridType_currentIndexChanged)
        self.pushButtonPlotEditOk.clicked.connect(self.pushButtonPlotEditOk_clicked)

    def add_validator(self):
        rx = QtCore.QRegExp("^[0-9]*$")
        integerValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)

        self.lineEditXAxisMajorInterval.setValidator(decimalValidator)
        self.lineEditXAxisMinorInterval.setValidator(decimalValidator)
        self.lineEditYAxisMajorInterval.setValidator(decimalValidator)
        self.lineEditYAxisMinorInterval.setValidator(decimalValidator)
        self.lineEditFontSize.setValidator(integerValidator)

    def initial_settings(self):
        self.comboBoxPlotHorizontalAlignment.addItems(["Left", "Center", "Right"])
        self.comboBoxAxisOption.addItems(["X-Axis", "Y-Axis", "Both"])
        self.comboBoxGridType.addItems(["Major Grid", "Minor Grid", "Both"])
        self.comboBoxPlotFont.setEnabled(False)

    def checkBoxShowPlotTitle_toggled(self):
        if self.plot is not None:
            self.plot.edit_feature.setShowPlotTitle(self.checkBoxShowPlotTitle.isChecked())

    def lineEditFontSize_textChanged(self):
        if self.plot is not None and len(self.lineEditFontSize.text()) > 0:
            self.plot.edit_feature.setTitleFontSize(float(self.lineEditFontSize.text()))

    def pushButtonPlotFontColor_clicked(self):
        if self.plot is not None:
            col = QtGui.QColorDialog.getColor()
            if col.isValid():
                self.plot.edit_feature.setTitleFontColor(col.name())
                self.pushButtonPlotFontColor.setStyleSheet("QWidget{background-color:%s}" % col.name())

    def checkBoxPlotTitleBold_toggled(self):
        if self.plot is not None:
            self.plot.edit_feature.setTitleBold(self.checkBoxPlotTitleBold.isChecked())

    def comboBoxPlotHorizontalAlignment_currentIndexChanged(self):
        if self.plot is not None:
            cur_index = self.comboBoxPlotHorizontalAlignment.currentIndex()
            if cur_index == 0: self.plot.edit_feature.setTitleHorizontalAlignment("left")
            elif cur_index == 1: self.plot.edit_feature.setTitleHorizontalAlignment("center")
            elif cur_index == 2: self.plot.edit_feature.setTitleHorizontalAlignment("right")

    def lineEditXAxisMajorInterval_textChanged(self):
        if self.plot is not None and len(self.lineEditXAxisMajorInterval.text()) > 0:
            self.plot.edit_feature.setXAxisMajorInterval(float(self.lineEditXAxisMajorInterval.text()))

    def lineEditXAxisMinorInterval_textChanged(self):
        if self.plot is not None and len(self.lineEditXAxisMinorInterval.text()) > 0:
            self.plot.edit_feature.setXAxisMinorInterval(float(self.lineEditXAxisMinorInterval.text()))

    def lineEditYAxisMajorInterval_textChanged(self):
        if self.plot is not None and len(self.lineEditYAxisMajorInterval.text()) > 0:
            self.plot.edit_feature.setYAxisMajorInterval(float(self.lineEditYAxisMajorInterval.text()))

    def lineEditYAxisMinorInterval_textChanged(self):
        if self.plot is not None and len(self.lineEditYAxisMinorInterval.text()) > 0:
            self.plot.edit_feature.setYAxisMinorInterval(float(self.lineEditYAxisMinorInterval.text()))

    def checkBoxShowGridLine_toggled(self):
        if self.plot is not None:
            self.plot.edit_feature.setGridShowOption(self.checkBoxShowGridLine.isChecked())

    def comboBoxAxisOption_currentIndexChanged(self):
        if self.plot is not None:
            cur_index = self.comboBoxAxisOption.currentIndex()
            if cur_index == 0: self.plot.edit_feature.setGridAxisOption("x")
            elif cur_index == 1: self.plot.edit_feature.setGridAxisOption("y")
            elif cur_index == 2: self.plot.edit_feature.setGridAxisOption("both")

    def comboBoxGridType_currentIndexChanged(self):
        if self.plot is not None:
            cur_index = self.comboBoxGridType.currentIndex()
            if cur_index == 0: self.plot.edit_feature.setGridAxisOption("major")
            elif cur_index == 1: self.plot.edit_feature.setGridAxisOption("minor")
            elif cur_index == 2: self.plot.edit_feature.setGridAxisOption("both")

    def set_values(self):
        if self.plot is not None:
            ef = self.plot.edit_feature
            self.checkBoxShowPlotTitle.setChecked(ef.getShowPlotTitle())
            self.lineEditFontSize.setText(str(ef.getTitleFontSize()))
            self.pushButtonPlotFontColor.setStyleSheet("QWidget { background-color: %s }" % ef.getTitleFontColor())
            self.checkBoxPlotTitleBold.setChecked(ef.getTitleBold())
            option_index = -1
            if ef.getTitleHorizontalAlignment() == "left": option_index = 0
            elif ef.getTitleHorizontalAlignment() == "center": option_index = 1
            elif ef.getTitleHorizontalAlignment() == "right": option_index = 2
            self.comboBoxPlotHorizontalAlignment.setCurrentIndex(option_index)

            self.lineEditXAxisMajorInterval.setText(str(ef.getXAxisMajorInterval()))
            self.lineEditXAxisMinorInterval.setText(str(ef.getXAxisMinorInterval()))
            self.lineEditYAxisMajorInterval.setText(str(ef.getYAxisMajorInterval()))
            self.lineEditYAxisMinorInterval.setText(str(ef.getYAxisMinorInterval()))

            self.checkBoxShowGridLine.setChecked(ef.getGridShowOption())

            option_index = -1
            if ef.getGridAxisOption() == "x": option_index = 0
            elif ef.getGridAxisOption() == "y": option_index = 1
            elif ef.getGridAxisOption() == "both": option_index = 2
            self.comboBoxAxisOption.setCurrentIndex(option_index)

            option_index = -1
            if ef.getGridWhichOption() == "major": option_index = 0
            elif ef.getGridWhichOption() == "minor": option_index = 1
            elif ef.getGridWhichOption() == "both": option_index = 2
            self.comboBoxGridType.setCurrentIndex(option_index)

    def pushButtonPlotEditOk_clicked(self):
        self.form.close()
from interface.DialogGraphProperties import Ui_DialogGraphProperties
from PyQt5 import QtGui, QtCore, QtWidgets

class DialogGraphProperties(Ui_DialogGraphProperties):
    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)
        self.add_socket()

        self.model_graph = None
        self.initial_settings()


    def add_socket(self):
        self.lineEditWindowWidth.textChanged.connect(self.lineEditWindowWidth_textChanged)
        self.lineEditWindowHeight.textChanged.connect(self.lineEditWindowHeight_textChanged)
        self.lineEditWindowTitle.textChanged.connect(self.lineEditWindowTitle_textChanged)
        self.pushButtonGraphFaceColor.clicked.connect(self.pushButtonGraphFaceColor_clicked)
        self.checkBoxShowGraphTitle.toggled.connect(self.checkBoxShowGraphTitle_toggled)
        self.lineEditGraphFontSize.textChanged.connect(self.lineEditGraphFontSize_textChanged)
        self.pushButtonGraphFontColor.clicked.connect(self.pushButtonGraphFontColor_clicked)
        self.checkBoxGraphTitleBold.toggled.connect(self.checkBoxGraphTitleBold_toggled)
        self.comboBoxGraphHorizontalAlignment.currentIndexChanged.connect(self.comboBoxGraphHorizontalAlignment_currentIndexChanged)
        self.pushButtonGraphEditOk.clicked.connect(self.pushButtonGraphEditOk_clicked)


    def add_validator(self):
        rx = QtCore.QRegExp("^[0-9]*$")
        integerValidator = QtGui.QRegExpValidator(rx)
        rx = QtCore.QRegExp("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
        decimalValidator = QtGui.QRegExpValidator(rx)

        self.lineEditWindowWidth.setValidator(integerValidator)
        self.lineEditWindowHeight.setValidator(integerValidator)
        self.lineEditGraphFontSize.setValidator(decimalValidator)

    def initial_settings(self):
        self.comboBoxGraphHorizontalAlignment.addItems(["Left", "Center", "Right"])
        self.comboBoxGraphFont.setEnabled(False)

    def set_values(self):
        if self.model_graph is not None:
            self.lineEditWindowWidth.setText(str(self.model_graph.edit_feature.getWidth()))
            self.lineEditWindowHeight.setText(str(self.model_graph.edit_feature.getHeight()))
            self.lineEditWindowTitle.setText(str(self.model_graph.edit_feature.getTitle()))
            self.pushButtonGraphFaceColor.setStyleSheet("QWidget{background-color:%s}" % self.model_graph.edit_feature.getFaceColor())
            self.checkBoxShowGraphTitle.setChecked(self.model_graph.edit_feature.getShowFigureTitle())
            self.lineEditGraphFontSize.setText(str(self.model_graph.edit_feature.getFontSize()))
            self.pushButtonGraphFontColor.setStyleSheet("QWidget{background-color:%s}" % self.model_graph.edit_feature.getFontColor())
            self.checkBoxGraphTitleBold.setChecked(self.model_graph.edit_feature.getShowBold())
            ndx = self.comboBoxGraphHorizontalAlignment.findText(self.model_graph.edit_feature.getHorizontalAlignment())
            if ndx >=0: self.comboBoxGraphHorizontalAlignment.setCurrentIndex(ndx)

    def lineEditWindowWidth_textChanged(self):
        if self.model_graph is not None and len(self.lineEditWindowWidth.text()) > 0:
            self.model_graph.edit_feature.setWidth(int(self.lineEditWindowWidth.text()))

    def lineEditWindowHeight_textChanged(self):
        if self.model_graph is not None and len(self.lineEditWindowHeight.text()) > 0:
            self.model_graph.edit_feature.setHeight(int(self.lineEditWindowHeight.text()))

    def lineEditWindowTitle_textChanged(self):
        if self.model_graph is not None and len(self.lineEditWindowTitle.text()) > 0:
            self.model_graph.edit_feature.setTitle(self.lineEditWindowTitle.text())

    def pushButtonGraphFaceColor_clicked(self):
        col = QtGui.QColorDialog.getColor()
        if self.model_graph is not None and col.isValid():
            self.model_graph.edit_feature.setFaceColor(col.name())
            self.pushButtonGraphFaceColor.setStyleSheet("QWidget{background-color:%s}" % col.name())

    def checkBoxShowGraphTitle_toggled(self):
        if self.model_graph is not None:
            self.model_graph.edit_feature.setShowFigureTitle(self.checkBoxShowGraphTitle.isChecked())

    def lineEditGraphFontSize_textChanged(self):
        if self.model_graph is not None and len(self.lineEditGraphFontSize.text()) > 0:
            self.model_graph.edit_feature.setFontSize(float(self.lineEditGraphFontSize.text()))

    def pushButtonGraphFontColor_clicked(self):
        col = QtGui.QColorDialog.getColor()
        if self.model_graph is not None and col.isValid():
            self.model_graph.edit_feature.setFontColor(col.name())
            self.pushButtonGraphFontColor.setStyleSheet("QWidget{background-color:%s}" % col.name())

    def checkBoxGraphTitleBold_toggled(self):
        if self.model_graph is not None:
            self.model_graph.edit_feature.setShowBold(self.checkBoxGraphTitleBold.isChecked())

    def comboBoxGraphHorizontalAlignment_currentIndexChanged(self):
        if self.model_graph is not None:
            cur_index = self.comboBoxGraphHorizontalAlignment.currentIndex()
            if cur_index == 0: self.model_graph.edit_feature.setHorizontalAlignment("left")
            elif cur_index == 1: self.model_graph.edit_feature.setHorizontalAlignment("center")
            elif cur_index == 2: self.model_graph.edit_feature.setHorizontalAlignment("right")

    def pushButtonGraphEditOk_clicked(self):
        self.form.close()
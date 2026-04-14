#!/usr/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

from application import ApplicationProperty
from interface.FormMain_Extended import FormMain
# from interface.DialogGraphData_Extended import DialogGraphData
from interface.FormHopspackProblemDefinition_Extended import FormHopspackProblemDefinition


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    ApplicationProperty.screenWidth = screen_rect.width()
    ApplicationProperty.screenHeight = screen_rect.height()
    # FormInOutSetting = QtWidgets.QWidget()
    # ui = FormInitialAndOutputSetting()
    # ui.form.showMaximized()
    # ui = FormEpcFile()
    ui = FormMain()
    #ui = FormHopspackProblemDefinition()
    # ui = FormGraph()
    # ui = DialogGraphData()
    # ui = FormShowGraph()
    # ui = FormDesignGraph()
    # ui = FormReadOutput()
    # ui = FormModelRun()
    # ui = FormSoilProfile()
    ui.form.showMaximized()
    #ui.form.show()
    # ui.setupUi(FormInOutSetting)
    # FormInOutSetting.show()
    sys.exit(app.exec_())


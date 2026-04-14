from interface.DialogShowLog import Ui_DialogShowLog
from PyQt5 import QtGui, QtWidgets
import os

class DialogLogShow(Ui_DialogShowLog):
    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        self.add_socket()

    def add_socket(self):
        self.buttonClose.clicked.connect(self.buttonClose_clicked)

    def buttonClose_clicked(self):
        self.form.close()

    def show_log_file(self, filename):
        log_text = ""

        if os.path.exists(filename):
            f = None
            try:
                f = open(filename, 'r')
                log_text = f.read()
            except: pass
            finally:
                try: f.close()
                except: pass

        if log_text: self.textBrowser.setText(log_text)

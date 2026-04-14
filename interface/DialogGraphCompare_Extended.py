from interface.DialogGraphCompare import Ui_DialogGraphCompare
from PyQt5 import QtGui, QtCore, QtWidgets


class DialogGraphCompare(Ui_DialogGraphCompare):
    def __init__(self):
        self.form = QtWidgets.QDialog()
        self.setupUi(self.form)

        self.add_socket()

        self.all_available_graphs = []  #structure = [{"version_index": 1, "graph_name": graph_name, "image_file": image_file}, {}]
        self.current_version_index = -1
        self.sa_width = 824
        self.sa_height = 449

        self.widgetContents = None

    def add_socket(self):
        self.buttonClose.clicked.connect(self.buttonClose_clicked)
        self.radioGraphCurrentVerion.toggled.connect(self.radio_button_toggled)
        self.comboGraphName.currentIndexChanged.connect(self.comboGraphName_currentIndexChanged)

    def buttonClose_clicked(self):
        self.form.close()

    def set_window_title(self, title):
        self.form.setWindowTitle(title)

    def radio_button_toggled(self):
        if self.radioGraphCurrentVerion.isChecked():
            if self.widgetContents:
                self.widgetContents.setParent(None)
                self.widgetContents = None
            self.comboGraphName.setEnabled(False)
            self.comboGraphName.setCurrentIndex(-1)

            if self.current_version_index >= 0:
                graph_list = []
                for item in self.all_available_graphs:
                    if item["version_index"] == self.current_version_index:
                        graph_list.append(item)
                self.draw_graph(graph_list)
        else:
            if self.widgetContents:
                self.widgetContents.setParent(None)
                self.widgetContents = None
            self.comboGraphName.setEnabled(True)

    def comboGraphName_currentIndexChanged(self):
        if self.comboGraphName.currentIndex() >= 0:
            graph_name = self.comboGraphName.currentText()
            graph_list = []
            for item in self.all_available_graphs:
                    if item["graph_name"] == graph_name:
                        graph_list.append(item)
            self.draw_graph(graph_list)

    def draw_graph(self, graph_list):
        graph_count = len(graph_list)
        if graph_count > 0:
            self.widgetContents = QtWidgets.QWidget()
            graphics_view_list = []
            if graph_count == 1:
                self.widgetContents.setGeometry(QtCore.QRect(0, 0, self.sa_width - 40, self.sa_height))
                x = (self.sa_width - 520) // 2
                y = (self.sa_height - 390 - 30) // 2
                graphicsView = QtGui.QGraphicsView(self.widgetContents)
                graphicsView.setGeometry(x, y, 520, 390)
                scene = QtGui.QGraphicsScene()
                pix_map = QtGui.QPixmap(graph_list[0]["image_file"])
                scene.addPixmap(pix_map)
                graphicsView.setScene(scene)

                label = QtGui.QLabel(self.widgetContents)
                label.setGeometry(QtCore.QRect(x, y + 400, 520, 20))
                label.setText("Figure: " + graph_list[0]["graph_name"])
                graphics_view_list.append(graphicsView)
            else:
                self.widgetContents.setGeometry(QtCore.QRect(0, 0, self.sa_width - 40, max(self.sa_height, ((graph_count - 1)//2 + 1) * 350)))
                x = (self.sa_width - 10 - 388 * 2) // 2
                y = x
                y_init = y

                for i in range(graph_count):
                    item = graph_list[i]
                    if i%2 == 0:
                        x = (self.sa_width - 10 - 388 * 2) // 2
                        y = y_init + (i//2) * 321
                    else: x += 398

                    graphicsView = QtGui.QGraphicsView(self.widgetContents)
                    graphicsView.setGeometry(x, y, 388, 291)
                    scene = QtGui.QGraphicsScene()
                    pix_map = QtGui.QPixmap(item["image_file"])
                    scene.addPixmap(pix_map)
                    graphicsView.setScene(scene)

                    label = QtGui.QLabel(self.widgetContents)
                    label.setGeometry(QtCore.QRect(x, y + 290, 388, 20))
                    label.setText("Figure-"+ str(i+1).rjust(2,"0") + ": " + item["graph_name"] + "(version: "+ str(item["version_index"]) +")")
                    graphics_view_list.append(graphicsView)

            if graphics_view_list:
                self.scrollAreaGraph.setWidget(self.widgetContents)
                for graph_view in graphics_view_list:
                    graph_view.fitInView(scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
                    graph_view.show()





import sys
from PyQt4.QtGui import *

class MyWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUI()
        self.apptext = ""

    def setupUI(self):


        #self.layout = QGridLayout()
        self.appLayout = QHBoxLayout()
        self.appLabel = QLabel("App Name :")
        self.appLineEdit = QLineEdit()
        self.appLineEdit.textChanged.connect(self.setAppName)
        self.appProcessButton = QPushButton("$(Process)")
        self.appProcessButton.clicked.connect(self.addProcess)
        self.appLayout.addWidget(self.appLabel)
        self.appLayout.addWidget(self.appLineEdit)
        self.appLayout.addWidget(self.appProcessButton)

        self.scriptLayout = QHBoxLayout()
        self.scriptLabel = QLabel("Script Name :")
        self.scriptLineEdit = QLineEdit()
        self.scriptButton = QPushButton("Open file")
        self.scriptButton.clicked.connect(self.openScriptFile)
        self.scriptLayout.addWidget(self.scriptLabel)
        self.scriptLayout.addWidget(self.scriptLineEdit)
        self.scriptLayout.addWidget(self.scriptButton)
        

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.appLayout)
        self.layout.addLayout(self.scriptLayout)
        self.setLayout(self.layout)

    def setAppName(self):
        pass

    def addProcess(self):
        self.appLineEdit.setText( self.appLineEdit.text() + "$(Process)")

    def openScriptFile(self):
        fname = QFileDialog.getOpenFileName(self)
        filename = fname.split("/")[-1]
        self.scriptLineEdit.setText(filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

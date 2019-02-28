import sys,os
from PyQt4.QtGui import *

class MyWindow(QWidget):
    def __init__(self,JDS=None):
        QWidget.__init__(self)
        self.appName = ""
        self.execFname = ""
        self.scriptFName = ""
        self.fileListFname = ""
        self.arguements= ""
        self.outError =""
        self.transfer_input_files=""
        self.transfer_output_files=""
        self.outputFname=""
        self.outputRemapFname=""
        if ( JDS is not None) : self.parseJDS(JDS)
        self.setupUI()

    def setupUI(self):
        #self.layout = QGridLayout()
        self.appLayout = QHBoxLayout()
        self.appLabel = QLabel("App Name :")
        self.appLineEdit = QLineEdit()
        self.appLineEdit.textChanged.connect(self.setAppName)
        #self.appProcessButton = QPushButton("$(Process)")
        #self.appProcessButton.clicked.connect(self.appAddProcess)
        self.appLayout.addWidget(self.appLabel)
        self.appLayout.addWidget(self.appLineEdit)
        #self.appLayout.addWidget(self.appProcessButton)

        self.executeLayout = QHBoxLayout()
        self.executeLabel = QLabel("Running Script File Name:")
        self.executeLineEdit = QLineEdit()
        self.executeButton = QPushButton("Open file")
        self.executeButton.clicked.connect(self.openExecuteFile)
        self.executeLayout.addWidget(self.executeLabel)
        self.executeLayout.addWidget(self.executeLineEdit)
        self.executeLayout.addWidget(self.executeButton)

        self.scriptLayout = QHBoxLayout()
        self.scriptLabel = QLabel("Analsis Code File Name:")
        self.scriptLineEdit = QLineEdit()
        self.scriptButton = QPushButton("Open file")
        self.scriptButton.clicked.connect(self.openScriptFile)
        self.scriptLayout.addWidget(self.scriptLabel)
        self.scriptLayout.addWidget(self.scriptLineEdit)
        self.scriptLayout.addWidget(self.scriptButton)

        self.fileListLayout = QHBoxLayout()
        self.fileListLabel = QLabel("FileList File Name:")
        self.fileListLineEdit = QLineEdit()
        self.fileListButton = QPushButton("Open file")
        self.fileListButton.clicked.connect(self.openFileListFile)
        self.fileListLayout.addWidget(self.fileListLabel)
        self.fileListLayout.addWidget(self.fileListLineEdit)
        self.fileListLayout.addWidget(self.fileListButton)

        self.outputFileLayout = QHBoxLayout()
        self.outputFileLabel = QLabel("output File Name:")
        self.outputFileLineEdit = QLineEdit()
        self.outputFileLineEdit.textChanged.connect(self.setOutputFileName)
        #self.outputFileButton = QPushButton("Open file")
        #self.outputFileButton.clicked.connect(self.openFileListFile)
        self.outputFileLayout.addWidget(self.outputFileLabel)
        self.outputFileLayout.addWidget(self.outputFileLineEdit)
        #self.outputFileLayout.addWidget(self.outputFileButton)

        self.doneLayout = QHBoxLayout()
        self.doneButton = QPushButton("Done")
        self.doneButton.clicked.connect(self.writeJDL)
        self.doneLayout.addWidget(self.doneButton)
        

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.appLayout)
        self.layout.addLayout(self.executeLayout)
        self.layout.addLayout(self.scriptLayout)
        self.layout.addLayout(self.fileListLayout)
        self.layout.addLayout(self.outputFileLayout)
        self.layout.addLayout(self.doneLayout)
        self.setLayout(self.layout)

    def writeJDL(self):
        jdl='''
executable = %s
universe   = vanilla
arguments  = $(DATAFile)
getenv     = True

transfer_input_files = %s
should_transfer_files = YES
when_to_transfer_output = ON_EXIT

transfer_output_files = %s
transfer_output_remaps = "%s = %s"


output = job_$(Process).out
error  = job_$(Process).err
log = condor.log

accounting_group=group_cms
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest"
+SingularityBind = "/cvmfs, /cms, /share"

queue DATAFile from %s
'''%(self.execFname, self.scriptFname, self.outputFname, self.outputFname, self.outputRemapFname, self.fileListFname)
        f = open( self.appName+".sub","w")
        f.write(jdl)
        f.close()
        sys.exit(0)
    def setOutputFileName(self):
        self.outputFname = self.outputFileLineEdit.text().toUtf8().data()
        name, ext = os.path.splitext(self.outputFname)
        self.outputRemapFname = name+"_"+"$(Process)"+ext

    def setAppName(self):
        self.appName = self.appLineEdit.text()

    def appAddProcess(self):
        self.appLineEdit.setText( self.appLineEdit.text() + "$(Process)")

    def openFileListFile(self):
        self.fileListFname = QFileDialog.getOpenFileName(self)
        filename = self.execFname.split("/")[-1]
        self.fileListLineEdit.setText(filename)
    def openExecuteFile(self):
        self.execFname = QFileDialog.getOpenFileName(self)
        filename = self.execFname.split("/")[-1]
        self.executeLineEdit.setText(filename)
    def openScriptFile(self):
        nameFilter = "ROOT macro files (*.C)"
        nameFilters = ["ROOT macro files (*.C)","Python script files (*.py)"]
        scriptDialog = QFileDialog()
        scriptDialog.setNameFilters(nameFilters)
        self.scriptFname = scriptDialog.getOpenFileName()
        filename = self.scriptFname.split("/")[-1]
        self.scriptLineEdit.setText(filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

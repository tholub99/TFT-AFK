from PyQt6 import QtCore, QtGui, QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("maingui.ui", self)
        
        self.startButton.clicked.connect(self.startProgram)
        self.stopButton.clicked.connect(self.stopProgram)
        self.autoRerollCheck.stateChanged.connect(self.toggleRerollBtn)
        self.searchBar.textChanged.connect(self.searchChamps)
        
    def test(self):
        print('test')
    #Public
    def ConnectStart(self, func):
        self.startButton.clicked.connect(func)
        
    def ConnectStop(self, func):
        self.stopButton.clicked.connect(func)
        
    def ConnectAdd(self, func):
        self.champAddButton.clicked.connect(func)
        
    def ConnectRemove(self, func):
        self.champRemoveButton.clicked.connect(func)
        
    def ConnectClear(self, func):
        self.champClearButton.clicked.connect(func)
        
    def SetChampList(self, baseList):
        self.champListWidget.addItems(baseList)
        
    def AddChamp(self):
        champ = self.champListWidget.selectedItems()[0]
        print('Adding ' + champ.text())
        self.champSelectedWidget.addItem(champ.clone())
        self.champListWidget.takeItem(self.champListWidget.row(champ))
        
    def RemoveChamp(self):
        champ = self.champSelectedWidget.selectedItems()[0]
        print('Removing ' + champ.text())
        self.champListWidget.addItem(champ.clone())
        self.champSelectedWidget.takeItem(self.champSelectedWidget.row(champ))
        
    def ClearChamps(self):
        while(self.champSelectedWidget.count() > 0):
            champ = self.champSelectedWidget.item(0)
            self.champListWidget.addItem(champ.clone())
            self.champSelectedWidget.takeItem(0)
    
    def GetEconMin(self):
        return self.econMinBox.value()
    
    def GetAutoRerollEnabled(self):
        return self.autoRerollCheck.isChecked()
            
    def GetSelectedChamps(self):
        champs = []
        for i in range(self.champSelectedWidget.count()):
            champs.append(self.champSelectedWidget.item(i).text())
        
        return champs
    
    def UpdateRound(self, txt):
        self.roundLabel.setText(txt)
        
    def GetCurrentRound(self):
        return self.roundLabel.text()
    
    #Private
    def startProgram(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        
    def stopProgram(self):
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        
    def toggleRerollBtn(self):
        self.rerollButton.setEnabled(not self.rerollButton.isEnabled())
        
    def searchChamps(self):
        text = self.searchBar.text()
        for i in range(self.champListWidget.count()):
            item = self.champListWidget.item(i)
            champName = item.text()
            item.setHidden(not self.filter(text, champName))
            
    def filter(self, text, name):
        return text.lower() in name.lower()
            
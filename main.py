import csv
import re
import sys
import time
from PyQt6 import QtWidgets
from actions import *
from mainwindow import *
from threading import Thread, Lock, Timer

#Reroll 500x 1380y
#Global
MoneyBox = ScreenBox(1165, 1175, 1205, 1211)

RoundBox = ScreenBox(1025, 15, 1075, 45)
TimerBox = ScreenBox(1500, 15, 1545, 45)
Round1Box = ScreenBox(1100, 15, 1150, 45)
Timer1Box = ScreenBox(1435, 15, 1470, 45)

Champ0 = StoreItem(ScreenBox(645,  1390, 840,  1420), ScreenCoords(765,  1320))
Champ1 = StoreItem(ScreenBox(913,  1390, 1108, 1420), ScreenCoords(1035, 1320))
Champ2 = StoreItem(ScreenBox(1182, 1390, 1377, 1420), ScreenCoords(1305, 1320))
Champ3 = StoreItem(ScreenBox(1451, 1390, 1646, 1420), ScreenCoords(1575, 1320))
Champ4 = StoreItem(ScreenBox(1720, 1390, 1915, 1420), ScreenCoords(1845, 1320))

Store = [Champ0, Champ1, Champ2, Champ3, Champ4]

lock = Lock()

def Initialize():
    global WINDOW
    setChamps = []
    with open('champions.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            setChamps.append(' '.join(row))
    
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(StopRoundCapture)
    
    WINDOW = MainWindow()
    
    WINDOW.SetChampList(setChamps)
    
    WINDOW.ConnectStart(StartRoundCapture)
    WINDOW.ConnectStop(StopRoundCapture)
    
    WINDOW.ConnectAdd(AddChampToSelection)
    WINDOW.ConnectRemove(RemoveChampFromSelection)
    WINDOW.ConnectClear(ClearChampFromSelection)
    
    WINDOW.show()
    
    app.exec()

def StartRoundCapture():
    global STOP_ROUND_COLLECTION
    STOP_ROUND_COLLECTION = False
    roundThread = Thread(target=RoundThread, args=())
    roundThread.start()
    
def StopRoundCapture():
    global STOP_ROUND_COLLECTION
    STOP_ROUND_COLLECTION = True
    
def PerformBuyCycle():
    global WINDOW
    global STOP_ROUND_COLLECTION
    rerollCost = 2
    rerollCoords = (500, 1380)
    
    if(STOP_ROUND_COLLECTION):
        return
    
    soughtChamps = WINDOW.GetSelectedChamps()
    print("Selection: ", soughtChamps)
    for item in Store:
        item.Update()
        if(item.name in soughtChamps):
            print('Buying ' + item.name)
            item.Buy()
    
    if(WINDOW.GetAutoRerollEnabled()):
        econ = GetMoneyInfo(0)
        econMin = WINDOW.GetEconMin()
        if(econ == None or econ < (econMin + rerollCost)):
            return
    
        DoClick(rerollCoords)
        PerformBuyCycle()
        
    
def RoundThread():
    global WINDOW
    global STOP_ROUND_COLLECTION
    
    while not STOP_ROUND_COLLECTION:
        curRound = WINDOW.GetCurrentRound()
        captureRound = GetRoundInfo()
        if(curRound != captureRound and captureRound != None):
            print('New Round: ' + captureRound)
            WINDOW.UpdateRound(captureRound)
            PerformBuyCycle()
        #roundTime = GetTimerInfo(False)
        #if(roundTime != None):
            #print("Waiting for " + str(roundTime) + " seconds")
            #time.sleep(roundTime)

def GetRoundInfo():
    pattern = re.compile(r'\d-\d')
    if(pattern.match(txt := ReadCapture(RoundBox.Capture()))):
        return txt
    elif(pattern.match(txt := ReadCapture(Round1Box.Capture()))):
        return txt
    else:
        return None
    
def GetMoneyInfo(n):
    econMaxAttempts = 3
    if(n > econMaxAttempts):
        print('Failed to read Econ')
        return None
        
    try:
        capture = ReadCapture(MoneyBox.Capture())
        print(capture)
        return int(capture)
    except:
        print('Unable to read Econ. Retrying in 0.25 seconds')
        #MoneyBox.CaptureAndOpen()
        time.sleep(0.25)
        return GetMoneyInfo(n + 1)
    
    
def GetTimerInfo(isStageOne):
    try:
        if(isStageOne):
            timer = int(ReadCapture(Timer1Box.Capture()))
        else:
            timer = int(ReadCapture(TimerBox.Capture())) 
        return timer + 0.25
    except:
        if(not isStageOne):
            return GetTimerInfo(True)
        return None
    
def AddChampToSelection():
    with lock:
        WINDOW.AddChamp()

def RemoveChampFromSelection():
    with lock:
        WINDOW.RemoveChamp()

def ClearChampFromSelection():
    with lock:
        WINDOW.ClearChamps()

def Test():
    print('test')

if __name__ == '__main__':
    Initialize()
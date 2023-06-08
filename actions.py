import time
import numpy as np
import pyautogui as gui
from PIL import Image, ImageGrab
import pytesseract as pt

class ScreenCoords:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def GetCoords(self):
        return (self.x,self.y)

class ScreenBox:
    def __init__(self, left, down, right, up):
        self.left = left
        self.down = down
        self.right = right
        self.up = up

    def GetBox(self):
        return (self.left, self.down, self.right, self.up)
    
    def Capture(self):
        img = ImageGrab.grab(bbox=(self.left, self.down, self.right, self.up))
        #img.show()
        return np.array(img)
    
    def CaptureAndOpen(self):
        img = ImageGrab.grab(bbox=(self.left, self.down, self.right, self.up))
        img.show()

class StoreItem:
    def __init__(self, screenBox, screenCoords):
        self.box = screenBox
        self.coords = screenCoords
        self.name = None
        
    def __str__(self):
        return f"{self.name}"
    
    def Update(self):
        self.name = ReadCapture(self.box.Capture())
    
    def Buy(self):
        gui.click(self.coords.x, self.coords.y, clicks=2, interval=0.25)

def ReadCapture(capture):
    return pt.image_to_string(capture, config='--psm 7').rstrip()

def GetPixelColor(x, y):
    return gui.screenshot().getpixel((x,y))
    
def DoClick(coords):
    gui.click(coords[0], coords[1], clicks=2, interval=0.25)
    
def RefreshStore():
    gui.hotkey("d")
    
def LevelUp():
    gui.hotkey("f")

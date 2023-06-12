import time
import numpy as np
import pydirectinput as pdi
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
        pdi.click(self.coords.x, self.coords.y, duration=0.25)

def ReadCapture(capture):
    return pt.image_to_string(capture, config='--psm 7').rstrip()

def GetPixelColor(x, y):
    return pdi.screenshot().getpixel((x,y))
    
def DoClick(coords):
    pdi.click(coords[0], coords[1], duration=0.25)
    
def RefreshStore():
    pdi.hotkey("d")
    
def LevelUp():
    pdi.hotkey("f")

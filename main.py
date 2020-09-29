import win32gui
import win32ui
import win32con
import win32api
import cv2
import numpy as np
from PIL import Image
import pywinauto
import time
from common.actions import Actions
from common.window import Window


w = Window()

#img = w.get_screenshot_from_window()
#Actions.save_image(img, "data/locations/map_outskirts.bmp")
#patt = cv2.imread("icon.png", 0)
#click_point = Actions.find_patt(img, patt)
#w.mouse_click(*click_point)

while True:
    Actions.define_location(w)





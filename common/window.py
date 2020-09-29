from typing import Union
import win32gui
import win32api
import win32con
import win32ui
import configparser
from common.decorators import after_sleep
import numpy as np
import cv2
from PIL import Image


config = configparser.ConfigParser()
config.read("config.ini")


class Window:
    def __init__(self) -> None:
        self.window_handle = win32gui.FindWindow(None, config["NOX_APP"]["NoxWindowName"])
        if not self.window_handle:
            raise AttributeError("Nox is not found")
        self.set_basic_configuration()

    @after_sleep()
    def mouse_click(self, x: int, y: int) -> None:
        # (x, y) to one windows parameter
        long_window_coordinates = win32api.MAKELONG(x, y)
        win32api.PostMessage(self.window_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_window_coordinates)
        win32api.PostMessage(self.window_handle, win32con.WM_LBUTTONUP, 0, long_window_coordinates)

    def set_basic_configuration(self) -> None:
        win32gui.SetWindowPos(self.window_handle, win32con.HWND_NOTOPMOST, 0, 0, 900, 600, win32con.SWP_DRAWFRAME)

    @after_sleep()
    def get_screenshot_from_window(self,
                                   w: int = int(config["DISPLAY"]["Width"]),
                                   h: int = int(config["DISPLAY"]["Height"]),
                                   output_file: Union[None, str] = None) -> Union[None, np.ndarray]:
        windows_device_context = win32gui.GetWindowDC(self.window_handle)
        object_device_context = win32ui.CreateDCFromHandle(windows_device_context)
        compatible_device_context = object_device_context.CreateCompatibleDC()
        data_bit_map = win32ui.CreateBitmap()
        data_bit_map.CreateCompatibleBitmap(object_device_context, w, h)
        compatible_device_context.SelectObject(data_bit_map)
        compatible_device_context.BitBlt((0, 0), (w, h), object_device_context, (0, 0), win32con.SRCCOPY)
        if output_file:
            data_bit_map.SaveBitmapFile(compatible_device_context, output_file)
            # Free resources
            object_device_context.DeleteDC()
            compatible_device_context.DeleteDC()
            win32gui.ReleaseDC(self.window_handle, windows_device_context)
            win32gui.DeleteObject(data_bit_map.GetHandle())
        else:
            bmp_info = data_bit_map.GetInfo()
            bmp_array = np.asarray(data_bit_map.GetBitmapBits(), dtype=np.uint8)
            pil_im = Image.frombuffer('RGB', (bmp_info['bmWidth'], bmp_info['bmHeight']), bmp_array, 'raw', 'BGRX', 0, 1)
            pil_array = np.array(pil_im)
            cv_image = cv2.cvtColor(pil_array, cv2.COLOR_RGB2BGR)
            # Free resources
            object_device_context.DeleteDC()
            compatible_device_context.DeleteDC()
            win32gui.ReleaseDC(self.window_handle, windows_device_context)
            win32gui.DeleteObject(data_bit_map.GetHandle())

            return cv_image

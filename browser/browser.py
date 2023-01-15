from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

import win32api
import webbrowser
import time
import pygetwindow
import win32gui
import win32con
import pyautogui
import pywinauto
import pyperclip
import os
import sys
import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
import winxpgui
import win32api
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import ctypes
from selenium import webdriver

user32 = ctypes.windll.user32
width,height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

item = ["1X1","1X2","2X2","1X3","2X3","3X3","1X4","2X4","3X4","4X4"]



class MainWindow(QMainWindow):
    def __init__(self, value):
        file = open("./list.txt", "r",encoding="UTF-8")
        para_list = [line.strip() for line in file.readlines()]
        file.close()

        windowTextSize = value.split("X")
        window_rows = windowTextSize[0]
        window_cols = windowTextSize[1]
        window_size = int(window_rows)*int(window_cols)
        print(window_rows,"x",window_cols)
        print("window_size",window_size)
        
        if len(para_list) <= window_size:
            for i in range(window_size-len(para_list)):
                para_list.append("None,None,None")
        

        super(MainWindow, self).__init__()
        self.setWindowTitle("multiple window setting page (by:ych)")

        ## make browser inside frame  v2
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        horizontal = QHBoxLayout(self.central_widget)
        
        index = 0
        for window_horizontal in range(int(window_cols)):
            vertical = QVBoxLayout(self.central_widget)
            for window_vertical in range(int(window_rows)):
                #frame =QFrame()
                browser = self.make_browser(para_list[index])
                #frame.addLayout(browser)
                vertical.addLayout(browser,stretch = 1)
                index = index + 1
            horizontal.addLayout(vertical,stretch = 1)

        self.show()

    def make_browser(self, para):

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        flagPW = para.split(",")[0]
        server_name = para.split(",")[1]
        url = para.split(",")[2]

        
        
        if flagPW == "None":
            print("flagPW NONE",url)
            browser = QWebEngineView()
            q = QUrl(url)
            if q.scheme() == "":
                q.setScheme("http")
            print(q,type(q))
            browser.setUrl(q)
            #browser.setUrl(QUrl(url))
            #browser.load(QUrl(str(url)))
            browser.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
            browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

            """browser.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
            #QWebEngineSettings.AllowRunningInsecureContent, QWebEngineSettings.AllowWindowActivationFromJavaScript, QWebEngineSettings.JavascriptCanPaste, PluginsEnabled
            browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
            browser.settings().setAttribute(QWebEngineSettings.JavascriptCanPaste, True)
            browser.settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
            browser.settings().setAttribute(QWebEngineSettings.AllowWindowActivationFromJavaScript, True)
            browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)"""

            title_frame =QFrame()
            title_frame.setMaximumHeight(30)
            title_frame_layout = QHBoxLayout()
            title_frame_layout.setContentsMargins(0, 0, 0, 0)

            toolbar_frame =QFrame()
            toolbar_frame.setMaximumHeight(30)
            toolbar_frame_layout = QHBoxLayout()
            toolbar_frame_layout.setContentsMargins(0, 0, 0, 0)

            title = QLabel(server_name)
            title.setFont(QtGui.QFont("Arial",20,weight=QtGui.QFont.Bold)) #폰트,크기 조절
            title.setStyleSheet("Color : black") #글자색 변환
            title.setStyleSheet("background-color: yellow")
            title_frame_layout.addWidget(title, alignment=Qt.AlignCenter)

            back_btn = QPushButton("back")
            back_btn.clicked.connect(browser.back)
            toolbar_frame_layout.addWidget(back_btn)

            next_btn = QPushButton("next")
            next_btn.clicked.connect(browser.forward)
            toolbar_frame_layout.addWidget(next_btn)

            reload_btn = QPushButton("Reload")
            reload_btn.clicked.connect(browser.reload)
            toolbar_frame_layout.addWidget(reload_btn)

            urlbar = QLineEdit()
            urlbar.returnPressed.connect(lambda : self.navigate_to_url(browser, urlbar))
            toolbar_frame_layout.addWidget(urlbar)

            toolbar_frame.setLayout(toolbar_frame_layout) 
            title_frame.setLayout(title_frame_layout) 
            
            layout.addWidget(title_frame)
            layout.addWidget(toolbar_frame)
            layout.addWidget(browser)
        
        else :
            print("flagPW PW",url)
 
            #webbrowser = webdriver.Chrome()
            #webbrowser.get("http://211.34.127.106/wmf/index.html#/login")

            
            try:
                print("start")

                webbrowser.open(url)

                time.sleep(3)
                #self.hwnd = win32gui.FindWindow(None, "Wisenet WEBVIEWER - 회사 - Microsoft​ Edge")

                self.window_list = self.getWindowList()
                for k,w in self.window_list:
                    if "Wisenet" in k:
                        self.hwnd = w
                        break

                print("self.hwnd",self.hwnd)
                print("end")
                
                pywinauto.application.Application().connect(handle=self.hwnd).top_window().set_focus()
                cus_id = flagPW.split("/")[0]
                cus_pw = flagPW.split("/")[1]
                pyautogui.write(cus_id)
                pyautogui.write("\t")
                pyautogui.write(cus_pw)
                pyautogui.write("\n")

                time.sleep(1)
                embed_window = QtGui.QWindow.fromWinId(self.hwnd)
                
                embed_widget = QtWidgets.QWidget.createWindowContainer(embed_window)
                #embed_widget.setMouseTracking(True)
            except Exception as ex :
                print(ex)

            title_frame =QFrame()
            title_frame.setMaximumHeight(30)
            title_frame_layout = QHBoxLayout()
            title_frame_layout.setContentsMargins(0, 0, 0, 0)

            toolbar_frame =QFrame()
            toolbar_frame.setMaximumHeight(30)
            toolbar_frame_layout = QHBoxLayout()
            toolbar_frame_layout.setContentsMargins(0, 0, 0, 0)

            title = QLabel(server_name)
            title.setFont(QtGui.QFont("Arial",20,weight=QtGui.QFont.Bold)) #폰트,크기 조절
            title.setStyleSheet("Color : black") #글자색 변환
            title.setStyleSheet("background-color: yellow")
            title_frame_layout.addWidget(title, alignment=Qt.AlignCenter)
            

            toolbar_frame.setLayout(toolbar_frame_layout) 
            title_frame.setLayout(title_frame_layout) 
            
            layout.addWidget(title_frame)
            layout.addWidget(toolbar_frame)
            layout.addWidget(embed_widget)
                    

        return layout
    
    def hwnd_method(self, hwnd, ctx):
        window_title = win32gui.GetWindowText(hwnd)
        if "wisenet" in window_title.lower():
            self.hwnd = hwnd
            print("window_title",window_title, self.hwnd)
            

    def navigate_to_url(self, browser, urlbar):  # Does not receive the Url
        q = QUrl(urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        print(q,type(q))
        browser.setUrl(q)
    
    def getWindowList(self):
        def callback(hwnd, hwnd_list: list):
            title = win32gui.GetWindowText(hwnd)
            if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
                hwnd_list.append((title, hwnd))
            return True
        output = []
        win32gui.EnumWindows(callback, output)
        return output

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('multiple window setting page (by:ych)')
        self.resize(500, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        verical = QHBoxLayout(self.central_widget)

        # 리스트 사용하여 데이터를 추가한 ComboBox
        self.combo_list = QComboBox(self)
        for i in range(len(item)):
            #self.listbox_1.insert(i, item[i])
            self.combo_list.addItem(item[i])
        #self.combo_list.move(50,100)

        

        self.list_button = QPushButton(self)
        #self.list_button.move(200, 100)
        self.list_button.setText('Open')
        self.list_button.setIcon(QtGui.QIcon('./images/ma-icon-64.png'))
        self.list_button.clicked.connect(self.button_event)
        verical.addWidget(self.combo_list)
        verical.addWidget(self.list_button)
        self.show()

    def button_event(self):
        list_text = self.combo_list.currentText()
        self.w = MainWindow(list_text)
        self.w.show()
        self.hide()


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = App()

    sys.exit(app.exec())
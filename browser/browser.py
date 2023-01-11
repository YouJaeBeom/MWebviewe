from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys
import tkinter as tk
from tkinter import ttk

item = ["1X1","1X2","2X2","1X3","2X3","3X3","1X4","2X4","3X4","4X4"]



class MainWindow(QMainWindow):
    def __init__(self, value):

        file = open("./list.txt", "r")
        url_list = file.readlines()
        file.close()

        print(url_list)
        windowTextSize = value.split("X")
        window_rows = windowTextSize[0]
        window_cols = windowTextSize[1]
        window_size = int(window_rows)*int(window_cols)
        print(window_rows,"x",window_cols)
        print("window_size",window_size)
        
        if len(url_list) <= window_size:
            for i in range(window_size-len(url_list)):
                url_list.append("none!!none")
        
        print(url_list)

        super(MainWindow, self).__init__()
        self.setWindowTitle("multiple window setting page (by:ych)")

        ## make browser inside frame  v2
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        horizontal = QHBoxLayout(self.central_widget)
        
        index = 0
        for window_horizontal in range(int(window_cols)):
            vertical = QVBoxLayout()
            for window_vertical in range(int(window_rows)):
                frame =QFrame()
                browser = self.make_browser(url_list[index])
                frame.setLayout(browser)
                vertical.addWidget(frame)
                index = index + 1
            horizontal.addLayout(vertical)

        self.show()

    def make_browser(self, para):

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        url = para.split("!!")[0]
        server_name = para.split("!!")[1]

        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        
        title_frame =QFrame()
        title_frame.setMaximumHeight(30)
        title_frame_layout = QHBoxLayout()
        title_frame_layout.setContentsMargins(0, 0, 0, 0)

        toolbar_frame =QFrame()
        toolbar_frame.setMaximumHeight(30)
        toolbar_frame_layout = QHBoxLayout()
        toolbar_frame_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel(server_name)
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
        
        """
        ## common toolbar
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(browser.reload)
        navtb.addAction(reload_btn)

        urlbar = QLineEdit()
        urlbar.returnPressed.connect(lambda : self.navigate_to_url(browser, urlbar))
        navtb.addWidget(urlbar)"""

        return layout

    def update_title(self, browser):
        title = browser.page().title()
        self.setWindowTitle("%s - MooseAche" % title)


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.browser.page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self, browser, urlbar):  # Does not receive the Url
        q = QUrl(urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        browser.setUrl(q)


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('multiple window setting page (by:ych)')
        self.resize(500, 200)
        #self.title("multiple window setting page (by:ych)")

        # 리스트 사용하여 데이터를 추가한 ComboBox
        self.combo_list = QComboBox(self)
        for i in range(len(item)):
            #self.listbox_1.insert(i, item[i])
            self.combo_list.addItem(item[i])
        self.combo_list.move(50,100)

        self.list_button = QPushButton(self)
        self.list_button.move(200, 100)
        self.list_button.setText('Open')
        self.list_button.clicked.connect(self.button_event)

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
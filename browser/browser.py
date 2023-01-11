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
        windowTextSize = item[value[0]].split("X")
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


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('300x200')
        self.title('Main Window')


        # 생성할 window 창의 크기 및 초기 위치 설정 매서드: geometry()
        window_width = 400
        window_height = 200
        window_pos_x = 700
        window_pos_y = 100

        self.geometry("{}x{}+{}+{}".format(window_width, window_height, window_pos_x, window_pos_y))

        # 생성한 Window 창의 크기 조절 가능 여부 설정: resizable()
        self.resizable(False, False)   # True, False 대신 1, 0을 사용할 수 있음

        # 생성한 Window 창의 Title 설정: title()
        self.title("multiple window setting page (by:ych)")

        # 생성한 Window 창의 Icon 설정: iconphoto()
        #window.iconphoto(False, tkinter.PhotoImage(file="icon1.png"))

        # tkinter.Label 클래스 선언 및 Button 위젯 생성
        self.listbox_1 = tk.Listbox(self, highlightbackground="red", highlightcolor="green", selectforeground="white", selectbackground="black", selectmode="single")
        
        for i in range(len(item)):
            self.listbox_1.insert(i, item[i])

        #def return_value(v): print(f'Listbox 선택 항목 위치 반환값: {self.listbox_1.curselection()}')
        self.button_test = tk.Button(self, text="Open", command= self.open_window)
        #self.button_test = tk.Button(self, text="선택값 반환", command= lambda: [self.open_window, self.destroy()] )
        
        # 생성한 Label 위젯을 pack() 매서드로 배치
        self.listbox_1.pack()
        self.button_test.pack()
    
    def open_window(self):
        app = QApplication(sys.argv)
        app.setApplicationName("MooseAche")
        app.setOrganizationName("MooseAche")
        app.setOrganizationDomain("MooseAche.org")

        window = MainWindow(self.listbox_1.curselection())

        app.exec_()


if __name__ == "__main__":
    app = App()
    app.mainloop()
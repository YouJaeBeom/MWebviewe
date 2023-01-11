from webui import webui

MyWindow = webui.window()
MyWindow.show('<html>Hello World</html>')
webui.wait()
print('Bye.')
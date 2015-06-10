'''
Under MIT License. Please see accompanying LICENSE document.
'''

import sys
from PyQt4 import QtGui as q
from PyQt4 import QtWebKit as qw
import PyQt4.QtCore as qcore
import bongy

class MappingWindow(q.QDialog):
    def __init__(self, parent=None):
        q.QDialog.__init__(self, parent)
        self.setWindowTitle('Mappings')
        self.resize(600, 400)
        self.webview = qw.QWebView()
        hbox = q.QHBoxLayout()
        hbox.addWidget(self.webview)
        self.setLayout(hbox)

    def add_html(self, html):
        self.webview.setContent(html)

    def show(self):
        self.showMaximized()

class App(q.QWidget):
    converted = qcore.pyqtSignal()

    @qcore.pyqtSlot()
    def clear(self):
        self.to.setText('')

    @qcore.pyqtSlot()
    def copy(self):
        text = self.to.toPlainText()
        if self.clipboard is not None:
            self.clipboard.setText(text)
            self.to.setFocus()

    @qcore.pyqtSlot()
    def cut(self):
        text = self.to.toPlainText()
        if self.clipboard is not None:
            self.clipboard.setText(text)
            self.to.setText('')

    @qcore.pyqtSlot()
    def show_mapping(self):
        mapw = MappingWindow(self)
        mapw.add_html(self.cobj.gen_mapping().encode('utf-8'))
        mapw.show()

    @qcore.pyqtSlot()
    def slot_convert(self):
        txt = self.frm.toPlainText()
        self.to.setText(self.cobj.convert(txt))
        self.converted.emit()

    def __init__(self, clipboard=None):
        q.QWidget.__init__(self)
        self.resize(600, 200)
        self.setWindowTitle('Convert-R')

        # Widgets
        self.frm = q.QTextEdit()
        self.to = q.QTextEdit()
        self.to.setFont(q.QFont('Courier', 12))
        self.to.setReadOnly(True)
        self.convert = q.QPushButton('Convert')
        self.convert.setFixedWidth(100)
        self.clearbutton = q.QPushButton('Clear')
        self.copybutton = q.QPushButton('Copy')
        self.cutbutton = q.QPushButton('Cut')
        self.mapbutton = q.QPushButton('Mappings')
        self.mapbutton.setFixedWidth(100)

        # Clipboard
        if clipboard is not None:
            self.clipboard = clipboard

        # Layouts
        hbox = q.QHBoxLayout()
        hbox2 = q.QHBoxLayout()

        self.toolbox = q.QWidget()
        hbox3 = q.QHBoxLayout()
        hbox3.addWidget(self.clearbutton)
        hbox3.addWidget(self.copybutton)
        hbox3.addWidget(self.cutbutton)
        self.toolbox.setLayout(hbox3)

        vbox3 = q.QVBoxLayout()
        vbox3.addWidget(self.toolbox)
        vbox3.addWidget(self.to)

        vbox = q.QVBoxLayout()
        hbox.addWidget(self.frm)
        hbox.addLayout(vbox3)
        hbox2.addWidget(self.mapbutton)
        hbox2.addWidget(self.convert)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

        # Connections
        self.convert.clicked.connect(self.slot_convert)
        self.clearbutton.clicked.connect(self.clear)
        self.copybutton.clicked.connect(self.copy)
        self.cutbutton.clicked.connect(self.cut)
        self.mapbutton.clicked.connect(self.show_mapping)

        # Create the converter
        self.cobj = bongy.Converter()

# MAIN

def start_gui():
    qapp = q.QApplication(sys.argv)
    app = App(qapp.clipboard())
    app.show()
    sys.exit(qapp.exec())

if __name__ == '__main__':
    start_gui()


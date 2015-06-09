'''
Under MIT License. Please see accompanying LICENSE document.
'''

import sys
from PyQt4 import QtGui as q
import PyQt4.QtCore as qcore
import re


class Converter:
    ignore_list = [r' ,.;?\'\"[]{}()']
    char_maps = {
        'a': {'r': '\u0985', 'm': '\u0985'},
        'A': {'r': '\u0986', 'm': '\u09BE'},
        'i': {'r': '\u0987', 'm': '\u09BF'},
        'I': {'r': '\u0988', 'm': '\u09C0'},
        'u': {'r': '\u0989', 'm': '\u09C1'},
        'U': {'r': '\u098A', 'm': '\u09C2'},
        'e': {'r': '\u098F', 'm': '\u09C7'},
        'E': {'r': '\u0990', 'm': '\u09C8'},
        'o': {'r': '\u0993', 'm': '\u09CB'},
        'O': {'r': '\u0994', 'm': '\u09CC'},
        'k': {'r': '\u0995'},
        'K': {'r': '\u0996'},
        'g': {'r': '\u0997'},
        'G': {'r': '\u0998'},
        'n1': {'r': '\u0999'},
        'c': {'r': '\u099A'},
        'C': {'r': '\u099B'},
        'j': {'r': '\u099C'},
        'J': {'r': '\u099D'},
        'n2': {'r': '\u099E'},
        't': {'r': '\u099F'},
        'T': {'r': '\u09A0'},
        'd': {'r': '\u09A1'},
        'D': {'r': '\u09A2'},
        'N': {'r': '\u09A3'},
        't1': {'r': '\u09A4'},
        'T1': {'r': '\u09A5'},
        'd1': {'r': '\u09A6'},
        'D1': {'r': '\u09A7'},
        'n': {'r': '\u09A8'},
        'p': {'r': '\u09AA'},
        'P': {'r': '\u09AB'},
        'b': {'r': '\u09AC'},
        'B': {'r': '\u09AD'},
        'm': {'r': '\u09AE'},
        'z': {'r': '\u09AF'},
        'r': {'r': '\u09B0'},
        'l': {'r': '\u09B2'},
        'S': {'r': '\u09B6'},
        's1': {'r': '\u09B7'},
        's': {'r': '\u09B8'},
        'h': {'r': '\u09B9'},
        'R': {'r': '\u09DC'},
        'r1': {'r': '\u09DD'},
        'y': {'r': '\u09DF'}
    }

    def convert(self, frms):
        parts = re.findall(r'(\{.+?\})|(\w\d)|(.)', frms)
        rparts = []
        for p in parts:
            if p[0] != '':
                rparts.append(p[0])
            elif p[1] != '':
                rparts.append(p[1])
            elif p[2] != '':
                rparts.append(p[2])
            else:
                rparts.append(p[0]+ p[1] + p[2])
        convs = ''
        for i in rparts:
            gs = re.search(r'^\{(.*?)\}$', i)
            if gs is not None:
                convs += self.convert_compound(gs.group(1))
            else:
                if i in self.char_maps:
                    convs += self.char_maps[i]['r']
                else:
                    convs += i
        return convs

    def isword(self, c):
        return re.match(r'[a-zA-Z]', c)

    def isconsonant(self, c):
        return self.isword(c) and re.match(r'[^aeiou]', c, re.I) is not None

    def isvowel(self, c):
        return not self.isconsonant(c)

    def lookup(self, c, m=False):
        if c in self.char_maps:
            return self.char_maps[c]['r' if not m else 'm']
        return c

    def convert_compound(self, frms):
        stk = []
        skipped = False
        for i in range(0, len(frms)):
            if skipped:
                skipped = False
                continue
            c = frms[i]
            if i < (len(frms) - 1) and (frms[i+1] in '1234567890'):
                c += frms[i+1]
                skipped = True
            if self.isconsonant(c):
                if i > 0:
                    stk.append('\u09CD')
                stk.append(self.lookup(c))
            elif self.isvowel(c):
                stk.append(self.lookup(c, m=True))
            else:
                stk.append(c)
        return ''.join(stk)


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
        self.convert.setFixedWidth(80)
        self.clearbutton = q.QPushButton('Clear')
        #self.clearbutton.setFixedWidth(40)
        self.copybutton = q.QPushButton('Copy')
        #self.copybutton.setFixedSize(40, 30)
        self.cutbutton = q.QPushButton('Cut')
        #self.cutbutton.setFixedWidth(40)

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
        hbox2.addWidget(self.convert)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

        # Connections
        self.convert.clicked.connect(self.slot_convert)
        self.clearbutton.clicked.connect(self.clear)
        self.copybutton.clicked.connect(self.copy)
        self.cutbutton.clicked.connect(self.cut)

        # Create the converter
        self.cobj = Converter()

    @qcore.pyqtSlot()
    def slot_convert(self):
        txt = self.frm.toPlainText()
        self.to.setText(self.cobj.convert(txt))
        self.converted.emit()

if __name__ == '__main__':
    qapp = q.QApplication(sys.argv)
    app = App(qapp.clipboard())
    app.show()
    sys.exit(qapp.exec())

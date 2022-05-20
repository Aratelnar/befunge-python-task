from io_handler import IOHandler
import machine
import commands
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

app = QApplication([])

class GridLabel(QLabel):
    def __init__(self, x, y):
        super().__init__()
        self.gridX = x
        self.gridY = y
        self.selected = False
        self.clickedEvent = []
        self.hoverEvent = []

        self.colorFront = 'white'
        self.colorBack = '#2f2f2f'
        self.border = ''
        self.update()
        self.installEventFilter(self)

    def setColorBack(self, color):
        self.colorBack = color
        self.update()

    def setColorFront(self, color):
        self.colorFront = color
        self.update()

    def setBorder(self, border):
        self.border = border
        self.update()

    def update(self):
        self.setStyleSheet(f'background-color:{self.colorBack}; color:{self.colorFront}; {self.border}')

    def eventFilter(self, object, event) -> bool:
        if event.type() == QEvent.Enter and not self.selected:
            for handler in self.hoverEvent:
                handler(object, True)
            return True
        elif event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.selected = not self.selected
                for handler in self.clickedEvent:
                    handler(object, self.selected)
            return True
        elif event.type() == QEvent.Leave and not self.selected:
            for handler in self.hoverEvent:
                handler(object, False)
        return False


class SandBox(QFrame):
    def __init__(self):
        super().__init__()
        # self.setStyleSheet('background-color: #f0f0f0')

        self.instr = QGridLayout(self)
        self.pointer = machine.Coord(0,0)

        self.chars = []
        self.breakpoints = []

    def setBreakpoint(self, pos, set):
        if not set:
            self.breakpoints.remove(machine.Coord(*pos))
        else:
            self.breakpoints.append(machine.Coord(*pos))

    def setPointer(self, pos):
        self.chars[self.pointer.y][self.pointer.x].setBorder('')
        self.pointer = pos
        self.chars[pos.y][pos.x].setBorder('border: 2px solid #ffd000')
        
    def setInstr(self, instr):
        h = len(instr)
        w = len(max(instr, key=len))
        for y in range(h):
            line = []
            for x in range(w):
                label = GridLabel(x, y)
                if x < len(instr[y]):
                    label.setText(instr[y][x])
                else:
                    label.setText('')
                label.clickedEvent.append(lambda obj, flag: self.setBreakpoint((obj.gridX, obj.gridY), flag))
                label.clickedEvent.append(lambda obj, flag: obj.setColorBack('#800000' if flag else '#2f2f0f'))
                label.hoverEvent.append(lambda obj, flag: obj.setColorBack('#2f2f0f' if flag else '#2f2f2f'))
                label.setFixedSize(20,20)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFont(QFont('Consolas', 12))
                line.append(label)
            self.chars.append(line)

    def setGrid(self):
        for y in range(len(self.chars)):
            for x in range(len(self.chars[0])):
                self.instr.addWidget(self.chars[y][x], y, x)


class Stack(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(110)
        self.lay = QVBoxLayout(self)
        self.lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lay.setContentsMargins(0,0,0,0)
        self.lay.setSpacing(10)

    def setStack(self, stack):
        self.setFixedHeight(40*len(stack))
        for i in reversed(range(self.lay.count())): 
            self.lay.itemAt(i).widget().setParent(None)
        for item in stack:
            i = QFrame()
            layout = QHBoxLayout()
            layout.addWidget(self.getLabel(str(item)))
            layout.addWidget(self.getLabel(str(chr(item).encode())[2:-1]))
            layout.setContentsMargins(0,0,0,0)
            i.setLayout(layout)
            self.lay.addWidget(i)

    def getLabel(self, text):
        label = QLabel(text)
        label.setFixedHeight(30)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont('Consolas', 12))
        label.setStyleSheet("background-color: #3f3f3f; color: white")
        return label


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_menu()
        self.setStyleSheet('background-color: #202020')

        self.setWindowTitle("Befunge debugger")
        self.resize(800, 600)

        with open('tests/a.txt') as f:
            self.data = f.read()

        self.machine = machine.Machine()
        self.machine.set(self.data)
        self.io = IOHandler()
        self.running = False
        commands.init(self.machine, self.io)

        self.sandbox = SandBox()
        self.sandbox.setInstr(self.data.split('\n'))
        self.sandbox.setGrid()

        f = QScrollArea()
        f.setWidget(self.sandbox)
        f.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons = [
            ('Run', 'Ctrl+F5', self.run),
            ('Debug', 'F5', self.debug),
            ('Step', 'F10', self.step),
            ('Stop', 'F6', self.stop)
        ]

        menu = QHBoxLayout()
        menu.setAlignment(Qt.AlignLeft)
        for b, c, a in buttons:
            button = QPushButton(b)
            button.setFixedSize(70, 35)
            button.setShortcut(c)
            button.setStyleSheet('background-color: #202020; color: white')
            if a is not None:
                button.clicked.connect(a)
            menu.addWidget(button)

        self.output = QTextBrowser()
        self.output.setFixedHeight(150)
        self.output.setStyleSheet('background-color: #202020; color: white')
        self.output.setText("")

        field = QVBoxLayout()
        field.addWidget(f)
        field.addWidget(self.output)

        self.stack = Stack()
        self.stack.setStack([1])

        scroll = QScrollArea()
        scroll.setWidget(self.stack)
        scroll.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        scroll.setFixedWidth(150)

        main = QHBoxLayout()
        main.addLayout(field)
        main.addWidget(scroll)

        stack = QVBoxLayout()
        stack.addLayout(menu)
        stack.addLayout(main)

        m = QFrame()
        m.setLayout(stack)

        self.setCentralWidget(m)
        self.show()

    def run(self):
        self.io.clear()
        self.machine.set(self.data)
        self.machine.run()
        self.output.setText(self.io.output)

    def debug(self):
        if not self.running:
            self.machine.set(self.data)
            self.io.clear()
        while self.machine.direction != machine.Coord(0,0):
            self.machine.run_one()
            if self.machine.position in self.sandbox.breakpoints:
                self.running = True
                self.sandbox.setPointer(self.machine.position)
                self.output.setText(self.io.output)
                self.stack.setStack(self.machine.stack)
                break
        else:
            self.running = False
            self.output.setText(self.io.output)

    def step(self):
        if not self.running:
            self.machine.set(self.data)
            self.io.clear()
        if self.machine.direction != machine.Coord(0,0):
            self.running = True
            self.machine.run_one()
            self.sandbox.setPointer(self.machine.position)
            self.output.setText(self.io.output)
            self.stack.setStack(self.machine.stack)
        else:
            self.running = False
            self.output.setText(self.io.output)

    def stop(self):
        self.running = False


    def init_menu(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(app.quit)

        menubar = self.menuBar()
        menubar.setStyleSheet('background-color: #202020; color: white')
        fileMenu = menubar.addMenu('&File')
        fileMenu.setStyleSheet('background-color: #202020; color: white')
        fileMenu.addAction(exitAction)


window = Main()

app.exec()
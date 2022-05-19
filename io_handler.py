class IOHandler:
    inputQueue = []
    outputLines = []

    def write(self, obj):
        if (len(self.outputLines) == 0 or type(obj) is int or type(self.outputLines[-1]) is int):
            self.outputLines.append(obj)
        else:
            self.outputLines[-1] += obj

    def clear(self):
        self.outputLines = []

    def read(self, type):
        if len(self.inputQueue):
            if type == 'int':
                return int(self.inputQueue.pop(0))
            return ord(self.inputQueue.pop(0)[0])
            

class StdIOHandler(IOHandler):
    def read(self, type):
        x = input()
        self.inputQueue.append(x if x else '\x00')
        return super().read(type)
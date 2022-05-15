from nbformat import read


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

    def read(self):
        return self.inputQueue.pop(0)
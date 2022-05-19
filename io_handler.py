class IOHandler:
    input = []
    output = ''

    def write(self, obj):
        if type(obj) is int:
            self.output += f"{obj} "
        else:
            self.output += obj

    def clear(self):
        self.output = ''

    def read(self, type):
        if len(self.input):
            if type == 'int':
                return int(self.input.pop(0))
            return ord(self.input.pop(0)[0])
            

class StdIOHandler(IOHandler):
    def read(self, type):
        x = input()
        self.input.append(x if x else '\x00')
        return super().read(type)

    def write(self, obj):
        if obj == '\n':
            print(self.output)
            self.clear()
        else:
            super().write(obj)

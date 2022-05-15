

class Machine:
    stack = []
    commands = {}
    direction = (1,0)
    position = (0,0)
    instructions = []
    stringmode = False

    def set(self, instr):
        self.instructions = instr.split('\n')
        self.position = (0,0)
        self.direction = (1,0)
        self.size = (len(self.instructions[0]), len(self.instructions))
        self.stack = []
    
    def run(self):
        while self.direction != (0,0):
            self.run_one()

    def move(self):
        self.position = tuple((i + j) % k for i,j,k in zip(self.position, self.direction, self.size))

    def run_one(self):
        comm = self.instructions[self.position[1]][self.position[0]]
        if self.stringmode and comm != '"':
            self.stack.append(ord(comm))
        elif comm in self.commands:
            self.commands[comm](self)
        self.move()

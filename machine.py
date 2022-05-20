class Coord:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coord(self.x+other.x, self.y+other.y)
    
    def __mod__(self, other):
        return Coord(self.x%other.x, self.y%other.y)

    def __neg__(self):
        return Coord(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Machine:
    stack = []
    commands = {}
    direction = Coord(1,0)
    position = Coord(0,0)
    size = Coord(0,0)
    instructions = []
    stringmode = False

    def set(self, instr):
        self.instructions = [[chr for chr in line] for line in instr.split('\n')]
        self.position = Coord(0,0)
        self.direction = Coord(1,0)
        self.stringmode = False
        self.size = Coord(len(max(self.instructions, key=len)), len(self.instructions))
        self.stack = []
    
    def run(self):
        while self.direction != Coord(0,0):
            self.run_one()

    def move(self):
        self.position += self.direction
        self.position %= self.size

    def reflect(self):
        self.direction = -self.direction

    def run_one(self):
        comm = self.instructions[self.position.y][self.position.x]
        if self.stringmode and comm != '"':
            self.stack.append(ord(comm))
        elif comm in self.commands:
            self.commands[comm](self)
        self.move()

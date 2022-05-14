

class Machine:
    stack = []
    commands = {}
    direction = (1,0)
    position = (0,0)
    instructions = []

    def __init__(self, instr) -> None:
        self.instructions = instr.split('\n')
    
    def run(self):
        while self.direction != (0,0):
            self.run_one()

    def run_one(self):
        comm = self.instructions[self.position[1]][self.position[0]]
        if comm in self.commands:
            self.commands[comm](self)
        self.position = tuple(i + j for i,j in zip(self.position, self.direction))

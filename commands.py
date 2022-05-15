def set_direction(machine, direction=(0,0)):
    machine.direction = direction

def stop(machine):
    set_direction(machine)

def right(machine):
    set_direction(machine, (1,0))

def left(machine):
    set_direction(machine, (-1,0))

def up(machine):
    set_direction(machine, (0,-1))

def down(machine):
    set_direction(machine, (0,1))

def push(machine, value):
    machine.stack.append(value)

def pop(machine):
    return machine.stack.pop()

def init(machine):
    machine.commands['@'] = stop
    machine.commands['>'] = right
    machine.commands['<'] = left
    machine.commands['^'] = up
    machine.commands['v'] = down

    machine.commands['0'] = lambda m: push(m,0)
    machine.commands['1'] = lambda m: push(m,1)
    machine.commands['2'] = lambda m: push(m,2)
    machine.commands['3'] = lambda m: push(m,3)
    machine.commands['4'] = lambda m: push(m,4)
    machine.commands['5'] = lambda m: push(m,5)
    machine.commands['6'] = lambda m: push(m,6)
    machine.commands['7'] = lambda m: push(m,7)
    machine.commands['8'] = lambda m: push(m,8)
    machine.commands['9'] = lambda m: push(m,9)
    pass
import random

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

def rnd(machine):
    dir = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
    set_direction(machine, dir)

def push(machine, value):
    machine.stack.append(value)

def pop(machine):
    return machine.stack.pop()

def stringmode(machine):
    machine.stringmode = not machine.stringmode

def dublicate(machine):
    val = pop(machine)
    machine.stack.extend([val]*2)

def swap(machine):
    a = pop(machine)
    b = pop(machine)
    push(machine, a)
    push(machine, b)

def input(machine, io):
    push(machine, io.read())

def output(machine, type, io):
    if type == "int":
        io.write(pop(machine))
    if type == "char":
        io.write(chr(pop(machine)))

def init(machine, io):
    init_move(machine)
    init_const(machine)
    init_stack(machine, io)
    pass

def init_move(machine):
    machine.commands['@'] = stop
    machine.commands['>'] = right
    machine.commands['<'] = left
    machine.commands['^'] = up
    machine.commands['v'] = down
    machine.commands['?'] = rnd

def init_const(machine):
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

    machine.commands['"'] = stringmode

def init_stack(machine, io):
    machine.commands[':'] = dublicate
    machine.commands['\\'] = swap
    machine.commands['$'] = pop
    machine.commands['.'] = lambda m: output(m, 'int', io)
    machine.commands[','] = lambda m: output(m, 'char', io)
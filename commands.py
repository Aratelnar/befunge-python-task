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

def add(machine):
    pass

def init(machine):
    machine.commands['@'] = stop
    machine.commands['>'] = right
    machine.commands['<'] = left
    machine.commands['^'] = up
    machine.commands['v'] = down
    pass
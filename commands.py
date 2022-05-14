def stop(machine):
    machine.direction = (0,0)

def add(machine):
    pass

def init(machine):
    machine.commands['@'] = stop
    pass
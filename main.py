#!/usr/bin/env python3
import argparse
import sys
import machine
import io_handler
import commands

parser = argparse.ArgumentParser()
parser.add_argument("file")

def main(argv=sys.argv[1:]):
    args = parser.parse_args(argv)
    m = machine.Machine()
    io = io_handler.StdIOHandler()
    commands.init(m, io)
    with open(args.file) as instr:
        m.set(instr.read())
        m.run()
    for line in io.output:
        print(line)

if __name__ == "__main__":
    main()
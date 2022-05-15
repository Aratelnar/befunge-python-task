import unittest
import machine
import commands
import io_handler

class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = machine.Machine()
        self.io = io_handler.IOHandler()
        commands.init(self.machine, self.io)

    def machine_run(self, instr):
        self.io.clear()
        self.machine.set(instr)
        self.machine.run()

    def test_exit(self):
        self.machine_run('@')
        self.machine_run('       @')
        pass

    def test_move(self):
        self.machine_run('>v\n @')
        self.machine_run('<  @')
        pass

    def test_const(self):
        self.machine_run('123@')
        self.assertEqual(self.machine.stack, [1,2,3])

    def test_string(self):
        self.machine_run('"hello, world!"@')
        self.assertEqual(self.machine.stack, [ord(i) for i in 'hello, world!'])

    def test_stack(self):
        self.machine_run('1:@')
        self.assertEqual(self.machine.stack, [1,1])
        self.machine_run('123...@')
        self.assertEqual(self.io.outputLines, [3,2,1])
        self.machine_run('"abc",,,@')
        self.assertEqual(self.io.outputLines, ['cba'])

    def test_math(self):
        self.machine_run('23+@')
        self.assertEqual(self.machine.stack, [5])
        self.machine_run('23-@')
        self.assertEqual(self.machine.stack, [-1])
        self.machine_run('23*@')
        self.assertEqual(self.machine.stack, [6])
        self.machine_run('53/@')
        self.assertEqual(self.machine.stack, [1])
        self.machine_run('53%@')
        self.assertEqual(self.machine.stack, [2])

if __name__ == "__main__":
    unittest.main()
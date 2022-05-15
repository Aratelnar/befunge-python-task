import unittest
import machine
import commands
import io_handler

class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = machine.Machine()
        self.io = io_handler.IOHandler()
        commands.init(self.machine, self.io)

    def test_exit(self):
        self.machine.set('@')
        self.machine.run()
        self.machine.set('         @')
        self.machine.run()
        pass

    def test_move(self):
        self.machine.set('>v\n @')
        self.machine.run()
        self.machine.set('<  @')
        self.machine.run()
        pass

    def test_const(self):
        self.machine.set('123@')
        self.machine.run()
        self.assertEqual(self.machine.stack, [1,2,3])

    def test_string(self):
        self.machine.set('"hello, world!"@')
        self.machine.run()
        self.assertEqual(self.machine.stack, [ord(i) for i in 'hello, world!'])

    def test_stack(self):
        self.machine.set('1:@')
        self.machine.run()
        self.assertEqual(self.machine.stack, [1,1])
        self.machine.set('123...@')
        self.machine.run()
        self.assertEqual(self.io.outputLines, [3,2,1])
        self.io.clear()
        self.machine.set('"abc",,,@')
        self.machine.run()
        self.assertEqual(self.io.outputLines, ['cba'])
        self.io.clear()

if __name__ == "__main__":
    unittest.main()
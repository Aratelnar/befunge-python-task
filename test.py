import unittest
import machine
import commands

class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = machine.Machine()
        commands.init(self.machine)

    def test_exit(self):
        self.machine.set('@')
        self.machine.run()
        self.machine.set('         @')
        self.machine.run()
        pass

    def test_move(self):
        self.machine.set('>v\n @')
        self.machine.run()
        pass

    def test_const(self):
        self.machine.set('123@')
        self.machine.run()
        self.assertEqual(self.machine.stack, [1,2,3])

if __name__ == "__main__":
    unittest.main()
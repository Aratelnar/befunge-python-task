import unittest
import machine
import commands
import io_handler

class MachineTest1(unittest.TestCase):
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
        self.assertEqual(self.io.output, '3 2 1 ')
        self.machine_run('"abc",,,@')
        self.assertEqual(self.io.output, 'cba')
        self.io.input = ['60','61','62']
        self.machine_run('&&&,,,@')
        self.assertEqual(self.io.output, '>=<')

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

    def test_logic(self):
        self.machine_run('1!0!@')
        self.assertEqual(self.machine.stack, [0,1])
        self.machine_run('32`@')
        self.assertEqual(self.machine.stack, [1])
        self.machine_run('0>v \n ^_@')
        self.machine_run('0v1 \n >| \n  >@')
        self.assertEqual(self.machine.stack, [])

    def test_spec(self):
        self.machine_run('00g,@')
        self.assertEqual(self.io.output, '0')
        self.machine_run('"@"00p@')
        self.assertEqual(''.join(self.machine.instructions[0]), '@@"00p@')

    def test_rand(self):
        list = []
        for i in range(10):
            self.machine_run('v  > v\n>#v?v \n  vvvv\n  1234\n@.<<<<')
            list.append(int(self.io.output))
        self.assertIn(1, list)
        self.assertIn(2, list)
        self.assertIn(3, list)
        self.assertIn(4, list)


class MachineTest2(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = machine.Machine()
        self.io = io_handler.IOHandler()
        commands.init(self.machine, self.io)

    def machine_run(self, instr):
        self.io.clear()
        self.machine.set(instr)
        self.machine.run()

    files = [
        ('hello.txt', 'Hello, World!'),
        ('sieve.txt', '2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 ')
    ]

    def test(self):
        for file,answer in self.files:
            with open(f'./tests/{file}', 'r') as f:
                self.machine_run(f.read())
                # print('\n'.join(self.io.outputLines))
                self.assertEqual(self.io.output, answer)


if __name__ == "__main__":
    unittest.main()
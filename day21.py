from intcodecomputer import IntcodeComputer


def execute_springscript(springscript, intcode):
    computer = IntcodeComputer(intcode)
    res = computer.execute([ord(c) for c in springscript])

    view_str = ''.join([chr(v) for v in res if v < 256])
    print(view_str)

    print(res[-1])

def main():
    with open("input21") as f:

        intcode = [int(v) for v in f.read().split(',')]


        # Part 1
        springscript1 = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

        execute_springscript(springscript1, intcode)
        # Part 2
        springscript2 = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT H T
NOT T T
OR E T
AND T J
RUN
"""
        execute_springscript(springscript2, intcode)



main()

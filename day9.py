from intcodecomputer import IntcodeComputer

with open("input9") as f:
    intcode = [int(v) for v in f.read().split(',')]

    computer = IntcodeComputer(intcode)

    print(computer.execute([2]))

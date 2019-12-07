def execute_opcode(opcode, noun, verb):
    memory = opcode.copy()
    memory[1] = noun
    memory[2] = verb

    pc = 0
    while True:
        opcode = memory[pc]
        if opcode in [1, 2]:
            op1 = memory[memory[pc + 1]]
            op2 = memory[memory[pc + 2]]
            res_ptr = memory[pc + 3]

            if opcode == 1:
                res = op1 + op2
            else:
                res = op1 * op2

            memory[res_ptr] = res

        elif opcode == 99:
            break
        else:
            raise Exception("Unknow opcode {}".format(opcode))

        pc += 4

    return memory[0]


with open("input2") as f:
    opcode = [int(v) for v in f.read().split(',')]

    for i in range(0, 100):
        for j in range(0, 100):
            res = execute_opcode(opcode, i, j)
            if res == 19690720:
                print("Found for i={} j={}".format(i, j))
                break

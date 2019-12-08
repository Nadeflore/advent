import asyncio
import itertools


def parse_instruction(instruction):
    opcode = instruction % 100
    p1_mode = int(instruction / 100) % 10
    p2_mode = int(instruction / 1000) % 10
    p3_mode = int(instruction / 10000) % 10

    return opcode, [p1_mode, p2_mode, p3_mode]


def get_parameter(parameter_id, parameter_modes, memory, pc):
    param = memory[pc + parameter_id]
    if parameter_modes[parameter_id - 1] == 0:
        param = memory[param]

    return param


async def execute_intcode(intcode, inputqueue, outputqueue):
    memory = intcode.copy()

    pc = 0
    while True:
        opcode, parameter_modes = parse_instruction(memory[pc])
        if opcode in [1, 2]:
            op1 = get_parameter(1, parameter_modes, memory, pc)
            op2 = get_parameter(2, parameter_modes, memory, pc)
            res_ptr = memory[pc + 3]

            if opcode == 1:
                res = op1 + op2
            else:
                res = op1 * op2

            memory[res_ptr] = res

            pc += 4

        elif opcode == 3:
            res_ptr = memory[pc + 1]
            # memory[res_ptr] = int(input())
            memory[res_ptr] = await inputqueue.get()

            pc += 2

        elif opcode == 4:
            op1 = get_parameter(1, parameter_modes, memory, pc)
            print("programe output: {}".format(op1))
            await outputqueue.put(op1)

            pc += 2

        elif opcode in [5, 6]:
            op1 = get_parameter(1, parameter_modes, memory, pc)
            op2 = get_parameter(2, parameter_modes, memory, pc)

            if opcode == 5:
                condition = op1 != 0
            else:
                condition = op1 == 0

            if condition:
                pc = op2
            else:
                pc += 3

        elif opcode in [7, 8]:
            op1 = get_parameter(1, parameter_modes, memory, pc)
            op2 = get_parameter(2, parameter_modes, memory, pc)
            res_ptr = memory[pc + 3]

            if opcode == 7:
                condition = op1 < op2
            else:
                condition = op1 == op2

            if condition:
                memory[res_ptr] = 1
            else:
                memory[res_ptr] = 0

            pc += 4

        elif opcode == 99:
            break
        else:
            raise Exception("Unknow opcode {}, pc={}".format(opcode, pc))

    return


async def calculate_output_from_phase(phases, intcode):
    # Create queues
    queues = [asyncio.Queue() for _ in phases]

    # Create each amplifier
    amplifiers = []
    for i, phase in enumerate(phases):
        inputqueue = queues[i]
        outputqueue = queues[(i + 1) % len(queues)]
        amplifiers.append(asyncio.create_task(execute_intcode(intcode, inputqueue, outputqueue)))
        # Give this amplifier its phase
        inputqueue.put_nowait(phase)

    # input initial value
    queues[0].put_nowait(0)

    # Wait until all amplifier are terminated
    await asyncio.gather(*amplifiers)

    # Return final gain
    return queues[0].get_nowait()


with open("input7") as f:
    intcode = [int(v) for v in f.read().split(',')]

    signals = []
    for phases in itertools.permutations(range(5, 10)):
        signals.append(asyncio.run(calculate_output_from_phase(phases, intcode)))

    print(max(signals))

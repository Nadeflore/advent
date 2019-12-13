import itertools


class CPU:

    def __init__(self, intcode):
        self.memory = intcode.copy()
        self.pc = 0
        self.inputs = []
        self.outputs = []
        self.terminated = False

    def execute(self, inputs):
        self.inputs.extend(inputs)

        while not self.terminated:
            r = self.execute_one_instruction()

            if not r:
                break

        outputs = self.outputs
        self.outputs = []

        return outputs

    def parse_instruction(self, instruction):
        opcode = instruction % 100
        p1_mode = int(instruction / 100) % 10
        p2_mode = int(instruction / 1000) % 10
        p3_mode = int(instruction / 10000) % 10

        return opcode, [p1_mode, p2_mode, p3_mode]

    def get_parameter(self, parameter_id, parameter_modes):
        param = self.memory[self.pc + parameter_id]
        if parameter_modes[parameter_id - 1] == 0:
            param = self.memory[param]

        return param

    def execute_one_instruction(self):
        """ Execute one instruction, return False if input is needed, but not available
        """
        opcode, parameter_modes = self.parse_instruction(self.memory[self.pc])
        if opcode in [1, 2]:
            op1 = self.get_parameter(1, parameter_modes)
            op2 = self.get_parameter(2, parameter_modes)
            res_ptr = self.memory[self.pc + 3]

            if opcode == 1:
                res = op1 + op2
            else:
                res = op1 * op2

            self.memory[res_ptr] = res

            self.pc += 4

        elif opcode == 3:
            res_ptr = self.memory[self.pc + 1]
            # self.memory[res_ptr] = int(input())
            if len(self.inputs) == 0:
                return False

            self.memory[res_ptr] = self.inputs.pop(0)

            self.pc += 2

        elif opcode == 4:
            op1 = self.get_parameter(1, parameter_modes)
            print("programe output: {}".format(op1))
            self.outputs.append(op1)

            self.pc += 2

        elif opcode in [5, 6]:
            op1 = self.get_parameter(1, parameter_modes)
            op2 = self.get_parameter(2, parameter_modes)

            if opcode == 5:
                condition = op1 != 0
            else:
                condition = op1 == 0

            if condition:
                self.pc = op2
            else:
                self.pc += 3

        elif opcode in [7, 8]:
            op1 = self.get_parameter(1, parameter_modes)
            op2 = self.get_parameter(2, parameter_modes)
            res_ptr = self.memory[self.pc + 3]

            if opcode == 7:
                condition = op1 < op2
            else:
                condition = op1 == op2

            if condition:
                self.memory[res_ptr] = 1
            else:
                self.memory[res_ptr] = 0

            self.pc += 4

        elif opcode == 99:
            self.terminated = True
        else:
            raise Exception("Unknow opcode {}, pc={}".format(opcode, self.pc))

        return True


def calculate_output_from_phase(phases, intcode):

    # Init all amplifiers with phase
    amplifiers = []
    for phase in phases:
        amplifier = CPU(intcode)
        amplifier.inputs.append(phase)
        amplifiers.append(amplifier)

    signal = 0

    while True:
        for amplifier in amplifiers:
            if amplifier.terminated:
                return signal

            res = amplifier.execute([signal])
            signal = res[0]

    return signal


with open("input7") as f:
    intcode = [int(v) for v in f.read().split(',')]

    signals = []
    for phases in itertools.permutations(range(5, 10)):
        signals.append(calculate_output_from_phase(phases, intcode))

    print(max(signals))

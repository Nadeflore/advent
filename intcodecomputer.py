class IntcodeComputer:

    instructions = {
        1: {
            "nb_param": 2,
            "result": True,
            "func": lambda _, p1, p2: p1 + p2
        },
        2: {
            "nb_param": 2,
            "result": True,
            "func": lambda _, p1, p2: p1 * p2
        },
        3: {
            "nb_param": 0,
            "result": True,
            "func": lambda s: s.inputs.pop(0)
        },
        4: {
            "nb_param": 1,
            "result": False,
            "func": lambda s, p1: s.outputs.append(p1)
        },
        5: {
            "nb_param": 2,
            "result": False,
            "func": lambda s, p1, p2: setattr(s, "pc", p2 - 3) if p1 != 0 else None
        },
        6: {
            "nb_param": 2,
            "result": False,
            "func": lambda s, p1, p2: setattr(s, "pc", p2 - 3) if p1 == 0 else None
        },
        7: {
            "nb_param": 2,
            "result": True,
            "func": lambda _, p1, p2: 1 if p1 < p2 else 0
        },
        8: {
            "nb_param": 2,
            "result": True,
            "func": lambda _, p1, p2: 1 if p1 == p2 else 0
        },
        9: {
            "nb_param": 1,
            "result": False,
            "func": lambda s, p1: setattr(s, "relativebase", s.relativebase + p1)
        },
        99: {
            "nb_param": 0,
            "result": False,
            "func": lambda s: setattr(s, "terminated", True)
        },

    }

    def __init__(self, intcode):
        self.memory = intcode.copy()
        self.pc = 0
        self.relativebase = 0
        self.inputs = []
        self.outputs = []
        self.terminated = False

    def expand_memory_if_needed(self, address):
        current_memory_size = len(self.memory)
        if address >= current_memory_size:
            self.memory += [0] * (address - current_memory_size + 1)

    def read(self, address):
        self.expand_memory_if_needed(address)
        return self.memory[address]

    def write(self, address, value):
        self.expand_memory_if_needed(address)
        self.memory[address] = value

    def execute(self, inputs):
        self.inputs.extend(inputs)

        while not self.terminated:
            self.execute_one_instruction()

        outputs = self.outputs
        return outputs

    def get_parameter(self, param, mode):
        if mode == 0:
            return self.read(param)
        elif mode == 1:
            return param
        elif mode == 2:
            return self.read(self.relativebase + param)
        else:
            raise Exception("unknown parameter mode {}".format(mode))

    def get_mode(self, instruction, param_id):
        return int(instruction / 10 ** (param_id + 2)) % 10

    def write_output(self, param, mode, value):
        if mode == 0:
            self.write(param, value)
        elif mode == 2:
            return self.write(self.relativebase + param, value)
        else:
            raise Exception("unknown output mode {}".format(mode))

    def execute_one_instruction(self):
        """ Execute one instruction
        """
        instruction = self.read(self.pc)
        opcode = instruction % 100

        if opcode not in self.instructions:
            raise Exception("Unknow opcode {} at {}".format(opcode, self.pc))

        instruction_info = self.instructions[opcode]
        nb_param = instruction_info["nb_param"]
        instruction_length = 1 + nb_param

        params = [
            self.get_parameter(
                self.read(self.pc + i + 1),
                self.get_mode(instruction, i)
            ) for i in range(nb_param)]

        result = instruction_info["func"](self, *params)

        if instruction_info["result"]:
            self.write_output(
                self.read(self.pc + nb_param + 1),
                self.get_mode(instruction, nb_param),
                result
            )

            instruction_length += 1

        self.pc += instruction_length

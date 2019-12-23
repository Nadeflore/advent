from intcodecomputer import IntcodeComputer


def main():
    with open("input23") as f:
        intcode = [int(v) for v in f.read().split(',')]

        # Init 50 computers
        computersbyaddress = {}
        for i in range(50):
            computer = IntcodeComputer(intcode)
            # Set computer address
            computer.inputs = [i]

            computersbyaddress[i] = computer

        # Run network IO for each computer one by one

        natx = None
        naty = None
        previousnatysent = None
        while True:
            idle = True
            for computer in computersbyaddress.values():
                # add -1 to input if there's nothing in queue
                if not computer.inputs:
                    computer.inputs.append(-1)
                else:
                    idle = False

                output = computer.execute([])
                while len(output) >= 3:
                    idle = False
                    # get packet sent by this computer
                    address = output.pop(0)
                    x = output.pop(0)
                    y = output.pop(0)

                    # Nat management
                    if address == 255:
                        print("packet sent to nat(255): {} {}".format(x, y))
                        natx = x
                        naty = y

                    else:
                        # Put it in the target computer queue
                        computersbyaddress[address].inputs.extend([x, y])

            if idle:
                # Idle network, nat send store packet to addresse 0
                computersbyaddress[0].inputs.extend([natx, naty])
                if previousnatysent == naty:
                    print("sending same y value twice in a row: {}".format(naty))
                    return

                previousnatysent = naty







main()

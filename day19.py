from intcodecomputer import IntcodeComputer


def isonbeam(x, y, intcode):
    computer = IntcodeComputer(intcode)
    res = computer.execute([x, y])
    return res[0]


def main():
    with open("input19") as f:

        intcode = [int(v) for v in f.read().split(',')]

        # Part1
        count = 0
        for y in range(50):
            line = ""
            for x in range(50):
                if isonbeam(x, y, intcode):
                    line += "#"
                    count += 1
                else:
                    line += "."

            print(line)

        print(count)

        # Part2
        # Follow lower bound of beam
        x = 0
        y = 1000

        while True:
            if isonbeam(x, y, intcode):
                # In the beam, check if square can fit
                if isonbeam(x + 99, y - 99, intcode):
                    print("Found for {} {}".format(x, y - 99))
                    break

                # Try next line
                y += 1
            else:
                # Not in the beam, try more to the right
                x += 1


main()

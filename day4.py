def does_meeet_criteria(value):
    previous_digit = None
    adj = False
    consecutive = 1
    for digit in value:
        if previous_digit:
            if digit == previous_digit:
                consecutive += 1

            else:
                if consecutive == 2:
                    adj = True

                consecutive = 1

            if int(digit) < int(previous_digit):
                return False

        previous_digit = digit

    if consecutive == 2:
        adj = True

    return adj


print(does_meeet_criteria("1222333"))

with open("input4") as f:
    start, end = f.read().split('-')
    start = int(start)
    end = int(end)
    print(start)
    print(end)

    count = 0
    for i in range(start, end+1):
        if does_meeet_criteria(str(i)):
            count += 1

    print(count)

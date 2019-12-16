basepattern = [0, 1, 0, -1]


def fft(signal):
    for k in range(len(signal)):
        elem = 0
        for n, e in enumerate(signal):
            elem += e * basepattern[((n + 1) // (k + 1)) % len(basepattern)]

        yield abs(elem) % 10


def partialfft(signal, offset):
    """ Calculates term starting from given offset
        for terms X(k) with k > N/3-1 the calculation can be simplified to
        the sum of terms x(n) with k <= n < 2k+1
        and for terms X(k) with k > N/2-1 the calculation can be further simplified to
        the sum of terms x(n) with n >= k
    """
    result = [0] * len(signal)

    prev = 0
    for k in range(len(signal) - 1, offset - 1, -1):
        val = prev + signal[k]
        result[k] = val % 10
        prev = val

    return result


with open("input16") as f:
    input_str = f.read().strip()
    initialsignal = [int(c) for c in input_str]

    # First part
    signal = initialsignal

    for i in range(100):
        signal = list(fft(signal))

    print(''.join([str(c) for c in signal[:8]]))

    # Second part
    offset = int(input_str[:7])
    if offset <= len(initialsignal) / 2 - 1:
        raise Exception("could not compute partial fft for this offset")

    signal = (initialsignal * 10000)

    for i in range(100):
        signal = list(partialfft(signal, offset))

    print(''.join([str(c) for c in signal[offset:offset + 8]]))

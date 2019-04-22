class sp:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def __str__(self):
        return bytes((S[self.start:self.end])).decode('utf-8')

    def __lt__(self, other):
        return bytes((S[self.start:self.end])) < bytes((S[other.start:other.end]))


def set_S(input):
    global S
    S = memoryview(input)


def sa(input):
    """ Slower, but less memory. """

    #set_S(bytes(input + '$', 'utf-8'))
    set_S(bytes(input, 'utf-8'))

    sufs = [(i, sp(i, len(S))) for i in range(len(S))]    
    sufs.sort(key = lambda x: x[1])
    
    
    l1, l2 = zip(*sufs)

    return l1, l2


if __name__ == '__main__':
    import t4
    #a = sa(t4.t4_genome())

    a, b = sa('mississippi')

    for i, j in zip(a, b):
        print(i, j);
import t4

def set_S(input):
    global S
    S = memoryview(input)


class sp:
    def __init__(self, start, end):
        self.start = start
        self.end = end


    def get(self):
        return bytes((S[self.start:self.end]))

    def __lt__(self, other):
        return self.get().decode('utf-8') < other.get().decode('utf-8')

#@profile
def sa(input):
    set_S(bytes(input, 'utf-8'))
    sufs = ((i, sp(i, len(S))) for i in range(len(S)))
    sufs = sorted(sufs, key = lambda x: x[1])
    return sufs





@profile
def sao(S):
    sufs = ((i, S[i:]) for i in range(len(S)))
    sufs = sorted(sufs, key = lambda x: x[1])
    
    l1, l2 = zip(*sufs)
    return l1, l2








if __name__ == '__main__':

    #set_S(b'mississippi')
    # print('hej')
    # print(sp(1,5).get())

    #a = sa(t4.t4_genome())
        #print(i)

    
    a = sao(t4.t4_genome())
        #print(i)

    

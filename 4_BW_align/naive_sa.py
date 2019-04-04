import t4
import time as t

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
        #return self.get().decode('utf-8') < other.get().decode('utf-8')
        return self.get() < other.get()


#@profile
def sa(input):
    """ Slower, but less memory """
    t0 = t.time()
    set_S(bytes(input, 'utf-8'))
    t1 = t.time()
    sufs = ((i, sp(i, len(S))) for i in range(len(S)))
    t2 = t.time()
    sufs = sorted(sufs, key = lambda x: x[1])
    t3 = t.time()
    
    l1, l2 = zip(*sufs)
    t4 = t.time()
    print('sa', t1-t0, t2-t1, t3-t2, t4-t3)
    return l1, l2






#@profile
def sao(S):
    """ Faster, but more memory """
    t0 = t.time()
    sufs = ((i, S[i:]) for i in range(len(S)))
    t1 = t.time()
    sufs = sorted(sufs, key = lambda x: x[1])
    t2 = t.time()
    
    l1, l2 = zip(*sufs)
    t3 = t.time()
    
    print('sao', t1-t0, t2-t1, t3-t2)
    return l1, l2








if __name__ == '__main__':

    #set_S(b'mississippi')
    # print('hej')
    # print(sp(1,5).get())

    a = sa(t4.t4_genome())
        #print(i)
    
    a = sao(t4.t4_genome())
        #print(i)


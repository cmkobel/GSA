from functools import cmp_to_key 
#@profile
def sa(s):
    
    def suf_cmp(i, j):

        while s[i] == s[j]:
            i = i + 1
            j = j + 1
        return -1 if s[i] < s[j] else 1

    return sorted([i for i in range(len(s))], key = cmp_to_key(suf_cmp))

if __name__ == '__main__':


    import t4



    a = t4.t4_genome()[:50000] + '$'


    print(sa(a)[:100])
    















import naive_sa

S = 'mississippi'
sa, sa_str = naive_sa.sa(S)
print(' '.join(S))
print(' '.join([str(i) for i in range(len(S))]))
print('=' * len(S)*2)

print(sa)
print(sa_str)
print('='*len(S)*2)

#print('this is the global S:', bytes(globalized.S).decode('utf-8'))
p = 'ssi'


# initialize L, M, R
l = 0
m = len(S)//2
r = len(S)


for i in range(10): # While True:; break later
    print(sa_str[m])
    print(l, m, r)

    if p < str(sa_str[m]):
        print(e)



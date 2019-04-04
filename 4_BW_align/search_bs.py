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


# initialize L, M, R
# l = 0
# m = len(S)//2
# r = len(S) -1



# for i in range(10): # While True:; break later
#     print(sa_str[m])
#     print(l, m, r)
#     minimum = min(len(str(sa_str[m])), len(p))
#     print('min', minimum)

#     if p == str(sa_str[m])[:len(p)]:
#         break
#     elif p > str(sa_str[m]):
#         print('greater')
#         l = m
#         r = r
#         m = (r+l)//2
#         print(p[:len(p)], str(sa_str[m])[:len(p)])        
#     elif p < str(sa_str[m]):
#         print('less')
#         l = l
#         r = m
#         m = (r+l)//2


# print(m)

p = 'i'

j = -1
L = 0
R = len(S) - 1
#for i in range(10):
while True:
    M = -(-(R+L)//2) # ceiling integer division
    print(L, M, R)
    print('comparing:', p, S[sa[M]:sa[M]+len(p)])



    if p == S[sa[M]:sa[M]+len(p)]:
        j = sa[M]
        break
        print('same')
    elif p > S[sa[M]:sa[M]+len(p)]:
        L = M
        print('more')
    else:
        R = M
        print('less')
    M = -(-(R+L)//2) # ceiling integer division
    
    # if L == M or j != -1:
    #     break

print(j)


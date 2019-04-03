
S = 'processing'
alphabet = sorted(set(S))
print(alphabet)

S0 = [i for i in range(0, len(S), 3)]
S1 = [i for i in range(1, len(S), 3)]
S2 = [i for i in range(2, len(S), 3)]


print(S0)
print(S1)
print(S2)

S12 = S1 + S2

print('S12', S12)
# bucket sort


rv = ''
for _j, j in enumerate(S12):
    for _i, i in enumerate(alphabet):
        if S[j] == i:
            rv += str(_i)
print(rv)
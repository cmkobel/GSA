a = [1,2,3]
b = [11,22,33]
c = [111,222,333]

z =iter(zip(a,b,c))

for a,b,c in z:
    print(a,b,c)
    print(next(z))


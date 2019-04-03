# Inspired by:
# https://gist.github.com/markormesher/59b990fba09972b4737e7ed66912e044

S = 'processing'

def initialize_arrays(S):
    empty = -1
    S0 = [empty for i in range(len(S)//3)]
    S1 = [empty for i in range(len(S)//3)]
    S2 = [empty for i in range(len(S)//3)]

    if len(S)%3 == 1:
        S0.append(empty)
    if len(S)%3 == 2:
        S0.append(empty)
        S1.append(empty)

    return S0, S1, S2

S0, S1, S2 = initialize_arrays(S)


print(S0)
print(S1)
print(S2)


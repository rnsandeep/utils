#https://practice.geeksforgeeks.org/problems/shortest-direction/0

def decode(S):
    index = (0,0)
    for s in S:
        if s=='S':
            index = (index[0], index[1]+1)
        if s=='E':
            index = (index[0]+1, index[1])
        if s=='N':
            index = (index[0], index[1]-1)
        if s=='W':
            index = (index[0]-1, index[1])

    return index


#a = 'SSSNEEEW'
a = 'NESNWES'

point = decode(a)

print(point)

point = [point[0], point[1]]

final = ''
while( point[0] > 0):
    final += 'E'
    point[0] -= 1

while(point[0] < 0):
    final += 'W'
    point[0] += 1

while(point[1] > 0):
    final += 'S'
    point[1] -= 1

while(point[1] < 0):
    final += 'N'
    point[1] += 1 

print(final)




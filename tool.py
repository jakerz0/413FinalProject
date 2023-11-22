
import networkx as nx # graph library

# finding the number of variable assignments
f = open('test1.c')
lines = f.readlines()

assignments_on = [] # is this even needed??
mallocs = []
frees = []

CFG = nx.DiGraph() # directed graph

# getting mallocs, frees, and general assignments by program point, no names/vals
i = 0
for i in range(len(lines)):
    if lines[0:2] == '//': continue # skip comments ;)
    if '=' in lines[i] and 'malloc' in lines[i]:
        mallocs.append(i)
    if '=' in lines[i] and '==' not in lines[i]:
        assignments_on.append(i)
    if 'free' in lines[i]:
        frees.append(i)

branches = []
i = 0
while i < len(lines):
    if lines[0:2] == '//': continue # skip comments ;)
    if 'if' in lines[i]:
        branches = [i]
        # look for elifs and else
        # HOW????

    i += 1

print(assignments_on)
print(mallocs)
print(frees)
# 2 cases: struct <...> and <type> (basic)
type = ['int','float','double','char'] # if not type, then its a struct

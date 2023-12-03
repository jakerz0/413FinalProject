
#import networkx as nx # graph library



# finding the number of variable assignments
f = open('test1.c')
lines = [str(l).strip() for l in f.readlines()]
f.close()

print(lines)

assignments_on = [] # is this even needed??
mallocs = []
frees = []
branches = []
'''
NOTE: THIS EXPECTS WELL FORMED AND STYLED C CODE
'''
def branchFinder(pp: int): # start at a given program point, end of selection to be analyzed
    isOpen = True
    curStart = pp
    curEnd = -1
    # if end != -1: curEnd = end
    # needs recurison, given a startpoint and endpoint
    for i in range(curStart, len(lines)):
        if lines[i][0:2] == '//': continue # skip comments ;)
        if 'if' in lines[i]:
            branchFinder(pp + 1)
        if 'else if' in lines[i]: # necessary?
            curStart = i
            curEnd = -1
            isOpen = True
        if 'else' in lines[i]: 
            curStart = i
            curEnd = -1
            isOpen  = True
        if isOpen and '}' in lines[i]:
            curEnd = i
            branchFinder(pp + 1)
            branches.append((curStart,curEnd)) # add
            curStart = -1 # reset markers
            curEnd = -1
            isOpen = False
            continue
        if curStart != -1 and curEnd == -1: # still in a branch block i.e start found, end has not been
            continue
        # break condn
        if not isOpen and curStart == -1 and curEnd == -1: # nothing after the end of consecutive ITE blocks
            break
        
            
        


# CFG = nx.DiGraph() # directed graph

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


i = 0
while i < len(lines):
    if lines[0:2] == '//': continue # skip comments ;)
    if 'if' in lines[i]:
        # branches = [i]
        # look for elifs and else
        # HOW????
        branchFinder(i+1)

    i += 1

print(assignments_on)
print(mallocs)
print(frees)
print(branches)
# 2 cases: struct <...> and <type> (basic)
type = ['int','float','double','char'] # if not type, then its a struct



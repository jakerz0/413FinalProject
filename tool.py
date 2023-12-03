
#import networkx as nx # graph library
from GraphNode import GraphNodeClass

cfg = GraphNodeClass()

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
def branchFinder(start: int, end: int, G: GraphNodeClass): # start at a given program point, end of selection to be analyzed
    #print(len(lines))
    i = start
    while i < end:
        if "//" in lines[i]: 
            i += 1
            continue
    #print(i)
        if "if" in lines[i]:
            thisBlock = findEndOfBlock(i)
            g = GraphNodeClass()
            g.data = thisBlock
            print(thisBlock)
            G.addChild(g)
            i = branchFinder(i+1,thisBlock[1]-1, g)
            # print("entering branch")
            # print(lines[i])
            # pp = i + 1
            # thisEnd = findEndOfBlock(i)
            # while "}" not in lines[pp]:
            #     i = branchFinder(pp, thisEnd)
            #     pp += 1
            # print("leaving branch")
            # branches.append((i,thisEnd))
            # return pp
        if "else" in lines[i]:
            thisEnd = findEndOfBlock(i)
            # print("entering branch")
            # print(lines[i])
            # pp = i + 1
            # thisEnd = findEndOfBlock(i)
            # while "}" not in lines[pp]:
            #     i = branchFinder(pp, thisEnd)
            #     pp += 1
            # print("leaving branch")
            # branches.append((i,thisEnd))
            # return pp
        if i == end:
            branches.append((start,end))
            return i
        i += 1
        
tmp = []
def findEndOfBlock(start: int):
    stack = []
    for i in range(start, len(lines)):
        if "//" in lines[i]: continue
        if "{" in lines[i]:
            stack.append(i)
        if "}" in lines[i]:
            y = stack.pop()
            if (y,i) not in tmp:
                tmp.append((y,i))
        if len(stack) == 0: 
            # print(tmp)

            return (start, i) 
        


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


# i = 0
# while i < len(lines):
#     if lines[0:2] == '//': continue # skip comments ;)
#     if 'if' in lines[i]:
#         # branches = [i]
#         # look for elifs and else
#         # HOW????
#         branchFinder(i+1)

#     i += 1

branchFinder(0, len(lines) - 1, cfg)

print(assignments_on)
print(mallocs)
print(frees)
print(branches)
print(tmp)
# 2 cases: struct <...> and <type> (basic)
type = ['int','float','double','char'] # if not type, then its a struct



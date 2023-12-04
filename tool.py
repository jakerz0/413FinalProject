
#import networkx as nx # graph library

# BEGIN GRAPH STUFF
graph = {}
vertices_no = 0
graphData = {}

# Add a vertex to the dictionary
def add_vertex(v, data):
  global graph
  global vertices_no
  global graphData
  if v in graph:
    print("Vertex ", v, " already exists.")
  else:
    vertices_no = vertices_no + 1
    graph[v] = []
    graphData[v] = data

# Add an edge between vertex v1 and v2 with edge weight e
def add_edge(v1, v2):
  global graph
  # Check if vertex v1 is a valid vertex
  if v1 not in graph:
    print("Vertex ", v1, " does not exist.")
  # Check if vertex v2 is a valid vertex
  elif v2 not in graph:
    print("Vertex ", v2, " does not exist.")
  else:
    # Since this code is not restricted to a directed or 
    # an undirected graph, an edge between v1 v2 does not
    # imply that an edge exists between v2 and v1
    graph[v1].append(v2)

# Print the graph
def print_graph():
  global graph
  for vertex in graph:
    for edges in graph[vertex]:
      print(vertex, " -> ", edges[0], " edge weight: ", edges[1])

# GRAPH STUFF DONE

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
# def branchFinder(start: int, end: int, G: GraphNodeClass): # start at a given program point, end of selection to be analyzed
#     #print(len(lines))
#     i = start
#     while i < end:
#         if "//" in lines[i]: 
#             i += 1
#             continue
#     #print(i)
#         if "if" in lines[i]:

#             # print("entering branch")
#             # print(lines[i])
#             # pp = i + 1
#             # thisEnd = findEndOfBlock(i)
#             # while "}" not in lines[pp]:
#             #     i = branchFinder(pp, thisEnd)
#             #     pp += 1
#             # print("leaving branch")
#             # branches.append((i,thisEnd))
#             # return pp
#         if "else" in lines[i]:
#             # print("entering branch")
#             # print(lines[i])
#             # pp = i + 1
#             # thisEnd = findEndOfBlock(i)
#             # while "}" not in lines[pp]:
#             #     i = branchFinder(pp, thisEnd)
#             #     pp += 1
#             # print("leaving branch")
#             # branches.append((i,thisEnd))
#             # return pp
#         if i == end:
#             branches.append((start,end))
#             return i
#         i += 1
        
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
add_vertex(vertices_no, "poop")
add_vertex(vertices_no, "pooop")
add_edge(0,1)
print(graph)
print(graphData)
print(graph[0][0])

branchFinder(0, len(lines) - 1)

print(assignments_on)
print(mallocs)
print(frees)
print(branches)
print(tmp)
# 2 cases: struct <...> and <type> (basic)
type = ['int','float','double','char'] # if not type, then its a struct



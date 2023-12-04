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

#print(lines)


assignments_on = [] # is this even needed??
mallocs = []
frees = []
branches = []
'''
NOTE: THIS EXPECTS WELL FORMED AND STYLED C CODE
'''
def branchFinder(start: int, end: int, G: int): # start at a given program point, end of selection to be analyzed, parent int
    global vertices_no
    global lines
    stack = []
    i = start
    while i < end:
        # comment or empty line
        if len(lines[i]) == 0 or lines[i][0] == "/":
            i += 1
        else:
            # start of if or else conditional
            if "if(" in lines[i] or "else{" in lines[i] or "else if{" in lines[i]:
                temp = i
                while True:
                    if "{" in lines[temp]:
                        stack.append("{")
                    if "}" in lines[temp]:
                        if stack[len(stack) - 1] == "{":
                            stack.pop()
                            if (len(stack) == 0):
                                #break when found end, end is held in temp
                                break
                        else:
                            # This should realistically never happen
                            stack.append("}")
                    temp += 1
                add_vertex(vertices_no, (i, temp)) # adds new vertice i=start, temp=end
                add_edge(G, vertices_no - 1)
                branchFinder(i + 1, temp, vertices_no - 1)
                i = temp
            elif "for(" in lines[i]  or "while(" in lines[i]:
              temp = i
              while True:
                  if "{" in lines[temp]:
                      stack.append("{")
                  if "}" in lines[temp]:
                      if stack[len(stack) - 1] == "{":
                          stack.pop()
                          if (len(stack) == 0):
                              #break when found end, end is held in temp
                              break
                      else:
                          # This should realistically never happen
                          stack.append("}")
                  temp += 1
              add_vertex(vertices_no, (i, temp)) # adds new vertice i=start, temp=end
              add_edge(G, vertices_no - 1)
              add_edge(vertices_no -1, vertices_no -1) # for loops, add an edge from that branch to itself
              branchFinder(i + 1, temp, vertices_no - 1)
              i = temp
            else:
                i += 1
            

        
# tmp = []
# def findEndOfBlock(start: int):
#     stack = []
#     for i in range(start, len(lines)):
#         if "//" in lines[i]: continue
#         if "{" in lines[i]:
#             stack.append(i)
#         if "}" in lines[i]:
#             y = stack.pop()
#             if (y,i) not in tmp:
#                 tmp.append((y,i))
#         if len(stack) == 0: 
#             # print(tmp)

#             return (start, i) 
        


# getting mallocs, frees, and general assignments by program point, no names/vals
i = 0
for i in range(len(lines)):
    if len(lines[i]) > 0 and lines[i][0] == "/": continue # skip comments ;)
    if '= malloc(' in lines[i]:
        mallocs.append(i)
    if '=' in lines[i] and '==' not in lines[i]:
        assignments_on.append(i)
    if 'free' in lines[i]:
        frees.append(i)


# All of the numbers are the line number - 1 because of starting at line 0
branchFinder(0, len(lines) - 1, vertices_no)
print("Graph:", graph)
print("Graph Data:", graphData)
print("Mallocs:", mallocs)
print("Frees:", frees)

# 2 cases: struct <...> and <type> (basic)
type = ['int','float','double','char'] # if not type, then its a struct



# BEGIN GRAPH STUFF
graph = {}
vertices_no = 0
graphData = {}
graphConds = {}
graphParents = {}

# Add a vertex to the dictionary
def add_vertex(v, data, cond):
  global graph
  global vertices_no
  global graphData
  global graphConds
  if v in graph:
    print("Vertex ", v, " already exists.")
  else:
    vertices_no = vertices_no + 1
    graph[v] = []
    graphData[v] = data
    graphConds[v] = cond
    graphParents[v] = []

# Add an edge between vertex v1 and v2 with edge weight e
def add_edge(v1, v2):
  global graph
  global graphParents
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
    if v2 not in graph[v1]: graph[v1].append(v2)
    if v1 not in graph[v2]: graphParents[v2].append(v1)

# Print the graph
def print_graph():
  global graph
  for vertex in graph:
    for edges in graph[vertex]:
      print(vertex, " -> ", edges[0], " edge weight: ", edges[1])

# GRAPH STUFF DONE

# finding the number of variable assignments
f = open('test3.c')
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
    while i <= end:
        # comment or empty line, comments should always be on their own lines
        if(i == end):
           print("something")
           #snapToParent(G)
           break
        if len(lines[i]) == 0 or "//" in lines[i]:
            i += 1
        else:
            # start of if or else conditional
            if "if(" in lines[i] or "else{" in lines[i] or "else if(" in lines[i]:
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
                thisCond = getLineCond(lines[i])
                cond = vertices_no # v_no of the conditional
                add_vertex(vertices_no, (i,i), thisCond) # the conditional statement itself
                body = vertices_no # v_no of body
                add_vertex(vertices_no, (i, temp), "body") # adds new vertice i=start, temp=end
                # below is here because the first node should not point to itself (0) unless it is a loop
                # if it is -1, meaning it is the very first branch, G should be changed to 0 afterword
                if(G != -1): 
                   add_edge(G, cond)
                else: 
                   G = 0
                add_edge(cond, body)
                branchFinder(i + 1, temp, cond)
                #snapToParent(cond)
                # i = temp + 1
                i += 1
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
              thisCond = getLineCond(lines[i])
              cond = vertices_no # v_no of the conditional
              add_vertex(cond, (i, i), thisCond) # adds new vertice i=start, temp=end
              body = vertices_no # v_no of body
              add_vertex(body, (i, temp), "body") # adds new vertice i=start, temp=end
              add_edge(G, cond) # between superbody and cond
              add_edge(cond, body) # between the cond and the body
              add_edge(body, cond) # for loops, add an edge from its body to its cond
              branchFinder(i + 1, temp, vertices_no - 1)
              i = temp
            else:
                # we are in a body section!
                # temp = i
                # while "}" not in lines[temp] and\
                #       "if(" not in lines[temp] and\
                #       "else{" not in lines[temp] and\
                #       "for(" not in lines[temp] and\
                #       "while(" not in lines[temp]:
                #    temp += 1
                # v = vertices_no
                # add_vertex(v, (i, temp), "body")
                # if len(graph[G]) > 0:
                #    for branch in graph[G]:
                #     add_edge(branch, v)
                # else:
                #    add_edge(G, v)
                # branchFinder(temp, end, v)
                # i = temp+1
                i += 1
            

def getLineCond(s: str):
   if "else if(" in s:
      return "else if"
   elif "if(" in s:
      return "if"
   elif "else{" in s:
      return "else"
   elif "for(" in s:
      return "for"
   elif "while(" in s:
      return "while"
   else:
      print("NO COND FOUND in " + s)

# TODO this is still not perfect, I think the body system needs to be refactored to include multiple 
# "bodies" in one block, i.e. between loops and ites in a given block
def snapToParent(g: int):
    if(g <= 0): return
    iter = g
    while iter > 1 and graphParents[iter] != None:

        if graphConds[graphParents[iter][0]] == "while" or graphConds[graphParents[iter][0]] == "for":
            break
        iter = graphParents[iter][0]
    iter = graphParents[iter][0]
    add_edge(g, iter)
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
mainstart = -1
mainend = -1
for i in range(0, len(lines) -1):
   if "//" in lines[i]: continue
   if "main(int argc, char* argv[])" in lines[i]:
      mainstart = i
      temp = i
      stack = []
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
      mainend = temp
      break
add_vertex(vertices_no, (mainstart,mainend), "ENTRY")
branchFinder(mainstart, mainend, 0)
print("Graph:", graph)
print("Graph Data:", graphData)
print("Graph Conds: " , graphConds)
print("Graph Parents: ", graphParents)
print("Mallocs:", mallocs)
print("Frees:", frees)

# 2 cases: struct <...> and <type> (basic)
type = ['int','float','double','char'] # if not type, then its a struct



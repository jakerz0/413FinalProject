import os
import sys

# BEGIN GRAPH STUFF
graph = {}
vertices_no = 0
graphData = {}
graphConds = {}
graphParents = {}
graphAvailable = {}

# Add a vertex to the dictionary
def add_vertex(v, data, cond):
  global graph
  global vertices_no
  global graphData
  global graphConds
  global graphAvailable
  if v in graph:
    print("Vertex ", v, " already exists.")
  else:
    vertices_no = vertices_no + 1
    graph[v] = []
    graphData[v] = data
    graphConds[v] = cond
    graphParents[v] = []
    graphAvailable[v] = set()

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

# gets next node for if/else statements when connecting edges
def getNextNode(endIndex):
   for data in graphData:
      if graphData[data][0] > endIndex:
         return data

# gets next node for loops when connecting edges
def getNextLoopNode(endIndexNode, endIndexLoop, loopNode):
    for data in graphData:
        if graphData[data][0] > endIndexNode and graphData[data][0] < endIndexLoop:
            return data
    return loopNode

# finding the number of variable assignments
if len(sys.argv) > 2:
   print("You must supply only one filepath as an argument, exiting.")
   exit(0)
f = open(sys.argv[1])
lines = [str(l).strip() for l in f.readlines()]
f.close()

#print(lines)


'''
NOTE: THIS EXPECTS WELL FORMED AND STYLED C CODE
'''
def branchFinder(start: int, end: int, G: int): # start at a given program point, end of selection to be analyzed, parent int
    global vertices_no
    global lines
    stack = []
    inLoop = False
    loopLocations = {} # start of loop, (end of loop, loopNode)
    pathsToAdd = {} # node number, line number ended
    pathsInLoops = {} # (node number, line number ended), (loopNodeNumber, line number ended)
    i = start
    while i <= end:
        # comment or empty line, comments should always be on their own lines
        if(i == end):
           break
        if len(lines[i]) == 0 or "//" in lines[i] or (len(lines[i]) == 1 and "}" in lines[i]):
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
                add_edge(G, vertices_no - 1)
                G = vertices_no - 1
                # will not add if in loops, instead added later
                firstIn = True
                for loc in loopLocations:
                    if (loc < i and loopLocations[loc][0] > temp):
                        inLoop = True
                        if (not firstIn and loopLocations[loc][0] < loopNode[0]):
                            loopNode = loopLocations[loc]
                        else:
                            loopNode = loopLocations[loc]
                        firstIn = False
                firstIn = False
                # add to if/else conditional dictionary
                if ("else{" not in lines[i]) and not inLoop:
                    pathsToAdd[vertices_no - 1] = temp
                # add to for/while conditional dictionary
                elif inLoop:
                    pathsInLoops[(vertices_no - 1, temp)] = (loopNode[1], loopNode[0])
                inLoop = False
                i += 1
            # case for for/while loops
            elif "for(" in lines[i]  or "while(" in lines[i]: # loop identification
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
                add_vertex(vertices_no, (i, i), thisCond) # adds new vertice of conditional
                pathsToAdd[cond] = temp
                # will not add if in loops, instead added later
                firstIn = True
                for loc in loopLocations:
                    if (loc < i and loopLocations[loc][0] > temp):
                        inLoop = True
                        if (not firstIn and loopLocations[loc][0] < loopNode[0]):
                            loopNode = loopLocations[loc]
                        else:
                            loopNode = loopLocations[loc]
                        firstIn = False
                firstIn = False
                # addition to for/while dictionary
                if inLoop:
                    pathsInLoops[(vertices_no - 1, temp)] = (loopNode[1], loopNode[0])
                inLoop = False
                loopLocations[i] = (temp, vertices_no - 1)
                body = vertices_no # v_no of body

                add_edge(G, cond) # between conditional and previous

                add_edge(cond, cond) # for loops, add an edge from its body to its cond

                G = vertices_no - 1
                i += 1
            else:
                # normal case for basic lines of code
                add_vertex(vertices_no, (i, i), "body")
                add_edge(G, vertices_no - 1)
                # will not add if in loops, instead added later
                firstIn = True
                for loc in loopLocations:
                    if (loc < i and loopLocations[loc][0] > i):
                        inLoop = True
                        if (not firstIn and loopLocations[loc][0] < loopNode[0]):
                            loopNode = loopLocations[loc]
                        else:
                            loopNode = loopLocations[loc]
                        firstIn = False
                firstIn = False
                if inLoop:
                    pathsInLoops[(vertices_no - 1, i)] = (loopNode[1], loopNode[0])
                inLoop = False
                G = vertices_no - 1
                i += 1
    # adds missing edges to if/else statements
    for path in pathsToAdd:
       nextNode = getNextNode(pathsToAdd[path])
       if (nextNode not in graph[path]):
          add_edge(path, nextNode)
    # adds missing edges to for/while statements
    for loopPath in pathsInLoops:
        nextNode = getNextLoopNode(loopPath[1], pathsInLoops[loopPath][1],
                                   pathsInLoops[loopPath][0])
        if (nextNode not in graph[loopPath[0]]):
            add_edge(loopPath[0], nextNode)
        # remove edges that leave loops
        for edge in graph[loopPath[0]]:
            if (graphData[edge][0] > pathsInLoops[loopPath][1]): # if start of edge is after end of loop
                graph[loopPath[0]].remove(edge)
            

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

# isolates the name of the variable being allocated
def getVarNameAlloc(line: str):
   elems = line.split()
   for i in range(len(elems)):
      if elems[i] == "=":
         return elems[i-1]

# isolates the name of the variable in a free()
def getVarNameFree(line: str):
    start: int
    end: int
    for i in range(len(line)):
      if line[i] == "(":
        elem = i+1
        start = elem
        while(line[elem] != ")"):
            elem = elem+1

        end = elem
        break
    return line[start:end]

freeStatements = {}
def traverse(root: int):
   global graph
   Q = [root]
   visited = []
   global freeStatements
   
   # BFS pattern
   while Q:
      # get node to process
      v = Q.pop()

      for neighbor in graph[v]:
        if neighbor in visited:
            continue
            # variable stuff
        if "for(" or "while(" in lines[neighbor]:
           # only add loops to visited since their children will return to their
           # parent-loop's conditional node. It does not need to be reevaluated.
           visited.append(neighbor)

        graphAvailable[neighbor] = set(graphAvailable[v]).union(set(graphAvailable[neighbor]))
        if graphData[neighbor][0] == graphData[neighbor][1]: # if it is an atomic operation/node
            theLine = graphData[neighbor][0]
            if "alloc(" in lines[theLine]: # GEN definitions
                theName = getVarNameAlloc(lines[theLine])
                graphAvailable[neighbor] = set(graphAvailable[neighbor]).union({theName})
            if "free(" in lines[theLine]: # KILL definitions
                theName = getVarNameFree(lines[theLine])
                graphAvailable[neighbor] = set(graphAvailable[neighbor]).difference({theName})
                if theName not in freeStatements:
                   freeStatements[theName] = []
                freeStatements[theName].append(neighbor)

        # bookkeeping... python does not like empty sets, it treats them as NONE and
        # not an empty data structure. I suppose that is mathematically correct though...        
        if graphAvailable[neighbor] == None:
           graphAvailable[neighbor] = set()

        Q.append(neighbor)

# Returns if there are no mem leaks otherwise shows the node/var where potential mem leaks are - uses the graphAvailable dictionary
def check_memory_leaks(f):
    leaks_detected = False
    # print(graphAvailable)
    # if len(graphAvailable) == 0:
       
    leakers = graphAvailable[len(graphAvailable)-1]
    if len(leakers) == 0:
       f.write("No memory leaks detected.\n")
       return
    f.write("! ! ! Potential memory leaks detected for varialbes " + str(leakers) + " ! ! !\n")
    
    for var in leakers:
    #    print(freeStatements)
       freeLines = []
       for node in freeStatements[var]:
          freeLines.append(graphData[node][0] + 1)
       leak_info = f"{var} is freed at node(s) {freeStatements[var]} (lines {freeLines}), but may still have living definitions on termination."
       f.write(leak_info)
    # for node in graphAvailable:
    #     if graphAvailable[node]:
    #         leak_info = f"  {node}: {graphAvailable[node]}\n"
    #         # print(leak_info) 
    #         f.write(leak_info)
    #         leaks_detected = True
    # if not leaks_detected:
    #     f.write("No memory leaks detected.\n")

        
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
        if "{" in lines[temp] and "//" not in lines[temp]:
            stack.append("{")
        if "}" in lines[temp] and "//" not in lines[temp]:
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


traverse(0)
# check_memory_leaks()

# OUTPUT TO FILE
if not os.path.exists("output.txt"):
  print("You took my output file! I'll just make another one...")

f = open("output.txt", 'a')
f.truncate(0)
f.write("Vertex to children map: " + str(graph) + "\n")
f.write("Node block ranges: " + str(graphData) + "\n")
f.write("\n")
for i in range(len(graph)):
   f.write("available at " + str(i) + ": " + str(graphAvailable[i]) + "\n")
f.write("\n")
check_memory_leaks(f)
if graphAvailable[len(graph)-1]:
   print("Memory leaks detected in " + str(sys.argv[1]) + " for variable pointers " + str(graphAvailable[len(graph)-1]))

print("View report in 'output.txt' ")
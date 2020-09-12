# Code ryan sent me on 9/1/20
# It is a template to create a network graph from an unknown location
# It does not work yet.


#imports the graph-tools library
from graph_tool.all import *

#opens your file in mode "read"
f = open("weights_node_node.txt","r")
#splits each line into a list of integers
lines = [[int(n) for n in x.split()] for x in f.readlines()]
#closes the file
f.close()

#makes the graph
g = Graph()
#adds enough vertices (the "1 + " is for position 0)
g.add_vertex(1 + max([l[1] for l in lines] + [l[2] for l in lines]))

#makes a "property map" to weight the edges
property_map = g.new_edge_property("int")
#for each line
for line in lines:
    #make a new edge
    g.add_edge(g.vertex(line[1]),g.vertex(line[2]))
    #weight it
    property_map[g.edge(g.vertex(line[1]),g.vertex(line[2]))] = line[0]


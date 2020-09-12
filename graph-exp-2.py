# Scratch code based on file Ryan initially sent me

#   to look into making network plots.
# I found some errors in the original file, and never got it to work.
# I used the network_log_info file to look at the network more comprehensively.

#imports the graph-tools library
# from graph_tool.all import *   # AEH proper import below
from graph_tools import *

#opens your file in mode "read"
# f = open("weights_node_node.txt","r")  # AEH typo in filename
fn = "weight_node_node.txt"
f = open(fn,"r")

# splits each line into a list of integers
# AEH next line fails (likely because of decimals)
# lines = [[int(n) for n in x.split()] for x in f.readlines()]

# AEH, not sure what the expected form of the listed data is
# but here is how to strip out the decimal places in a node and treat it as a single number
lines = [[int(n) for n in x.replace(".", "").split()] for x in f.readlines()]
print(lines)
# There is a later error of AttributeError: 'Graph' object has no attribute 'new_edge_property'
# This may have something to do with the for lines format or some other reason, perhaps incompatible versions?

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


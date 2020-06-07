from graphviz import Digraph


dot = Digraph(comment='The Round Table')
# Add dot A, the label of A is King Arthur
dot.node('A', 'king')


# Add dot B, B's label is Sir Bedevere the Wise
dot.node('B', 'Sir Bedevere the Wise')
#dot.view()

# Add dots L, L label is Sir Lancelot the Brave
dot.node('L', 'Sir Lancelot the Brave')
#dot.view()

#Create a bunch of edges, that is, the edges connecting AB and AL.
dot.edges(['AB', 'AL'])
#dot.view()

# Create an edge between two dots
dot.edge('B', 'L', constraint='false')
#dot.view()

# Get the string form of the DOT source source code
print(dot.source)

# Save source to file and provide Graphviz engine
dot.render('./test_output/round-table.gv', view=True)


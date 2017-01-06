Grapheap 
Its a read optimised graph (inspired by heap) implemented in python and memcache
Every node has list of incoming nodes and outgoing nodes which are sorted by various keys, which you define while creating the grapheap. This makes the read optimised while traversing.
Each node can have n list of key-value pairs but it must have the optimisation keys, keys on which sorting is to be enabled for the Grapheap

Read more about
Graph: https://en.wikipedia.org/wiki/Graph_(abstract_data_type) Heap: https://en.wikipedia.org/wiki/Heap_(data_structure)


How does it work?
Example:

# Create a grapheap
g = Grapheap()

# Add optimisation keys
g.optimise_for(‘bananas’)
g.optimise_for(‘apples’)

# Create Nodes
n1 = g.add_vertex({
	‘name’: ‘Tom’,
	‘bananas’: 5,
	‘apples’: 4
})
n2 = g.add_vertex({
	‘name’: ‘Bob’,
	‘bananas’: 0,
	‘apples’: 8
})
n3 = g.add_vertex({
	‘name’: ‘Harry’,
	‘bananas’: 3,
	‘apples’: 1
})
n4 = g.add_vertex({
	‘name’: ‘Jill’,
	‘bananas’: 8,
	‘apples’: 1
})

# Connect them
g.add_edge(g.entry, n2) # g.entry specifies the entry point for graph
g.add_edge(g.entry, n3)
g.add_edge(n2, n3)
g.add_edge(n3, n4)
g.add_edge(n2, n1)


# Operations

# Filter By
# Get all outgoing nodes (only adjacent) from n2 which have only 1 apples
nodes1 = n2.get_outgoing().filter_by(“apples”, [1]).get_all_nodes() 

# Sort By
# Get all incoming nodes (only adjacent) to n3 sorted by number of bananas they have
nodes2 = n3.get_outgoing().sort_by(“bananas”).get_all_nodes() 

# Get first incoming node to n1 sorted by bananas
node1 = n1.get_incoming().sort_by(‘bananas’).get_node_indexed_at(0)
 

 


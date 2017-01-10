==========
 grapheap
==========

A read optimised graph (DS) library    


Read more about:   

Graph: https://en.wikipedia.org/wiki/Graph_(abstract_data_type)    
Heap: https://en.wikipedia.org/wiki/Heap_(data_structure)   

Installation
------------

To install grapheap, simply:   

```sh
pip install grapheap
```

Or:    

```sh
easy_install grapheap
```

Basic Use
---------

To use grapheap, you must first create an instance of Grapheap,
and construct your nodes and edges:    

```python
# Import Grapheap
from grapheap import Grapheap

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
```


Then you can perform filter, sort operations on any of the node to get the required adjacent nodes from that node:    

```python
# Filter By
# Get all outgoing nodes (only adjacent) from n2 which have only 1 apples
nodes1 = n2.get_outgoing().filter_by(“apples”, [1]).get_all_nodes()

# Sort By
# Get all incoming nodes (only adjacent) to n3 sorted by number of bananas they have
nodes2 = n3.get_outgoing().sort_by(“bananas”).get_all_nodes()

# Get first incoming node to n1 sorted by bananas
node1 = n1.get_incoming().sort_by(‘bananas’).get_node_indexed_at(0)
```


Contributing
------------

Contributions are awesome. You are most welcome to [submit issues](https://github.com/practo/grapheap/issues),
or [fork the repository](https://github.com/practo/grapheap).\

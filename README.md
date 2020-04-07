# graphcache

Python Library to store connected nodes and their properties on cache storage (redis)


Installation
------------

To install `graphcache`, simply:   
```sh
pip install graphcache
```



Development
-----------

* Install [`pyenv`](https://github.com/pyenv/pyenv#installation) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv#installation)
* Run
  ```
  pyenv install 3.7.0 --skip-existing
  pyenv virtualenv 3.7.0 graphcache
  ```
* Update requirements
  ```
  pip install -r requirements.txt
  ```
* Install [`Redis`](https://gist.github.com/tomysmile/1b8a321e7c58499ef9f9441b2faa0aa8)


Basic Use
---------

Ensure you have `redis` service running    
On macos
```sh
redis-server /usr/local/etc/redis.conf
```


To use graphcache, you must first create an instance of GraphCache,
and construct your nodes and edges:    

```python
# Import GraphCache
from graphcache import GraphCache

# default 
# host = localhost
# port = 6379
# db = 0
g = GraphCache(host='localhost', port=6379, db=0)

# Add optimisation keys
g.optimise_for('bananas')
g.optimise_for('apples')

# Create Nodes (need 'apples', 'bananas' keys in all nodes, as they have been added to optimisation_keys)
n1 = g.add_vertex({
    'name': 'Tom',
    'age': 24,
    'bananas': 5,
    'apples': 4
})
n2 = g.add_vertex({
    'name': 'Bob',
    'bananas': 0,
    'apples': 8
})
n3 = g.add_vertex({
    'name': 'Harry',
    'gender': 'Male',
    'bananas': 3,
    'apples': 1
})
n4 = g.add_vertex({
    'name': 'Jill',
    'bananas': 8,
    'apples': 1
})

# Connect them
g.add_edge(g.entry, n2) # g.entry specifies the entry point for graph
g.add_edge(g.entry, n3)
g.add_edge(n2, n3)
g.add_edge(n3, n4)
g.add_edge(n2, n1)
```

![graphcache](http://i.imgur.com/mbWiYet.png)


Then you can perform filter/sort operations on any of the node to get the required adjacent nodes from that node:

```python
# Filter By
# Get all outgoing nodes (only adjacent) from n2 which have only 1 apples
nodes1 = n2.get_outgoing().filter_by('apples', [1]).get_all_nodes()

# Sort By
# Get all incoming nodes (only adjacent) to n3 sorted by number of bananas they have
nodes2 = n3.get_incoming().sort_by('bananas').get_all_nodes()

# Get first incoming node to n1 sorted by bananas
node1 = n1.get_incoming().sort_by('bananas').get_node_indexed_at(0)
```


Also you can perform chained complex operations:

```python
# Filter By, Sort By
# Get all outgoing nodes (only adjacent) from n2 with apples less than 5 and sorted by bananas
nodes1 = n2.get_outgoing().filter_by('apples', 5, "lt").sort_by('bananas').get_all_nodes()

# Sort By, Filter By, Filter By
nodes2 = n3.get_incoming().sort_by('bananas').filter_by('bananas', [1, 5], "in").filter_by('apples', [1]).get_all_nodes()
```


Get the key for the graphcache object
```python
g.cache_key
# graphcache-MZ5SQR
```


Retrieve previously stored graphcache object from redis cache (cache_key = `graphcache-MZ5SQR`)
```python
# using default redis connection
# host = localhost
# port = 6379
# db = 0
g1 = GraphCache(graphcache_ref='graphcache-MZ5SQR')
```
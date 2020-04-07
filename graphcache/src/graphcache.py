from .node import Node
from ..utils.cache import Cache


class GraphCache:
    """
    GraphCache class

    Members
    -------
    optimisation_keys: list
        specifies key (which are mandatory part of node.data)
        for ordering the nodes in incoming/outgoing paths (supports numeric values)
    entry_node: Node object
        Node type object which specifies the starting point for graph
    entry_node_ref: string
        reference to entry node
    cache_key: string
        reference to self ie graphcache
    """

    # Global class variable which maintains unique id for nodes across each graphcache
    # Also used for 'graphcache_node_id' optimisation key for each node
    count_nodes = 0

    def __init__(self, host="localhost", port=6379, db=0, graphcache_ref=None):
        """
        Init method (constructor)

        Parameters
        ----------
        graphcache_ref: string
            reference to graphcache object to load saved graphcache object, if any (optional)
        cache_sync: bool
            sync to cache, default true
        """

        self.cache = Cache(host=host, port=port, db=db)

        # Create new graphcache
        if graphcache_ref is None:
            # default optimisation key
            self.optimisation_keys = ["graphcache_node_id"]
            entry_node = Node(
                self.cache,
                GraphCache.count_nodes,
                {"graphcache_node_type": "entry node"},
                self.optimisation_keys,
            )  # todo: cache
            self.entry_node_ref = entry_node.cache_key

            # Set the object in Cache
            self.cache_key = self.cache.get_random_key()
            self.cache.set(self.cache_key, self)

        # Load existing from cache
        else:
            graphcache = self.cache.get(graphcache_ref)
            self.optimisation_keys = graphcache.optimisation_keys
            self.entry_node_ref = graphcache.entry_node_ref
            self.cache_key = graphcache.cache_key

        self.entry = self.cache.get(self.entry_node_ref)

    def get_node(self, node_ref):
        """
        Get node object from cache, if exists

        Parameters
        ----------
        node_ref: string
            reference to node object

        Returns
        -------
        Node
            Node class type object
        """

        return self.cache.get(node_ref)

    def add_vertex(self, data):
        """
        Add vertex to graphcache
        Creates a new node for given data and adds it to graphcache

        Parameters
        ----------
        data: dict
            dictionary of all data values for node

        Returns
        -------
        Node object
            Node class type object which has all the specified data values
        """

        if self.__validate_node_data(data):
            GraphCache.count_nodes += 1
            node = Node(
                self.cache, GraphCache.count_nodes, data, self.optimisation_keys
            )

            return node

        else:
            # _validate_node_data will return True or raise exception
            pass

    def add_edge(self, vertex1, vertex2):
        """
        Add edge from vertex1 to vertex2
        Outgoing path is added for vertex1 and Incoming path is added to vertex2

        Parameters
        ----------
        vertex1: Node
            Node object
        vertex2: Node
            Node object
        """

        vertex1.add_outgoing_node(vertex2)
        vertex2.add_incoming_node(vertex1)

    def optimise_for(self, key):
        """
        Append a new optimisation key to graphcache and all its nodes
        Currently updates optimisation keys in entry node only. TODO: update in all nodes

        Parameters
        ----------
        key: string
            data field key, present in all nodes
        """

        self.optimisation_keys.append(key)
        self.entry.incoming_node_refs_list.add_optimisation_key(key)
        self.entry.outgoing_node_refs_list.add_optimisation_key(key)
        if key not in self.entry.data:
            self.entry.update_data(key, 0)

    def __validate_node_data(self, data):
        """
        Validates if all optimisation keys (specified for graphcache) exist in data

        Parameters
        ----------
        data: dict
            dictionary of all key-value pairs

        Returns
        -------
        bool
            boolean value describing if node data is valid
        """

        # skipping check of 'graphcache_node_id' optimisation key
        if all(key in data for key in self.optimisation_keys[1:]):
            return True

        else:
            missing_keys = [x for x in self.optimisation_keys[1:] if x not in data]
            raise ValueError(
                "GraphCache Error: "
                + str(missing_keys)
                + " optimisation keys missing in data"
            )

    def traverse(self, node=None):
        """
        Traverse each node
        """

        cur_node = self.entry
        reached = []
        to_traverse = [self.entry]
        if node is not None:
            to_traverse = [node]

        while to_traverse:
            cur_node = to_traverse.pop()
            if cur_node.cache_key in reached:
                continue
            cur_node.print_data()
            reached.append(cur_node.cache_key)
            to_traverse.extend(cur_node.get_outgoing().get_all_nodes())

    def __repr__(self):
        return "<GraphCache %r>" % self.cache_key

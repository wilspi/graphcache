from node import Node
from .. utils.cache import Cache



"""
Grapheap class

:var optimisation_keys: specifies key (which are mandatory part of node.data)
		for ordering the nodes in incoming/outgoing paths (supports numeric values)
:var entry: Node type object which specifies the starting point for graph
:var entry_node_ref: reference to entry node
:var cache_key: reference to self grapheap

"""
class Grapheap:

	# Global class variable which maintains unique id for nodes across each graph
	count_nodes = 0

	def __init__(self, grapheap_ref=None, cache_sync=True):
		"""
		Init method (constructor)

		:param grapheap_ref: string
		:param cache_sync: bool
		"""

		# Create new grapheap
		if grapheap_ref is None:
			self.optimisation_keys = ['grapheap_node_id'] # atleast one key required
			entry_node = Node(Grapheap.count_nodes,
				{"grapheap_node_type": "entry node"},
				self.optimisation_keys) # todo: cache
			self.entry_node_ref = entry_node.cache_key

			if cache_sync:
				self.cache_key = Cache.get_random_key()
				Cache.set(self.cache_key, self)

		# Load existing from cache
		else:
			grapheap = Cache.get(grapheap_ref)
			self.optimisation_keys = grapheap.optimisation_keys
			self.entry_node_ref = grapheap.entry_node_ref
			self.cache_key = grapheap.cache_key

		self.entry = Cache.get(self.entry_node_ref)


	def get_node(self, node_ref):
		"""
		Get node from cache, if exists

		:param node_ref: string

		:return node class type object
		"""

		return Cache.get(node_ref)


	def add_vertex(self, data):
		"""
		Add vertex to graph

		:param data: dict

		:return node class type object
		"""

		if self.__validate_node_data(data):
			Grapheap.count_nodes += 1
			node = Node(
				Grapheap.count_nodes,
				data,
				self.optimisation_keys)

			return node

		else:
			# _validate_node_data will return True or raise exception
			pass


	def add_edge(self, vertex1, vertex2):
		"""
		Edge from vertex1 to vertex2

		:param vertex1: node class type object
		:param vertex2: node class type object
		"""

		vertex1.add_outgoing_node(vertex2)
		vertex2.add_incoming_node(vertex1)


	def optimise_for(self, key):
		"""
		Append optimisation keys to graph for all its nodes

		:param key: string
		"""

		self.optimisation_keys.append(key)
		self.entry.incoming_node_refs_list.add_optimisation_key(key)
		self.entry.outgoing_node_refs_list.add_optimisation_key(key)
		if key not in self.entry.data:
			self.entry.update_data(key, 0)
		# todo: update in all nodes


	def traverse(self, node=None):
		"""
		Traverse each node (once only)
		"""

		cur_node = self.entry
		reached = []
		to_traverse = [self.entry]
		if node is not None:
			to_traverse = [node]

		while to_traverse:
			cur_node = to_traverse.pop()
			if (cur_node.cache_key in reached):
				continue
			cur_node.print_data()
			reached.append(cur_node.cache_key)
			to_traverse.extend(cur_node.get_outgoing().get_all_nodes())


	def __validate_node_data(self, data):
		"""
		Validates if all optimisation keys exist in data

		:param data: dict

		:return bool
		"""

		# skipping check of 'grapheap_node_id' optimisation key
		if all(key in data for key in self.optimisation_keys[1:]):
			return True

		else:
			missing_keys = [x for x in self.optimisation_keys[1:] if x not in data]
			raise ValueError("Grapheap Error: " + str(missing_keys) + " optimisation keys missing in data")


	def __repr__(self):
		return '<Grapheap %r>' % self.entry.cache_key



from model.node import Node

"""
Grapheap class

:var optimisation_keys: specifies key (which are mandatory part of node.data)
		for ordering the nodes in incoming/outgoing paths (supports integer values only)
:var entry: Node type object which specifies the starting point for graph

"""
class Grapheap:

	# Global class variable which maintains unique id for nodes across each graph
	count_nodes = 0

	def __init__(self):
		"""
		Init method (constructor)
		"""

		self.optimisation_keys = ['node_id'] # atleast one key required
		self.entry = Node(
			Grapheap.count_nodes,
			{"type": "entry node"},
			self.optimisation_keys)


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
			self.entry.append_data(key, 0)
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

		# skipping check of 'node_id' optimisation key
		if all(key in data for key in self.optimisation_keys[1:]):
			return True

		else:
			missing_keys = [x for x in self.optimisation_keys[1:] if x not in data]
			raise ValueError("Grapheap Error: " + str(missing_keys) + " optimisation keys missing in data")


	def __repr__(self):
		return '<Grapheap %r>' % self.entry.cache_key



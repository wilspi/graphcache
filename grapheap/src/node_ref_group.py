
from bisect import bisect_right
from .. utils.cache import Cache

"""
NodeRefGroup class

:var _ref_lists: dictionary with keys as optimisation key and
		value as references to nodes sorted by that optimisation key
:var _temp_list: temporary node reference list for internal calculation

"""
class NodeRefGroup:

	def __init__(self, optimisation_keys):
		"""
		Init method (constructor)

		:param optimisation_keys: list of strings
		"""

		self._ref_lists = {}
		for key in optimisation_keys:
			self._ref_lists[key] = []
		self._temp_list = None


	def add_optimisation_key(self, key):
		"""
		Add optimisation key to _ref_lists (for optimised search/sort on that key)

		:param key: string
		"""

		self._ref_lists[key] = []


	def remove_node_ref(self, node):
		"""
		Remove node reference from _ref_lists in all optimisation keys

		"""

		optimisation_keys = list(self._ref_lists.keys())
		for key in optimisation_keys:
			if node.cache_key in self._ref_lists[key]:
				self._ref_lists[key].remove(node.cache_key)


	def add_node_ref(self, node):
		"""
		Add new node reference in _ref_lists in all optimisation keys

		:param node: Node class type object
		"""

		optimisation_keys = list(self._ref_lists.keys())
		for key in optimisation_keys:
			self.__add_node_at_appr_pos(key, node)


	def sort_by(self, key):
		"""
		Sort by (any specified optimisation key)

		:param key: string

		:return NodeRefGroup class type object
		"""

		if self._temp_list is None:
			if key in self._ref_lists:
				self._temp_list = self._ref_lists[key]
			else:
				self._temp_list = []

		else:
			# list of all filtered nodes
			self._temp_list = [node_ref for node_ref in self._ref_lists[key] if node_ref in self._temp_list]

		return self


	def filter_by(self, key, values):
		"""
		Filter nodes in the list
		Returns nodes which has node.data[key] in given list of values

		:param key: string
		:param values: list of values (value supports integer only)

		:return NodeRefGroup class type object
		"""

		if self._temp_list is None:
			optimisation_keys = list(self._ref_lists.keys())
			self._temp_list = self._ref_lists[optimisation_keys[0]]

		# list of all filtered nodes
		self._temp_list = [node.cache_key for node in self.get_all_nodes() if node.data[key] in values]

		return self


	def get_all_nodes(self):
		"""
		Get all nodes (if method chaining is done, it will return nodes for previous operations)

		:param index: int

		:return list of nodes
		"""

		if self._temp_list is None:
			optimisation_keys = list(self._ref_lists.keys())
			self._temp_list = self._ref_lists[optimisation_keys[0]]

		# expired node ref keys still exist in _ref_lists
		nodes = filter(None, map(lambda x: Cache.get(x, True), self._temp_list))
		self._temp_list = None # reset _temp_list

		return list(nodes)


	def get_node_indexed_at(self, index):
		"""
		Get node at given index

		:param index: int

		:return Node class type object
		"""

		if self._temp_list is None:
			optimisation_keys = list(self._ref_lists.keys())
			self._temp_list = self._ref_lists[optimisation_keys[0]]

		if len(self._temp_list) > index:
			node = Cache.get(self._temp_list[index])
			self._temp_list = None # reset _temp_list

			return node

		else:
			raise Exception("Index Error: " + index + " is not found")


	def __add_node_at_appr_pos(self, key, node_to_add):
		"""
		Adds ref of node at appropriate index in sorted _ref_lists for given optimisation key
		(private)

		:param key: string
		:param node_to_add: Node class type object
		"""

		nodes = self.sort_by(key).get_all_nodes()

		if nodes:
			# list of all node values of given key
			list_of_values = list(filter(None, ((yield node.data[key]) for node in nodes)))

			# get appropriate position and insert
			pos = bisect_right(list_of_values, node_to_add.data[key])
			self._ref_lists[key].insert(pos, node_to_add.cache_key)

		else:
			self._ref_lists[key].append(node_to_add.cache_key)




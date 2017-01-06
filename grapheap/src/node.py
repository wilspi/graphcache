
from operator import attrgetter
from datetime import datetime
import math

from util.cache import Cache
from model.node_ref_group import NodeRefGroup



"""
Node class

:var cache_key: reference to self node in cache
:var data: dictionary to accomodate data with any number of key-value pairs
:var incoming_node_refs_list: NodeRefGroup class type object
:var outgoing_node_refs_list: NodeRefGroup class type object
:var ttl: TTL
:var ttl_set_at: time at which ttl is set

"""
class Node:

	def __init__(self, id, data=None, optimisation_keys=[], ttl=None, cache_sync=True):
		"""
		Init method (constructor)

		:param id: int
		:param data: dict
		:param optimisation_keys: list
		:param ttl: int
		:param cache_sync: bool
		"""

		if data is None:
			self.data = {}
		else:
			self.data = data
		self.data['node_id'] = id
		self.incoming_node_refs_list = NodeRefGroup(optimisation_keys)
		self.outgoing_node_refs_list = NodeRefGroup(optimisation_keys)
		self.ttl_set_at = datetime.now()
		self.ttl = ttl
		if cache_sync:
			self.cache_key = Cache.get_random_key()
			Cache.set(self.cache_key, self, self.ttl)


	def append_data(self, key, value, cache_sync=True):
		"""
		Append more key-value pair into node.data

		:param key: string
		:param value: any type
		:param cache_sync: bool
		"""

		self.data[key] = value
		self.__update_in_cache(cache_sync) # update in cache


	def get_incoming(self):
		"""
		Get NodeRefGroup class object for incoming nodes

		:return NodeRefGroup class type object
		"""

		return self.incoming_node_refs_list



	def add_incoming_node(self, node, cache_sync=True):
		"""
		Adds incoming node to self NodeRefGroup for incoming nodes

		:param node: Node class type object
		:param cache_sync: bool
		"""

		self.incoming_node_refs_list.add_node_ref(node)
		self.__update_in_cache(cache_sync) # update in cache


	def get_outgoing(self):
		"""
		Get NodeRefGroup class object for outgoing nodes

		:return NodeRefGroup class type object
		"""

		return self.outgoing_node_refs_list


	def add_outgoing_node(self, node, cache_sync=True):
		"""
		Adds outgoing node to self NodeRefGroup for outgoing nodes

		:param node: Node class type object
		:param cache_sync: bool
		"""

		self.outgoing_node_refs_list.add_node_ref(node)
		self.__update_in_cache(cache_sync) # update in cache


	def set_ttl(self, ttl):
		"""
		Sets ttl for self node

		:param ttl: int
		"""

		self.ttl = ttl
		self.ttl_set_at = datetime.now()
		Cache.set(self.cache_key, self, self.ttl)


	def get_ttl(self):
		"""
		Get self node ttl

		:return int or None
		"""

		if self.ttl is None:
			return None;

		else:
			elapsed_time = datetime.now() - self.ttl_set_at
			modified_ttl = self.ttl - math.ceil(elapsed_time.total_seconds())
			if modified_ttl > 0:
				return modified_ttl
			else:
				return 0


	def __update_in_cache(self, cache_sync=True):
		"""
		Update self node in cache
		(private)

		:param cache_sync: bool
		"""

		if self.cache_key and cache_sync:
			Cache.set(self.cache_key, self, self.get_ttl())


	def print_data(self):
		"""
		Prints self node
		"""

		print("## " + self.cache_key)
		print("###########")
		print("OUTGOING (sorted by ID): " + str(self.outgoing_node_refs_list.get_all_nodes()))
		print("INCOMING (sorted by ID): " + str(self.incoming_node_refs_list.get_all_nodes()))
		print("DATA: ")
		for k in self.data:
			print(k + ": " + str(self.data[k]))
		print()


	def __repr__(self):
		return '<Node %r>' % self.cache_key





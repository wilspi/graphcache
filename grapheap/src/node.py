
from datetime import datetime
import math

from .. utils.cache import Cache
from .node_ref_group import NodeRefGroup


"""
Node class

Members
-------
cache_key: string
    reference to self node in cache
data: dict
    specifies node's data (key-value pairs)
incoming_node_refs_list: NodeRefGroup object
    NodeRefGroup class type object which specifies all incoming nodes to self node
outgoing_node_refs_list: NodeRefGroup object
    NodeRefGroup class type object which specifies all outgoing nodes to self node
ttl: integer
    TTL (time to live) after which node will not be accessible
ttl_set_at: time
    time at which ttl is set
"""


class Node:

    def __init__(self, id, data=None, optimisation_keys=[], ttl=None, cache_sync=True):
        """
        Init method (constructor)

        Parameters
        ----------
        id: int
            id defined by grapheap's count_nodes
        data: dict
            data dictionary for self node
        optimisation_keys: list
            list of all optimisation keys
        ttl: int
            TTL (time to live) after which node will not be accessible
        cache_sync: bool
            sync to cache, default true
        """

        if data is None:
            self.data = {}
        else:
            self.data = data
        self.data['grapheap_node_id'] = id
        self.incoming_node_refs_list = NodeRefGroup(optimisation_keys)
        self.outgoing_node_refs_list = NodeRefGroup(optimisation_keys)

        if ttl or cache_sync:
            self.ttl_set_at = datetime.now()
            self.ttl = ttl
            self.cache_key = Cache.get_random_key()
            Cache.set(self.cache_key, self, self.ttl)

    def update_data(self, key, value, cache_sync=True):
        """
        Update existing or append more key-value pair into node.data

        Parameters
        ----------
        key: string
            attribute name to add
        value: any type
            value of that attribute
        cache_sync: bool
            sync to cache, default true
        """

        self.data[key] = value
        self.__update_in_cache(cache_sync)  # updates in cache
        self.__refresh()  # updates order when value changes

    def get_incoming(self):
        """
        Get NodeRefGroup class object for incoming nodes

        Returns
        -------
        NodeRefGroup object
            NodeRefGroup class type object which specifies all the incoming nodes
        """

        return self.incoming_node_refs_list

    def add_incoming_node(self, node, cache_sync=True):
        """
        Adds incoming node to self NodeRefGroup for incoming nodes

        Parameters
        ----------
        node: Node object
            Node class type object to add to self incoming nodes
        cache_sync: bool
            sync to cache
        """

        self.get_incoming().add_node_ref(node)
        self.__update_in_cache(cache_sync)  # updates in cache

    def remove_incoming_node(self, node, cache_sync=True):
        """
        Removes incoming node from self NodeRefGroup for incoming nodes

        Parameters
        ----------
        node: Node object
            Node class type object to remove from self incoming nodes
        cache_sync: bool
            sync to cache
        """

        self.get_incoming().remove_node_ref(node)
        self.__update_in_cache(cache_sync)  # updates in cache

    def get_outgoing(self):
        """
        Get NodeRefGroup class object for outgoing nodes

        Returns
        -------
        NodeRefGroup object
            NodeRefGroup class type object which specifies all the outgoing nodes
        """

        return self.outgoing_node_refs_list

    def add_outgoing_node(self, node, cache_sync=True):
        """
        Adds outgoing node to self NodeRefGroup for outgoing nodes

        Parameters
        ----------
        node: Node object
            Node class type object to add to self outgoing nodes
        cache_sync: bool
            sync to cache
        """

        self.get_outgoing().add_node_ref(node)
        self.__update_in_cache(cache_sync)  # updates in cache

    def remove_outgoing_node(self, node, cache_sync=True):
        """
        Removes outgoing node from self NodeRefGroup for outgoing nodes

        Parameters
        ----------
        node: Node object
            Node class type object to remove from self outgoing nodes
        cache_sync: bool
            sync to cache
        """

        self.get_outgoing().remove_node_ref(node)
        self.__update_in_cache(cache_sync)  # updates in cache

    def set_ttl(self, ttl):
        """
        Sets ttl for self node

        Parameters
        ----------
        ttl: int
            TTL (time to live) after which node will not be accessible
        """

        self.ttl = ttl
        self.ttl_set_at = datetime.now()
        Cache.set(self.cache_key, self, self.ttl)

    def get_ttl(self):
        """
        Get self node ttl

        Returns
        -------
        int or None
            seconds from current time after which node will die
            return None, if ttl is not specified
        """

        if self.ttl is None:
            return None

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
        (private method)

        Parameters
        ----------
        cache_sync: bool
            sync to cache
        """

        if self.cache_key and cache_sync:
            Cache.set(self.cache_key, self, self.get_ttl())

    def __refresh(self, cache_sync=True):
        """
        Updates order of self node in all self incoming nodes' outgoing paths, according to the current data value
        (private method)

        Parameters
        ----------
        cache_sync: bool
            sync to cache
        """

        nodes = self.get_incoming().get_all_nodes()
        for node in nodes:
            node.remove_outgoing_node(self)
            node.add_outgoing_node(self)  # add at appropriate place

        self.__update_in_cache(cache_sync)  # updates in cache

    def print_data(self):
        """
        Prints self node
        """

        print("## " + self.cache_key)
        print("###########")
        print("OUTGOING (sorted by ID): " +
              str(self.outgoing_node_refs_list.get_all_nodes()))
        print("INCOMING (sorted by ID): " +
              str(self.incoming_node_refs_list.get_all_nodes()))
        print("DATA: ")
        for k in self.data:
            print(k + ": " + str(self.data[k]))
        print()

    def __repr__(self):
        return '<Node %r>' % self.cache_key

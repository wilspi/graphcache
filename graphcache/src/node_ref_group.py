import numbers
from bisect import bisect_right
from ..utils.cache import Cache


class NodeRefGroup:
    """
    NodeRefGroup class

    Members
    -------
    _ref_lists: dict
        dictionary with keys as optimisation key and value as references to nodes sorted by that optimisation key
    _temp_list: list
        temporary node reference list for storing operations output (for function chaining)
    """

    def __init__(self, optimisation_keys):
        """
        Init method (constructor)

        Parameters
        ----------
        optimisation_keys: list
            list of all optimisation keys
        """

        self._ref_lists = {}
        for key in optimisation_keys:
            self._ref_lists[key] = []
        self._temp_list = None

    def add_optimisation_key(self, key):
        """
        Add optimisation key to _ref_lists (for optimised search/sort on that key)

        Parameters
        ----------
        key: string
            add a new optimisation key to self object
        """

        self._ref_lists[key] = []

    def remove_node_ref(self, node):
        """
        Remove node reference from _ref_lists in all optimisation keys

        Parameters
        ----------
        node: Node object
            Node class type object to remove from lists of every optimisation key

        """

        optimisation_keys = list(self._ref_lists.keys())
        for key in optimisation_keys:
            if node.cache_key in self._ref_lists[key]:
                self._ref_lists[key].remove(node.cache_key)

    def add_node_ref(self, node):
        """
        Add new node reference in _ref_lists in all optimisation keys

        Parameters
        ----------
        node: Node object
            Node class type object to add to all lists of all optimisation key
        """

        optimisation_keys = list(self._ref_lists.keys())
        for key in optimisation_keys:
            self.__add_node_at_appr_pos(key, node)

    def sort_by(self, key):
        """
        Sort by (any specified optimisation key)

        Parameters
        ----------
        key: string
            one of the optimisation key

        Returns
        -------
        NodeRefGroup object
            self object with modified _temp_list, which stores the output
        """

        if self._temp_list is None:
            if key in self._ref_lists:
                self._temp_list = self._ref_lists[key]
            else:
                self._temp_list = []

        else:
            # list of all filtered nodes
            self._temp_list = [
                node_ref
                for node_ref in self._ref_lists[key]
                if node_ref in self._temp_list
            ]

        return self

    def filter_by(self, key, input1, operator="eq"):
        """
        Filter nodes in the list
        Returns nodes which has node.data[key] based on operator and respective values

        Parameters
        ----------
        key: string
            any of the keys in node.data
        input1: list
            list of values (value supports numerical values only)
        operator: string
            defines what type of filter is being applied (optional)
            example: "gt" defines greater than

        Returns
        -------
        NodeRefGroup object
            self object with modified _temp_list, which stores the output
        """

        if self._temp_list is None:
            optimisation_keys = list(self._ref_lists.keys())
            self._temp_list = self._ref_lists[optimisation_keys[0]]

        # less than
        if operator == "lt":
            assert isinstance(input1, numbers.Real), (
                "Error: numerical value required, " + str(input1) + " given"
            )

            self._temp_list = [
                node.cache_key
                for node in self.get_all_nodes()
                if node.data[key] < input1
            ]

        # less than or equal to
        if operator == "le":
            assert isinstance(input1, numbers.Real), (
                "Error: numerical value required, " + str(input1) + " given"
            )

            self._temp_list = [
                node.cache_key
                for node in self.get_all_nodes()
                if node.data[key] <= input1
            ]

        # greater than
        elif operator == "gt":
            assert isinstance(input1, numbers.Real), (
                "Error: numerical value required, " + str(input1) + " given"
            )

            self._temp_list = [
                node.cache_key
                for node in self.get_all_nodes()
                if node.data[key] > input1
            ]

        # greater than or equal to
        elif operator == "ge":
            assert isinstance(input1, numbers.Real), (
                "Error: numerical value required, " + str(input1) + " given"
            )

            self._temp_list = [
                node.cache_key
                for node in self.get_all_nodes()
                if node.data[key] >= input1
            ]

        # not equal to
        elif operator == "ne":
            assert isinstance(input1, (list)), (
                "Error: value must be list of numbers, " + str(input1) + " given"
            )

            self._temp_list = [
                node.cache_key
                for node in self.get_all_nodes()
                if node.data[key] not in input1
            ]

        # equal to
        elif operator == "eq":
            assert isinstance(input1, (list)), (
                "Error: value must be list of numbers, " + str(input1) + " given"
            )

            self._temp_list = [
                node.cache_key
                for node in self.get_all_nodes()
                if node.data[key] in input1
            ]

        # between range
        elif operator == "range":
            assert isinstance(input1, (list)) and len(input1) == 2, (
                "Error: input must be a list with two values defining the range, "
                + str(input1)
                + " given"
            )

            self._temp_list = [
                node.cache_key
                for node in self.get_all_nodes()
                if ((node.data[key] >= input1[0]) and (node.data[key] <= input1[1]))
            ]

        # in array list
        elif operator == "in":
            assert isinstance(input1, (list)), (
                "Error: input must be a list, " + str(input1) + " given"
            )

            self._temp_list = [
                node.cache_key
                for node in self.get_all_nodes()
                if (node.data[key] in input1)
            ]

        else:
            raise Exception(
                "Error: operator does not match, " + str(operator) + " given"
            )

        return self

    def get_all_nodes(self):
        """
        Get all nodes (if method chaining is done, it will return nodes for previous operations)

        Returns
        -------
        list
            list of Node objects (if method chaining is done, it will return nodes for previous operations)
            example:
            node.get_outgoing().filter_by("bananas", [10]).get_all_nodes()
            will give list of outgoing nodes with node.data['bananas'] equal to 10
        """

        if self._temp_list is None:
            optimisation_keys = list(self._ref_lists.keys())
            self._temp_list = self._ref_lists[optimisation_keys[0]]

        # expired node ref keys still exist in _ref_lists
        nodes = filter(None, map(lambda x: Cache.get(x, True), self._temp_list))
        self._temp_list = None  # reset _temp_list

        return list(nodes)

    def get_node_indexed_at(self, index):
        """
        Get node at given index (if method chaining is done, it will return node at index in list from previous operations)

        Parameters
        ----------
        index: int
            index of required node

        Returns
        -------
        Node object
            Node class type object at specified index
            example:
            node.get_outgoing().filter_by("bananas", [10]).get_node_indexed_at(3)
            will give node at index 3 from list of outgoing nodes with node.data['bananas'] equal to 10
        """

        if self._temp_list is None:
            optimisation_keys = list(self._ref_lists.keys())
            self._temp_list = self._ref_lists[optimisation_keys[0]]

        if len(self._temp_list) > index:
            node = Cache.get(self._temp_list[index])
            self._temp_list = None  # reset _temp_list

            return node

        else:
            raise Exception("Index Error: " + index + " is not found")

    def __add_node_at_appr_pos(self, key, node_to_add):
        """
        Adds reference of node (ie node.cache_key) at appropriate index in sorted _ref_lists for given optimisation key
        (private method)

        Parameters
        ----------
        key: string
            optimisation key which specifies the list to add into
        node_to_add: Node object
            Node class type object to add in 'key' optimisation key's list of nodes
        """

        nodes = self.sort_by(key).get_all_nodes()

        if nodes:
            # list of all node values of given key
            list_of_values = list(
                filter(None, ((yield node.data[key]) for node in nodes))
            )

            # get appropriate position and insert
            pos = bisect_right(list_of_values, node_to_add.data[key])
            self._ref_lists[key].insert(pos, node_to_add.cache_key)

        else:
            self._ref_lists[key].append(node_to_add.cache_key)

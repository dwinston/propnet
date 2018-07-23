"""
Module containing classes and methods for Material functionality in propnet code.
"""

from itertools import chain

from typing import *

from propnet.core.symbols import Symbol
from propnet.core.quantity import Quantity, weighted_mean


class Material(object):
    """
    Class containing methods for creating and interacting with Material objects.

    Under the Propnet infrastructure, Materials are the medium through which properties are
    communicated. While Model and Symbol nodes create a web of interconnected properties,
    Materials, as collections of Quantity nodes, provide concrete numbers to those properties.

    At runtime, a Material can be constructed and evaluated under a Graph instance, allowing
    for derivation of additional Quantity objects through the property web.

    A unique hashcode is stored with each Material upon instantiation. This is used to
    differentiate between different materials at runtime.

    Attributes:
        _symbol_to_quantity (dict<Symbol, set<Quantity>>): data structure mapping Symbols to a list of corresponding
                                                           Quantity objects of that type.

    """
    def __init__(self):
        """
        Creates a Material instance, instantiating a trivial graph of one node.
        """
        self._symbol_to_quantity = DefaultDict(set)

    def add_quantity(self, quantity):
        """
        Adds a property to this material's property graph.
        If the material has been bound to a Graph instance, correctly adds the property to that instance.
        Mutates this graph instance variable and its parent.
        Args:
            quantity (Quantity): property to be bound to the material.
        Returns:
            void
        """
        self._symbol_to_quantity[quantity.symbol].add(quantity)

    def remove_quantity(self, quantity):
        """
        Removes the Quantity object attached to this Material.

        Args:
            quantity (Quantity): Quantity object reference indicating with property is to be
            removed from this Material.

        Returns:
            None
        """
        if quantity.symbol not in self._symbol_to_quantity:
            raise Exception("Attempting to remove quantity not present in the material.")
        self._symbol_to_quantity[quantity.symbol].remove(quantity)

    def remove_symbol(self, symbol):
        """
        Removes all Quantity Nodes attached to this Material of type symbol.

        Args:
            symbol (Symbol): object indicating which property type
                is to be removed from this material.

        Returns:
            None
        """
        if symbol not in self._symbol_to_quantity:
            raise Exception("Attempting to remove Symbol not present in the material.")
        del self._symbol_to_quantity[symbol]

    def get_symbols(self):
        """
        Obtains all Symbol objects bound to this Material.

        Returns:
            (set<Symbol>) set containing all symbols bound to this Material.
        """
        return set(self._symbol_to_quantity.keys())

    def get_quantities(self):
        """
        Method obtains all Quantity objects bound to this Material.
        Returns:
            (list<Quantity>) list of all Quantity objects bound to this Material.
        """
        return list(chain.from_iterable(self._symbol_to_quantity.values()))

    def get_aggregated_quantities(self):
        """
        Return mean values for all quantities for each symbol.

        Args:
            func (callable): function with which to aggregate quantities

        Returns:
            (dict<Symbol, weighted_mean) mapping from a Symbol to
            an aggregated statistic.
        """
        # TODO: proper weighting system, and more flexibility in object handling
        aggregated = {}
        for symbol, quantities in self._symbol_to_quantity.items():
            if not symbol.category =='object':
                aggregated[symbol] = weighted_mean(list(quantities))
        return aggregated

    def __str__(self):
        QUANTITY_LENGTH_CAP = 35
        building = []
        building += ["Material: " + str(hex(id(self))), ""]
        for symbol in self._symbol_to_quantity.keys():
            building += ["\t" + symbol.name]
            for quantity in self._symbol_to_quantity[symbol]:
                qs = str(quantity)
                if "\n" in qs or len(qs) > QUANTITY_LENGTH_CAP:
                    qs = "..."
                building += ["\t\t" + qs]
            building += [""]
        return "\n".join(building)

    def __eq__(self, other):
        if not isinstance(other, Material):
            return False
        if len(self._symbol_to_quantity) != len(other._symbol_to_quantity):
            return False
        for symbol in self._symbol_to_quantity.keys():
            if symbol not in other._symbol_to_quantity.keys():
                return False
            if len(self._symbol_to_quantity[symbol]) != len(other._symbol_to_quantity[symbol]):
                return False
            for quantity in self._symbol_to_quantity[symbol]:
                if quantity not in other._symbol_to_quantity[symbol]:
                    return False
        return True


class SuperMaterial(Material):
    """
    Class representing a material composed of one or more sub-materials.

    Useful for representing materials properties that arise from multiple materials
    (ie. contact voltage in metals)

    Attributes:
        _symbol_to_quantity (dict<Symbol, set<Quantity>>): data-structure storing all properties / descriptors
                                                           that arise from the joining of multiple materials
        materials (list<Material>): set of materials contained in the Composite
    """
    def __init__(self, materials_list):
        """
        Creates a Composite Material instance.
        Args:
            materials_list (list<Material>): list of materials contained in the Composite
        """
        Material.__init__(self)
        self.materials = materials_list

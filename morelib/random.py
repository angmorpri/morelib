#!python3
#-*- coding: utf-8 -*-
"""
    MoreLib Random Module

    This module includes the random-related features.

    Functions:
        biased_choice() -> Item: Given a list of elements and their associated
            weights, it randomly chooses one of them, having higher weights
            more chance to be chosen.

    Classes:
        RandomList(): Offers some random-related operations for lists of objets,
            such as shuffling, biased choosing, aging, etc.
        RandomGenerator(): Variant of the RandomList that allows to use the class
            as an iterator. You can also build this using the RandomList method
            `get_generator()`.

    Exceptions:
        NoItemsLeftException: Raises when a RandomList runs out of elements to
            returns as result of choosing.


    Created:        17 Sep 2020
    Last modified:  21 Sep 2020
        - Ready for version 0.1.0
        - Changed the repr() representation.

"""
from collections.abc import Generator
from itertools import zip_longest
import random


#
# Defines
#
DEFAULT_AGING_COEF = 2
NO_ITEMS_LEFT_MSG = "RandomList has no more items to choose from " \
                    "(perhaps you need to reset the repeated cache?)"


#
# Functions
#
def biased_choice (*args, **kwargs):
    """Returns a random choice from the given iterable, where each item has
    a specific probability (weight) to be chosen.

    You can provide as item list:
     - A list of tuples, where its first element must be the object, and the
     second, its weight.
     - Two lists, the first with elements, the second with weights. If
     the second list is shorter, remaining elements will have a 0 weight.
     If it is larger, remaining values will be ignored.
     - A list and a `key` keyword with a function that will be applied to each
     element of the list in order to generate its weight.

    It will return the randomly chosen element, without its weight.

    """
    _rl = RandomList(*args, **kwargs)
    return _rl.choice()[-1]


#
# Classes
#
class NoItemsLeftException (Exception):
    """Custom exception for when there are no items left to choose"""
    pass


class RandomList (object):
    """Class for random-related operations with lists of elements.

    This class provides a bunch of functions meant to handle groups of elements,
    such as biased choices, normalization, random choice with elimination, etc.

    Public attributes:
        items (list[tuple]): List with all the items with their weights.
        key (callable): Key applied to an item to get its weight.

    Public methods:
        shuffle() -> None: Randomly rearranges the items in the list.
        choice() -> list[Item]: Randomly chooses one of more items from the list,
            taking into account their weights as probabilities of be chosen.
        uchoice() -> list[Item]: Randomly chooses one of more items from the list,
            without taking into account their weights.

        uniform() -> None: Gives all the elements in the list the same weight.
        normalize() -> None: Remaps the weights in the items so they are between
            0 and 1.
        age() -> None: Changes the weights of the items so the ones that were not
            chosen the last time have a bigger chance to be chosen the next time.

        append() -> None: Appends a new element to the list, with many forms to
            give it its weight.
        remove() -> None: Removes the first item whichs element matches the
            given.
        pop() -> Item: Removes the item in the given position and returns it.
        clear() -> None: Removes all the items in the list.
        clear_all() -> None: Removes all the items, keys and extra features from
            the object.
        index() -> int: Given an element, returns the index of its first occurence
            in the list.
        count() -> int: Counts the times the given element appears in the list.
        sort() -> None: Sorts the elements in the list, treated as tuples.
        copy() -> list[tuple]: Returns a copy of the current list.
        elems() -> list[Item]: Returns the list with all the elements in the list.
        weights() -> list[float]: Returns a list with all the weights in the list.
        weight_of() -> float: Given an element in the list, returns its weight.
        at() -> Item: Returns the element in the position requested.

        configure() -> None: Sets some parameters and adjustes some behaviors.
        reset_repeated() -> None: Resets the repeated cache.
        reset_aging() -> None: Resets the weights of the items before aging.

        get_generator() -> RandomGenerator: Builds and returns a RandomGenerator
            based on this RandomList.

    """
    def __init__ (self, *args, **kwargs):
        """Main constructor.

        You can provide as item list:
         - A list of tuples, where its first element must be the object, and the
         second, its weight.
         - Two lists, the first with elements, the second with weights. If
         the second list is shorter, remaining elements will have a 0 weight.
         If it is larger, remaining values will be stored, and given to possible
         future values appended to the list.
         - A list and a `key` keyword with a function that will be applied to
         each element of the list in order to generate its weight. If this
         keyword is used but also the previous method, it won't apply, but can
         be used for possible future values appended.
         - A sole list, in which case, all elements will have the same weights.

        Also, you can use some of the following keywords to configure the way
        the object behaves. You can always change them later using the method
        `configure` with the same parameters:
            - no_repeat (bool): If set to True, elements that appear once, won't
                be chosen anymore. When no more elements can be returned, it
                will start throwing a NoElementsLeft exception. You can reset
                it by using the `reset_repeated` method.
            - always_age (bool): If set to True, always after generating an
                element from the list, it will automatically age. You can reset
                the weights using `reset_aging`.
            - aging_coef (float): Changes the aging coeficent, by default, 2.

        """
        self.items = list()             # List of [item, weight].
        self.key = kwargs.get('key')    # Possible weights key generator.

        self._stored_weights = (_ for _ in ())
        self._last = list()             # List of last chosen items.
        self._no_repeat = False
        self._repeated_cache = list()
        self._always_age = False
        self._aging_coef = DEFAULT_AGING_COEF           # Aging coeficient.
        self._backup = None                             # For aging backup.

        # Check arguments and build
        if len(args) == 2:
            # List of items AND list of weights.
            items = args[0]
            weights = [float(n) for n in args[1][:len(items)]]
            self._stored_weights = (float(w) for w in args[1][len(items):])
            for item, weight in zip_longest(items, weights):
                self.items.append([item, weight or 0.0])

        elif len(args) == 1:
            for item in args[0]:
                if isinstance(item, (tuple, list)):
                    # List of tuples
                    self.items.append([item[0], float(item[1])])
                elif self.key is not None:
                    # Raw list and key
                    self.items.append([item, float(self.key(item))])
                else:
                    # Uniform probability
                    self.items.append([item, 1/len(args[0])])

        # Checks weights are correct
        if not all(w >= 0 for w in self.weights()):
            raise ValueError("RandomList requires positive weights")

        # Configure
        self.configure(**kwargs)

    def get_generator (self):
        """Returns a RandomGenerator created from this list"""
        _rg = RandomGenerator()
        _rg.items = self.items.copy()
        _rg.key = self.key
        _rg._no_repeat = self._no_repeat
        _rg._always_age = self._always_age
        _rg._aging_coef = self._aging_coef
        return _rg


    # Generic list methods and extended list methods
    def append (self, item, weight=None):
        """Appends a new element to the list.

        If `weight` is None, it will try to generate the item weight from the
        previous stored values; if there are not, it will try to use the key;
        if there is none, it will set it to 0.

        """
        if weight is None:
            try:
                weight = next(self._stored_weights)
            except StopIteration:
                if self.key is not None:
                    weight = float(self.key(item))
                else:
                    weight = 0.0
        if weight < 0:
            raise ValueError("RandomList requires positive weights")
        self.items.append([item, weight])
        self.configure()

    def remove (self, req):
        """Removes the first item of the list that matches given `item`"""
        _copy = self.items.copy()
        _removed = None
        for elem in _copy:
            if elem[0] == req:
                self.items.remove(elem)
                _removed = elem
                break
        else:
            raise ValueError(f"RandomList could not remove element {req!r}: "\
                             f"it does not exist")
        return _removed

    def pop (self, pos=-1):
        """Pops the last item of the list, or the `i` one, if given"""
        return self.remove(self.items[pos][0])[0]

    def clear (self):
        """Clear the items list, only the items list"""
        self.items = list()

    def clear_all (self):
        """Clear the items list, the stored values, and the key"""
        self.items = list()
        self._stored_weights = (_ for _ in ())
        self.key = None

    def index (self, req, start=None, end=None):
        """Returns a zero-based index in the list for the first item whose
        value is equal to `req`.

        If `start` and/or `stop` are given, they'll be used to slice the list.

        """
        return [elem[0] for elem in self.items].index(req)

    def count (self, req):
        """Returns the number of times `req` appears in the list."""
        return [elem[0] for elem in self.items].count(req)

    def sort (self, key=None, reverse=False):
        """Sorts the items in the list given a key.

        Keep in mind that [0] position is the list object, and [1] its weight.

        """
        self.items.sort(key=key, reverse=reverse)

    def copy (self):
        """Returns a copy of the items in the list, with its weights also"""
        return self.items.copy()

    def elems (self):
        """Returns a copy of the list of elements in the list, without weights"""
        return [x[0] for x in self.items]

    def weights (self):
        """Returns a copy of the list of weights in the list, without elems"""
        return [x[1] for x in self.items]

    def weight_of (self, req):
        """Returns the weight of the first occurrence of the requested element.

        If it is not found, it will raise a ValueError.

        """
        _ret = None
        for elem, weight in self.items:
            if elem == req:
                _ret = weight
                break
        else:
            raise ValueError(f"RandomList element {req!r} not in list")
        return _ret

    def at (self, pos):
        """Returns the element at the position `pos`"""
        return self.items[pos][0]

    def __getitem__ (self, pos):
        return self.at(pos)

    def __len__ (self):
        return len(self.items)


    # Random operations methods and extended random operations
    def shuffle (self):
        """Shuffles all the objects in the list"""
        return random.shuffle(self.items)

    def choice (self, k=1, no_repeat=False, age=False):
        """Returns `k` randomly generated elements from the list, based on their
        weight to appear.

        If `no_repeat` is set to True, items that are chosen once will no longer
        be chosen in the same execution. This option overrides whatever is
        set for global repeatition, but just for this execution.

        If `age` is set to True, items will age each time they generate. This
        overrides the global configuration.

        It only returns the element, never the weight.

        """
        choices = list()
        no_repeat = no_repeat or self._no_repeat
        age = age or self._always_age
        repeated = self._repeated_cache     # List of repeated elements.
        for _ in range(k):
            # Filtering 0 weights
            allowed = list(filter(lambda x: x[1] > 0.0, self.items))
            # Filtering non-repeated
            if no_repeat:
                allowed = list(filter(lambda x: x[0] not in repeated, allowed))

            # Checking there are still elements where to chose
            if not allowed:
                raise NoItemsLeftException("RandomList has no items left to "\
                                           "return (perhaps you need to clear "\
                                           "the repeated cache?)")

            # Running the algorithm
            random.shuffle(allowed)
            total_weight = sum([x[1] for x in allowed])
            rndval = random.uniform(0.0, total_weight)
            rmin = 0.0
            rmax = 0.0
            choice = None
            for elem in allowed:
                item = elem[0]
                weight = elem[1]
                rmax += weight
                if (rmin <= rndval < rmax):
                    choice = item
                    break
            else:
                choice = allowed[-1][0]
            choices.append(choice)

            # Saving extra parameters
            self._last = choices.copy()
            if no_repeat:
                repeated.append(choice)
            if age:
                self.age()

        if self._no_repeat:
            self._repeated_cache += repeated

        return choices

    def uchoice (self, k=1, no_repeat=False):
        """Uniform choice, ignoring specific weights.

        Does not have into account any global repeatition nor aging configuration

        """
        elems = self.elems()
        repeated = list()
        choices = list()
        for _ in range(k):
            if no_repeat:
                allowed = list(filter(lambda x: x not in repeated, elems))
            else:
                allowed = elems
            choice = random.choice(allowed)
            repeated.append(choice)
            choices.append(choice)

        return choices


    # Modificators
    def uniform (self):
        """Makes all objects have the same weight"""
        for elem in self.items:
            elem[1] = 1/len(self.items)

    def normalize (self):
        """Normalizes the weights of each item from 0 to 1"""
        suma = sum([x[1] for x in self.items])
        for elem in self.items:
            elem[1] /= suma

    def age (self):
        """Makes all the items, except from the lasts chosen increase their
        weights, making them more probable to appear in the following executions

        It normalizes the value between 0 and 1.

        """
        for item in self.items:
            # If item not in last choices, increase
            if item[0] not in self._last:
                item[1] *= self._aging_coef
        self.normalize()

    def configure (self, **kwargs):
        """Configures some parameters and behaviors of the class. Options are:
            - no_repeat (bool): If set to True, elements that appear once, won't
                be chosen anymore. When no more elements can be returned, it
                will start throwing a NoElementsLeft exception. You can reset
                it by using the `reset_repeated` method.
            - always_age (bool): If set to True, always after generating an
                element from the list, it will automatically age. You can reset
                the weights using `reset_aging`.
            - aging_coef (float): Changes the aging coeficent, by default, 2.

        """
        self._no_repeat = kwargs.get('no_repeat', self._no_repeat)
        self._always_age = kwargs.get('always_age', self._always_age)
        self._aging_coef = kwargs.get('aging_coef', self._aging_coef)

        if self._always_age:
            self._backup = self.items.copy()    # Backup for resetting


    # Resetting methods
    def reset_repeated (self):
        """Resets the repeated list"""
        self.repeated = list()

    def reset_aging (self):
        """Resets the weights of the elements before start aging"""
        if self._backup:
            self.items = self._backup
            self._backup = list()


    # Output and testing methods
    def __repr__ (self):
        return f"RandomList({self.items})"

    def __str__ (self):
        return str(self.items)


class RandomGenerator (RandomList, Generator):
    """RandomList which also allows generator operations.

    Iterating through it will constantly generate new choices from the original
    list. If the no repeatition mode is activated, it will end up raising an
    StopIteration exception.

    """
    def send (self, arg):
        try:
            return self.choice()[0]
        except NoItemsLeftException:
            self.throw()

    def throw (self, type=None, value=None, traceback=None):
        raise StopIteration

    def __repr__ (self):
        return f"RandomGenerator({self.items})"


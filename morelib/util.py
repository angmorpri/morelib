#!python3
#-*- coding: utf-8 -*-
"""
    MoreLib Utils Module

    This module defines some multipurpose functions and classes to use in many
    standard situations.

    Functions:
        For list handling:
            isiterable() -> bool: Determines whether a given item is iterable.
            lcut() -> list, list: Divides a list in two by a given position.

        For dict handling:
            djoin() -> dict: Joins two or more dictionaries safelly, which means
                repeated keys between dicts won't be overriden, but added.
            dsort() -> OrderedDict: Sorts a given dictionary by a given key, and
                returns an OrderedDict to preserve the order.

        For string handling:
            cleansplit() -> *str: Splits a string and returns the substrings
                stripped.
            multisplit() -> *str: Splits up a string given a group of
                different substring to separate from.
            nsplit() -> str, str: Splits a string in two dividing by the
                n-appearance of the given substring to split from.

        For other types:
            empty_generator() -> generator: Returns a generator that always
                raises a StopIteration.

        For classification and sorting:
            multisorted() -> list: Sorts just like `sorted()`, but you can
                provide infinite keys to un-tie items.
            ranked() -> list: Much like `sorted()`, but equal items will be
                grouped in a tuple, marking they are equal.
            distributed() -> dict: Distributes a given group of items depending
                on their results after running a function towards them.

    Classes:
        Singleton (metaclass): Provides a metaclass for singleton pattern future
            classes.
        Globale: Singleton class that provides a C-like global behavior. It is
            a safe dictionary that can be used anywhere in the package just by
            importing the `globale` defined object, or instaciating from this
            class.
        Biter: Bidirectional iterator.
        DataList: Class that handles a list which items have a counter assigned.
            It is much like Counter, but more orientated to statistics.


    Created:        20 Sep 2020
    Last modified:  24 Sep 2020
        - Ready for version 0.1.0
        - Fixed the docs for DataList.

"""
from collections.abc import Iterable
from collections import OrderedDict


#
# Functions
#
#   List related
def isiterable (it):
    """Returns True if the given `it` is an iterable"""
    return isinstance(it, Iterable)

def lcut (l, n):
    """Returns the given list `l` divided in two by index `n`"""
    return l[:n], l[n:]


#   Dict-related
def djoin (x, y, *args, **kwargs):
    """Safely joins two or more dictionaries, without losing information.

    If dictionaries have repeated keys, their contents are joined by using the
    `add` operation (+), or the custom function given with the key arg `key`.

    It returns the result of the join, or raises a TypeError if two same-key
    values can't be joined.

    """
    each = [x, y, *args]
    ret = dict()
    oper = kwargs.get('key')
    for d in each:
        for key, value in d.items():
            if key not in ret.keys():
                ret[key] = value
            else:
                if oper:
                    ret[key] = oper(ret[key], value)
                else:
                    try:
                        ret[key] += value
                    except TypeError:
                        raise TypeError("dict_join() needs same-key values to "\
                                        "be addible")
    return ret

def dsort (d, key=None, reverse=False):
    """Sorts a dictionary and returns an OrderedDict with the sort made"""
    ds = sorted(d.items(), key=key, reverse=reverse)
    return OrderedDict(ds)


#   String-related
def cleansplit (string, chars):
    """Splits a the given `string` by `chars` and returns the substrings stripped"""
    return tuple([ss.strip() for ss in string.split(chars)])

def multisplit (string, subs):
    """Given a `string` and an iterable of strings, it splits the string by
    each one of the substrings, and returns a tuple with them in order.

    """
    try:
        sub = subs[0]
    except IndexError:
        return (string,)
    else:
        tokens = multisplit(string, subs[1:])
        splitted = list()
        for token in tokens:
            token = token.strip()
            splitted += token.split(sub)
        return tuple(splitted)

def nsplit (string, chars, n):
    """Splits the given `string` in two slices, one before the `n` occurence
    of `chars`, and the other after it.

    """
    slices = string.split(chars)
    before, after = lcut(slices, n+1)
    return chars.join(before).strip(), chars.join(after).strip()


#   Others types
def empty_generator ():
    """Returns an empty generator that always raises StopIteration"""
    return (_ for _ in ())


#   Classification
def multisorted (l, key=None, reverse=False):
    """Given a list, it sorts it using all the keys given.

    `key` must be a function or a list of functions, which will be applied
    subsequently until the draw between to items ceases; or until it runs out
    of keys, when it will stop too.

    """
    # Checking the key
    if isinstance(key, (list, tuple)):
        # List of keys is default behavior.
        current_key = key[0]
        more_keys = key[1:]
    else:
        # Empty or unique key will make the it act as it if were just `sorted`.
        current_key = key or (lambda x: x)
        more_keys = list()

    # Running the algorithm
    chance = ranked(l, key=current_key, reverse=reverse)
    #print(" ## ", chance, current_key, more_keys)
    ms = list()
    for equals in chance:
        if len(equals) > 1:
            # We check if there are more keys to call
            if len(more_keys) >= 1:
                # Call this function again to sort this sublist.
                again = multisorted(equals, key=more_keys, reverse=reverse)
                ms += again
            else:
                # No more keys left, the sublist is left the same.
                ms += list(equals)
        else:
            ms.append(equals[0])
    return ms


def ranked (l, key=None, reverse=False, cmpkey=None):
    """Given a list, it ranks its items returning a sorted tuple-based list.

    It sorts the items in `l`, and, then, groups them that are equal, returning
    a list of tuples.
    If given, `key` must be a one-argument function used to compare both for
    sorting and equal-comparision; although you may change the last one providing
    a `cmpkey`.

    """
    sl = sorted(l, key=key, reverse=reverse)
    compare = cmpkey or (key or (lambda x: x))
    rl = list()         # Final list of values
    chain = [sl[0]]     # Here will save equal-valued items.
    prev_item = sl[0]   # To compare with the next one and check equality.
    for item in sl[1:]:
        if compare(item) == compare(prev_item):
            chain.append(item)
        else:
            rl.append(tuple(chain))
            chain = [item]
        prev_item = item
    if chain:
        rl.append(tuple(chain))
    return rl


def distributed (l, key=None, no_errors=False):
    """Given a list `l` and a function `key`, it organizes the items in the list
    by the return result from appliying `key`.

    It returns a dictionary, where each key is the result, and the value is a
    list with all the items from `l` that returned that result.

    If `no_errors` is set to True, errors raised during the execution of `key`
    won't cause the program to stop, instead, its type will be used as the
    return result of the function and saved too.

    """
    dret = dict()
    key = key or (lambda x: x)
    for item in l:
        try:
            ans = key(item)
        except Exception as e:
            if no_errors:
                ans = type(e)
            else:
                raise
        if ans not in dret:
            dret[ans] = list()
        dret[ans].append(item)
    return dret



#
# Metaclasses
#
class Singleton (type):
    """Metaclass for defining singleton objects.

    It shall be inherited by the target class with the keyword 'metaclass':

        class MyClass (BaseClass, metaclass=Singleton):
            pass

    """
    _instances = {}
    def __call__ (cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


#
# Classes
#
class Globale (object, metaclass=Singleton):
    """C-like global variables behavior class.

    This class provides a dictionary which can be used anywhere in the package,
    even between modules.

    You can start using with the defined instance `globale` or by creating an
    instance by yourself; either way, all the instances will point to the same
    object, as it is a Singleton.

    Globale class allows you to access the variables as properties, and use any
    variable even if they have not previously been created (its value will be
    None).

    You can check if a variable has been user-defined with the only method
    defined in the class: `is_user_defined()`.

    """
    def __init__ (self):
        self.__dict__['_vars'] = dict()
        self.__dict__['__user_defined__'] = list()

    def __setattr__ (self, varname, value):
        self.__dict__['_vars'][varname] = value
        self.__dict__['__user_defined__'].append(varname)

    def __getattr__ (self, varname):
        if varname not in self.__dict__['_vars']:
            return None
        else:
            return self.__dict__['_vars'][varname]

    def is_user_defined (self, varname):
        return varname in self.__dict__['__user_defined__']

globale = Globale()     # Main instance



class Biter (object):
    """Provides a bidirectional iterator.

    Given an iterable, it provides methods that allows you to iterate both
    backward and forward through the iterable, using similar mechanisms to
    standard iterators.

    Public attributes:
        current (Any): Current element from which to move.

    Public methods:
        next() -> self: Moves to the next element of the iterable. Raises a
            StopIteration exception if it tries to surpass the last item.
        prev() -> self: Moves to the previous element of the iterable. Raises a
            StopIteration exception if it tries to infrpass the first item.
        has_next() -> bool: Returns True if `next()` can be run again.
        has_prev() -> bool: Returns True if `prev()` can be run again.

        index() -> int: Returns the current elements index.
        len() -> int: Returns the size of the list.

        forward() -> generator: Returns a generator that will go from the
            position given to the last one.
        backward() -> generator: Returns a generator that will go from the
            position given to the first one.

    Raises:
        StopIteration: When iterable ends its iteration.

    """
    def __init__ (self, iterable, pos=0):
        """Constructs from the iterable"""
        self._iter = [item for item in iterable]
        self._pos = pos
        self.current = self._iter[self._pos]

    def next (self):
        """Moves to the next position, or raises StopIteration"""
        if (self._pos + 1) >= len(self):
            raise StopIteration
        else:
            self._pos += 1
            self.current = self._iter[self._pos]
            return self

    def prev (self):
        """Moves to the previous position, or raises StopIteration"""
        if (self._pos - 1) < 0:
            raise StopIteration
        else:
            self._pos -= 1
            self.current = self._iter[self._pos]
            return self

    def has_next (self):
        """Returns True if `next()` can be performed"""
        return (self._pos + 1) < len(self)

    def has_prev (self):
        """Returns True of `prev()` can be performed"""
        return (self._pos - 1) >= 0

    def index (self):
        """Returns the current index in the original iterable"""
        return self._pos

    def __len__ (self):
        return len(self._iter)

    def forward (self, pos=None):
        """Returns a forward generator from this iter.

        If a `pos` is given, it will start from there, if not, it will do from
        the current position; both till the end.

        """
        pos = pos or self._pos
        return (item for item in self._iter[pos:])

    def backward (self, pos=None):
        """Returns a backward generator from this iter.

        If a `pos` is given, it will start from there, if not, it will do from
        the current position; both till the start.

        """
        pos = pos or self._pos
        return (item for item in self._iter[pos::-1])

    def __repr__ (self):
        return f"Biter({self._iter})"



class _DataItem (object):
    def __init__ (self, i, c, w):
        self.item = i
        self.count = c
        self.weight = w

    def __repr__ (self):
        return f"DataItem(item={self.item}, count={self.count}, weight={self.weight})"

class DataList (object):
    """Class for counted data storage.

    This class provides a way to count groups of items, much like Python's
    vanilla Counter, but orientated to stats generation, probability view,
    and group handling.

    Public methods:
        update() -> None: Adds new values, or updates old ones, from lists or
            dictionaries.
        add() -> self: Adds a new value, or updates an old one.
        subtract() -> self: Removies an item, or decreases its value, if any
            given.
        clear() -> self: Resets all the counters to 0.

        items() -> list: Returns a list with the items, with many available
            formats.
        elements() -> list: Returns a list with the items, repeated once per
            its count.
        counts() -> list: Returns the counts of the items.
        weights() -> list: Returns the weights of the items.
        total() -> float: Returns the sum of the counts of the items.
        get() -> float: Returns the count of the asked element, or None.
        set() -> None: Changes the value of an already existing item.

        filter() -> list: Returns a list of items filtered by the given key.
        rank() -> list: Ranks the items in the list.
        top() -> tuple: Returns the top ranked items.
        bottom() -> tuple: Returns the bottom ranked items.
        sort() -> list: Multisorts the items, and returns a list.

    """
    def __init__ (self, *args, **kwargs):
        """Constructor may take:
            - One argument as an iterator of items, where each can be a tuple of
            (element, initial_count) or a simple element (count = 0).
            - One argument as a dictionary of items and their initial counts.
            - Multiple arguments with count = 0.
            - Multiple keyword arguments as initially counted items.

        The last is compatible with all the previous methods.
        If keys are repeated, their values won't be overriden, but added.

        """
        self._items = list()
        self._total = 0
        self.update(*args, **kwargs)


    # Update methods
    def _item_only_update (self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], dict):
                for key, cnt in args[0].items():
                    self.add(key, cnt)
            else:
                for item in args[0]:
                    if isinstance(item, (list, tuple)):
                        self.add(item[0], item[1])
                    else:
                        self.add(item)
        else:
            for arg in args:
                self.add(arg)
        for key, cnt in kwargs.items():
            self.add(key, cnt)

    def _weight_update (self):
        self._total = sum(map(lambda x: x.count, self._items))
        for i in range(len(self._items)):
            try:
                self._items[i].weight = self._items[i].count / self._total
            except ZeroDivisionError:
                self._items[i].weight = 0.0

    def update (self, *args, **kwargs):
        """Extends the construction to new items. As it, it allows:
            - One argument as an iterator of items, where each can be a tuple of
            (element, initial_count) or a simple element (count = 0).
            - One argument as a dictionary of items and their initial counts.
            - Multiple arguments with count = 0.
            - Multiple keyword arguments as initially counted items.

        If keys are repeated, their values won't be overriden, but added.

        Also, after adding a new item or modifying one of the existing, it
        updates the total score and the weights of each item.

        """
        # Adding
        self._item_only_update(*args, **kwargs)

        # Updating
        self._weight_update()


    # Standard operations
    def add (self, new_item, init_count=0.0):
        """Main method for adding information to the list.

        If the `new_item` is actually new, it will be appended with the given
        `initial_count`. If it already exists, the given `init_count` will be
        added to the current count.

        """
        init_count = 0.0 if init_count < 0 else init_count
        for dataitem in self._items:
            if dataitem.item == new_item:
                dataitem.count += float(init_count)
                break
        else:
            self._items.append(_DataItem(new_item, float(init_count), None))
        return self

    def subtract (self, old_item, cnt=None):
        """It performs two operations:
         - If `cnt` is different to None, it subtracts the given `cnt`
        to the original (fixed to 0).
         - If `cnt` is None, it removes the item from the list.

        If `old_item` is not in the list, it does nothing.

        """
        for i in range(len(self._items)):
            if self._items[i].item == old_item:
                if cnt is None:
                    del self._items[i]    # Item is deleted
                    break
                else:
                    self._items[i].count -= float(cnt)
        self._weight_update()
        return self

    def clear (self):
        """Resets to 0 all the counters"""
        for dataitem in self._items:
            dataitem.count = 0.0
        self._weight_update()
        return self


    # Set / Get operations.
    def _group_items (self, items, returns):
        """Given a list of DataItem items, returns the correct attributes"""
        _returns_placeholders = {'all': 'item|count|weight',
                                 'basic': 'item|count',
                                 'stats': 'item|weight'}
        returns = _returns_placeholders.get(returns, returns)
        return_tokens = cleansplit(returns, '|')
        ret = list()
        for dataitem in items:
            retobj = list()
            for token in return_tokens:
                if token == 'dataitem':
                    retobj.append(dataitem)
                elif token == 'item':
                    retobj.append(dataitem.item)
                elif token == 'count':
                    retobj.append(dataitem.count)
                elif token == 'weight':
                    retobj.append(dataitem.weight)
            if len(retobj) == 1:
                ret.append(retobj[0])
            else:
                ret.append(tuple(retobj))
        return ret

    def items (self, returns='dataitem'):
        """Returns the current list of items.

        You can specify what you want to be returned, using the `returns` kw.
        It receives a string of |-separated words, which determines what will
        be returned (as a tuple if more than one thing):
            - 'dataitem': The whole DataItem namedtuple object.
            - 'item': The item
            - 'count': The count
            - 'weight': The count, normalized

        For example, if you set it to 'item|count|weight', you'll receive a list
        of tuples with all the DataItem attributes.

        Also, you can use some placeholders to sum what you want:
            - 'all' == 'item|count|weight'
            - 'basic' == 'item|count'
            - 'stats' == 'item|weight'

        """
        return self._group_items(self._items, returns)

    def elements (self):
        """Returns a list with the items only, repeated each `total` times"""
        from itertools import chain
        return list(chain(*[[x.item]*int(x.count) for x in self._items]))

    def counts (self):
        """Returns a list of tuples (item, count)"""
        return self.items('count')

    def weights (self):
        """Returns a list of tuples (item, weight)"""
        return self.items('weight')

    def total (self):
        return self._total


    # Setters and getters
    def get (self, key):
        """Given a key, it searches for the item and returns its count.

        It will try to find the given key as the proper item, but if it fails
        and the key is an integer, it will return the positional item.
        If everything fails, it will return None.

        """
        for dataitem in self._items:
            if dataitem.item == key:
                return dataitem.count
        else:
            if isinstance(key, int):
                try:
                    return self._items[key].count
                except IndexError:
                    return None
        self._weight_update()

    def set (self, key, value):
        """Forces the count of a given key to be `value`.

        It will try to find the given key as a proper item, but if it fails and
        the key is an integer, it will change the positional item.

        If it fails, it will call `add`; but keep in mind that this is not the
        method proposed to add new items to the list. Instead, if you know that
        the item is going to be new, call `add`.

        """
        value = 0.0 if (value < 0) else value
        for dataitem in self._items:
            if dataitem.item == key:
                dataitem.count = value
                break
        else:
            if isinstance(key, int):
                try:
                    dataitem.count = value
                except IndexError:
                    self.add(key, value)
        self._weight_update()

    def __getitem__ (self, key):
        return self.get(key)

    def __setitem__ (self, key, value):
        self.set(key, value)


    # Group methods
    def filter (self, key, returns='dataitem'):
        """Filters the list by the given function `key`.

        The key function must receive one argument, that will be the list item,
        which has three attributes `item`, `count` and `weight`, being the
        first the actual item, and the weight the normalized count.

        By default, it will return a list with the DataItems that pass the
        filter, but you can also use the keyword `returns` to specify what do
        you want to receive, following the system provided at `self.items()`.

        """
        fitems = filter(key, self._items)
        return self._group_items(fitems, returns)

    def rank (self, key=None, reverse=False, returns='dataitem'):
        """Ranks the items in the list using the key given.

        The key function must receive one argument, that will be the list item,
        which has three attributes `item`, `count` and `weight`, being the
        first the actual item, and the weight the normalized count.
        By default, it will be the count of the items.

        It will return a list of tuples, where each tuple will have equally
        evaluated items. The items in the tuples will be DataItems by default,
        although you can change them with the `returns` keyword the same way
        as with `self.items()`.

        """
        key = key or (lambda x: x.count)
        rlist = ranked(self._items, key=key, reverse=reverse)
        retlist = list()
        for chained in rlist:
            fixed = self._group_items(chained, returns)
            retlist.append(tuple(fixed))
        return retlist

    def top (self, key=None, reverse=False, returns='dataitem'):
        """Returns the top ranked DataItems"""
        return self.rank(key, reverse, returns)[0]

    def bottom (self, key=None, reverse=False, returns='dataitem'):
        """Returns the bottom ranked DataItems"""
        return self.rank(key, reverse, returns)[-1]

    def sort (self, key=None, reverse=False, returns='dataitem'):
        """Returns the items in this list sorted.

        The key function must receive one argument, that will be the list item,
        which has three attributes `item`, `count` and `weight`, being the
        first the actual item, and the weight the normalized count.
        By default, it will be the count of the items.

        You can provide, instead of one key, a tuple with multiple keys, so
        they are used sequentally to sort items when they are equally evalued
        at first time.

        It will return a list of tuples, where each tuple will have equally
        evaluated items. The items in the tuples will be DataItems by default,
        although you can change them with the `returns` keyword the same way
        as with `self.items()`.

        """
        key = key or (lambda x: x.count)
        slist = multisorted(self._items, key=key, reverse=reverse)
        return self._group_items(slist, returns)


    # Outputting:
    def __repr__ (self):
        return f"DataList({', '.join(str(di) for di in self.items())})"

    def __str__ (self):
        out = ""
        out += "DataList {\n"
        for di in self._items:
            out += f"  '{str(di.item)}' = {di.count:.2f} ({di.weight:.4f}),\n"
        out = out[:-2]
        out += "\n}"
        return out










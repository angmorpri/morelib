# MoreLib
This module brings some general-purpose features to standard Python, such as improved inputs, file handling, operations and useful classes.

It is divided in the following submodules:

* **io**: For input/output features.
* **math**: For extended, simplified and easy-to-understand math features.
* **random**: For extra random functions and classes.
* **util**: For multipurpose functions, abstract classes, and more.



## IO

* **`lines(file, splitchar, jump_empties)`** 

  Given a file, yields all its lines stripped.



## Math

* **`normalize(vector)`** 

  Given a list of natural numbers, normalizes them between 0 and 1.

* **`remap(value, *args)`** 

  Given a value between a range and another range, it returns the value mapped to the second range.

* **`vector_product(v, w, *args)`** 

  Performs integer to list or list to list vector product.

* **`dot_product(v, w , *args)`**

  Given two or more lists of numbers, performs the dot product.



## Util

#### List related

* **`isiterable(arg)`**

  Checks if the given argument is an iterable.

* **`lcut(l, n)`**

  Divides a list in two, given a position in the list.

* **`multisorted(l, keys, reverse)`**

  Sorts a list just like `sorted()`, but allowing multiple keys to compare in case of equality.

* **`ranked(l, key, reverse, cmpkey)`**

  Sorts a list just like `sorted()`, but grouping equal-evaluated items in tuples.

* **`distributed(l, key, no_errors)`**

  Distributes a given group of items by the result they get after applying the given key function.

* __`Biter`__

  Bidirectional iterator class.

  * **Constructor**: It allows any iterator to build the object.
  * **`current`**: Current element.
  * **`next()`**: Movies to the next item, or raises `StopIteration`.
  * __`prev()`__: Moves to the previous item, or raises `StopIteration`.
  * __`has_next()`__: Checks if there are forward elements left.
  * __`has_prev()`__: Checks if there are backward elements left.
  * __`index()`__: Returns the current element index.
  * **`forward()`**: Returns a forward generator from this list.
  * **`backkward()`**: Returns a backward generator from this list.

* __`DataList`__

  Class that provides a list which items are counted and weighted.

  * **Constructor**: Accepts a dictionary, a list of tuples, or just item names.
  * __`update()`__: Adds new elements to the list, or updates existing ones.
  * __`add()`__: Adds a new item, or updates it if exists.
  * __`subtract()`__: Subtracts from an existing item, or removes it.
  * __`clear()`__: Resets the counts from each item.
  * __`items()`__: Returns the items in the list in many different ways.
  * __`get()`__: Returns the count of an item.
  * __`set()`__: Changes the count of an item.
  * __`filter()`__: Filters the items in the list, given a function.
  * __`rank()`__: Ranks the items in the list, and returns a list of tuples.
  * __`sort()`__: Multisorts the items in the list, and returns a list.

  

#### Dictionary related

* __`djoin(x, y, *args, **kwargs)`__

  Safely joins two or more dictionaries, without overriding repeated keys, but adding their values.

* __`dsort(x, key, reverse)`__

  Sorts a dictionary, returning an `OrderedDict` object.

  

#### String related

* __`cleansplit(string, chars)`__

  Splits a string just like `str.split()`, but returning the substrings stripped.

* __`multisplit(string, subs)`__

  Clean-splits a string by a group of different substrings.

* __`nsplit(string, chars, n)`__

  Clean-splits the given string in two, by the `n` occurrence of `chars`.

  

#### Others

* __`empty_generator()`__

  Returns a generator that raises `StopIteration` always.

* __`Singleton`__

  Metaclass for building singleton-pattern classes.

* __`Globale`__

  Class that provides C-like global variables behavior. It works just like a safe-dict that can be used anywhere just by instantiating an object or using the default `globale` auto-declared one.
  
  * __`is_user_defined()`__: Determines whether the given name has been defined by the user, or has its default value.



## Random

* __`biased_choice(*args, **kwargs)`__

  Given a list of items with a values associated, it randomly chooses one of them, having the ones with higher weights, the most probability of being chosen.

* __`RandomList`__

  List that handles items with random-related operations.

  * __`Constructor`__: May accept various lists or dictionaries with items and values.
  * __`shuffle()`__: Shuffles the items in the list. Same as `random.shuffle(list)`.
  * __`choice()`__: Chooses one of more items from the list, taking into account their related weights.
  * __`uchoice()`__: Chooses one of more items from the list, having all of them the same probability. Same as `random.choice(list)`.
  * __`uniform()`__: Gives all the elements in the list the same weight.
  * __`normalize()`__: Remaps all the weights to fit between 0 and 1.
  * __`age()`__: Makes the weights of the items that have not been chosen the last time increase by a coefficient. This can be set as the default behavior with `configure()`, so every time an item is chosen, this function will be called.
  * __`append()`__: Appends new elements to the list.
  * __`remove()`__: Removes elements from the list.
  * __`pop()`__: Pops an element from the list, identified by its index.
  * __`clear()`__: Removes all the elements from the list.
  * __`clear_all()`__: Removes all the elements from the list and also removes all the metadata.
  * __`configure()`__: Configures the object behavior. You can set the aging or the non-repetition as default.
  * __`get_generator()`__: Returns a `RandomGenerator` based on this list.

* __`RandomGenerator`__

  Generator that infinitely yields new choices. It inherits from `RandomList`, so all the methods are available.


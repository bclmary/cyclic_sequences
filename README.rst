Cyclic-Sequences
################

Sequence type objects with cyclic indexing::

Description
===========

The cyclic indexation works as for usual sequences, with the possible use 
of negative indexes. But it makes a jump-back to the beginning (or the end for 
negative indexes) if the index is higher than the length of the sequence::

      ┌───────────────────────────┐
      │                           ▼
    ┏━│━┳━━━┳━━━┳━╍┅   ┅╍━┳━━━━━┳━━━┳━━━┓
    ┃ ● ┃ 0 ┃ 1 ┃   ⋅⋅⋅   ┃ N-1 ┃ N ┃ ● ┃
    ┗━━━┻━━━┻━━━┻━╍┅   ┅╍━┻━━━━━┻━━━┻━│━┛
          ▲                           │
          └───────────────────────────┘

Iterating over a cyclic sequence is bounded (no infinite loop).


.. note:: This module is based on a Chris Lawlor forum publication.


Content
=======

:CyclicTuple:
    Class object.
    An immutable cyclic sequence based on built-in class *tuple*.

:CyclicList:
    Class object.
    A mutable cyclic sequence based on built-in class *list*.

:CyclicStr:
    Class object.
    An immutable cyclic sequence based on built-in class *str*.


Immutable class methods
-----------------------

:with_first:
    foo.with_first(elt) -> new instance
    New instance of 'foo' with first occurence of 'elt' at first position.
    Raises ValueError if 'elt' is not present.

:turned:
    foo.turned(step) -> new instance
    New instance of 'foo' with all elements shifted of given step.
    (default is 1 unit onward).


Mutable class methods
---------------------

:set_first:
    foo.set_first(elt) -> None
    Set first occurence of 'elt' at first position.
    Raises ValueError if 'elt' is not present.

:turn:
    foo.turn(step) -> None
    Change all elements indexes of given step (default is 1 unit onward)
    Equivalent to set at first position the element at index 'step'.


Examples
========

The following examples are using CyclicList class for demonstration. CyclicTuple and CyclicStr classes get similar behaviours.

- Construction from any iterable::

    >>> foo = CyclicList(['a', 'b', 'c', 'd', 'e'])
    >>> foo
    CyclicList(['a', 'b', 'c', 'd', 'e'])

- Gets its specific string representation with chevrons figuring cycling::

    >>> print(foo)
    <['a', 'b', 'c', 'd', 'e']>

- Accessing works like a regular list::

    >>> foo[1]
    'b'
    >>> foo[-4]
    'b'

- Except indexes higher than length wraps around::

    >>> foo[6]
    'b'
    >>> foo[11]
    'b'
    >>> foo[-9]
    'b'

- Slices work and return list objects::

    >>> foo[1:4]
    ['b', 'c', 'd']
    >>> foo[3:0:-1]
    ['d', 'c', 'b']

- Slices work also out of range with cyclic output::

    >>> foo[3:7]
    ['d', 'e', 'a', 'b']
    >>> foo[8:12]
    ['d', 'e', 'a', 'b']
    >>> foo[3:12]
    ['d', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b']
    >>> foo[-2:2]
    ['d', 'e', 'a', 'b']
    >>> foo[-7:-3]
    ['d', 'e', 'a', 'b']
    >>> foo[-7:2]
    ['d', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b']

- Slices with non unitary steps work also::

    >>> foo[:7:2]
    ['a', 'c', 'e', 'b']
    >>> foo[:7:3]
    ['a', 'd', 'b']
    >>> foo[:7:5]
    ['a', 'a']

- As well for reversed steps::

    >>> foo[1:-3:-1]
    ['b', 'a', 'e', 'd']
    >>> foo[-4:-8:-1]
    ['b', 'a', 'e', 'd']
    >>> foo[-4:-9:-2]
    ['b', 'e', 'c']
    >>> foo[-4:-9:-3]
    ['b', 'd']
    >>> foo[-5:-11:-5]
    ['a', 'a']

- Incoherent slices return empty list::

    >>> foo[11:5]
    []

Edge effects:

- Indexing an empty CyclicList returns an IndexError.

- Indexing on a unique element returns always this element.


First element can be played with using specific methods:

- **with_first**: return a new CyclicList with given element at first
  position::

    >>> foo.with_first('c')
    CyclicList(['c', 'd', 'e', 'a', 'b'])

- **turned**: return a new CyclicList with all elements indexes changed
  of given step (default is 1 unit onward)::

    >>> foo.turned()
    CyclicList(['b', 'c', 'd', 'e', 'a'])
    >>> foo.turned(-3)
    CyclicList(['c', 'd', 'e', 'a', 'b'])
    >>> foo.turned(10)
    CyclicList(['a', 'b', 'c', 'd', 'e'])

- **set_first**: put given element at first position::

    >>> foo.set_first('c')
    >>> foo
    CyclicList(['c', 'd', 'e', 'a', 'b'])

- **turn**: change all elements index of given step
  (default is 1 unit onward)::

    >>> foo.turn()
    >>> foo
    CyclicList(['d', 'e', 'a', 'b', 'c'])
    >>> foo.turn(-3)
    >>> foo
    CyclicList(['a', 'b', 'c', 'd', 'e'])
    >>> foo.turn(11)
    >>> foo
    CyclicList(['b', 'c', 'd', 'e', 'a'])

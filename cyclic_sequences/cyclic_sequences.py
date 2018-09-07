#!/usr/bin/env python3
# -*- coding: utf8 -*-

import itertools
import abc
#from itertools import cycle


cyclic_doc = """
{classname}() -> new empty {classname}.

{classname}(iterable) -> new {classname} initialized from iterable’s items.

Author : BCL Mary, based on a Chris Lawlor forum publication

**Description**

A {classparent} with cyclic indexing::

      ┌───────────────────────────┐
      │                           ▼
    ┏━│━┳━━━┳━━━┳━╍┅   ┅╍━┳━━━━━┳━━━┳━━━┓
    ┃ ● ┃ 0 ┃ 1 ┃   ⋅⋅⋅   ┃ N-1 ┃ N ┃ ● ┃
    ┗━━━┻━━━┻━━━┻━╍┅   ┅╍━┻━━━━━┻━━━┻━│━┛
          ▲                           │
          └───────────────────────────┘

- Construction from any iterable::

    >>> foo = {classname}(['a{M}b{M}c{M}d{M}e'])
    >>> foo
    {classname}({A}'a{M}b{M}c{M}d{M}e'{Z})

- Gets its specific string representation with chevrons figuring cycling::

    >>> print(foo)
    <{A}'a{M}b{M}c{M}d{M}e'{Z}>

- Iterating is bounded by the number of elements::

    >>> for x in foo: print(x)
    ...
    a
    b
    c
    d
    e

- Accessing works like a regular {classparent}::

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

- Slices work and return {classparent} objects::

    >>> foo[1:4]
    {A}'b{M}c{M}d'{Z}
    >>> foo[2:]
    {A}'c{M}d{M}e'{Z}
    >>> foo[3:0:-1]
    {A}'d{M}c{M}b'{Z}

- Slices work also out of range with cyclic output::

    >>> foo[3:7]
    {A}'d{M}e{M}a{M}b'{Z}
    >>> foo[8:12]
    {A}'d{M}e{M}a{M}b'{Z}
    >>> foo[3:12]
    {A}'d{M}e{M}a{M}b{M}c{M}d{M}e{M}a{M}b'{Z}
    >>> foo[-2:2]
    {A}'d{M}e{M}a{M}b'{Z}
    >>> foo[-7:-3]
    {A}'d{M}e{M}a{M}b'{Z}
    >>> foo[-7:2]
    {A}'d{M}e{M}a{M}b{M}c{M}d{M}e{M}a{M}b'{Z}

- Slices with non unitary steps work also::

    >>> foo[:7:2]
    {A}'a{M}c{M}e{M}b'{Z}
    >>> foo[:7:3]
    {A}'a{M}d{M}b'{Z}
    >>> foo[:7:5]
    {A}'a{M}a'{Z}

- As well for reversed steps::

    >>> foo[1:-3:-1]
    {A}'b{M}a{M}e{M}d'{Z}
    >>> foo[-4:-8:-1]
    {A}'b{M}a{M}e{M}d'{Z}
    >>> foo[-4:-9:-2]
    {A}'b{M}e{M}c'{Z}
    >>> foo[-4:-9:-3]
    {A}'b{M}d'{Z}
    >>> foo[-5:-11:-5]
    {A}'a{M}a'{Z}

- Incoherent slices return empty {classparent}::

    >>> foo[11:5]
    {A}{Z}

Edge effects:

- Indexing an empty {classname} returns an IndexError.

- Indexing on a unique element returns always this element.
"""


mutable_cyclic_doc = cyclic_doc + """
**Methods**

First element can be set using specific methods:

- **set_first**: put given element at first position::

    >>> foo.set_first('c')
    >>> foo
    {classname}({A}'c{M}d{M}e{M}a{M}b'{Z})

- **turn**: change all elements index of given step
  (default is 1 unit onward)::

    >>> foo.turn()
    >>> foo
    {classname}({A}'d{M}e{M}a{M}b{M}c'{Z})
    >>> foo.turn(-3)
    >>> foo
    {classname}({A}'a{M}b{M}c{M}d{M}e'{Z})
    >>> foo.turn(11)
    >>> foo
    {classname}({A}'b{M}c{M}d{M}e{M}a'{Z})
"""


class AbstractCyclic(abc.ABC):

    _girf = NotImplemented  # get item return function

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            super().__repr__()
            )

    def __str__(self):
        return "<" + super().__repr__() + ">"

    def __getitem__(self, key):
        """x.__getitem__(y) <==> x[y]"""
        N = self.__len__()
        if N == 0:
            raise IndexError(
                '{} is empty'.format(self.__class__.__name__)
                )
        if isinstance(key, int):
            return super().__getitem__(key % N)
        elif isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else N
            step = 1 if key.step is None else key.step
            sim_start = self.index(self[start])
            if step > 0:
                direction = lambda x: x
                length = stop - start
            elif step < 0:
                direction = reversed
                length = start - stop
                step = abs(step)
                sim_start = N - sim_start - 1  # Reverse index
            else:
                raise ValueError("slice step cannot be zero")
            if length > 0:
                # Redifine start and stop with equivalent and simpler indexes.
                start = sim_start
                stop = sim_start + length
                cyclic_self = itertools.cycle(direction(self))
                iterator = ((i, next(cyclic_self)) for i in range(stop))
                return self._girf(elt for i, elt in iterator if i >= start and (i - start) % step == 0)
            else:
                return self._girf([])
        else:
            raise TypeError('{} indices must be integers or slices, '
                            'not {}'.format(self.__class__, type(key)))

class AbstractMutableCyclic(AbstractCyclic):

    def turn(self, step=1):
        """
        foo.turn(step) -> None – change elements index of given step
        (move higher index to lower index with poisitive value).
        Equivalent to set at first position element at index 'step'.
        """
        try:
            step = int(step) % self.__len__()
        except ValueError:
            raise TypeError(
                "{} method 'turn' requires an integer but received a {}"
                .format(self.__class__.__name, type(step))
                )
        self._set_first_using_index(step)

    def set_first(self, elt):
        """
        foo.set_first(elt) -> None – set first occurence of 'elt' at first
        position.
        Raises ValueError if 'elt' is not present.
        """
        try:
            index = self.index(elt)
        except ValueError:
            raise ValueError("{} is not in CyclicList".format(elt))
        self._set_first_using_index(index)

    def _set_first_using_index(self, index):
        self.__init__(
            super().__getitem__(slice(index, None, None))
            + super().__getitem__(slice(None, index, None))
            )


class CyclicTuple(AbstractCyclic, tuple):
    _girf = tuple
    __doc__ = cyclic_doc.format(
        classname="CyclicTuple",
        classparent="tuple",
        A="(",
        M="', '",
        Z=")",
        )

class CyclicList(AbstractMutableCyclic, list):
    _girf = list
    __doc__ = mutable_cyclic_doc.format(
        classname="CyclicList",
        classparent="list",
        A="[",
        M="', '",
        Z="]",
        )



class CyclicStr(AbstractCyclic, str):

#    __doc__ = cyclic_doc.format(
#        classname="CyclicStr",
#        classparent="str",
#        A="",
#        M="",
#        Z="",
#        )

    """
    CyclicStr(object='') -> CyclicStr.

    Create a new cyclic string object from the given object using 
    object.__str__() (if defined) or repr(object).

    Author : BCL Mary

    **Description**

    A string with cyclic indexing::

          ┌───────────────────────────┐
          │                           ▼
        ┏━│━┳━━━┳━━━┳━╍┅   ┅╍━┳━━━━━┳━━━┳━━━┓
        ┃ ● ┃ 0 ┃ 1 ┃   ⋅⋅⋅   ┃ N-1 ┃ N ┃ ● ┃
        ┗━━━┻━━━┻━━━┻━╍┅   ┅╍━┻━━━━━┻━━━┻━│━┛
              ▲                           │
              └───────────────────────────┘

    - Classic string construction::

        >>> foo = CyclicStr('abcde')
        >>> foo
        CyclicStr('abcde')

    - Gets classic string representation::

        >>> print(foo)
        abcde

    - Iterating is bounded by the number of elements::

        >>> for x in foo: print(x)
        ...
        a
        b
        c
        d
        e

    - Accessing works like a regular string::

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

    - Slices work and return string objects::

        >>> foo[1:4]
        'bcd'
        >>> foo[2:]
        'cde'
        >>> foo[3:0:-1]
        'dcb'

    - Slices work also out of range with cyclic output::

        >>> foo[3:7]
        'deab'
        >>> foo[8:12]
        'deab'
        >>> foo[3:12]
        'deabcdeab'
        >>> foo[-2:2]
        'deab'
        >>> foo[-7:-3]
        'deab'
        >>> foo[-7:2]
        'deabcdeab'

    - Slices with non unitary steps work also::

        >>> foo[:7:2]
        'aceb'
        >>> foo[:7:3]
        'adb'
        >>> foo[:7:5]
        'aa'

    - As well for reversed steps::

        >>> foo[1:-3:-1]
        'baed'
        >>> foo[-4:-8:-1]
        'baed'
        >>> foo[-4:-9:-2]
        'bec'
        >>> foo[-4:-9:-3]
        'bd'
        >>> foo[-5:-11:-5]
        'aa'

    - Incoherent slices return empty string::

        >>> foo[11:5]
        ''

    Edge effects:

    - Indexing an empty CyclicStr returns an IndexError.

    - Indexing on a unique element returns always this element.
    """

    _girf = "".join  # get item return function

    def __str__(self):
        return str.__str__(self)



###############################################################################


if __name__ == "__main__":

    import doctest

    doctest_result = doctest.testmod()
    print("\ndoctest >", doctest_result, "\n")


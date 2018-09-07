#!/usr/bin/env python3
# -*- coding: utf8 -*-

import itertools


cyclic_doc = """
{classname}() -> new empty {classname}.

{classname}({init}) -> new {classname} initialized from {init_desc}.

Author : BCL Mary, based on a Chris Lawlor forum publication


Description
-----------

A {classparent} with cyclic indexing::

      ┌───────────────────────────┐
      │                           ▼
    ┏━│━┳━━━┳━━━┳━╍┅   ┅╍━┳━━━━━┳━━━┳━━━┓
    ┃ ● ┃ 0 ┃ 1 ┃   ⋅⋅⋅   ┃ N-1 ┃ N ┃ ● ┃
    ┗━━━┻━━━┻━━━┻━╍┅   ┅╍━┻━━━━━┻━━━┻━│━┛
          ▲                           │
          └───────────────────────────┘

- Construction from any {init_desc}::

    >>> foo = {classname}({A}a{M}b{M}c{M}d{M}e{Z})
    >>> foo
    {classname}({A}a{M}b{M}c{M}d{M}e{Z})

- Gets {str_desc}::

    >>> print(foo)
    {str_out}

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
    {A}b{M}c{M}d{Z}
    >>> foo[2:]
    {A}c{M}d{M}e{Z}
    >>> foo[3:0:-1]
    {A}d{M}c{M}b{Z}

- Slices work also out of range with cyclic output::

    >>> foo[3:7]
    {A}d{M}e{M}a{M}b{Z}
    >>> foo[8:12]
    {A}d{M}e{M}a{M}b{Z}
    >>> foo[3:12]
    {A}d{M}e{M}a{M}b{M}c{M}d{M}e{M}a{M}b{Z}
    >>> foo[-2:2]
    {A}d{M}e{M}a{M}b{Z}
    >>> foo[-7:-3]
    {A}d{M}e{M}a{M}b{Z}
    >>> foo[-7:2]
    {A}d{M}e{M}a{M}b{M}c{M}d{M}e{M}a{M}b{Z}

- Slices with non unitary steps work also::

    >>> foo[:7:2]
    {A}a{M}c{M}e{M}b{Z}
    >>> foo[:7:3]
    {A}a{M}d{M}b{Z}
    >>> foo[:7:5]
    {A}a{M}a{Z}

- As well for reversed steps::

    >>> foo[1:-3:-1]
    {A}b{M}a{M}e{M}d{Z}
    >>> foo[-4:-8:-1]
    {A}b{M}a{M}e{M}d{Z}
    >>> foo[-4:-9:-2]
    {A}b{M}e{M}c{Z}
    >>> foo[-4:-9:-3]
    {A}b{M}d{Z}
    >>> foo[-5:-11:-5]
    {A}a{M}a{Z}

- Incoherent slices return empty {classparent}::

    >>> foo[11:5]
    {empty}

Edge effects:

- Indexing an empty {classname} returns an IndexError.

- Indexing on a unique element returns always this element.


Methods
-------

First element can be played with using specific methods:

- **with_first**: return a new {classname} with given element at first
  position::

    >>> foo.with_first('c')
    {classname}({A}c{M}d{M}e{M}a{M}b{Z})

- **turned**: return a new {classname} with all elements indexes changed
  of given step (default is 1 unit onward)::

    >>> foo.turned()
    {classname}({A}b{M}c{M}d{M}e{M}a{Z})
    >>> foo.turned(-3)
    {classname}({A}c{M}d{M}e{M}a{M}b{Z})
    >>> foo.turned(10)
    {classname}({A}a{M}b{M}c{M}d{M}e{Z})
"""


mutable_cyclic_doc = (
    cyclic_doc
    + """
- **set_first**: put given element at first position::

    >>> foo.set_first('c')
    >>> foo
    {classname}({A}c{M}d{M}e{M}a{M}b{Z})

- **turn**: change all elements index of given step
  (default is 1 unit onward)::

    >>> foo.turn()
    >>> foo
    {classname}({A}d{M}e{M}a{M}b{M}c{Z})
    >>> foo.turn(-3)
    >>> foo
    {classname}({A}a{M}b{M}c{M}d{M}e{Z})
    >>> foo.turn(11)
    >>> foo
    {classname}({A}b{M}c{M}d{M}e{M}a{Z})
"""
)


class AbstractCyclic(object):

    _girf = NotImplemented  # get item return function

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, super().__repr__())

    def __str__(self):
        return "<" + super().__repr__() + ">"

    def __getitem__(self, key):
        """x.__getitem__(y) <==> x[y]"""
        N = self.__len__()
        if N == 0:
            raise IndexError("{} is empty".format(self.__class__.__name__))
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
                return self._girf(
                    elt for i, elt in iterator if i >= start and (i - start) % step == 0
                )
            else:
                return self._girf([])
        else:
            raise TypeError(
                "{} indices must be integers or slices, "
                "not {}".format(self.__class__, type(key))
            )

    def turned(self, step=1):
        """
        foo.turned(step) -> new instance with first element the one from 
        self at index 'step'.
        """
        try:
            step = int(step) % self.__len__()
        except ValueError:
            raise TypeError(
                "{} method 'turned' requires an integer but received a {}".format(
                    self.__class__.__name, type(step)
                )
            )
        return self._get_first_using_index(step)

    def with_first(self, elt):
        """
        foo.with_first(elt) -> new instance with first occurence of 'elt' at first
        position.
        Raises ValueError if 'elt' is not present.
        """
        try:
            index = self.index(elt)
        except ValueError:
            raise ValueError("{} is not in CyclicList".format(elt))
        return self._get_first_using_index(index)

    def _get_first_using_index(self, index):
        return self.__class__(
            super().__getitem__(slice(index, None, None))
            + super().__getitem__(slice(None, index, None))
        )


class AbstractMutableCyclic(AbstractCyclic):
    def turn(self, step=1):
        """
        foo.turn(step) -> None – change elements indexes of given step
        (move higher index to lower index with poisitive value).
        Equivalent to set at first position element at index 'step'.
        """
        try:
            step = int(step) % self.__len__()
        except ValueError:
            raise TypeError(
                "{} method 'turn' requires an integer but received a {}".format(
                    self.__class__.__name, type(step)
                )
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
        A="('",
        M="', '",
        Z="')",
        empty="()",
        init="iterable",
        init_desc="iterable",
        str_desc="its specific string representation with chevrons figuring cycling",
        str_out="<('a', 'b', 'c', 'd', 'e')>",
    )


class CyclicList(AbstractMutableCyclic, list):
    _girf = list
    __doc__ = mutable_cyclic_doc.format(
        classname="CyclicList",
        classparent="list",
        A="['",
        M="', '",
        Z="']",
        empty="[]",
        init="iterable",
        init_desc="iterable",
        str_desc="its specific string representation with chevrons figuring cycling",
        str_out="<['a', 'b', 'c', 'd', 'e']>",
    )


class CyclicStr(AbstractCyclic, str):
    _girf = "".join
    __doc__ = cyclic_doc.format(
        classname="CyclicStr",
        classparent="string",
        A="'",
        M="",
        Z="'",
        empty="''",
        init="object",
        init_desc="object using object.__str__()",
        str_desc="classic string representation",
        str_out="abcde",
    )

    def __str__(self):
        return str.__str__(self)


###############################################################################


if __name__ == "__main__":

    import doctest

    doctest_result = doctest.testmod()
    print("\ndoctest >", doctest_result, "\n")

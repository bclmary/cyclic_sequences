#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
A collection of sequence type objects with cyclic indexing.

Indexing or slicing are cyclic; iterating is bounded.
::

    ┏━━by━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒┃
    ┃▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒┃
    ┃▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒┃
    ┃▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▓▓▓▓▓▓██▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒┃
    ┃░░░░░░░░░░░░░░░░░░░░██▓▓▓▓▓▓▓▓▓▓████████░░░░░░░░░░░░░░░░░░┃
    ┃▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▓▓▓▓▓▓▓▓▓▓██▒▒▒▒▓▓██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒┃
    ┃░░░░░░░░░░░░░░░░░░██▒▒▓▓▓▓▓▓▓▓▓▓▓▓████▓▓██░░░░░░░░░░░░░░░░┃
    ┃░░░░░░░░░░░░░░░░░░██▒▒▓▓▓▓░░      ▓▓▓▓  ██░░░░░░░░░░░░░░░░┃
    ┃                  ██▒▒▓▓░░    ████░░██  ██                ┃
    ┃                    ██▓▓░░    ████░░██  ██                ┃
    ┃                  ████▓▓░░░░      ░░  ░░██                ┃
    ┃              ████▒▒▒▒██▓▓░░████████░░██████              ┃
    ┃            ██▓▓▒▒▒▒▒▒▒▒██░░░░░░░░░░██▒▒▒▒▓▓██            ┃ 
    ┃            ██▓▓▓▓▒▒▒▒▒▒▒▒██████████▒▒▒▒▓▓▓▓██            ┃
    ┃          ██▓▓▓▓▓▓▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▓▓▓▓▓▓██          ┃
    ┃          ██▓▓▓▓██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████▓▓▓▓██          ┃
    ┃          ██▓▓▓▓▓▓████▒▒▒▒▒▒▒▒▒▒▒▒▒▒████▓▓▓▓▓▓██          ┃
    ┃░░░░░░░░░░██▓▓▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓▓▓▓▓▓██░░░░░░░░░░┃
    ┃░░░░░░░░░░░░██████░░██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██░░██████░░░░░░░░░░░░┃
    ┃▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒┃
    ┃░░░░░░░░░░░░░░░░██▓▓▓▓▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▓▓██░░░░░░░░░░░░░░░░┃
    ┃▒▒▒▒▒▒▒▒▒▒▒▒▒▒████▓▓▓▓▓▓▒▒██▒▒██▒▒▓▓▓▓▓▓████▒▒▒▒▒▒▒▒▒▒▒▒▒▒┃
    ┃▒▒▒▒▒▒▒▒▒▒████▓▓▓▓▓▓▓▓▓▓██▒▒▒▒▒▒██▓▓▓▓▓▓▓▓▓▓████▒▒▒▒▒▒▒▒▒▒┃
    ┃▒▒▒▒▒▒▒▒██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▒▒▒▒▒▒██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▒▒▒▒▒▒▒▒┃
    ┃▒▒▒▒▒▒▒▒██████████████████▒▒▒▒▒▒██████████████████▒▒▒▒▒▒▒▒┃
    ┃▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━bclmary━━┛

"""

from cyclic_sequences.cyclic_sequences import CyclicTuple
from cyclic_sequences.cyclic_sequences import CyclicList


__all__ = [
    "CyclicTuple",
    "CyclicList",
    ]
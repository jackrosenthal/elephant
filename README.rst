The Elephant Stack (ELS) Programming Language
---------------------------------------------

ELS is a concatenative language with lexical (static) scoping. ELS prides
itself for having very few builtin operators: most operators are defined in its
own language (see ``core.els``).

To try a few examples, run ``iels`` (which can be invoked by calling either
``iels.py`` or ``elephant.py`` with no arguments)::

    $ python3 iels.py
    iels> 3 4 add
    iels> 7 4 mul
    iels> 28

Notice that the remainder of the stack was left to the next input in ``iels``.

The language is pretty useless without its core library, lets load that and try
a few more complex examples::

    $ python3 iels.py
    iels> core load
    iels> 1 10 range
    iels> begin 1 2 3 4 5 6 7 8 9 10 end begin 2 mul end map
    iels> begin 2 4 6 8 10 12 14 16 18 20 end
    iels> math load
    iels> 2 sqrt
    iels> 1.4142135623730951

Some of the more coplex examples will require ``pypy`` to execute (due to
smaller stack frames). For example, try ``pypy3 elephant.py chudnovsky.els``.

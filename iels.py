# Interactive Elephant Interpreter
# Author: Jack Rosenthal

import sys
import readline
from functools import reduce
from elephant import els, parse, unparse

def interact():
    els.vars.append({})

    def input_hook():
        readline.insert_text(' '.join(unparse(els.stack)) + (' ' if els.stack else ''))
        els.stack = []

    def completer(text, state):
        def gen():
            variables = reduce(set.union, map(dict.keys, els.vars), set())
            for s in '%', '$':
                for v in variables:
                    if (s + v).startswith(text):
                        yield s + v
            for op in els.operators:
                if op.startswith(text):
                    yield op
            for syntax in 'begin', 'end':
                if syntax.startswith(text):
                    yield syntax

        if state == 0:
            completer.it = gen()

        try:
            return next(completer.it)
        except StopIteration:
            return None

    readline.set_completer(completer)
    readline.set_completer_delims(' ')
    readline.parse_and_bind("tab: complete")
    readline.set_startup_hook(input_hook)
    while True:
        try:
            iput = input('iels> ')
        except EOFError:
            print('\nBye bye!', file=sys.stderr)
            sys.exit(0)
        except KeyboardInterrupt:
            print(file=sys.stderr)
            continue
        for itm in parse(iput.split()):
            els.push(itm)

if __name__ == '__main__':
    interact()

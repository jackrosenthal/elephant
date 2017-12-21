# Interactive Elephant Interpreter
# Author: Jack Rosenthal

import sys
import readline
from elephant import els, build_closures, flatten_closures

def interact():
    els.vars.append({})

    def input_hook():
        readline.insert_text(' '.join(flatten_closures(els.stack)) + (' ' if els.stack else ''))
        els.stack = []

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
        for itm in build_closures(iput.split()):
            els.push(itm)

if __name__ == '__main__':
    interact()

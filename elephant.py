# Interpreter for my Elephant stack based programming language
# Author: Jack Rosenthal
import sys
from functools import wraps
from inspect import signature
from math import floor

def build_closures(tokens):
    tokens = iter(tokens)
    result = []
    for t in tokens:
        if t == 'begin':
            result.append(build_closures(tokens))
        elif t == 'end':
            return result
        else:
            result.append(t)
    return result

def flatten_closures(closures):
    result = []
    for itm in closures:
        if isinstance(itm, list):
            result.append('begin')
            result += flatten_closures(itm)
            result.append('end')
        else:
            result.append(str(itm))
    return result

def entypify(token):
    if token == 'None':
        return None
    for typ in int, float, str:
        try:
            return typ(token)
        except ValueError:
            continue

class ElsInterpreter:
    def __init__(self):
        self.operators = {}
        self.vars = []
        self.stack = []
        self.loaded = set()

    def push(self, item):
        if isinstance(item, str):
            if item in self.operators.keys():
                self.operators[item]()
            elif item[0] == '$':
                self.push(item[1:])
                self.push('get')
            elif item[0] == '%':
                self.push(item[1:])
                self.push('set')
            else:
                self.stack.append(entypify(item))
        else:
            self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def exec(self, input_str):
        self.push(build_closures(input_str.split()))
        self.push('call')

    def build_op(self, f):
        sig = signature(f)

        @wraps(f)
        def op_wrapper():
            res = f(**{parm: self.pop() for parm in reversed(list(sig.parameters))})
            if res is not None:
                if type(res) != tuple:
                    res = (res,)
                for itm in res:
                    self.push(itm)

        self.operators[f.__name__[1:] if f.__name__[0] == '_' else f.__name__] = op_wrapper
        return f

els = ElsInterpreter()
@els.build_op
def call(clo):
    els.vars.append({})
    for itm in clo:
        els.push(itm)
    els.vars.pop()

@els.build_op
def add(v1, v2):
    if v1 == None:
        return v2
    if v2 == None:
        return v1
    t = tuple(isinstance(v, list) for v in (v1, v2))
    return {
            (True, True):   lambda: v1 + v2,
            (False, False): lambda: v1 + v2,
            (True, False):  lambda: v1 + [v2],
            (False, True):  lambda: [v1] + v2,
    }[t]()

@els.build_op
def mul(v1, v2):
    return v1 * v2

@els.build_op
def inv(v):
    return 1 / v

@els.build_op
def sep(v):
    return floor(v), v - floor(v)

@els.build_op
def _len(clo):
    return len(clo)

@els.build_op
def _next(clo):
    if not clo:
        return clo, None
    return clo[:-1], clo[-1]

@els.build_op
def fnext(clo):
    if not clo:
        return None, clo
    return clo[0], clo[1:]

@els.build_op
def test(v1, v2, less, equal, greater):
    if v1 < v2:
        return less
    if v1 == v2:
        return equal
    return greater

@els.build_op
def _print(v):
    if isinstance(v, list):
        v = ' '.join(map(str, v))
    print(v)

@els.build_op
def _getchar():
    try:
        return sys.stdin.read(1)
    except EOFError:
        return 'EOF'

@els.build_op
def opdef(opname, clo):
    if isinstance(opname, list):
        opname = opname[0]
    def defined_operator(clo=clo):
        els.push(clo)
        els.push('call')
    els.operators[opname] = defined_operator

@els.build_op
def load(fn):
    if fn in els.loaded:
        return
    with open(fn + '.els') as f:
        for itm in build_closures(f.read().split()):
            els.push(itm)
    els.loaded.add(fn)

@els.build_op
def set(v, r):
    els.vars[-1][r] = v

@els.build_op
def get(r):
    for d in reversed(els.vars):
        if r in d.keys():
            return d[r]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        import iels
        iels.interact()
    else:
        with open(sys.argv[1]) as f:
            els.exec(f.read())


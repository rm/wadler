# 4.3 Array readers

from collections import namedtuple

# Monads: T is array transformer, R is array reader

# same as M in Wadler-4.2
class T(namedtuple('T', 'Callable')):
    def __mul__(self, func):
        def callable(x):
            a, y = self(x)
            b, z = func(a)(y)
            return b, z
        return T(callable)

    def __call__(self, x):
        return self.Callable(x)

# R is a "commutative" monad, T is not
# m * (lambda a: n * (lambda b: o)) == n * (lambda b: m * (lambda a: o))
class R(namedtuple('R', 'Callable')):
    def __mul__(self, func):
        def callable(x):
            a = self(x)
            return func(a)(x)
        return R(callable)

    def __call__(self, x):
        return self.Callable(x)

def unit_T(a):
    return T(lambda x: (a, x))

def unit_R(a):
    return R(lambda x: a)


# same as in Wadler-4.1
class Array(object):
    def __init__(self, val, set=None):
        self.val = val
        if set is None:
            set = dict()
        self.set = set

    def index(self, i):
        return self.set.get(i, self.val)

    def update(self, i, val):
        new_set = self.set.copy()
        new_set[i] = val
        return Array(self.val, new_set)

    def __str__(self):
        return 'Array[' + str(self.set) + ']'


def block(v, m):
    a, x = m(Array(v))
    return a

# def fetch_T(i):
#     return T(lambda x: (x.index(i), x))

def fetch_R(i):
    return R(lambda x: x.index(i))

def assign(i, val):
    return T(lambda x: (None, x.update(i, val)))

def coerce(m):
    # change a R monad into a  T monad
    return T(lambda x: (m(x), x))


# from wadler-4.1
class Term(object): pass

class Var(Term, namedtuple('Var', 'Id')):
    def eval(self):
        return fetch_R(self.Id)

class Con(Term, namedtuple('Con', 'Int')):
    def eval(self):
        return unit_R(self.Int)

class Add(Term, namedtuple('Add', 'Term1 Term2')):
    def eval(self):
        return eval(self.Term1)         * \
            (lambda a: eval(self.Term2) * \
             (lambda b: unit_R(a + b)))

def eval(term):
    # print 'eval(%s, %s)' % (term, state)
    return term.eval()


class Comm(object): pass

class Asgn(Comm, namedtuple('Asgn', 'Id Term')):
    def exec_(self):
        return coerce(eval(self.Term)) * (lambda a: assign(self.Id, a))

class Seq(Comm, namedtuple('Seq', 'Comm1 Comm2')):
    def exec_(self):
        return self.Comm1.exec_()         * \
            (lambda _: self.Comm2.exec_() * \
             (lambda _: unit_T(None)))

class If(Comm, namedtuple('If', 'Term Comm1 Comm2')):
    def exec_(self):
        return coerce(eval(self.Term)) * \
            (lambda a: self.Comm1.exec_() if a == 0 else self.Comm2.exec_())

class Prog(namedtuple('Prog', 'Comm Term')):
    def elab(self):
        return block(0, self.Comm.exec_()               * \
                     (lambda _: coerce(eval(self.Term)) * \
                      (lambda a: unit_T(a))))

# ------------------------------------------------------------------------

p = Prog(Seq(Seq(Asgn('x', Con(4)),
                 Asgn('y', Con(5))),
             If(Con(0),
                Asgn('x', Con(3)),
                Asgn('y', Con(3)))),
         Var('x')).elab()
print p

# 4.2 Array transformers

from collections import namedtuple

# same as in Wadler-2.8
class M(namedtuple('M', 'Callable')):
    def __mul__(self, func):
        def callable(x):
            a, y = self(x)
            b, z = func(a)(y)
            return b, z
        return M(callable)

    def __call__(self, x):
        return self.Callable(x)

def unit(a):
    return M(lambda x: (a, x))


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

def fetch(i):
    return M(lambda x: (x.index(i), x))

def assign(i, val):
    return M(lambda x: (None, x.update(i, val)))


# from wadler-4.1
class Term(object): pass

class Var(Term, namedtuple('Var', 'Id')):
    def eval(self):
        return fetch(self.Id)

class Con(Term, namedtuple('Con', 'Int')):
    def eval(self):
        return unit(self.Int)

class Add(Term, namedtuple('Add', 'Term1 Term2')):
    def eval(self):
        return eval(self.Term1)         * \
            (lambda a: eval(self.Term2) * \
             (lambda b: unit(a + b)))

def eval(term):
    # print 'eval(%s, %s)' % (term, state)
    return term.eval()


class Comm(object): pass

class Asgn(Comm, namedtuple('Asgn', 'Id Term')):
    def exec_(self):
        return eval(self.Term) * (lambda a: assign(self.Id, a))

class Seq(Comm, namedtuple('Seq', 'Comm1 Comm2')):
    def exec_(self):
        return self.Comm1.exec_()         * \
            (lambda _: self.Comm2.exec_() * \
             (lambda _: unit(None)))

class If(Comm, namedtuple('If', 'Term Comm1 Comm2')):
    def exec_(self):
        return eval(self.Term) * \
            (lambda a: self.Comm1.exec_() if a == 0 else self.Comm2.exec_())

class Prog(namedtuple('Prog', 'Comm Term')):
    def elab(self):
        return block(0, self.Comm.exec_()        * \
                     (lambda _: eval(self.Term) * \
                      (lambda a: unit(a))))

# ------------------------------------------------------------------------

p = Prog(Seq(Seq(Asgn('x', Con(4)),
                 Asgn('y', Con(5))),
             If(Con(0),
                Asgn('x', Con(3)),
                Asgn('y', Con(3)))),
         Var('x')).elab()
print p

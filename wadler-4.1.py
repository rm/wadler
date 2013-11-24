# 4.1 Arrays

from collections import namedtuple

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


class Term(object): pass

class Var(Term, namedtuple('Var', 'Id')):
    def eval(self, state):
        return state.index(self.Id)

class Con(Term, namedtuple('Con', 'Int')):
    def eval(self, state):
        return self.Int

class Add(Term, namedtuple('Add', 'Term1 Term2')):
    def eval(self, state):
        return eval(self.Term1, state) + eval(self.Term2, state)

def eval(term, state):
    # print 'eval(%s, %s)' % (term, state)
    return term.eval(state)


class Comm(object): pass

class Asgn(Comm, namedtuple('Asgn', 'Id Term')):
    def exec_(self, State):
        return State.update(self.Id, eval(self.Term, State))

class Seq(Comm, namedtuple('Seq', 'Comm1 Comm2')):
    def exec_(self, State):
        return self.Comm2.exec_(self.Comm1.exec_(State))

class If(Comm, namedtuple('If', 'Term Comm1 Comm2')):
    def exec_(self, State):
        if eval(self.Term, State) == 0:
            return self.Comm1.exec_(State)
        else:
            return self.Comm2.exec_(State)

class Prog(namedtuple('Prog', 'Comm Term')):
    def elab(self):
        return eval(self.Term, self.Comm.exec_(Array(0)))

# ------------------------------------------------------------------------

p = Prog(Seq(Seq(Asgn('x', Con(4)),
                 Asgn('y', Con(5))),
             If(Con(0),
                Asgn('x', Con(3)),
                Asgn('y', Con(3)))),
         Var('x')).elab()
print p

# 2.3 Variation two: State

from collections import namedtuple

# type M a = State -> (a, State)

class Con(namedtuple('Con', 'Int')):
    def eval(self):
        def M(x):
            return (self.Int, x)
        return M

class Div(namedtuple('Div', 'Term1 Term2')):
    def eval(self):
        def M(x):
            a, y = eval(self.Term1, x)
            b, z = eval(self.Term2, y)
            return (a / b, z + 1)
        return M


def eval(term, x):
    return term.eval()(x)


answer = Div(Div(Con(1972), Con(2)), Con(23))
error = Div(Con(1), Con(0))

print answer, '->', eval(answer, 0)
# print error, '->', eval(error, 0)

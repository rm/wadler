# 2.7 Variation one, revisited: Exceptions

from collections import namedtuple

class M(object):
    #  __init__ is unit
    def __mul__(self, func):    # bind
        # func :: (a -> M b)
        if isinstance(self, Raise):
            return self
        return func(self.Value)

class Raise(M, namedtuple('Raise', 'Except')): pass
class Return(M, namedtuple('Return', 'Value')): pass


# Con, Div are Terms

class Con(namedtuple('Con', 'Int')):
    def eval(self):
        return Return(self.Int)

class Div(namedtuple('Div', 'Term1 Term2')):
    def safe_divide(self, a, b):
        if b == 0:
            return Raise('Divide by Zero')
        return Return(a / b)

    def eval(self):
        return eval(self.Term1) * \
            (lambda a: eval(self.Term2) * (lambda b: self.safe_divide(a, b)))


def eval(term):
    return term.eval()


answer = Div(Div(Con(1972), Con(2)), Con(23))
error = Div(Con(1), Con(0))

print answer, '->', eval(answer)
print error, '->', eval(error)

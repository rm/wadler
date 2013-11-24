# 2.6 Variation zero, revisited: The basic evaluator

from collections import namedtuple

class M(namedtuple('M', 'Value')):
    #  __init__ is unit
    def __mul__(self, func):    # bind
        # func :: (a -> M b)
        return func(self.Value)


# Con, Div are Terms

class Con(namedtuple('Con', 'Int')):
    def eval(self):
        return M(self.Int)

class Div(namedtuple('Div', 'Term1 Term2')):
    def eval(self):
        return eval(self.Term1) * \
            (lambda a: eval(self.Term2) * (lambda b: M(a / b)))


def eval(term):
    return term.eval()


answer = Div(Div(Con(1972), Con(2)), Con(23))
# error = Div(Con(1), Con(0))

print answer, '->', eval(answer)
# print error, '->', eval(error)

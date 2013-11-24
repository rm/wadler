# 2.9 Variation three, revisited: Output

from collections import namedtuple

class M(namedtuple('M', 'Output Value')):
    #  __init__ is unit
    def __mul__(self, func):    # bind
        # func :: (a -> M b)
        x, a = self
        y, b = func(a)
        return M(x + y, b)

def unit(a):
    return M('', a)

def out(x):
    return M(x, None)

def line(term, value):
    return 'eval(' + str(term) + ') <= ' + str(value) + '\n'


# Con, Div are Terms

class Con(namedtuple('Con', 'Int')):
    def eval(self):
        return out(line(self, self.Int)) * (lambda _: unit(self.Int))

class Div(namedtuple('Div', 'Term1 Term2')):
    def eval(self):
        return eval(self.Term1)                * \
            (lambda a: eval(self.Term2)        * \
             (lambda b: out(line(self, a / b)) * \
              (lambda _: unit(a / b))))


def eval(term):
    return term.eval()


answer = Div(Div(Con(1972), Con(2)), Con(23))
output, value = eval(answer)
print output
print value

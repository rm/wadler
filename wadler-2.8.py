# 2.8 Variation two, revisited: State

# Note: sample trace provided in wadler-2.8.trace

from collections import namedtuple

class M(namedtuple('M', 'Callable')):
    # type M a = State -> (a, State)
    #  __init__ is unit
    def __mul__(self, func):    # bind
        # func :: (a -> M b)
        def callable(x):
            a, y = self(x)
            b, z = func(a)(y)
            return (b, z)
        return M(callable)

    def __call__(self, x):
        return self.Callable(x)

def unit(a):
    return M(lambda x: (a, x))

def tick():
    return M(lambda x: (None, x + 1))


# Con, Div are Terms
class Con(namedtuple('Con', 'Int')):
    def eval(self):
        return unit(self.Int)

class Div(namedtuple('Div', 'Term1 Term2')):
    def eval(self):
        return self.Term1.eval()         * \
            (lambda a: self.Term2.eval() * \
             (lambda b: tick()           * \
              (lambda _: unit(a / b))))


def eval(term, x):
    return term.eval()(x)


answer = Div(Div(Con(1972), Con(2)), Con(23))
print answer, '->', eval(answer, 0)

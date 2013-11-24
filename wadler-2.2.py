# 2.2 Variation one: Exceptions

from collections import namedtuple

# Con, Div are Terms

class Con(namedtuple('Con', 'Int')):
    def eval(self):
        return Return(self.Int)

class Div(namedtuple('Div', 'Term1 Term2')):
    def eval(self):
        one = self.Term1.eval()
        if isinstance(one, Raise):
            return one

        two = self.Term2.eval()
        if isinstance(two, Raise):
            return two

        if two.Value == 0:
            return Raise("Divide by Zero")

        return Return(one.Value / two.Value)


# data M a = Raise Exception | Return a

Raise = namedtuple('Raise', 'Except')
Return = namedtuple('Return', 'Value')


def eval(term):
    return term.eval()

answer = Div(Div(Con(1972), Con(2)), Con(23))
error = Div(Con(1), Con(0))

print answer, '->', eval(answer)
print error, '->', eval(error)

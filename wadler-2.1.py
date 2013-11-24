# 2.1 Variation zero: The basic evaluator

from collections import namedtuple

# Con, Div are Terms

class Con(namedtuple('Con', 'Int')):
    def eval(self):
        return self.Int

class Div(namedtuple('Div', 'Term1 Term2')):
    def eval(self):
        return eval(self.Term1) / eval(self.Term2)


def eval(term):
    return term.eval()


answer = Div(Div(Con(1972), Con(2)), Con(23))
error = Div(Con(1), Con(0))

print answer, '->', eval(answer)
print error, '->', eval(error)

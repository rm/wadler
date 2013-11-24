# 2.4 Variation three: Output

from collections import namedtuple

# Con, Div are Terms

class Con(namedtuple('Con', 'Int')):
    def eval(self):
        return M(line(self, self.Int), self.Int)

class Div(namedtuple('Div', 'Term1 Term2')):
    def eval(self):
        x, a = eval(self.Term1)
        y, b = eval(self.Term2)
        value = a / b
        # return M(x + y + line(self, value), value)
        # print output in reverse order
        return M(line(self, value) + y + x, value)


# type M a = (Output, a)

M = namedtuple('M', 'Output Value')


def eval(term):
    return term.eval()

def line(term, value):
    return 'eval(' + str(term) + ') <= ' + str(value) + '\n'


answer = Div(Div(Con(1972), Con(2)), Con(23))
# error = Div(Con(1), Con(0))

output, value = eval(answer)
print value
print output

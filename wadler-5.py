from pprint import pprint

def heading(s):
    print
    print s
    print '-' * len(s)


# 5 Parsers

# 5.1 Lists
heading('5.1 Lists')

class List(list):
    def __mul__(self, func):
        if len(self) == 0:
            return List([])
        return func(self[0]) + List(self[1:]) * func

    def __add__(self, other):
        return List(super(List, self).__add__(other))

    def __str__(self):
        return 'List(' + super(List, self).__str__() + ')'

def unit_List(a):
    return List([a])

print 'List tests'
print unit_List(1)
print List([1, 2])
print List([1, 2]) + List([3, 4])
print List([1, 2]) * (lambda x: unit_List(x + 1))
# associativity
print  List([1, 2, 3]) * (lambda x: unit_List(x + 1)   * (lambda y: [y * 2]))
print (List([1, 2, 3]) * (lambda x: unit_List(x + 1))) * (lambda y: [y * 2])


# 5.2 Representing parsers
heading('5.2 Representing parsers')

from collections import namedtuple

# same as M in Wadler-2.8
class Parser(namedtuple('M', 'Callable')):
    # type M a = State -> (a, State)
    #  __init__ is unit
    def __mul__(self, func):    # bind
        # func :: (a -> M b)
        def callable(state):
            return [(b, z)
                    for (a, y) in self(state)
                    for (b, z) in func(a)(y)]
        return Parser(callable)

    def __call__(self, x):
        return self.Callable(x)

def unit_Parser(a):
    return Parser(lambda state: [(a, state)])


# Meaningless tests to check correct form of monad M
def xform(a):
    # a -> Parser(b)
    return Parser(lambda state: [(a + 2, state * 3), (a * 4, state + 5)])
print unit_Parser(1)(1)
print (unit_Parser(1) * xform)(1)
print (unit_Parser(1) * xform * xform)(1)
print (unit_Parser(1) * xform * xform * xform)(1)


# 5.3 Parsing an item
heading('5.3 Parsing an item')

def takeOne(string):
    if not string: return []
    return [(string[0], string[1:])]

item = Parser(takeOne)
print item('monad')
print item('')


# 5.4 Sequencing
heading('5.4 Sequencing')

twoItems = item * (lambda a: item * (lambda b: unit_Parser((a, b))))
print twoItems('monad')
print twoItems('')


# 5.5 Alternation
heading('5.5 Alternation')

zero = Parser(lambda _: [])
print zero('monad')

def both(M, N):
    # M, N are Parsers, return Parser that has parsed output of both
    return Parser(lambda x: M(x) + N(x))

oneOrTwoItems = both(item * (lambda a: unit_Parser((a))),
                     item * (lambda a: item * (lambda b: unit_Parser((a, b)))))
print oneOrTwoItems('monad')
print oneOrTwoItems('m')
print oneOrTwoItems('')


# 5.6 Filtering
heading('5.6 Filtering')

def filter(M, predicate):
    return M * (lambda a: unit_Parser(a) if predicate(a) else zero)

letter = filter(item, lambda x: x.isalpha())
digit = filter(item, lambda x: x.isdigit()) * (lambda a: unit_Parser(int(a)))
def literal(c):
    return filter(item, lambda a: a == c)

print literal('m')('monad')
print literal('m')('parse')


# 5.7 Iteration
heading('5.7 Iteration')

def iterate(M):
    return both(
        M * (lambda a: iterate(M) * \
             (lambda x: unit_Parser(([a] + x)))),
        unit_Parser([]))

def asNumber(digits):
    return int(''.join(map(str, digits)))

number = digit                     * \
         (lambda a: iterate(digit) * \
          (lambda x: unit_Parser(asNumber([a] + x))))

print digit('23 and more')
print iterate(digit)('23 and more')
print number('23 and more')


# 5.8 Biased choice
heading('5.8 Biased choice')

def biased(M, N):
    # unlike both, this will return parses by N only if M has no parses
    def callback(x):
        Mx = M(x)
        if Mx:
            return Mx
        return N(x)
    return Parser(callback)

def reiterate(M):
    return biased(M * (lambda a: reiterate(M) * \
                       (lambda x: unit_Parser(([a] + x)))),
                  unit_Parser([]))

number2 = digit * (lambda a: reiterate(digit) * \
                   (lambda x: unit_Parser(asNumber([a] + x))))

print reiterate(digit)('23 and more')
print number2('23 and more')

print oneOrTwoItems('many')
pprint(iterate(oneOrTwoItems)('many'))
pprint(reiterate(oneOrTwoItems)('many'))


# 5.9 A parser for terms
heading('5.9 A parser for terms')

# Con, Div are Terms
Con = namedtuple('Con', 'Int')
Div = namedtuple('Div', 'Term1 Term2')

term = both(number2                    * \
            (lambda a: unit_Parser(Con(a))),

            literal('(')               * \
            (lambda _:    term         * \
             (lambda t:   literal('/') * \
              (lambda _:  term         * \
               (lambda u: literal(')') * \
                (lambda _: unit_Parser(Div(t, u))))))))

# term = both((number2                * (lambda a:
#                  unit_Parser(Con a))),

#             (literal('(')           * (lambda _:
#              term                   * (lambda t:
#              literal('/')           * (lambda _:
#              term                   * (lambda u:
#              literal(')')           * (lambda _:
#                  unit_Parser(Div(t, u)))))))))

print term('((1972/23)/2) foo bar baz')


# 5.10 Left recursion
heading('5.10 Left recursion')

factor = both(number2                   * \
              (lambda a: unit_Parser(Con(a))),

              (literal('(')             * \
               (lambda _: term          * \
                (lambda t: literal(')') * \
                 (lambda _: unit_Parser(t))))))

term = factor * (lambda t: term2(t))

def term2(t):
    return biased(literal('/')          * \
                  (lambda _: factor     * \
                   (lambda u: term2(Div(t, u)))),
                  unit_Parser(t))

print term('1972/23/2')
print term('1972/(23/2)')

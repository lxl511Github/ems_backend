from django.test import TestCase
from functools import reduce
# Create your tests here.


# 阶乘
def f(n):
    return 1 if n < 2 else n*f(n-1)


print(list(map(f, range(5))))


def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))


print(fact(5))



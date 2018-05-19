import sympy
from sympy.parsing.sympy_parser import parse_expr, \
                                       standard_transformations, \
                                       implicit_multiplication_application

def tran_p(p):
    transformations = (standard_transformations +(implicit_multiplication_application, ))
    return parse_expr(p, transformations=transformations)

def dif(p, symbol, times):
    if isinstance(symbol, str):
        symbol = sympy.Symbol(symbol)
    dif = sympy.diff(p, symbol, times)
    return dif

def S(p, symbol, *args):
    if isinstance(symbol, str):
        symbol = sympy.Symbol(symbol)
    if args:
        upperbound = args[0]
        lowerbound = args[1]
        S = sympy.integrate(p, (symbol, upperbound, lowerbound))
    else:
        S = sympy.integrate(p, symbol)

    return S

def l(p, symbol, num):
    if isinstance(symbol, str):
        symbol = sympy.Symbol(symbol)
    limit = sympy.limit(p, symbol, num)
    return limit
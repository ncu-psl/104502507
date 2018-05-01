import numpy
import sympy

class matrix(object):

    def __init__(self, name, row, col, *args):
        self.row = row
        self.col = col
        self.name = name
        if args:
            self.matrix = numpy.array(args[0])
        else:
            self.matrix = numpy.zeros((row, col))


    def T(self):        # 轉置矩陣
        self.matrixT = self.matrix.T
        return self.matrixT

    def I(self):      # 反矩陣
        self.matrixI = numpy.linalg.inv(self.matrix)
        return self.matrixI

    def D(self):        # 行列式
        matrixD = numpy.linalg.det(self.matrix)
        return matrixD

class polynomial(object):           # 考慮若有兩個以上的symbol

    def __init__(self, name, p, symbol):
        self.name = name
        self.p = p
        self.symbol = sympy.Symbol(symbol)

    def dif(self, times):
        self.dif = sympy.diff(self.p, self.symbol, times)
        return self.dif

    def S(self, *args):
        if args:
            upperbound = args[0]
            lowerbound = args[1]
            self.S = sympy.integrate(self.p, (self.symbol, upperbound, lowerbound))
        else:
            self.S = sympy.integrate(self.p, self.symbol)

        return self.S

    def l(self, symbol, num):
        self.limit = sympy.limit(self.p, symbol, num)
        return self.limit
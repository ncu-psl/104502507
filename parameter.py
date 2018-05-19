from collections import OrderedDict
import sympy

import matrix
import polynomial


currentline = 1.0
outputline = 1.0
inputline = 1.0

user_var = 1

parameterdic = OrderedDict()
parameterdic['x'] = sympy.Symbol('x')
parameterdic['y'] = sympy.Symbol('y')
parameterdic['z'] = sympy.Symbol('z')
parameterdic['dif'] = polynomial.dif
parameterdic['S'] = polynomial.S
parameterdic['l'] = polynomial.l
parameterdic['T'] = matrix.T
parameterdic['I'] = matrix.I
parameterdic['D'] = matrix.D
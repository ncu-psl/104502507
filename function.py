import linearalgebra
import matplotlib.pylab as plt
import numpy as np
import parameter
import re


currentline = 1.0

def cleanmem():
    parameter.matrixdic = {}
    parameter.polynomialdic = {}

def creatematrix(name, matrix, row, col):
    parameter.matrixdic[name] = linearalgebra.matrix(name, row, col, matrix)

def plot(xlowerbound, xupperbound, formula):
    isconst = False
    isfirstco = False
    polynomial = []
    formula = '101*x**9+5*x**8+3*x-9'
    coefficient = re.split(r'[+-]', formula)
    degree = int(re.split(r'[0-9]?\*?x\*\*', coefficient[0])[1])

    for _ in range(degree+1):
        polynomial.append(0)

    print(coefficient)
    for i in range(len(coefficient)):
        if 'x' not in coefficient[i]:
            isconst = True
        if '**' not in coefficient[i]:
            isfirstco = True

        if 'x' not in coefficient[i] and isconst:
            polynomial[len(polynomial)-1] = int(coefficient[i])
            coefficient[i] = 'del'
        elif 'x' not in coefficient[i] and not isconst:
            polynomial[len(polynomial)-1] = 0
        elif '**' not in coefficient[i] and isfirstco:
            num = int(re.match(r'[0-9]', coefficient[i])[0])
            polynomial[len(polynomial)-2] = num
            coefficient[i] = 'del'
        elif '**' not in coefficient[i] and not isfirstco:
            polynomial[len(polynomial)-2] = 0

    coefficient = filter(lambda x: x != 'del', coefficient)

    for i in coefficient:
        degreeforpoly = int(re.split(r'[0-9]?\*?x\*\*', i)[1])
        coefficientforpoly = int(re.match(r'[0-9]', i)[0])
        polynomial[9-degreeforpoly] = coefficientforpoly

    print(polynomial)




    # x = np.arange(xlowerbound, xupperbound, 1)
    # y = formula
    # plt.plot(x, y)
    # plt.show()


plot(1,2,3)
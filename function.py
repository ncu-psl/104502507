from matrix import *
from polynomial import *
import matplotlib.pylab as plt
import numpy as np
import parameter
import re
import sys


def isintegral(checkintegral):
    if checkintegral:
        return True
    else:
        return False

def isplots(checkplot):
    if checkplot:
        return True
    else:
        return False

def cleanmem():
    parameter.parameterdic = {}

def creatematrix(name, matrix, row, col):
    parameter.parameterdic[name] = makematrix(row, col, matrix)

def createpoly(name, p):
    p = tran_p(p)
    parameter.parameterdic[name] = p

def plot(xlowerbound, xupperbound, formulas):       # 先呼叫合併多項式
    for i in formulas:
        polynomial = []
        temp = []
        p = list(i)
        for j in p:
            if j =='-':
                temp.append('+')
                temp.append(j)
            else:
                temp.append(j)
        p = ''
        for j in temp:
            p += j
        if p[0] == '+':
            p = p[1:]

        coefficient = re.split(r'[+]', p)
        maxdegree = -1


        for j in range(len(coefficient)):
            if 'x' not in coefficient[j]:
                degree = 0
            elif '**' not in coefficient[j]:
                degree = 1
            else:
                degree = int(re.split(r'-?[0-9]?\*?x\**', coefficient[j])[1])
            if degree > maxdegree:
                maxdegree = degree


        for _ in range(maxdegree+1):
            polynomial.append(0)

        for j in range(len(coefficient)):
            if 'x' not in coefficient[j]:
                constant = int(coefficient[j])
                polynomial[-1] = constant
            else:
                match = re.match(r'(-?\d*)\D*(\d*)', coefficient[j])

                if match.group(1) == '-':
                    polyco = -1
                elif match.group(1) != '-':
                    polyco = 1
                else:
                    polyco = int(match.group(1))

                if match.group(2):
                    polyde = int(match.group(2))
                else:
                    polyde = 1

                polynomial[maxdegree-polyde] = polyco

        polynomial = np.poly1d(polynomial)

        x = np.linspace(xlowerbound, xupperbound, 100)
        y = [polynomial(i) for i in x]

        plt.plot(x, y)
    plt.show()

def iscomment(cmd, currentline):
    temp = cmd
    if '#' in temp:
        for i in range(len(temp)):
            if temp[i] == '#':
                cmd = temp[:i]
                comments = '0.' + str(i)
                currentline += float(comments)
                currentline = round(currentline, 5)
                break
        return {'iscomment': True, 'cmd': cmd, 'comments': currentline}
    else:
        return {'iscomment': False, 'cmd': cmd}

def command(cmd):
    try:
        if re.match(r'^\s*cl[a-z]+\s*$', cmd):
            if re.match(r'\s*cleanmem\s*', cmd):       # cleanmem
                cleanmem()
                cmddic = {
                    'instruction': 'cleanmem',
                }
                return cmddic
            if re.match(r'\s*clear\s*', cmd):        # clear
                cmddic = {
                    'instruction': 'clear',
                }
                return cmddic
            else:
                cmddic = {
                    'instruction': 'error',
                }
                return cmddic
        elif re.match(r'^\s*show\(.*\)\s*$', cmd):        # show
            var = re.match(r'^\s*show\((.*)\)\s*$', cmd)
            ans = eval(var.group(1), parameter.parameterdic)
            cmddic = {
                'instruction': 'show',
                'varname': var.group(1),
                'ans': ans,
            }
            return cmddic
        elif re.match(r'^\s*_?[A-Za-z]+_?[0-9]*\s*=(\s*([0-9]+([+\-*/]?[0-9]*){0,}\s*))$', cmd):        # 賦值
            var = re.match(r'^(\s*_?[A-Za-z]+_?[0-9]*)\s*=(\s*[0-9]+([+\-*/]?[0-9]*){0,}\s*)$', cmd)
            value = eval(var.group(2))
            cmddic = {
                'instruction': 'assignvalue',
                'varname': var.group(1),
                'varvalue': value,
            }
            parameter.parameterdic[cmddic['varname']] = int(cmddic['varvalue'])
            return cmddic
        elif re.match(r'^\s*_?[A-Za-z]+_?[0-9]*\(?[xyz]?\)?\s*=\s*[0-9xyz*+\-/\s]+\s*$', cmd):  # 多項式
            poly = re.match(r'^(\s*_?[A-Za-z]+_?[0-9]*)\(?[xyz]{1,3}\)?\s*=\s*([0-9xyz*+\-/\s]+)\s*$', cmd)
            if not poly:
                cmddic = {
                    'instruction': 'polyerror',
                }
                return cmddic
            polyname = poly.group(1)
            polyp = poly.group(2)
            # polysymbol = poly.group(2)
            createpoly(polyname, polyp)
            cmddic = {
                'instruction': 'assignpoly',
                'poly': parameter.parameterdic[polyname],
            }
            return cmddic
        elif re.match(r'^\s*_?[A-Za-z]+_?[0-9]*\(\d+\)\s*$', cmd):      # 多項式代換
            poly = re.match(r'^(\s*_?[A-Za-z]+_?[0-9]*)\((\d+)\)\s*$', cmd)
            polyname = poly.group(1)
            value = poly.group(2)
            evalpoly = parameter.parameterdic[polyname].subs({parameter.parameterdic['x']: value,})
            ans = eval(str(evalpoly))
            cmddic = {
                'instruction': 'evalpoly',
                'ans': ans,
            }
            return cmddic
        elif re.match(r'^\s*_?[A-Za-z]+_?[0-9]*\s*=\s*\[[0-9;,\s]+\]\s*$', cmd):  # 創建矩陣
            matrixname = cmd.strip().split('=')[0].strip()
            matrixvalue = cmd.strip().split('=')[1].strip()
            matrix = []
            while ';' in matrixvalue:
                row = matrixvalue[:matrixvalue.find(';')]
                if row[0] == '[':
                    row = row[1:]
                elements = re.split(',', row)
                for i in range(len(elements)):
                    elements[i] = int(elements[i])
                matrix.append(elements)
                matrixvalue = matrixvalue[matrixvalue.find(';') + 1:]
            creatematrix(matrixname, matrix, len(matrix), len(matrix[0]))
            cmddic = {
                'instruction': 'assignmatrix',
                'varname': matrixname,
                'var': parameter.parameterdic[matrixname],
            }
            return cmddic
        else:
            exec(cmd, parameter.parameterdic)
            return {
                'instruction': 'default',
            }
    except Exception:
        tracebackvalue = sys.exc_info()[1]
        errormsg = str(tracebackvalue)
        if 'invalid syntax' in errormsg:
            errormsg = 'invalid syntax'
        cmddic = {
            'instruction': 'error',
            'errormsg': errormsg,
        }
        return cmddic




# command('a=[1,2;3,4;]')
# command('print(a.D())')
# a=[1,2;3,4;]
# print(a.D())
# f(x)=2x**2-6x-2
# show(f.dif(1))
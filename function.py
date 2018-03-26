import linearalgebra
import matplotlib.pylab as plt
import numpy as np
import parameter
import re



currentline = 1.0

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
    parameter.parameterdic[name] = linearalgebra.matrix(name, row, col, matrix)

def createpoly(name, p, symbol):
    parameter.parameterdic[name] = linearalgebra.polynomial(name, p, symbol)

def plot(xlowerbound1, xupperbound1, formula1, *args):
    if args:
        isconst1 = False
        isfirstco1 = False
        isconst2 = False
        isfirstco2 = False

        xlowerbound2 = args[0]
        xupperbound2 = args[1]
        formula2 = args[2]

        polynomial1 = []
        polynomial2 = []
        # 尚未處理負項

        coefficient1 = re.split(r'[+-]', formula1)
        degree1 = int(re.split(r'[0-9]?\*?x\*\*', coefficient1[0])[1])
        coefficient2 = re.split(r'[+-]', formula2)
        degree2 = int(re.split(r'[0-9]?\*?x\*\*', coefficient2[0])[1])

        for _ in range(degree1 + 1):
            polynomial1.append(0)
        for _ in range(degree2 + 1):
            polynomial2.append(0)

        for i in range(len(coefficient1)):
            if 'x' not in coefficient1[i]:
                isconst1 = True
            if '**' not in coefficient1[i]:
                isfirstco1 = True

            if 'x' not in coefficient1[i] and isconst1:
                polynomial1[len(polynomial1) - 1] = int(coefficient1[i])
                coefficient1[i] = 'del'
            elif 'x' not in coefficient1[i] and not isconst1:
                polynomial1[len(polynomial1) - 1] = 0
            elif '**' not in coefficient1[i] and isfirstco1:
                try:
                    num1 = int(re.match(r'[0-9]*', coefficient1[i])[0])
                    polynomial1[len(polynomial1) - 2] = num1
                except:
                    polynomial1[len(polynomial1) - 2] = 1
                coefficient1[i] = 'del'
            elif '**' not in coefficient1[i] and not isfirstco1:
                polynomial1[len(polynomial1) - 2] = 0


        for i in range(len(coefficient2)):
            if 'x' not in coefficient2[i]:
                isconst2 = True
            if '**' not in coefficient2[i]:
                isfirstco2 = True

            if 'x' not in coefficient2[i] and isconst2:
                polynomial2[len(polynomial2) - 1] = int(coefficient2[i])
                coefficient2[i] = 'del'
            elif 'x' not in coefficient2[i] and not isconst2:
                polynomial2[len(polynomial2) - 1] = 0
            elif '**' not in coefficient2[i] and isfirstco2:
                try:
                    num2 = int(re.match(r'[0-9]*', coefficient2[i])[0])
                    polynomial2[len(polynomial2) - 2] = num2
                except:
                    polynomial2[len(polynomial2) - 2] = 1
                coefficient2[i] = 'del'
            elif '**' not in coefficient2[i] and not isfirstco2:
                polynomial2[len(polynomial2) - 2] = 0

        coefficient1 = filter(lambda x: x != 'del', coefficient1)
        coefficient2 = filter(lambda x: x != 'del', coefficient2)

        for i in coefficient1:
            degreeforpoly1 = int(re.split(r'[0-9]?\*?x\*\*', i)[1])
            try:
                coefficientforpoly1 = int(re.match(r'[0-9]*', i)[0])
            except:
                coefficientforpoly1 = 1
            polynomial1[degree1 - degreeforpoly1] = coefficientforpoly1

        for i in coefficient2:
            degreeforpoly2 = int(re.split(r'[0-9]?\*?x\*\*', i)[1])
            try:
                coefficientforpoly2 = int(re.match(r'[0-9]*', i)[0])
            except:
                coefficientforpoly2 = 1
            polynomial2[degree2 - degreeforpoly2] = coefficientforpoly2


        polynomial1 = np.array(polynomial1)
        polynomial1 = np.poly1d(polynomial1)
        x1 = np.linspace(xlowerbound1, xupperbound1, 100)
        y1 = [polynomial1(i) for i in x1]

        polynomial2 = np.array(polynomial2)
        polynomial2 = np.poly1d(polynomial2)
        x2 = np.linspace(xlowerbound2, xupperbound2, 100)
        y2 = [polynomial2(i) for i in x2]

        plt.plot(x1, y1, x2, y2)
        plt.show()


    else:
        isconst1 = False
        isfirstco1 = False
        polynomial1 = []
        # 尚未處理負項
        coefficient1 = re.split(r'[+-]', formula1)
        degree1 = int(re.split(r'[0-9]?\*?x\*\*', coefficient1[0])[1])

        for _ in range(degree1+1):
            polynomial1.append(0)

        for i in range(len(coefficient1)):
            if 'x' not in coefficient1[i]:
                isconst1 = True
            if '**' not in coefficient1[i]:
                isfirstco1 = True

            if 'x' not in coefficient1[i] and isconst1:
                polynomial1[len(polynomial1)-1] = int(coefficient1[i])
                coefficient1[i] = 'del'
            elif 'x' not in coefficient1[i] and not isconst1:
                polynomial1[len(polynomial1)-1] = 0
            elif '**' not in coefficient1[i] and isfirstco1:
                try:
                    num1 = int(re.match(r'[0-9]*', coefficient1[i])[0])
                    polynomial1[len(polynomial1)-2] = num1
                except:
                    polynomial1[len(polynomial1) - 2] = 1
                coefficient1[i] = 'del'
            elif '**' not in coefficient1[i] and not isfirstco1:
                polynomial1[len(polynomial1)-2] = 0

        coefficient1 = filter(lambda x: x != 'del', coefficient1)

        for i in coefficient1:
            degreeforpoly1 = int(re.split(r'[0-9]?\*?x\*\*', i)[1])
            try:
                coefficientforpoly1 = int(re.match(r'[0-9]*', i)[0])
            except:
                coefficientforpoly1 = 1
            polynomial1[degree1-degreeforpoly1] = coefficientforpoly1

        polynomial1 = np.array(polynomial1)
        polynomial1 = np.poly1d(polynomial1)
        x1 = np.linspace(xlowerbound1, xupperbound1, 100)
        y1 = [ polynomial1(i)  for i in x1]

        plt.plot(x1, y1)
        plt.show()

def iscomment(cmd, currentline):
    if '#' in cmd:
        for i in range(len(cmd)):
            if cmd[i] == '#':
                cmd = cmd[:i]
                comments = i/10
                currentline += comments
                break
        return {'iscomment': True, 'cmd': cmd, 'comments': currentline}
    else:
        return {'iscomment': False, 'cmd': cmd}

def command(cmd):
    print(cmd)
    try:
        if re.match(r'^\s*[\w]+\s*$', cmd):
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
        elif re.match(r'^\s*print\([A-Za-z]+[0-9]*\)\s*$', cmd):        # print
            var = re.match(r'^\s*print\(([a-zA-Z]+[0-9]*)\)\s*$', cmd)
            cmddic = {
                'instruction': 'print',
                'varname': var.group(1),
            }
            return cmddic
        elif re.match(r'^\s*[A-Za-z]+[0-9]*\s*=\s*[0-9]+\s*$', cmd):        # 賦值
            var = re.match(r'^(\s*[A-Za-z]+[0-9]*)\s*=\s*([0-9]+)\s*$', cmd)
            cmddic = {
                'instruction': 'assignvalue',
                'varname': var.group(1),
                'varvalue': var.group(2),
            }
            parameter.parameterdic[cmddic['varname']] = int(cmddic['varvalue'])
            return cmddic
        elif re.match(r'^\s*[A-Za-z]+[0-9]*\(?[xyz]?\)?\s*=\s*[0-9xyz*+\-/]+\s*$', cmd):  # 多項式
            poly = re.match(r'^(\s*[A-Za-z]+[0-9]*)\(+([xyz]{1,3})\)+\s*=\s*([0-9xyz*+\-/]+)\s*$', cmd)
            if not poly:
                cmddic = {
                    'instruction': 'polyerror',
                }
                return cmddic
            polyname = poly.group(1)
            polyp = poly.group(3)
            polysymbol = poly.group(2)
            createpoly(polyname, polyp, polysymbol)
            cmddic = {
                'instruction': 'assignpoly',
                'poly': parameter.parameterdic[polyname],
            }
            return cmddic
        elif re.match(r'^\s*[A-Za-z]+[0-9]*\(\d+\)\s*$', cmd):      # 多項式代換
            poly = re.match(r'^(\s*[A-Za-z]+[0-9]*)\((\d+)\)\s*$', cmd)
            polyname = poly.group(1)
            value = poly.group(2)
            evalpoly = parameter.parameterdic[polyname].p.replace(str(parameter.parameterdic[polyname].symbol), str(value))
            ans = eval(evalpoly)
            cmddic = {
                'instruction': 'evalpoly',
                'ans': ans,
            }
            return cmddic

        elif re.match(r'^\s*[A-Za-z]+[0-9]*\s*=\s*\[[0-9;,\s]+\]\s*$', cmd):  # 創建矩陣
            matrixname = cmd.strip().split('=')[0]
            matrixvalue = cmd.strip().split('=')[1]
            matrix = []
            while ';' in matrixvalue:
                row = list(matrixvalue[:matrixvalue.find(';')])
                for i in range(len(row)):
                    if row[i] == ',' or row[i] == ' ' or row[i] == '[' or row[i] == ']':
                        row[i] = 'del'
                while 'del' in row:
                    row.remove('del')
                for i in range(len(row)):
                    if row[i] != 'del':
                        row[i] = int(row[i])
                matrix.append(row)
                matrixvalue = matrixvalue[matrixvalue.find(';') + 1:]
            creatematrix(matrixname, matrix, len(matrix), len(matrix[0]))
            cmddic = {
                'instruction': 'assignmatrix',
                'var': parameter.parameterdic[matrixname],
            }
            return cmddic
        else:
            exec(cmd, parameter.parameterdic)
            return {
                'instruction': 'default',
            }
    except:
        cmddic = {
            'instruction': 'error',
        }
        return cmddic

def callworkspace():
    for i in parameter.parameterdic:
        pass

import linearalgebra
import matplotlib.pylab as plt
import numpy as np
import parameter
import re
import speech_recognition


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

def plot(xlowerbound, xupperbound, formulas):
    # else:
    for i in formulas:
        isconst = False
        isfirstco = False

        polynomial = []
        # 尚未處理負項
        coefficient = re.split(r'[+-]', i)

        if re.split(r'[0-9]?\*?x\**', coefficient[0])[1]:
            degree = int(re.split(r'[0-9]?\*?x\**', coefficient[0])[1])
        elif not re.split(r'[0-9]?\*?x\**', coefficient[0])[1]:
            degree = 1

        for _ in range(degree+1):
            polynomial.append(0)

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
                try:
                    num1 = int(re.match(r'[0-9]*', coefficient[i])[0])
                    polynomial[len(polynomial)-2] = num1
                except:
                    polynomial[len(polynomial) - 2] = 1
                coefficient[i] = 'del'
            elif '**' not in coefficient[i] and not isfirstco:
                polynomial[len(polynomial)-2] = 0

        coefficient = filter(lambda x: x != 'del', coefficient)

        for i in coefficient:
            degreeforpoly = int(re.split(r'[0-9]?\*?x\*\*', i)[1])
            try:
                coefficientforpoly = int(re.match(r'[0-9]*', i)[0])
            except:
                coefficientforpoly = 1
            polynomial[degree-degreeforpoly] = coefficientforpoly

        polynomial = np.array(polynomial)
        polynomial = np.poly1d(polynomial)
        x1 = np.linspace(xlowerbound, xupperbound, 100)
        y1 = [ polynomial(i)  for i in x1]

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
        elif re.match(r'^\s*show\([A-Za-z]+[0-9]*\)\s*$', cmd):        # print
            var = re.match(r'^\s*show\(([a-zA-Z]+[0-9]*)\)\s*$', cmd)
            cmddic = {
                'instruction': 'show',
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

def speak():
    r = speech_recognition.Recognizer()

    with speech_recognition.Microphone() as source:
        audio = r.listen(source)

    print(r.recognize_google(audio, language='zh-TW'))

# speak()
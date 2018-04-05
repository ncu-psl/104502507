from tkinter import *
from tkinter import messagebox
import linearalgebra
import parameter
import function
import re


class GUI(object):

    def __init__(self, master):
        self.master = master
        frmroot = Frame(self.master)
        frmroot.grid(row=0, column=0)
        self.frm1 = Frame(frmroot)
        self.frm2 = Frame(frmroot)
        self.currentline = 1.0      # currentline 要打在 function 模組裡面
        self.outputline = 1.0
        self.inputline = 1.0
        self.frm1.grid(row=0, column=0, columnspan=2, rowspan=10)
        self.frm2.grid(row=0, column=6, columnspan=5, rowspan=10)
        self.init_window()


    def hello(self):
        pass

    def updateworkspace(self):
        self.workspace.config(state=NORMAL)
        self.workspace.delete('1.0', END)
        for k,v in parameter.parameterdic.items():
            if k == 'x' or k == 'y' or k == 'z':
                pass
            elif isinstance(v, linearalgebra.matrix):
                self.workspace.insert(INSERT, str(k) + ' : ' + str(v.matrix) + '\n')
            elif isinstance(v, linearalgebra.polynomial):
                self.workspace.insert(INSERT, str(k) + ' : ' + str(v.p) + '\n')
            else:
                self.workspace.insert(INSERT, str(k) + ' : ' + str(v) + '\n')
        self.workspace.config(state=DISABLED)

    def comment(self, iscomment):
        if iscomment['iscomment']:
            self.panel.tag_add('comment_tag', iscomment['comments'], 'end-1c')
            self.panel.tag_config('comment_tag', foreground='green')

    def command(self, event):
        cmd = self.panel.get(self.currentline, 'end-1c')
        self.comment(function.iscomment(cmd, self.currentline))
        no_comment_cmd = function.iscomment(cmd, self.currentline)['cmd']
        cmddic = function.command(no_comment_cmd)
        if cmddic['instruction'] == 'cleanmem':
            self.currentline = 1.0

        elif cmddic['instruction'] == 'clear':
            # self.panel.delete(1.0, END)
            # self.panel.mark_set(CURRENT, '1.0')
            self.panel = Text(self.frm1, height=2,font=("Helvetica", 20))
            self.panel.bind('<Return>', self.command)
            self.panel.grid(row=0, column=0, ipady=363, sticky=S)
            self.panel.mark_set(INSERT, '1.0')
            self.currentline = 1.0
            # self.outputline = 1.0
            self.inputline = 1.0

        elif cmddic['instruction'] == 'show':
            self.panel.tag_config('print_tag', foreground='blue')

            if isinstance(parameter.parameterdic[cmddic['varname']], linearalgebra.matrix):
                self.panel.insert(INSERT,'\nOut [' + str(int(self.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']].matrix), 'print_tag')
            elif isinstance(parameter.parameterdic[cmddic['varname']], linearalgebra.polynomial):
                self.panel.insert(INSERT,'\nOut [' + str(int(self.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']].p), 'print_tag')
            else:
                self.panel.insert(INSERT, '\nOut [' + str(int(self.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']]), 'print_tag')

            self.outputline += 1
            self.currentline += 2

        elif cmddic['instruction'] == 'assignvalue':
            self.currentline += 1

        elif cmddic['instruction'] == 'assignpoly':
            self.currentline += 1

        elif cmddic['instruction'] == 'evalpoly':
            self.panel.insert(INSERT, '\nOut [' + str(int(self.outputline)) + ']: ' + str(cmddic['ans']))
            self.outputline += 1
            self.currentline += 2

        elif cmddic['instruction'] == 'assignmatrix':
            self.panel.insert(INSERT, '\nOut [' + str(int(self.outputline)) + ']: ' + str(cmddic['var'].name) + ' = ' + str(parameter.parameterdic[cmddic['var'].name].matrix))
            # self.outputline += len(cmddic['var'].matrix)
            self.currentline += len(cmddic['var'].matrix)+1

        elif cmddic['instruction'] == 'polyerror':
            self.panel.tag_config('error_tag', foreground='red')
            self.panel.insert(INSERT, '\nPlease follow the format when you assign a polynomial: "polynomialname(symbol)" ', 'error_tag')
            # self.outputline += 1
            self.currentline += 2

        elif cmddic['instruction'] == 'default':
            self.currentline += 1
            self.updateworkspace()

        elif cmddic['instruction'] == 'error':
            self.panel.tag_config('error_tag', foreground='red')
            self.panel.insert(INSERT, '\nThere is an error in your input.', 'error_tag')
            # self.outputline += 1
            self.currentline += 2
        '''if not self.panel.get(self.currentline, 'end-1c'):
            self.panel.insert(INSERT, '\n')
            self.panel.insert(INSERT, 'In [' + str(int(self.inputline)) + ']: ')'''       # In [currentline]: 會多換一行
        self.updateworkspace()

    def makematrix(self, event):  # 建構矩陣
        if not self.matrixrowentry.get() \
           or not self.matrixcolentry.get() \
           or not self.matrixnameentry.get():
            messagebox.showerror('錯誤', '請輸入完整資訊')
            # 讓按下去的按鈕彈回來
        else:
            row = int(self.matrixrowentry.get())
            col = int(self.matrixcolentry.get())
            name = self.matrixnameentry.get()
            parameter.parameterdic[name] = linearalgebra.matrix(name, row, col)
            self.panel.insert(INSERT, 'Out [' + str(int(self.outputline)) + ']: ' + name + ' = ')
            self.panel.insert(INSERT, parameter.parameterdic[name].matrix)
            self.panel.insert(INSERT, '\n')
            self.currentline += 1
            self.outputline += 1
            self.matrix.destroy()

    def matrix_row_col(self):      # 輸入矩陣維度
        self.matrix = Tk()
        self.matrix.geometry('200x150+650+250')
        self.matrix.title("矩陣")
        self.matrix.iconbitmap('psl.ico')

        self.matrixnamelabel = Label(self.matrix, text = '  名稱: ')       # 矩陣文字標籤
        self.matrixrowlabel = Label(self.matrix, text = '  列: ')
        self.matrixcollabel = Label(self.matrix, text = '  行: ')

        self.matrixnamelabel.grid(row = 0, column = 0, sticky = E)
        self.matrixrowlabel.grid(row = 2, column = 0, sticky = E)
        self.matrixcollabel.grid(row = 4, column = 0, sticky = E)

        self.matrixnameentry = Entry(self.matrix)      # 輸入的矩陣名稱
        self.matrixrowentry = Entry(self.matrix)      # 輸入的列數
        self.matrixcolentry = Entry(self.matrix)      # 輸入的行數

        self.matrixnameentry.grid(row = 0, column = 2, sticky = E)
        self.matrixrowentry.grid(row = 2, column = 2, sticky = E)
        self.matrixcolentry.grid(row = 4, column = 2, sticky = E)

        self.matrixconfirm = Button(self.matrix, text = '確定')       # 確定按鈕
        self.matrixconfirm.bind('<Button-1>', self.makematrix)
        self.matrixcancel = Button(self.matrix, text = '取消')      # 取消按鈕
        self.matrixcancel.bind('<Button-1>', lambda _: self.matrix.destroy())

        self.matrixconfirm.grid(row = 6, column = 1)
        self.matrixcancel.grid(row = 6, column = 2)

        self.matrix.mainloop()

    def dotranspose(self, event):  # 建構轉置矩陣          先複製該矩陣，再作轉置，原本矩陣的名稱a，轉置過後的名稱a.transpose
        name = self.matrixTnameentry.get()
        row = parameter.parameterdic[name].row
        col = parameter.parameterdic[name].col
        if not parameter.parameterdic[name]:
            parameter.parameterdic[name] = linearalgebra.matrix(name, row, col)
        else:
            pass
        parameter.parameterdic[name].T()
        self.panel.insert(INSERT, 'Out [' + str(int(self.outputline)) + ']: ' + name + ' = ')
        self.panel.insert(INSERT, parameter.parameterdic[name].matrixT)
        self.panel.insert(INSERT, '\n')
        self.currentline += 1
        self.outputline += 1
        self.matrixT.destroy()

    def matrixtranspose(self):      # 轉置矩陣                              尚未防呆(當輸入未創建的物件名稱)
        self.matrixT = Tk()
        self.matrixT.geometry('150x80+650+250')
        self.matrixT.title("轉置矩陣")
        self.matrixT.iconbitmap('psl.ico')

        self.matrixTnamelabel = Label(self.matrixT, text = '  欲轉置的矩陣: ')
        self.matrixTnamelabel.grid(row = 2, column = 0, sticky = E)

        self.matrixTnameentry = Entry(self.matrixT)
        self.matrixTnameentry.grid(row = 2, column = 2, sticky = E)

        self.matrixTconfirm = Button(self.matrixT, text = '確定')
        self.matrixTconfirm.bind('<Button-1>', self.dotranspose)
        self.matrixTcancel = Button(self.matrixT, text = '取消')
        self.matrixTcancel.bind('<Button-1>', lambda _: self.matrixT.destroy())

        self.matrixTconfirm.grid(row = 6, column = 1)
        self.matrixTcancel.grid(row = 6, column = 2)

        self.matrixT.mainloop()

    def doinverse(self, event):  # 建構反矩陣                            尚未防呆(行列式為0)
        name = self.matrixInameentry.get()
        row = parameter.parameterdic[name].row
        col = parameter.parameterdic[name].col
        if not name \
                or not row \
                or not col \
                or not parameter.parameterdic[name] \
                or row != col:
            messagebox.showerror('錯誤', '輸入矩陣須為方陣')
        else:
            parameter.parameterdic[name + '.inverse'] = linearalgebra.matrix(name + '.transpose', row, col)
            name = name + '.inverse'
            parameter.parameterdic[name].I()
            self.panel.insert(INSERT, 'Out [' + str(int(self.outputline)) + ']: ' + name + ' = ')
            self.panel.insert(INSERT, parameter.parameterdic[name].matrix)
            self.panel.insert(INSERT, '\n')
            self.currentline += 1
            self.outputline += 1
            self.matrixI.destroy()

    def matrixinverse(self):

        self.matrixI = Tk()
        self.matrixI.geometry('150x80+650+250')
        self.matrixI.title("轉置矩陣")
        self.matrixI.iconbitmap('psl.ico')

        self.matrixInamelabel = Label(self.matrixI, text = '  欲轉置的矩陣: ')
        self.matrixInamelabel.grid(row = 2, column = 0, sticky = E)

        self.matrixInameentry = Entry(self.matrixI)
        self.matrixInameentry.grid(row = 2, column = 2, sticky = E)

        self.matrixIconfirm = Button(self.matrixI, text = '確定')
        self.matrixIconfirm.bind('<Button-1>', self.doinverse)
        self.matrixIcancel = Button(self.matrixI, text = '取消')
        self.matrixIcancel.bind('<Button-1>', lambda _: self.matrixI.destroy())

        self.matrixIconfirm.grid(row = 6, column = 1)
        self.matrixIcancel.grid(row = 6, column = 2)

        self.matrixI.mainloop()

    def dodeterminate(self, event):
        name = self.matrixDnameentry.get()
        row = parameter.parameterdic[name].row
        col = parameter.parameterdic[name].col
        if not parameter.parameterdic[name] or row != col:
            messagebox.showerror('錯誤', '輸入矩陣須為方陣')
        else:
            parameter.parameterdic[name].D()
            parameter.parameterdic['det(' + name + ')'] = parameter.parameterdic[name].matrixD
            self.panel.insert(INSERT, 'Out [' + str(int(self.outputline)) + ']: ' + 'det(' + name + ') = ')
            self.panel.insert(INSERT, parameter.parameterdic['det(' + name + ')'])
            self.panel.insert(INSERT, '\n')
            self.currentline += 1
            self.outputline += 1
            self.matrixD.destroy()

    def matrixdeterminate(self):
        self.matrixD = Tk()
        self.matrixD.geometry('150x80+650+250')
        self.matrixD.title("行列式")
        self.matrixD.iconbitmap('psl.ico')

        self.matrixDnamelabel = Label(self.matrixD, text = '  矩陣: ')
        self.matrixDnamelabel.grid(row = 2, column = 0, sticky = E)

        self.matrixDnameentry = Entry(self.matrixD)
        self.matrixDnameentry.grid(row = 2, column = 2, sticky = E)

        self.matrixDconfirm = Button(self.matrixD, text = '確定')
        self.matrixDconfirm.bind('<Button-1>', self.dodeterminate)
        self.matrixDcancel = Button(self.matrixD, text = '取消')
        self.matrixDcancel.bind('<Button-1>', lambda _: self.matrixD.destroy())

        self.matrixDconfirm.grid(row = 6, column = 1)
        self.matrixDcancel.grid(row = 6, column = 2)

        self.matrixD.mainloop()

    def differential(self, event):      # 微分

        # 防呆(輸入多項式中沒有出現的符號)

        if not self.difpolynomialnameentry.get() \
           or not self.difpolynomialentry.get() \
           or not self.differentialsymbolentry.get() \
           or not self.timesentry.get():
            messagebox.showerror('錯誤', '請輸入完整資訊')
            # 讓按下去的按鈕彈回來
        else:
            name = self.difpolynomialnameentry.get()
            p = self.difpolynomialentry.get()
            symbol = self.differentialsymbolentry.get()
            times = int(self.timesentry.get())
            parameter.parameterdic[name] = linearalgebra.polynomial(name, p, symbol)
            parameter.parameterdic[name].dif(times)
            parameter.parameterdic[name + '.dif'] = parameter.parameterdic[name].dif
            self.panel.insert(INSERT, 'Out [' + str(int(self.outputline)) + ']: ' + name + '.dif' + ' = ')
            self.panel.insert(INSERT, parameter.parameterdic[name + '.dif'])
            self.panel.insert(INSERT, '\n')
            self.currentline += 1
            self.outputline += 1
            self.dif.destroy()

    def differentation(self):
        self.dif = Tk()
        self.dif.geometry('200x150+650+250')
        self.dif.title("微分")
        self.dif.iconbitmap('psl.ico')

        self.difpolynomialnamelabel = Label(self.dif, text = ' 名稱: ')        # 多項式文字標籤
        self.difpolynomiallabel = Label(self.dif, text = '  多項式: ')
        self.differentialsymbollabel = Label(self.dif, text = '  變數: ')
        self.timeslabel = Label(self.dif, text = ' 微分次數: ')

        self.difpolynomialnamelabel.grid(row = 0, column = 0, sticky = E)
        self.difpolynomiallabel.grid(row = 2, column = 0, sticky = E)
        self.differentialsymbollabel.grid(row = 4, column = 0, sticky = E)
        self.timeslabel.grid(row = 6, column = 0, sticky = E)

        self.difpolynomialnameentry = Entry(self.dif, width = 13)      # 輸入的多項式名稱
        self.difpolynomialentry = Entry(self.dif, width = 13)        # 輸入的多項式
        self.differentialsymbolentry = Entry(self.dif, width = 13 )      # 輸入的微分的變數
        self.timesentry = Entry(self.dif, width = 13)     # 輸入的微分次數

        self.difpolynomialnameentry.grid(row = 0, column = 1, sticky = E)
        self.difpolynomialentry.grid(row = 2, column = 1, sticky = E)
        self.differentialsymbolentry.grid(row = 4, column = 1, sticky = E)
        self.timesentry.grid(row = 6, column = 1, sticky = E)

        self.differentialconfirm = Button(self.dif, text = '確定')      # 確定按鈕
        self.differentialconfirm.bind('<Button-1>', self.differential)
        self.differentialcancel = Button(self.dif, text = '取消')       # 取消按鈕
        self.differentialcancel.bind('<Button-1>', lambda _: self.dif.destroy())
        # Label(self.dif, text = '').grid(row = 8, column = 2)
        self.differentialconfirm.grid(row = 10, column = 1)
        self.differentialcancel.grid(row = 10, column = 2)

        self.dif.mainloop()

    def integral(self,event):
        if self.checkSvar.get():        # 定積分
            if not self.intpolynomialnameentry.get() \
               or not self.intpolynomialnameentry.get() \
               or not self.intpolynomialentry.get() \
               or not self.lowerboundentry.get() \
               or not self.upperboundentry.get():
                messagebox.showerror('錯誤', '請輸入完整資訊')
            else:
                name = self.intpolynomialnameentry.get()
                p = self.intpolynomialentry.get()
                symbol = self.integrationsymbolentry.get()
                upperbound = self.upperboundentry.get()
                lowerbound = self.lowerboundentry.get()
                parameter.parameterdic[name] = linearalgebra.polynomial(name, p, symbol)
                parameter.parameterdic[name].S(upperbound, lowerbound)
                parameter.parameterdic[name + '.definite_S'] = parameter.parameterdic[name].S
                self.panel.insert(INSERT, 'Out [' + str(int(self.outputline)) + ']: ' + name + '.definite_S' + ' = ')
                self.panel.insert(INSERT, parameter.parameterdic[name + '.definite_S'])
                self.panel.insert(INSERT, '\n')
                self.currentline += 1
                self.outputline += 1
                self.S.destroy()
        else:       # 不定積分
            if not self.intpolynomialnameentry.get() \
               or not self.integrationsymbolentry.get() \
               or not self.intpolynomialentry.get():
                messagebox.showerror('錯誤', '請輸入完整資訊')
            else:
                name = self.intpolynomialnameentry.get()
                p = self.intpolynomialentry.get()
                symbol = self.integrationsymbolentry.get()
                parameter.parameterdic[name] = linearalgebra.polynomial(name, p, symbol)
                parameter.parameterdic[name].S()
                parameter.parameterdic[name + '.S'] = parameter.parameterdic[name].S
                self.panel.insert(INSERT, 'Out [' + str(int(self.outputline)) + ']: ' + name + '.S' + ' = ')
                self.panel.insert(INSERT, parameter.parameterdic[name + '.S'])
                self.panel.insert(INSERT, '\n')
                self.currentline += 1
                self.outputline += 1
                self.S.destroy()

    def checkintegral(self):  # 檢查是否為定積分
        isintegral = self.checkSvar.get()
        if function.isintegral(isintegral):
            self.checkSvar.set(0)
            self.upperboundentry.configure(state = DISABLED)
            self.lowerboundentry.configure(state = DISABLED)
        else:
            self.checkSvar.set(1)
            self.upperboundentry.configure(state = NORMAL)
            self.lowerboundentry.configure(state = NORMAL)

    def integration(self):
        self.S = Tk()
        self.S.geometry('300x250+650+250')
        self.S.title("積分")
        self.S.iconbitmap('psl.ico')

        self.intpolynomialnamelabel = Label(self.S, text = ' 名稱: ')  # 多項式文字標籤
        self.intpolynomiallabel = Label(self.S, text = '  多項式: ')
        self.integrationsymbollabel = Label(self.S, text = '  變數: ')
        self.upperboundlabel = Label(self.S, text = ' 上界: ')
        self.lowerboundlabel = Label(self.S, text = ' 下界: ')

        self.intpolynomialnamelabel.grid(row = 0, column = 0, sticky = E)
        self.intpolynomiallabel.grid(row = 2, column = 0, sticky = E)
        self.integrationsymbollabel.grid(row = 4, column = 0, sticky = E)
        self.upperboundlabel.grid(row = 8, column = 0, sticky = E)
        self.lowerboundlabel.grid(row = 10, column = 0, sticky = E)

        self.intpolynomialnameentry = Entry(self.S, width = 13)      # 輸入的多項式名稱
        self.intpolynomialentry = Entry(self.S, width = 13)      # 輸入的多項式
        self.integrationsymbolentry = Entry(self.S, width = 13)     # 輸入的積分的變數
        self.upperboundentry = Entry(self.S, width = 13, state = DISABLED)      # 輸入定積分的上界
        self.lowerboundentry = Entry(self.S, width = 13, state = DISABLED)      # 輸入定積分的下界

        self.intpolynomialnameentry.grid(row = 0, column = 1, sticky = E)
        self.intpolynomialentry.grid(row = 2, column = 1, sticky = E)
        self.integrationsymbolentry.grid(row = 4, column = 1, sticky = E)
        self.upperboundentry.grid(row = 8, column = 1, sticky = E)
        self.lowerboundentry.grid(row = 10, column = 1, sticky = E)

        self.checkSvar = IntVar()
        self.checkS = Checkbutton(self.S, text = '定積分', variable = self.checkSvar, command = self.checkintegral)
        self.checkS.grid(row = 6, columnspan = 2, sticky = E)

        self.differentialconfirm = Button(self.S, text = '確定')  # 確定按鈕
        self.differentialconfirm.bind('<Button-1>', self.integral)
        self.differentialcancel = Button(self.S, text = '取消')  # 取消按鈕
        self.differentialcancel.bind('<Button-1>', lambda _: self.S.destroy())
        self.differentialconfirm.grid(row = 12, column = 1)
        self.differentialcancel.grid(row = 12, column = 2)

        self.S.mainloop()

    def doplot(self, event):
        xlowerbound = int(self.xlowerboundentry.get())
        xupperbound = int(self.xupperboundentry.get()) + 1
        formulas = self.formulaentry.get().split(',')

        function.plot(xlowerbound, xupperbound, formulas)


        self.draw.destroy()


    def plot(self):
        self.draw = Tk()
        self.draw.geometry('300x250+650+250')
        self.draw.title("繪圖")
        self.draw.iconbitmap('psl.ico')

        self.formulalabel = Label(self.draw, text='  方程式: ')
        self.xlabel = Label(self.draw, text='  x的範圍: ')


        Label(self.draw, text = ' ').grid(row = 0, column = 0, sticky = E)
        self.formulalabel.grid(row = 2, column = 0, sticky = E)
        self.xlabel.grid(row = 4, column = 0, sticky = E)
        Label(self.draw, text = '~').grid(row = 4, column = 2, sticky = E)


        self.formulaentry = Entry(self.draw, width = 13)
        self.xlowerboundentry = Entry(self.draw, width = 13)
        self.xupperboundentry = Entry(self.draw, width = 13)


        self.formulaentry.grid(row=2, column=1, sticky=E)
        self.xlowerboundentry.grid(row=4, column=1, sticky=E)
        self.xupperboundentry.grid(row=4, column=3, sticky=E)



        self.drawconfirm = Button(self.draw, text='確定')  # 確定按鈕
        self.drawconfirm.bind('<Button-1>', self.doplot)
        self.drawcancel = Button(self.draw, text='取消')  # 取消按鈕
        self.drawcancel.bind('<Button-1>', lambda _: self.draw.destroy())
        Label(self.draw, text=' ').grid(row=6, column=1, sticky=E)
        self.drawconfirm.grid(row=20, column=1)
        self.drawcancel.grid(row=20, column=2)

        self.draw.mainloop()

    def init_window(self):      # 初始化介面
        self.master.state('zoomed')
        self.master.title("還沒想好名字")  # 檔案名稱(還沒想)
        self.master.iconbitmap('psl.ico')  # 設定實驗室logo
        self.frm1.grid_columnconfigure(0, weight=1)
        self.frm1.grid_rowconfigure(0, weight=1)
        '''When using grid, any extra space in the parent is allocated proportionate to the "weight" of a row and/or a column (ie: a column with a weight of 2 gets twice as much of the space as one with a weight of 1). 
           By default, rows and columns have a weight of 0 (zero), meaning no extra space is given to them.
           You need to give the column that the widget is in a non-zero weight, so that any extra space when the window grows is allocated to that column.
           root.grid_columnconfigure(0, weight=1)
           You'll also need to specify a weight for the row, and a sticky value of N+S+E+W if you want it to grow in all directions.'''

        # messagebox.showinfo('歡迎!!!', '歡迎進入本數學軟體')
        self.toolbar = Menu(self.master)

        self.tool0 = Menu(self.toolbar, tearoff = 0)  # 工具列 1
        self.toolbar.add_cascade(label = '檔案', menu = self.tool0)

        self.tool0.add_command(label = '新增檔案', command = self.hello)
        self.tool0.add_command(label = '開啟檔案', command = self.hello)
        self.tool0.add_command(label = '另存新檔', command = self.hello)

        self.tool1 = Menu(self.toolbar, tearoff=0)  # 工具列 2
        self.toolbar.add_cascade(label = '代數', menu = self.tool1)

        self.tool1.add_command(label = '產生零矩陣', command = self.matrix_row_col)
        self.tool1.add_command(label = '反矩陣', command = self.matrixinverse)
        self.tool1.add_command(label = '行列式', command = self.matrixdeterminate)
        self.tool1.add_command(label = '轉置矩陣', command = self.matrixtranspose)
        # tool1.add_command(label = '上三角矩陣', command = hello)
        # tool1.add_command(label = '因式分解', command = hello)
        # tool1.add_command(label = '展開式', command = hello)
        # tool1.add_command(label = '化簡', command = hello)

        self.tool2 = Menu(self.toolbar, tearoff = 0)  # 工具列 3
        self.toolbar.add_cascade(label = '微積分', menu = self.tool2)

        self.tool2.add_command(label = '微分', command = self.differentation)
        self.tool2.add_command(label = '積分', command = self.integration)

        # tool2.add_command(label = '泰勒展開式')

        self.tool2.add_command(label = '極值')

        self.tool3 = Menu(self.toolbar, tearoff=0)  # 工具列 4
        self.toolbar.add_cascade(label='繪圖', menu=self.tool3)

        self.tool3.add_command(label='二維繪圖', command=self.plot)

        self.master.config(menu = self.toolbar)

        self.panel = Text(self.frm1, height = 2, font = ("Helvetica", 20))     # 文字面板 ------------------------------> 使用者輸入指令
        # self.panel.insert(INSERT, 'In [' + str(int(self.inputline)) + ']: ')
        self.panel.bind('<Return>', self.command)
        self.panel.grid(row=0, column=0, ipady=363, sticky=S)


        self.workspace = Text(self.frm2, height=2, font=("Helvetica", 20))      # workspace
        self.workspace.grid(row=0, column=0, ipady=363, sticky=S)

        '''Since your window only contains one widget and you want this widget to fill the entire window, 
           it would be easier to use the pack geometry manager instead of grid
           input_text_area.pack(expand=True, fill='both')
           expand=True tells Tkinter to allow the widget to expand to fill any extra space in the geometry master. 
           fill='both' enables the widget to expand both horizontally and vertically.'''


# if __main__ == '__main__':
#     root = Tk()
#
#     root.geometry('400x300')
#
#     app = gui.GUI(root)
#
#     mainloop()
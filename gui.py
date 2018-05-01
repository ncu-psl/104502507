from tkinter import *
from tkinter import messagebox, simpledialog, filedialog
import fileinput
import linearalgebra
import os
import parameter

import function
import speak


class GUI(object):

    def __init__(self, master, width, height):
        self.master = master
        self.width = width
        self.height = height
        self.panelframe = Frame(self.master)
        self.workspaceframe = Frame(self.master)
        self.panelframe.grid(row=1, column=0, columnspan=self.width)
        self.workspaceframe.grid(row=1, column=self.width)
        self.init_window()

    def icon_bar(self):
        self.tool_bar_copy = PhotoImage(file='/home/alvin_zhan/中央大學/三年級/專題/icons/copy.png')
        self.tool_bar3 = Button(self.master, image=self.tool_bar_copy, command=self.copy)
        self.tool_bar3.grid(row=0, column=0, columnspan=1, sticky=W)

        self.tool_bar_cut = PhotoImage(file='/home/alvin_zhan/中央大學/三年級/專題/icons/cut.png')
        self.tool_bar1 = Button(self.master, image=self.tool_bar_cut, command=self.cut)
        self.tool_bar1.grid(row=0, column=1, columnspan=1, sticky=W)

        self.tool_bar_paste = PhotoImage(file='/home/alvin_zhan/中央大學/三年級/專題/icons/paste.png')
        self.tool_bar2 = Button(self.master, image=self.tool_bar_paste, command=self.paste)
        self.tool_bar2.grid(row=0, column=2, columnspan=1, sticky=W)

        self.tool_bar_search = PhotoImage(file='/home/alvin_zhan/中央大學/三年級/專題/icons/search.png')
        self.tool_bar2 = Button(self.master, image=self.tool_bar_search, command=self.search)
        self.tool_bar2.grid(row=0, column=3, columnspan=1, sticky=W)

        self.tool_bar_speak = PhotoImage(file='/home/alvin_zhan/中央大學/三年級/專題/icons/speak.png')
        self.tool_bar2 = Button(self.master, image=self.tool_bar_speak, command=self.speak)
        self.tool_bar2.grid(row=0, column=4, columnspan=1, sticky=W)

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
        cmd = self.panel.get(parameter.currentline, 'end-1c')
        self.comment(function.iscomment(cmd, parameter.currentline))
        no_comment_cmd = function.iscomment(cmd, parameter.currentline)['cmd']
        cmddic = function.command(no_comment_cmd)
        if cmddic['instruction'] == 'cleanmem':
            parameter.currentline = 1.0
        elif cmddic['instruction'] == 'clear':
            self.panel = Text(self.panelframe, height=20,font=("Helvetica", 20))
            self.panel.bind('<Return>', self.command)
            self.panel.grid(row=1, column=0, ipady=self.height, sticky=S)
            self.panel.mark_set(INSERT, '1.0')
            parameter.currentline = 1.0
            # self.outputline = 1.0
            parameter.inputline = 1.0

        elif cmddic['instruction'] == 'show':
            self.panel.tag_config('print_tag', foreground='blue')
            try:
                if isinstance(parameter.parameterdic[cmddic['varname']], linearalgebra.matrix):
                    self.console.insert(INSERT,'\nOut [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']].matrix), 'print_tag')
                elif isinstance(parameter.parameterdic[cmddic['varname']], linearalgebra.polynomial):
                    self.console.insert(INSERT,'\nOut [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']].p), 'print_tag')
                else:
                    self.console.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']]), 'print_tag')
            except:
                ans = eval(cmddic['varname'], parameter.parameterdic)
                self.panel.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(ans))
            parameter.outputline += 1
            parameter.currentline += 2

        elif cmddic['instruction'] == 'assignvalue':
            parameter.currentline += 1
            self.updateworkspace()

        elif cmddic['instruction'] == 'assignpoly':
            parameter.currentline += 1
            self.updateworkspace()

        elif cmddic['instruction'] == 'evalpoly':
            self.panel.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + str(cmddic['ans']))
            parameter.outputline += 1
            parameter.currentline += 2

        elif cmddic['instruction'] == 'assignmatrix':
            self.panel.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + str(cmddic['var'].name) + ' = ' + str(parameter.parameterdic[cmddic['var'].name].matrix))
            # self.outputline += len(cmddic['var'].matrix)
            parameter.currentline += len(cmddic['var'].matrix)+1
            self.updateworkspace()

        elif cmddic['instruction'] == 'polyerror':
            self.panel.tag_config('error_tag', foreground='red')
            self.panel.insert(INSERT, '\nPlease follow the format when you assign a polynomial: "polynomialname(symbol)" ', 'error_tag')
            # parameter.outputline += 1
            parameter.currentline += 2

        elif cmddic['instruction'] == 'default':
            parameter.currentline += 1
            self.updateworkspace()

        elif cmddic['instruction'] == 'error':
            self.panel.tag_config('error_tag', foreground='red')
            self.panel.insert(INSERT, '\nThere is an error in your input.', 'error_tag')
            # parameter.outputline += 1
            parameter.currentline += 2
        '''if not self.panel.get(parameter.currentline, 'end-1c'):
            self.panel.insert(INSERT, '\n')
            self.panel.insert(INSERT, 'In [' + str(int(self.inputline)) + ']: ')'''       # In [currentline]: 會多換一行

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
            self.panel.insert(INSERT, 'Out [' + str(int(parameter.outputline)) + ']: ' + name + ' = ')
            self.panel.insert(INSERT, parameter.parameterdic[name].matrix)
            self.panel.insert(INSERT, '\n')
            parameter.currentline += 1
            parameter.outputline += 1
            self.matrix.destroy()

    def matrix_row_col(self):      # 輸入矩陣維度
        self.matrix = Tk()
        self.matrix.geometry('200x150+650+250')
        self.matrix.title("矩陣")
        # self.matrix.iconbitmap('psl.xbm')

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
        self.panel.insert(INSERT, 'Out [' + str(int(parameter.outputline)) + ']: ' + name + ' = ')
        self.panel.insert(INSERT, parameter.parameterdic[name].matrixT)
        self.panel.insert(INSERT, '\n')
        parameter.currentline += 1
        parameter.outputline += 1
        self.matrixT.destroy()

    def matrixtranspose(self):      # 轉置矩陣                              尚未防呆(當輸入未創建的物件名稱)
        self.matrixT = Tk()
        self.matrixT.geometry('150x80+650+250')
        self.matrixT.title("轉置矩陣")
        # self.matrixT.iconbitmap('psl.xbm')

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
            self.panel.insert(INSERT, 'Out [' + str(int(parameter.outputline)) + ']: ' + name + ' = ')
            self.panel.insert(INSERT, parameter.parameterdic[name].matrix)
            self.panel.insert(INSERT, '\n')
            parameter.currentline += 1
            parameter.outputline += 1
            self.matrixI.destroy()

    def matrixinverse(self):

        self.matrixI = Tk()
        self.matrixI.geometry('150x80+650+250')
        self.matrixI.title("轉置矩陣")
        # self.matrixI.iconbitmap('psl.xbm')

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
            self.panel.insert(INSERT, 'Out [' + str(int(parameter.outputline)) + ']: ' + 'det(' + name + ') = ')
            self.panel.insert(INSERT, parameter.parameterdic['det(' + name + ')'])
            self.panel.insert(INSERT, '\n')
            parameter.currentline += 1
            parameter.outputline += 1
            self.matrixD.destroy()

    def matrixdeterminate(self):
        self.matrixD = Tk()
        self.matrixD.geometry('150x80+650+250')
        self.matrixD.title("行列式")
        # self.matrixD.iconbitmap('psl.xbm')

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
            self.panel.insert(INSERT, 'Out [' + str(int(parameter.outputline)) + ']: ' + name + '.dif' + ' = ')
            self.panel.insert(INSERT, parameter.parameterdic[name + '.dif'])
            self.panel.insert(INSERT, '\n')
            parameter.currentline += 1
            parameter.outputline += 1
            self.dif.destroy()

    def differentation(self):
        self.dif = Tk()
        self.dif.geometry('200x150+650+250')
        self.dif.title("微分")
        # self.dif.iconbitmap('psl.xbm')

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
                self.panel.insert(INSERT, 'Out [' + str(int(parameter.outputline)) + ']: ' + name + '.definite_S' + ' = ')
                self.panel.insert(INSERT, parameter.parameterdic[name + '.definite_S'])
                self.panel.insert(INSERT, '\n')
                parameter.currentline += 1
                parameter.outputline += 1
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
                self.panel.insert(INSERT, 'Out [' + str(int(parameter.outputline)) + ']: ' + name + '.S' + ' = ')
                self.panel.insert(INSERT, parameter.parameterdic[name + '.S'])
                self.panel.insert(INSERT, '\n')
                parameter.currentline += 1
                parameter.outputline += 1
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

    def find_limit(self, event):
        if self.limitpolynomialentry.get()\
           and self.limitsymbolentry.get()\
           and self.limitnumentry.get():
            try:
                if not parameter.parameterdic[self.limitpolynomialentry.get()]:
                    pass
                else:
                    name = self.limitpolynomialentry.get()
                    symbol = self.limitsymbolentry.get()
                    num = int(self.limitnumentry.get())
                    ans = parameter.parameterdic[name].l(symbol, num)
                    self.panel.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + str(ans))
                    self.limit.destroy()
            except KeyError:
                if self.limitsymbolentry.get() not in self.limitpolynomialentry.get():
                    raise NameError
                else:
                    poly = self.limitpolynomialentry.get()
                    symbol = self.limitsymbolentry.get()
                    num = int(self.limitnumentry.get())
                    name = 'user_var' + str(parameter.user_var)
                    temp = linearalgebra.polynomial(name, poly,symbol)
                    parameter.user_var += 1
                    ans = temp.l(symbol, num)
                    self.panel.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + str(ans))
                    self.limit.destroy()
            except NameError:
                messagebox.showerror('錯誤', '請輸入正確資訊')
                self.limit.destroy()
        else:
            messagebox.showerror('錯誤', '請輸入完整資訊')
            # self.limit.destroy()

    def limit_gui(self):
        self.limit = Tk()
        self.limit.geometry('300x250+650+250')
        self.limit.title("極限")

        self.limitpolynomiallabel = Label(self.limit, text='  多項式: ')
        self.limitsymbollabel = Label(self.limit, text='  變數: ')
        self.limitnumlabel = Label(self.limit, text='  趨近於: ')

        self.limitpolynomiallabel.grid(row=2, column=0, sticky=E)
        self.limitsymbollabel.grid(row=4, column=0, sticky=E)
        self.limitnumlabel.grid(row=6, column=0, sticky=E)

        self.limitpolynomialentry = Entry(self.limit, width=13)
        self.limitsymbolentry = Entry(self.limit, width=13)
        self.limitnumentry = Entry(self.limit, width=13)

        self.limitpolynomialentry.grid(row=2, column=1, sticky=E)
        self.limitsymbolentry.grid(row=4, column=1, sticky=E)
        self.limitnumentry.grid(row=6, column=1, sticky=E)

        confirm = Button(self.limit, text='確定')  # 確定按鈕
        confirm.bind('<Button-1>', self.find_limit)
        cancel = Button(self.limit, text='取消')  # 取消按鈕
        cancel.bind('<Button-1>', lambda _: self.limit.destroy())
        confirm.grid(row=12, column=1)
        cancel.grid(row=12, column=2)

        self.limit.mainloop()

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

    def cut(self):
        try:
            text = self.panel.get(SEL_FIRST, SEL_LAST)
            self.panel.delete(SEL_FIRST, SEL_LAST)
            self.panel.clipboard_clear()
            self.panel.clipboard_append(text)
        except:
            pass

    def paste(self):
        try:
            text = self.panel.selection_get(selection="CLIPBOARD")
            self.panel.insert(INSERT, text)
            self.panel.clipboard_clear()
        except:
            pass

    def copy(self):
        try:
            text = self.panel.get(SEL_FIRST, SEL_LAST)
            self.panel.clipboard_clear()
            self.panel.clipboard_append(text)
        except:
            pass

    def search(self):
        target = simpledialog.askstring("搜尋", "尋找字符串", parent=self.master)
        if target:
            end = self.panel.index(END)
            endindex = end.split(".")
            end_line = int(endindex[0])
            end_column = int(endindex[1])
            pos_line = 1
            pos_column = 0
            length = len(target)
            while pos_line <= end_line:
                if pos_line == end_line and pos_column + length > end_column:
                    break
                elif pos_line < end_line and pos_column + length > 500:
                    pos_line = pos_line + 1
                    pos_column = (pos_column + length) - 500
                    if pos_column > end_column:
                        break
                else:
                    pos = str(pos_line) + "." + str(pos_column)
                    where = self.panel.search(target, pos, END)
                    if where:
                        where1 = where.split(".")
                        sele_end_col = str(int(where1[1]) + length)
                        sele = where1[0] + "." + sele_end_col
                        self.panel.tag_add(SEL, where, sele)
                        self.panel.mark_set(INSERT, sele)
                        self.panel.see(INSERT)
                        self.panel.focus()

                        pos_line = int(where1[0])
                        pos_column = int(sele_end_col)
                    else:
                        break

    def openfile(self):
        oname = filedialog.askopenfilename(filetypes=[("打開文件", "*.txt")])
        if oname:
            for line in fileinput.input(oname):
                self.panel.insert(1.0, line)
            self.master.title(oname + ' - NCUproject')

    def savefile(self):
        if os.path.isfile(self.master.title()):
            opf = open(self.master.title(), "w")
            opf.write(self.panel.get(1.0, END))
            opf.flush()
            opf.close()
        else:
            filename = filedialog.asksaveasfilename(title="儲存檔案", filetypes=[("文字文件", "*.txt")], defaultextension=".txt")
            if filename:
                ofp = open(filename, "w")
                ofp.write(self.panel.get(1.0, END))
                ofp.flush()
                ofp.close()
            self.master.title(filename + ' - NCUproject')

    def saveasfile(self):
        filename = filedialog.asksaveasfilename(title="另存新檔", filetypes=[("文字文件", "*.txt")], defaultextension=".txt")
        if filename:
            ofp = open(filename, "w")
            ofp.write(self.panel.get(1.0, END))
            ofp.flush()
            ofp.close()
            self.master.title(filename + ' - NCUproject')

    def speak(self):
        service = speak.speak()
        if service >= 0:
            exec(speak.functions[service])
        else:
            messagebox.showerror('錯誤', '請再說清楚一些')
        self.updateworkspace()

    def init_window(self):
        self.master.state('normal')
        self.master.title("NCUproject")

        # messagebox.showinfo('歡迎!!!', '歡迎進入本數學軟體')
        self.toolbar = Menu(self.master, font=30)


        self.tool0 = Menu(self.toolbar, tearoff = 0, font=30)  # 工具列 1
        self.toolbar.add_cascade(label = '檔案', menu = self.tool0)

        self.tool0.add_command(label='開啟新檔', command = self.openfile)
        self.tool0.add_command(label='儲存檔案', command=self.savefile)
        self.tool0.add_command(label='另存新檔', command = self.saveasfile)

        self.tool1 = Menu(self.toolbar, tearoff=0, font=30)  # 工具列 2
        self.toolbar.add_cascade(label = '代數', menu = self.tool1)

        self.tool1.add_command(label = '產生零矩陣', command = self.matrix_row_col)
        self.tool1.add_command(label = '反矩陣', command = self.matrixinverse)
        self.tool1.add_command(label = '行列式', command = self.matrixdeterminate)
        self.tool1.add_command(label = '轉置矩陣', command = self.matrixtranspose)
        # tool1.add_command(label = '上三角矩陣', command = hello)
        # tool1.add_command(label = '因式分解', command = hello)
        # tool1.add_command(label = '展開式', command = hello)
        # tool1.add_command(label = '化簡', command = hello)

        self.tool2 = Menu(self.toolbar, tearoff = 0, font=30)  # 工具列 3
        self.toolbar.add_cascade(label = '微積分', menu = self.tool2)

        self.tool2.add_command(label = '微分', command = self.differentation)
        self.tool2.add_command(label = '積分', command = self.integration)

        # tool2.add_command(label = '泰勒展開式')

        self.tool2.add_command(label = '極值', command=self.limit_gui)

        self.tool3 = Menu(self.toolbar, tearoff=0, font=30)  # 工具列 4
        self.toolbar.add_cascade(label='繪圖', menu=self.tool3)

        self.tool3.add_command(label='二維繪圖', command=self.plot)

        self.master.config(menu = self.toolbar)

        self.icon_bar()

        self.panel = Text(self.panelframe, height=20, font = ("Helvetica", 20))     # text panel
        self.panel.bind('<Return>', self.command)
        self.panel.grid(row=0, column=0)

        self.workspace = Text(self.workspaceframe, height=48, font=("Helvetica", 12))      # workspace
        self.workspace.grid(row=0, column=0)

        self.console = Text(self.panelframe, height=10, font=("Helvetica", 20), bg='black', fg='white')        # console
        self.console.grid(row=1, column=0)
import matplotlib
matplotlib.use("TkAgg")
from tkinter import *
from tkinter import messagebox, simpledialog, filedialog
import fileinput
import os


import function
import matrix
import polynomial
import parameter
import speak



class GUI(object):

    def __init__(self, master, width, height):
        self.master = master
        self.width = width
        self.height = height
        self.panelframe = Frame(self.master)
        self.workspaceframe = Frame(self.master)
        self.icon = Frame(self.master)
        self.icon.grid(row=0, column=0)
        self.panelframe.grid(row=1, column=0, columnspan=self.width, sticky=N)
        self.workspaceframe.grid(row=1, column=self.width+1, sticky=N)
        self.icon_bar()
        self.init_window()

    def icon_bar(self):
        photo_func = [
            ('copy', self.copy, 0),
            ('cut', self.cut, 1),
            ('paste', self.paste, 2),
            ('undo', self.undo, 3),
            ('redo', self.redo, 4),
            ('search', self.search, 5),
            ('speak', self.speak, 6),

        ]
        for photo,func,num in photo_func:
            tool_bar_copy = PhotoImage(file='/home/alvin_zhan/中央大學/三年級/專題/icons/' + photo + '.png')
            tool_icon = Button(self.icon, image=tool_bar_copy, command=func)
            tool_icon.image = tool_bar_copy
            tool_icon.grid(row=0, column=num, sticky=W)

    def updateworkspace(self):
        self.workspace.config(state=NORMAL)
        self.workspace.delete('1.0', END)
        for k,v in parameter.parameterdic.items():
            if k == 'x' or k == 'y' or k == 'z' or callable(v):
                pass
            else:
                self.workspace.insert(INSERT, str(k) + ' : ' + str(v) + '\n')
            # if k == 'x' or k == 'y' or k == 'z':
            #     pass
            # elif isinstance(v, linearalgebra.matrix):
            #     self.workspace.insert(INSERT, str(k) + ' : ' + str(v.matrix) + '\n')
            # elif isinstance(v, linearalgebra.polynomial):
            #     self.workspace.insert(INSERT, str(k) + ' : ' + str(v.p) + '\n')
            # else:
            #     self.workspace.insert(INSERT, str(k) + ' : ' + str(v) + '\n')
        self.workspace.config(state=DISABLED)

    def comment(self, commentdic):
        if commentdic['iscomment']:
            self.panel.tag_add('comment_tag', commentdic['comments'], 'end-1c')
            self.panel.tag_config('comment_tag', foreground='green')

    def newline(self, event):
        parameter.inputline += 1
        self.panel.insert(INSERT, 'In [' + str(int(parameter.inputline)) + ']: ')

    def command(self, event):
        self.console.config(state=NORMAL)
        cmd = self.panel.get(parameter.currentline, 'end-1c')
        self.comment(function.iscomment(cmd, parameter.inputline))
        cmd = cmd.split(':')[1]
        for i in range(len(cmd)):
            if cmd[i] != ' ' and cmd[i] != '\t':
                cmd = cmd[i:]
                break
        no_comment_cmd = function.iscomment(cmd, parameter.inputline)['cmd']
        cmddic = function.command(no_comment_cmd)
        if cmddic['instruction'] == 'cleanmem':
            parameter.currentline += 1.0
            self.updateworkspace()
        elif cmddic['instruction'] == 'clear':
            parameter.currentline = 1.0
            parameter.inputline = 1.0
            self.panel = Text(self.panelframe, height=20, font=("Helvetica", 20), undo=True)  # text panel
            self.panel.insert(INSERT, 'In [' + str(int(parameter.inputline)) + ']: ')
            self.panel.bind('<Return>', self.command)
            # self.panel.bind('<KeyRelease-Return>', self.newline)
            # self.panel.bind('<Button-3>', self.rClicker)
            self.panel.grid(row=0, column=0)

            self.console = Text(self.panelframe, height=10, font=("Helvetica", 20), bg='black', fg='white')  # console
            self.console.config(state=DISABLED)
            self.console.grid(row=1, column=0)

        elif cmddic['instruction'] == 'show':
            self.panel.tag_config('print_tag', foreground='blue')
            try:
                self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + str(cmddic['varname']) + ' = ' + str(parameter.parameterdic[cmddic['varname']]) + '\n')
                # if isinstance(parameter.parameterdic[cmddic['varname']], matrix.matrix):
                #     if parameter.outputline == 1:
                #         self.console.insert(INSERT,'Out [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']].matrix), 'print_tag')
                #     else:
                #         self.console.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']].matrix), 'print_tag')
                # elif isinstance(parameter.parameterdic[cmddic['varname']], matrix.polynomial):
                #     if parameter.outputline == 1:
                #         self.console.insert(INSERT,'Out [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']].p), 'print_tag')
                #     else:
                #         self.console.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']].p), 'print_tag')
                # else:
                #     if parameter.outputline == 1:
                #         self.console.insert(INSERT, 'Out [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']]), 'print_tag')
                #     else:
                #         self.console.insert(INSERT, '\nOut [' + str(int(parameter.outputline)) + ']: ' + cmddic['varname'] + ' = ' + str(parameter.parameterdic[cmddic['varname']]), 'print_tag')
            except:
                self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + cmddic['varname'] + ' = ' + str(cmddic['ans']) + '\n')
            parameter.outputline += 1
            parameter.currentline += 1
        elif cmddic['instruction'] == 'assignvalue':
            parameter.currentline += 1
            self.updateworkspace()
        elif cmddic['instruction'] == 'assignpoly':
            parameter.currentline += 1
            self.updateworkspace()
        elif cmddic['instruction'] == 'evalpoly':
            self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + str(cmddic['ans']) + '\n')
            parameter.outputline += 1
            parameter.currentline += 1
        elif cmddic['instruction'] == 'assignmatrix':
            # self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + str(cmddic['varname']) + ' = ' + str(cmddic['var']) + '\n')
            parameter.currentline += 1
            # parameter.outputline += len(cmddic['var']) + 1
            self.updateworkspace()
        elif cmddic['instruction'] == 'polyerror':
            self.console.tag_config('error_tag', foreground='red')
            self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ''Please follow the format when you assign a polynomial: "polynomialname(symbol)" ' + '\n', 'error_tag')
            parameter.currentline += 1
            parameter.outputline += 1
        elif cmddic['instruction'] == 'default':
            parameter.currentline += 1
            self.updateworkspace()
        elif cmddic['instruction'] == 'error':
            self.console.tag_config('error_tag', foreground='red')
            self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + cmddic['errormsg'] + '\n', 'error_tag')
            parameter.currentline += 1
            parameter.outputline += 1
        self.console.config(state=DISABLED)

    def makematrix(self, event):  # 建構矩陣
        if not self.matrixrowentry.get() \
           or not self.matrixcolentry.get() \
           or not self.matrixnameentry.get():
            messagebox.showerror('錯誤', '請輸入完整資訊')
            self.matrixconfirm = Button(self.matrix, text='確定')  # 確定按鈕
            self.matrixconfirm.bind('<Button-1>', self.makematrix)
            self.matrixcancel = Button(self.matrix, text='取消')  # 取消按鈕
            self.matrixcancel.bind('<Button-1>', lambda _: self.matrix.destroy())

            self.matrixconfirm.grid(row=3, column=0, sticky=W)
            self.matrixcancel.grid(row=3, column=1, sticky=W)
        else:
            row = int(self.matrixrowentry.get())
            col = int(self.matrixcolentry.get())
            name = self.matrixnameentry.get()
            parameter.parameterdic[name] = matrix.makematrix(row, col)
            self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + name + ' = ' + str(parameter.parameterdic[name]) + '\n')
            # parameter.inputline += 1
            parameter.outputline += 1
            self.updateworkspace()
            self.matrix.destroy()

    def matrix_row_col(self):      # 輸入矩陣維度
        self.matrix = Tk()
        self.matrix.geometry('200x150+650+250')
        self.matrix.title("矩陣")
        # self.matrix.iconbitmap('psl.xbm')

        self.matrixnamelabel = Label(self.matrix, text = '       名稱: ')       # 矩陣文字標籤
        self.matrixrowlabel = Label(self.matrix, text = '       列: ')
        self.matrixcollabel = Label(self.matrix, text = '       行: ')

        self.matrixnamelabel.grid(row = 0, column = 0, sticky = W)
        self.matrixrowlabel.grid(row = 1, column = 0, sticky = W)
        self.matrixcollabel.grid(row = 2, column = 0, sticky = W)

        self.matrixnameentry = Entry(self.matrix, width=13)      # 輸入的矩陣名稱
        self.matrixrowentry = Entry(self.matrix, width=13)      # 輸入的列數
        self.matrixcolentry = Entry(self.matrix, width=13)      # 輸入的行數

        self.matrixnameentry.grid(row = 0, column = 1, sticky = W)
        self.matrixrowentry.grid(row = 1, column = 1, sticky = W)
        self.matrixcolentry.grid(row = 2, column = 1, sticky = W)

        self.matrixconfirm = Button(self.matrix, text = '確定')       # 確定按鈕
        self.matrixconfirm.bind('<Button-1>', self.makematrix)
        self.matrixcancel = Button(self.matrix, text = '取消')      # 取消按鈕
        self.matrixcancel.bind('<Button-1>', lambda _: self.matrix.destroy())

        self.matrixconfirm.grid(row = 3, column = 0, sticky=W)
        self.matrixcancel.grid(row = 3, column = 1, sticky=W)

        self.matrix.mainloop()

    def dotranspose(self, event):  # 建構轉置矩陣
        if not self.matrixTnameentry.get():
            messagebox.showerror('錯誤', '請輸入完整資訊')
            self.matrixconfirm = Button(self.matrix, text='確定')  # 確定按鈕
            self.matrixconfirm.bind('<Button-1>', self.makematrix)
            self.matrixcancel = Button(self.matrix, text='取消')  # 取消按鈕
            self.matrixcancel.bind('<Button-1>', lambda _: self.matrix.destroy())

            self.matrixconfirm.grid(row=2, column=0)
            self.matrixcancel.grid(row=2, column=1)
        else:
            name = self.matrixTnameentry.get()
            if name not in parameter.parameterdic:
                messagebox.showerror('錯誤', '矩陣不存在')
                self.matrixTconfirm = Button(self.matrixT, text='確定')
                self.matrixTconfirm.bind('<Button-1>', self.dotranspose)
                self.matrixTcancel = Button(self.matrixT, text='取消')
                self.matrixTcancel.bind('<Button-1>', lambda _: self.matrixT.destroy())

                self.matrixTconfirm.grid(row=2, column=0)
                self.matrixTcancel.grid(row=2, column=1)
            else:
                m = parameter.parameterdic[name]
                ans = matrix.T(m)
                self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + name + '.T = ' + str(ans) + '\n')
                # parameter.inputline += 1
                parameter.outputline += 1
                self.updateworkspace()
                self.matrixT.destroy()

    def matrixtranspose(self):      # 轉置矩陣                              尚未防呆(當輸入未創建的物件名稱)
        self.matrixT = Tk()
        self.matrixT.geometry('245x80+650+250')
        self.matrixT.title("轉置矩陣")

        self.matrixTnamelabel = Label(self.matrixT, text = '     欲轉置的矩陣: ')
        self.matrixTnamelabel.grid(row=1, column =0, sticky=W)

        self.matrixTnameentry = Entry(self.matrixT, width=13)
        self.matrixTnameentry.grid(row=1, column=1, sticky=W)

        self.matrixTconfirm = Button(self.matrixT, text='確定')
        self.matrixTconfirm.bind('<Button-1>', self.dotranspose)
        self.matrixTcancel = Button(self.matrixT, text='取消')
        self.matrixTcancel.bind('<Button-1>', lambda _: self.matrixT.destroy())

        self.matrixTconfirm.grid(row=2, column=0)
        self.matrixTcancel.grid(row=2, column=1)

        self.matrixT.mainloop()

    def doinverse(self, event):  # 建構反矩陣                            尚未防呆(行列式為0)
        if not self.matrixInameentry.get():
            messagebox.showerror('錯誤', '請輸入正確的資訊！')
            self.matrixIconfirm = Button(self.matrixI, text='確定')
            self.matrixIconfirm.bind('<Button-1>', self.doinverse)
            self.matrixIcancel = Button(self.matrixI, text='取消')
            self.matrixIcancel.bind('<Button-1>', lambda _: self.matrixI.destroy())

            self.matrixIconfirm.grid(row=1, column=0)
            self.matrixIcancel.grid(row=1, column=1)
        else:
            name = self.matrixInameentry.get()
            if name not in parameter.parameterdic:
                messagebox.showerror('錯誤', '矩陣不存在')
                self.matrixTconfirm = Button(self.matrixI, text='確定')
                self.matrixTconfirm.bind('<Button-1>', self.dotranspose)
                self.matrixTcancel = Button(self.matrixI, text='取消')
                self.matrixTcancel.bind('<Button-1>', lambda _: self.matrixT.destroy())

                self.matrixTconfirm.grid(row=2, column=0)
                self.matrixTcancel.grid(row=2, column=1)
            else:
                m = parameter.parameterdic[name]
                row = len(m[0])
                col = len(m[:,0])
                if row != col:
                    messagebox.showerror('錯誤', '輸入矩陣須為方陣')
                    self.matrixIconfirm = Button(self.matrixI, text='確定')
                    self.matrixIconfirm.bind('<Button-1>', self.doinverse)
                    self.matrixIcancel = Button(self.matrixI, text='取消')
                    self.matrixIcancel.bind('<Button-1>', lambda _: self.matrixI.destroy())

                    self.matrixIconfirm.grid(row=1, column=0)
                    self.matrixIcancel.grid(row=1, column=1)
                elif matrix.D(m) == 0:
                    messagebox.showerror('錯誤', '行列式不得為0')
                    self.matrixIconfirm = Button(self.matrixI, text='確定')
                    self.matrixIconfirm.bind('<Button-1>', self.doinverse)
                    self.matrixIcancel = Button(self.matrixI, text='取消')
                    self.matrixIcancel.bind('<Button-1>', lambda _: self.matrixI.destroy())

                    self.matrixIconfirm.grid(row=1, column=0)
                    self.matrixIcancel.grid(row=1, column=1)
                else:
                    ans = matrix.I(m)
                    # parameter.parameterdic[name + '.inverse'] = matrix.matrix(name + '.transpose', row, col)
                    # name = name + '.inverse'
                    # parameter.parameterdic[name].I()
                    self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + name + ' = ' + str(ans) + '\n')
                    # parameter.inputline += 1
                    parameter.outputline += 1
                    self.updateworkspace()
                    self.matrixI.destroy()

    def matrixinverse(self):

        self.matrixI = Tk()
        self.matrixI.geometry('245x80+650+250')
        self.matrixI.title("反矩陣")

        self.matrixInamelabel = Label(self.matrixI, text='     矩陣: ')
        self.matrixInamelabel.grid(row=0, column=0, sticky=W)

        self.matrixInameentry = Entry(self.matrixI, width=13)
        self.matrixInameentry.grid(row=0, column=1, sticky=W)

        self.matrixIconfirm = Button(self.matrixI, text='確定')
        self.matrixIconfirm.bind('<Button-1>', self.doinverse)
        self.matrixIcancel = Button(self.matrixI, text='取消')
        self.matrixIcancel.bind('<Button-1>', lambda _: self.matrixI.destroy())

        self.matrixIconfirm.grid(row=1, column=0)
        self.matrixIcancel.grid(row=1, column=1)

        self.matrixI.mainloop()

    def dodeterminate(self, event):
        if not self.matrixDnameentry.get():
            messagebox.showerror('錯誤', '請輸入正確的資訊！')
            self.matrixDconfirm = Button(self.matrixD, text='確定')
            self.matrixDconfirm.bind('<Button-1>', self.dodeterminate)
            self.matrixDcancel = Button(self.matrixD, text='取消')
            self.matrixDcancel.bind('<Button-1>', lambda _: self.matrixD.destroy())

            self.matrixDconfirm.grid(row=1, column=0)
            self.matrixDcancel.grid(row=1, column=1)
        else:
            name = self.matrixDnameentry.get()
            if name not in parameter.parameterdic:
                messagebox.showerror('錯誤', '矩陣不存在')
                self.matrixDconfirm = Button(self.matrixD, text='確定')
                self.matrixDconfirm.bind('<Button-1>', self.dodeterminate)
                self.matrixDcancel = Button(self.matrixD, text='取消')
                self.matrixDcancel.bind('<Button-1>', lambda _: self.matrixD.destroy())

                self.matrixDconfirm.grid(row=1, column=0)
                self.matrixDcancel.grid(row=1, column=1)
            else:
                m = parameter.parameterdic[name]
                row = len(m[0])
                col = len(m[:, 0])
                if row != col:
                    messagebox.showerror('錯誤', '輸入矩陣須為方陣')
                    self.matrixDconfirm = Button(self.matrixD, text='確定')
                    self.matrixDconfirm.bind('<Button-1>', self.dodeterminate)
                    self.matrixDcancel = Button(self.matrixD, text='取消')
                    self.matrixDcancel.bind('<Button-1>', lambda _: self.matrixD.destroy())

                    self.matrixDconfirm.grid(row=1, column=0)
                    self.matrixDcancel.grid(row=1, column=1)
                else:
                    ans = matrix.D(m)
                    self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + str(ans) + '\n')
                    # parameter.inputline += 1
                    parameter.outputline += 1
                    self.matrixD.destroy()

    def matrixdeterminate(self):
        self.matrixD = Tk()
        self.matrixD.geometry('200x80+650+250')
        self.matrixD.title("行列式")

        self.matrixDnamelabel = Label(self.matrixD, text = '     矩陣: ')
        self.matrixDnamelabel.grid(row=0, column=0, sticky=W)

        self.matrixDnameentry = Entry(self.matrixD, width=13)
        self.matrixDnameentry.grid(row=0, column=1, sticky=W)

        self.matrixDconfirm = Button(self.matrixD, text='確定')
        self.matrixDconfirm.bind('<Button-1>', self.dodeterminate)
        self.matrixDcancel = Button(self.matrixD, text='取消')
        self.matrixDcancel.bind('<Button-1>', lambda _: self.matrixD.destroy())

        self.matrixDconfirm.grid(row=1, column=0)
        self.matrixDcancel.grid(row=1, column=1)

        self.matrixD.mainloop()

    def differential(self, event):      # 微分
        # 防呆(輸入多項式中沒有出現的符號)
        if not self.difpolynomialnameentry.get() \
           or not self.difpolynomialentry.get() \
           or not self.differentialsymbolentry.get() \
           or not self.timesentry.get():
            messagebox.showerror('錯誤', '請輸入完整資訊')
            self.differentialconfirm = Button(self.dif, text='確定')  # 確定按鈕
            self.differentialconfirm.bind('<Button-1>', self.differential)
            self.differentialcancel = Button(self.dif, text='取消')  # 取消按鈕
            self.differentialcancel.bind('<Button-1>', lambda _: self.dif.destroy())
            self.differentialconfirm.grid(row=4, column=0)
            self.differentialcancel.grid(row=4, column=1)
        else:
            name = self.difpolynomialnameentry.get()
            p = self.difpolynomialentry.get()
            symbol = self.differentialsymbolentry.get()
            times = int(self.timesentry.get())
            p = polynomial.tran_p(p)
            # parameter.parameterdic[name].dif(times)
            # parameter.parameterdic[name + '.dif'] = parameter.parameterdic[name].dif
            parameter.parameterdic[name] = polynomial.dif(p, times, symbol)
            self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + name + ' = ' + str(parameter.parameterdic[name]) + '\n')
            # parameter.inputline += 1
            parameter.outputline += 1
            self.updateworkspace()
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
        self.difpolynomiallabel.grid(row = 1, column = 0, sticky = E)
        self.differentialsymbollabel.grid(row = 2, column = 0, sticky = E)
        self.timeslabel.grid(row = 3, column = 0, sticky = E)

        self.difpolynomialnameentry = Entry(self.dif, width = 13)      # 輸入的多項式名稱
        self.difpolynomialentry = Entry(self.dif, width = 13)        # 輸入的多項式
        self.differentialsymbolentry = Entry(self.dif, width = 13 )      # 輸入的微分的變數
        self.timesentry = Entry(self.dif, width = 13)     # 輸入的微分次數

        self.difpolynomialnameentry.grid(row = 0, column = 1, sticky = E)
        self.difpolynomialentry.grid(row = 1, column = 1, sticky = E)
        self.differentialsymbolentry.grid(row = 2, column = 1, sticky = E)
        self.timesentry.grid(row = 3, column = 1, sticky = E)

        self.differentialconfirm = Button(self.dif, text = '確定')      # 確定按鈕
        self.differentialconfirm.bind('<Button-1>', self.differential)
        self.differentialcancel = Button(self.dif, text = '取消')       # 取消按鈕
        self.differentialcancel.bind('<Button-1>', lambda _: self.dif.destroy())
        # Label(self.dif, text = '').grid(row = 8, column = 2)
        self.differentialconfirm.grid(row = 4, column = 0)
        self.differentialcancel.grid(row = 4, column = 1)

        self.dif.mainloop()

    def integral(self,event):
        if self.checkSvar.get():        # 定積分
            if not self.intpolynomialnameentry.get() \
               or not self.intpolynomialnameentry.get() \
               or not self.intpolynomialentry.get() \
               or not self.lowerboundentry.get() \
               or not self.upperboundentry.get():
                messagebox.showerror('錯誤', '請輸入完整資訊')
                self.differentialconfirm = Button(self.S, text='確定')  # 確定按鈕
                self.differentialconfirm.bind('<Button-1>', self.integral)
                self.differentialcancel = Button(self.S, text='取消')  # 取消按鈕
                self.differentialcancel.bind('<Button-1>', lambda _: self.S.destroy())
                self.differentialconfirm.grid(row=6, column=0)
                self.differentialcancel.grid(row=6, column=1)
            else:
                name = self.intpolynomialnameentry.get()
                p = self.intpolynomialentry.get()
                symbol = self.integrationsymbolentry.get()
                upperbound = self.upperboundentry.get()
                lowerbound = self.lowerboundentry.get()
                p = polynomial.tran_p(p)
                parameter.parameterdic[name] = polynomial.S(p, symbol, upperbound, lowerbound)
                self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + name + ' = ' + str(parameter.parameterdic[name]) + '\n')
                # parameter.inputline += 1
                parameter.outputline += 1
                self.updateworkspace()
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
                p = polynomial.tran_p(p)
                parameter.parameterdic[name] = polynomial.S(p, symbol)
                self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + name + ' = ' + str(parameter.parameterdic[name]) + '\n')
                parameter.inputline += 1
                parameter.outputline += 1
                self.updateworkspace()
                self.S.destroy()

    def checkintegral(self):  # 檢查是否為定積分
        isintegral = self.checkSvar.get()
        if function.isintegral(isintegral):
            self.checkSvar.set(0)
            self.upperboundentry.configure(state=DISABLED)
            self.lowerboundentry.configure(state=DISABLED)
        else:
            self.checkSvar.set(1)
            self.upperboundentry.configure(state=NORMAL)
            self.lowerboundentry.configure(state=NORMAL)

    def integration(self):
        self.S = Tk()
        self.S.geometry('200x200+650+250')
        self.S.title("積分")

        self.intpolynomialnamelabel = Label(self.S, text=' 名稱: ')  # 多項式文字標籤
        self.intpolynomiallabel = Label(self.S, text=' 多項式: ')
        self.integrationsymbollabel = Label(self.S, text=' 變數: ')
        self.upperboundlabel = Label(self.S, text=' 上界: ')
        self.lowerboundlabel = Label(self.S, text=' 下界: ')

        self.intpolynomialnamelabel.grid(row=0, column=0, sticky=E)
        self.intpolynomiallabel.grid(row=1, column=0, sticky=E)
        self.integrationsymbollabel.grid(row=2, column=0, sticky=E)
        self.upperboundlabel.grid(row=4, column=0, sticky=E)
        self.lowerboundlabel.grid(row=5, column=0, sticky=E)

        self.intpolynomialnameentry = Entry(self.S, width=13)      # 輸入的多項式名稱
        self.intpolynomialentry = Entry(self.S, width=13)      # 輸入的多項式
        self.integrationsymbolentry = Entry(self.S, width=13)     # 輸入的積分的變數
        self.upperboundentry = Entry(self.S, width=13, state=DISABLED)      # 輸入定積分的上界
        self.lowerboundentry = Entry(self.S, width=13, state=DISABLED)      # 輸入定積分的下界

        self.intpolynomialnameentry.grid(row=0, column=1, sticky=E)
        self.intpolynomialentry.grid(row=1, column=1, sticky=E)
        self.integrationsymbolentry.grid(row=2, column=1, sticky=E)
        self.upperboundentry.grid(row=4, column=1, sticky=E)
        self.lowerboundentry.grid(row=5, column=1, sticky=E)

        self.checkSvar = IntVar()
        self.checkS = Checkbutton(self.S, text='定積分', variable=self.checkSvar, command=self.checkintegral)
        self.checkS.grid(row=3, column=0, sticky=E)

        self.differentialconfirm = Button(self.S, text='確定')  # 確定按鈕
        self.differentialconfirm.bind('<Button-1>', self.integral)
        self.differentialcancel = Button(self.S, text='取消')  # 取消按鈕
        self.differentialcancel.bind('<Button-1>', lambda _: self.S.destroy())
        self.differentialconfirm.grid(row=6, column=0)
        self.differentialcancel.grid(row=6, column=1)

        self.S.mainloop()

    def find_limit(self, event):
        if not self.limitpolynomialentry.get() \
           or not self.limitsymbolentry.get() \
           or not self.limitnumentry.get():
            messagebox.showerror('錯誤', '請輸入完整資訊')
            confirm = Button(self.limit, text='確定')  # 確定按鈕
            confirm.bind('<Button-1>', self.find_limit)
            cancel = Button(self.limit, text='取消')  # 取消按鈕
            cancel.bind('<Button-1>', lambda _: self.limit.destroy())
            confirm.grid(row=3, column=0)
            cancel.grid(row=3, column=1)
        else:
            p = self.limitpolynomialentry.get()
            symbol = self.limitsymbolentry.get()
            num = self.limitnumentry.get()
            ans = polynomial.l(p, symbol, num)
            self.console.insert(INSERT, 'Out [' + str(int(parameter.inputline)) + ']: ' + str(p) + '.l = ' + str(ans) + '\n')
            self.updateworkspace()
            self.limit.destroy()

    def limit_gui(self):
        self.limit = Tk()
        self.limit.geometry('200x180+650+250')
        self.limit.title("極限")

        self.limitpolynomiallabel = Label(self.limit, text='  多項式: ')
        self.limitsymbollabel = Label(self.limit, text='  變數: ')
        self.limitnumlabel = Label(self.limit, text='  趨近於: ')

        self.limitpolynomiallabel.grid(row=0, column=0, sticky=E)
        self.limitsymbollabel.grid(row=1, column=0, sticky=E)
        self.limitnumlabel.grid(row=2, column=0, sticky=E)

        self.limitpolynomialentry = Entry(self.limit, width=13)
        self.limitsymbolentry = Entry(self.limit, width=13)
        self.limitnumentry = Entry(self.limit, width=13)

        self.limitpolynomialentry.grid(row=0, column=1, sticky=E)
        self.limitsymbolentry.grid(row=1, column=1, sticky=E)
        self.limitnumentry.grid(row=2, column=1, sticky=E)

        confirm = Button(self.limit, text='確定')  # 確定按鈕
        confirm.bind('<Button-1>', self.find_limit)
        cancel = Button(self.limit, text='取消')  # 取消按鈕
        cancel.bind('<Button-1>', lambda _: self.limit.destroy())
        confirm.grid(row=3, column=0)
        cancel.grid(row=3, column=1)

        self.limit.mainloop()

    def doplot(self, event):
        xlowerbound = int(self.xlowerboundentry.get())
        xupperbound = int(self.xupperboundentry.get()) + 1
        formulas = self.formulaentry.get().split(',')

        self.draw.destroy()

        function.plot(xlowerbound, xupperbound, formulas)


    def plot(self):
        self.draw = Tk()
        self.draw.geometry('350x150+650+250')
        self.draw.title("繪圖")

        self.formulalabel = Label(self.draw, text='  方程式: ')
        self.xlabel = Label(self.draw, text='  x的範圍: ')

        self.formulalabel.grid(row=0, column=0, sticky=W)
        self.xlabel.grid(row=1, column=0, sticky=W)
        Label(self.draw, text='~').grid(row=1, column=2)

        self.formulaentry = Entry(self.draw, width=13)
        self.xlowerboundentry = Entry(self.draw, width=13)
        self.xupperboundentry = Entry(self.draw, width=13)

        self.formulaentry.grid(row=0, column=1, sticky=W)
        self.xlowerboundentry.grid(row=1, column=1, sticky=W)
        self.xupperboundentry.grid(row=1, column=3, sticky=W)

        self.drawconfirm = Button(self.draw, text='確定')  # 確定按鈕
        self.drawconfirm.bind('<Button-1>', self.doplot)
        self.drawcancel = Button(self.draw, text='取消')  # 取消按鈕
        self.drawcancel.bind('<Button-1>', lambda _: self.draw.destroy())
        self.drawconfirm.grid(row=2, column=1)
        self.drawcancel.grid(row=2, column=2)

        self.draw.mainloop()

    def cut(self, *args):
        if args:
            args[0].widget.event_generate('<<Cut>>')
        else:
            self.panel.event_generate('<<Cut>>')
        # try:
        #     text = self.panel.get(SEL_FIRST, SEL_LAST)
        #     self.panel.delete(SEL_FIRST, SEL_LAST)
        #     self.panel.clipboard_clear()
        #     self.panel.clipboard_append(text)
        # except:
        #     pass

    def paste(self, *args):
        if args:
            args[0].widget.event_generate('<<Paste>>')
        else:
            self.panel.event_generate('<<Paste>>')
        # try:
        #     text = self.panel.selection_get(selection="CLIPBOARD")
        #     self.panel.insert(INSERT, text)
        #     self.panel.clipboard_clear()
        # except:
        #     pass

    def copy(self, *args):
        if args:
            args[0].widget.event_generate('<<Copy>>')
        else:
            self.panel.event_generate('<<Copy>>')
        # try:
        #     text = self.panel.get(SEL_FIRST, SEL_LAST)
        #     self.panel.clipboard_clear()
        #     self.panel.clipboard_append(text)
        # except:
        #     pass

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

    def undo(self):
        self.panel.event_generate('<<Undo>>')

    def redo(self):
        self.panel.event_generate('<<Redo>>')

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

    def rClicker(self, event):
        try:
            nclst = [
                (' Cut', lambda e=event: self.cut(e)),
                (' Copy', lambda e=event: self.copy(e)),
                (' Paste', lambda e=event: self.paste(e)),
            ]

            rmenu = Menu(None, tearoff=0, takefocus=0)

            for txt, cmd in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(event.x_root + 40, event.y_root + 10, entry="0")

        except TclError:
            print(' - rClick menu, something wrong')
            pass

        return "break"

    def init_window(self):
        self.master.state('normal')
        self.master.title("NCUproject")

        # messagebox.showinfo('歡迎!!!', '歡迎進入本數學軟體')
        self.toolbar = Menu(self.master, font=30)

        toolbar = ['檔案', '矩陣', '微積分', '繪圖']
        menu = [
            [('開啟新檔', self.openfile), ('儲存檔案', self.savefile), ('另存新檔', self.saveasfile)],
            [('產生零矩陣', self.matrix_row_col), ('反矩陣', self.matrixinverse), ('行列式', self.matrixdeterminate), ('轉置矩陣', self.matrixtranspose)],
            [('微分', self.differentation), ('積分', self.integration), ('極值', self.limit_gui)],
            [('二維繪圖', self.plot)]
        ]

        for t in range(len(toolbar)):
            tool = Menu(self.toolbar, tearoff=0, font=30)
            self.toolbar.add_cascade(label=toolbar[t], menu=tool)
            for m,func in menu[t]:
                tool.add_command(label=m, command=func)

        self.master.config(menu = self.toolbar)

        self.panel = Text(self.panelframe, height=20, font = ("Helvetica", 20), undo=True)     # text panel
        self.panel.insert(INSERT, 'In [' + str(int(parameter.inputline)) + ']: ')
        self.panel.bind('<Return>', self.command)
        self.panel.bind('<KeyRelease-Return>', self.newline)
        self.panel.bind('<Button-3>', self.rClicker)
        self.panel.grid(row=0, column=0)

        self.workspace = Text(self.workspaceframe, width=71, height=48, font=("Helvetica", 20))      # workspace
        self.workspace.config(state=DISABLED)
        self.workspace.grid(row=0, column=0)

        self.console = Text(self.panelframe, height=10, font=("Helvetica", 20), bg='black', fg='white')        # console
        self.console.config(state=DISABLED)
        self.console.grid(row=1, column=0)
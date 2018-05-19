from tkinter import *
import gui

root = Tk()

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

root.geometry('%dx%d'%(w, h))

app = gui.GUI(root, w, h)

root.mainloop()
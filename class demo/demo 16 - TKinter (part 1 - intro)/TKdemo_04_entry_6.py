# Tk entry demo: Adds two entered numbers, shows result in a label.
# Uses a Tk variable.

import tkinter as Tk

def fun1():
    c = float(E1.get()) + float(E2.get())
    s.set(str(c))

root = Tk.Tk()

# Define Tk variable
s = Tk.StringVar()

# Define widgets
L1 = Tk.Label(root, text = 'Enter two numbers')
E1 = Tk.Entry(root)
E2 = Tk.Entry(root) 
B1 = Tk.Button(root, text = 'Add', command = fun1)
L2 = Tk.Label(root, textvariable = s)
B2 = Tk.Button(root, text = 'Quit', command = root.quit)

# Place widgets
L1.pack()
E1.pack()
E2.pack()
B1.pack()
L2.pack()
B2.pack()

root.mainloop()

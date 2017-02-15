#!/usr/bin/env python3

# quick and dirty import :)
from tkinter import *
from tkinter import ttk

APP_NAME = 'Invariants Membership System'

def checkmember():
    pass

class TextBox:
    def __init__(self, name, row):
        # label
        self.label = ttk.Label(frame, text=name+': ')
        self.label.grid(column=1, row=row, sticky=W)

        # textbox
        self.value = StringVar()
        self.widget = ttk.Entry(frame, width=7, textvariable=self.value)
        self.widget.grid(column=2, row=row, sticky=(W, E))

# make app
root = Tk()
root.title(APP_NAME)

frame = ttk.Frame(root, padding='3 3 12 12')
frame.grid(column=0, row=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

barcode = TextBox('Barcode', row=1)
firstname = TextBox('First Name', row=2)
lastname = TextBox('Last Name', row=3)

result = StringVar()
label = ttk.Label(textvariable=result)
label.grid(column=0, row=4, sticky=(W, E))
button = ttk.Button(text='Add')
button.grid(column=0, row=5, sticky=(W, E))

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)
barcode.widget.focus()
root.bind('<Return>', checkmember())

root.mainloop()

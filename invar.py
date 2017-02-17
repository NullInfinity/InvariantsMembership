#!/usr/bin/env python3

# quick and dirty import :)
import sqlite3
from tkinter import *
from tkinter import ttk

APP_NAME = 'Invariants Membership'
BARCODE_LENGTH = 7

TEXT_ACCEPTED = 'MEMBER'
TEXT_REJECTED = 'NOTMEMBER'

def querydb(barcode=None, firstname=None, lastname=None):
    return False

def checkmember(sv):
    barcode = sv.get()

    if len(barcode) < BARCODE_LENGTH:
        return

    barcode = barcode[:BARCODE_LENGTH]

    if querydb(barcode=barcode):
        result_label.config(text=TEXT_ACCEPTED)
        add_button.config(state=DISABLED)
    else:
        result_label.config(text=TEXT_REJECTED)
        add_button.config(state=NORMAL)


class TextBox:
    def __init__(self, name, row, callback=None):
        # label
        self.label = ttk.Label(frame, text=name+': ')
        self.label.grid(column=1, row=row, sticky=W)

        # textbox
        self.value = StringVar()
        self.widget = ttk.Entry(frame, width=7, textvariable=self.value)
        self.widget.grid(column=2, row=row, sticky=(W, E))

        # text entered callback
        if callback is not None:
            self.value.trace('w', callback=lambda name, index, mode, var=self.value: callback(var))

# make app
root = Tk()
root.title(APP_NAME)

frame = ttk.Frame(root, padding='3 3 12 12')
frame.grid(column=0, row=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

barcode = TextBox('Barcode', row=1, callback=checkmember)
firstname = TextBox('First Name', row=2)
lastname = TextBox('Last Name', row=3)

result_var = StringVar()
result_label = ttk.Label(text='test')
result_label.grid(column=0, row=4, columnspan=4, sticky=(W, E))
add_button = ttk.Button(text='Add')
add_button.grid(column=0, row=5, sticky=(W, E))
add_button.config(state=DISABLED)

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

barcode.widget.focus()

#root.bind('<Return>', checkmember())

root.mainloop()

#!/usr/bin/env python3

# quick and dirty import :)
import sqlite3
from tkinter import *
from tkinter import ttk

APP_NAME = 'Invariants Membership'
BARCODE_LENGTH = 7
DBFILE = 'development.sqlite3'

TEXT_ACCEPTED = 'MEMBER'
TEXT_REJECTED = 'NOTMEMBER'
CHECK_BUTTON_TEXT = 'CHECKMEMBER'
ADD_BUTTON_TEXT = 'ADDMEMBER'

class NotAMemberException(Exception):
    pass

class BadInputException(Exception):
    pass

def querydb(bc=None, fn=None, ln=None):
    queries = []
    values = []

    if bc:
        queries.append('barcode=?')
        values.append(bc)
    if fn and ln:
        queries.append('firstName=? AND lastName=?')
        values.append(fn)
        values.append(ln)
    if not queries:
        raise BadInputException()

    query = 'SELECT barcode,firstName,lastName FROM users WHERE ' + ' AND '.join(queries)
    cursor = conn.cursor()
    cursor.execute(query, values)

    result = cursor.fetchone()
    if result is None:
        raise NotAMemberException()
    return result

def on_barcode_entered(var):
    barcode_entry = var.get()

    if len(barcode_entry) < BARCODE_LENGTH:
        return

    barcode_entry = barcode_entry[:BARCODE_LENGTH]
    barcode.set(barcode_entry)

    checkmember()

def set_textboxes(values):
    if values is None:
        values = ('', '', '')
    barcode.set(values[0])
    firstname.set(values[1])
    lastname.set(values[2])

def checkmember():
    bc = barcode.content()
    fn = firstname.content()
    ln = lastname.content()

    try:
        out = querydb(bc, fn, ln)
    except NotAMemberException:
        result_label.config(text=TEXT_REJECTED)
        add_button.config(state=NORMAL)
        return
    except BadInputException:
        return

    set_textboxes(out)
    #root.after(1000, set_textboxes(None))

    result_label.config(text=TEXT_ACCEPTED)
    add_button.config(state=DISABLED)

def addmember():
    pass

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

    def content(self):
        return self.value.get()

    def set(self, string):
        self.value.set(string)


# make app
root = Tk()
root.title(APP_NAME)

frame = ttk.Frame(root, padding='3 3 12 12')
frame.grid(column=0, row=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

barcode = TextBox('Barcode', row=1, callback=on_barcode_entered)
firstname = TextBox('First Name', row=2)
lastname = TextBox('Last Name', row=3)

result_var = StringVar()
result_label = ttk.Label(text='test')
result_label.grid(column=0, row=4, columnspan=4, sticky=(W, E))

check_button = ttk.Button(text=CHECK_BUTTON_TEXT, command=checkmember)
check_button.grid(column=0, row=5, sticky=(W, E))

add_button = ttk.Button(text=ADD_BUTTON_TEXT, command=addmember)
add_button.grid(column=0, row=6, sticky=(W, E))
add_button.config(state=DISABLED)

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

barcode.widget.focus()

#root.bind('<Return>', checkmember())

# setup SQL db
conn = sqlite3.connect(DBFILE)

root.mainloop()

conn.commit()
conn.close()

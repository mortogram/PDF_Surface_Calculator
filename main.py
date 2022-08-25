from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PyPDF2 import PdfReader
import os


import re

from tkinterdnd2 import DND_FILES, TkinterDnD

#1.0 \/\/\/\/\/
global unit
global sum_var
sum_var = 0.0
sum_var = "XXXX"
global l5


def unit_pick(pick):
    if pick == "mm^2":
        unit = 1.0
    elif pick == "cm^2":
        unit = 100.0
    elif pick == "m^2":
        unit = 10000.0
    recalculate(list1, unit)
    pass


def recalculate(list, unit):
    global sum_var
    i=0
    list3.delete(0, END)
    sum = 0
    for i in range(i, list.size()):
        x = calculate(list1.get(i), unit)
        list3.insert(i, round(x[1], 2))
        sum = sum + x[1]
        i = i+1
    sum_var = str(round(sum, 2))
    sum_label_text_update()
    pass


def sum_label_text_update():
    print("Sum_label_text_update check    " + str(sum_var))
    l5.configure(text=sum_var)
    l5.grid(row=2, column=2)
    pass

def calculate(file,unit):
    reader = PdfReader(file)
    calc = [0, 0]
    for page in reader.pages:
        #print(unit)
        calc[1] = float(calc[1]) + float(page.mediabox[2]) * 1/72 * 2.54 * float(page.mediabox[3]) * 1 / 72 * 2.54 / unit
        calc[0] = calc[0] + 1
    return calc


def drop_inside_list_box(list,unit):
    global sum_var
    sum = 0
    for item in list:
        list1.insert("end", item)
        x = calculate(item, unit)
        list2.insert("end", x[0])
        list3.insert("end", round(x[1], 2))
        sum = sum + x[1]
    sum_var = sum

    sum_label_text_update()
    pass


def select_file(unit):
    filetypes = (
        ('pdf', '*.pdf'),
    )

    filename = fd.askopenfilenames(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    drop_inside_list_box(filename, unit)
    showinfo(
        title='Selected File',
        message=filename
    )


unit = 10000.0
screen = TkinterDnD.Tk()
screen.geometry("800x400")
screen.title("PDF Surface Calculator")

l1 = Label(screen, text="File name")
l1.grid(row=0, column=0, columnspan=2)

l2 = Label(screen, text="Pages")
l2.grid(row=0, column=2)

l3 = Label(screen, text="Surface")
l3.grid(row=0, column=3)

l4 = Label(screen, text="Sum:")
l4.grid(row=2, column=1)

l5 = Label(screen, text="XXXX")
l5.grid(row=2, column=2)

variable = StringVar(screen)
options = ["mm^2", "cm^2", "m^2"]
variable.set("m^2")     # default value
w = OptionMenu(screen, variable, *options, command=unit_pick)
w.grid(row=2, column=3)

sb1 = Scrollbar(screen)
sb1.grid(row=1, column=4)

list1 = Listbox(screen, selectmode=MULTIPLE, height=20, width=100)
list1.grid(row=1, column=0, sticky="N")

list2 = Listbox(screen, selectmode=SINGLE, height=20, width=10)
list2.grid(row=1, column=2, sticky="N")

list3 = Listbox(screen, selectmode=SINGLE, height=20, width=10)
list3.grid(row=1, column=3, sticky="N")

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)
print("test")
open_button = Button(screen, text='Open a File', command=lambda: select_file(unit))
open_button.grid(row=2, column=0)
print("test2")
screen.mainloop()

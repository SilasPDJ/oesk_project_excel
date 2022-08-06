import tkinter as tk

root = tk.Tk()
my_entries = []
entry_row = 1


def addentry():
    global entry_row
    ent = tk.Entry(entries_widget, bd=5)
    ent.grid(row=entry_row, column=0)

    my_entries.append(ent)
    entry_row = entry_row+1


def getter():
    for entry in my_entries:
        my_stuff = entry.get()
        print(my_stuff)


entries_widget = tk.Frame(root)


addent = tk.Button(root, text="Add Entry", command=addentry)
addent.pack(side=tk.TOP)
getent = tk.Button(root, text='get input', command=getter)
getent.pack(side=tk.TOP)
entries_widget.pack(side=tk.BOTTOM, fill=tk.X)
root.mainloop()

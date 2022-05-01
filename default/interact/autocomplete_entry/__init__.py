"""
Inspired by http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
Changes:
    - Fixed AttributeError: 'AutocompleteEntry' object has no attribute 'listbox'
    - Fixed scrolling listbox
    - Case-insensitive search
    - Added focus to entry field
    - Custom listbox length, listbox width matches entry field width
    - Custom matches function
"""

from multiprocessing.sharedctypes import Value
from tkinter import *
import re


class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, extramethod: tuple = None, *args, **kwargs):
        """
        # incoming = yourMethod, int
        # incoming int options (2nd arg in tuple): 
            0 -> return
            1 -> on_write (self.changed)

        # sortedlist if True = alphabetical order 
            whereas elif False = no ordering 
            :default: True
        """

        # extra method execution, on_write or on return of value [I am pdj]
        if extramethod is not None:
            if isinstance(extramethod, tuple):
                try:
                    self.incoming_func, self.incoming_int = extramethod
                except ValueError as e:
                    raise e
            else:
                self.incoming_func = extramethod
                self.incoming_int = 0
            if not callable(self.incoming_func) or not isinstance(self.incoming_int, int):
                raise ValueError
        else:
            self.incoming_func = False

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile(
                    '.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches

        if 'sortedlist' in kwargs:
            if kwargs['sortedlist']:  # True
                self.autocompleteList = sorted(autocompleteList)
            else:  # False
                self.autocompleteList = autocompleteList
            del kwargs['sortedlist']  # Entry init's cause
        else:  # default
            self.autocompleteList = sorted(autocompleteList)

        Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)

        self.listboxUp = False

    def changed(self, name, index, mode):
        self.__write_changed(name, index, mode)
        if self.incoming_func and self.incoming_int == 1:
            self.incoming_func()

    def selection(self, event):
        if self.listboxUp:
            self.__return_right(event)

            if self.incoming_func and self.incoming_int == 0:
                self.incoming_func()

    def __write_changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(
                        width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(
                        x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END, w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False

    def __return_right(self, event):
        self.var.set(self.listbox.get(ACTIVE))
        self.listbox.destroy()
        self.listboxUp = False
        self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]


def matches(fieldValue, acListEntry):
    pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
    return re.match(pattern, acListEntry)

# if __name__ == '__main__':
#     autocompleteList = [
#         'Teste DASDASFASFAS AKFSKJLAS FLKJAS LKJFLKJAS LKJFLKJASF LKJASFLJK ASLKJ FLKJASKLJFKJLASF SA', 'Silas', 'Osiel']


#     root = Tk()
#     entry = AutocompleteEntry(
#         autocompleteList, root, listboxLength=6, width=32, matchesFunction=matches)
#     entry.grid(row=0, column=0)

#     root.mainloop()

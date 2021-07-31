# SyntaxWarning: import * only allowed at module level
from time import sleep
import threading


def press_key_b4(key: str):
    from keyboard import is_pressed
    """
    Só dá break quando uma tecla específica é pressionada, e então, continua o código
    :param key:
    :return:
    """

    while True:
        #
        if is_pressed(key):
            if is_pressed(key):
                return True
        else:
            ...


def press_keys_b4(*keys: str):
    from keyboard import is_pressed
    """
    :param keys: any key you wish
    :return:
    """
    while True:
        for key in keys:
            if is_pressed(key):
                if is_pressed(key):
                    return key
            else:
                pass
                # print(key)

def foritab(n, *hkeys, interval=.13):
    import pyautogui as pygui
    """
    :param int n: how many times
    :param str hkey: hotkey
    :param float interval:
    :return:
    """
    for ii in range(n):
        for hkey in hkeys:
            pygui.hotkey(hkey, interval=interval)


def all_keys(*keys, interval=.13, only1_by1=True):
    import pyautogui as pygui
    from time import sleep
    """
    :param str keys: Any
    :param float interval:
    :param bool only1_by1: True [safe/DEFAULT]; False => Allows hotkeys with write
    :return:

    # Quando tiver hotkey, aparentemente sempre vai começar com ctrl, shift, alguma coisa do tipo... por isso
    # if cont > 0 and only_by1 True, break
    """
    full_hotkey_list = pygui.KEYBOARD_KEYS
    for cont, key in enumerate(keys):
        if key in full_hotkey_list:
            if cont > 0 and only1_by1:
                raise UserWarning("Security warning, SET only1_by1 as False [then you'll be able to use hotkeys with write]")

            list_keys = []
            for kd in keys:
                pygui.keyDown(kd, _pause=interval)
                list_keys.append(kd)
            list_keys.reverse()
            for k in list_keys:
                pygui.keyUp(k)
            if only1_by1:
                break
        else:
            pygui.write(key)
            sleep(interval)


def contmatic_select_by_name(name):
    import os

    p1path = os.getenv('APPDATA')
    CONTMATIC_PATH = p1path + r'\Microsoft\Windows\Start Menu\Programs\Contmatic Phoenix'
    print(CONTMATIC_PATH)
    for file in os.listdir(CONTMATIC_PATH):
        if name.lower() in file.lower():
            return CONTMATIC_PATH + f'\\{file}'
        print(file)


def activate_window(title, where=''):
    """
    :param title: nome/name janela/window
    :param where: optional. Message
    :return: última janela de um title específico ativada para manipular a princípio o diálogo do sistema operacional

    # done
    """
    from pyautogui import getWindowsWithTitle, hotkey, getActiveWindow, keyUp, keyDown
    # my_window = getWindowsAt(-1055, 0)[0]

    window = getWindowsWithTitle(title)
    window = window[0]

    # print(window.right, window.top, '..', window.title)
    # window.move(1055, 0)
    sleep(2)
    msg = f'{window.title}.\n\n {where.upper() if where != "" else ""}'
    # self.mensagem(msg)
    tk_msg(msg)
    tabs = ['tab']
    while True:

        sleep(2)
        try:
            var = getActiveWindow().title
            var = var.lower()
            win_logic = window.title.lower()
            print(var, window.title)
            if var == win_logic:
                break
            else:
                keyDown('alt')
                for tab in tabs:
                    hotkey(tab)
                sleep(.5)
                keyUp('alt')
                tabs.append('tab')
        except AttributeError:
            print('window not found')
            pass


def tk_msg(mensagem:str, time=7):
    """
    chamada em activate_driver_window
    :param mensagem: text displayed
    :param time: cont time before closes
    """
    import tkinter as tk

    class ExampleApp(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            tk.Label(text=mensagem, pady=10).pack()

            tk.Button(self, text="OK", fg='white', bg='black', command=self.destroy, activeforeground="black",
                      activebackground="green4", pady=10, width=10).pack()

            self.label = tk.Label(self, text="", width=10)
            self.label.pack()
            self.remaining = 0
            self.countdown(time)
            # self.after(time * 1000, lambda: self.destroy())

            self.geometry('500x250+1400+10')

        def countdown(self, remaining=None):
            if remaining is not None:
                self.remaining = remaining

            if self.remaining <= 0:
                self.label.configure(text="000000")
                self.destroy()
            else:
                self.label.configure(text="%d" % self.remaining)
                self.remaining = self.remaining - 1
                self.after(1000, self.countdown)

    print('Mensagem: ', mensagem)
    ExampleApp().mainloop()


class DownloadToWorldThread (threading.Thread):
    def __init__(self, threadID, name, counter, *args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.args = args

    def run(self):
        print('Args are: {}'.format(self.args))
        self.downloadToMyHouse(self.args)

    def downloadToMyHouse(self, *args):
        for i in args:
            print(i)

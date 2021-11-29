from time import sleep
import pyautogui as pygui
from default.interact import press_keys_b4, foritab

win = pygui.getWindowsWithTitle('G5 Phoenix')[0]
win.restore()
win.show()
win.activate()
sleep(2)
while True:
    pygui.hotkey('alt')
    foritab(6, 'down')
    pygui.hotkey('right', 'enter', interval=.2)
    press_keys_b4('=')

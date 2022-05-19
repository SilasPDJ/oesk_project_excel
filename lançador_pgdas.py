import pyautogui as pygui
from default.interact import *
from default.sets import InitialSetting, get_compt
p = pygui
COMPT = get_compt(-1)


def press(keys="F8"):
    keys = keys.upper()
    if keys == "F8":
        p.click(669, 392)
    elif keys == "F9":
        p.click(490, 560)
    else:
        p.click(138, 275)


def ate_atual_compt(first_compt=None):
    from datetime import date
    from dateutil import relativedelta
    if first_compt is None:
        yield COMPT
    else:
        first_compt = first_compt.split('-')
        if len(first_compt) == 1:
            first_compt = first_compt.split('/')
        first_compt = [int(val) for val in first_compt]
        first_compt = date(first_compt[1], first_compt[0], 1)

        # next_date = first_compt + relativedelta.relativedelta(months=1)

        last_compt = COMPT.split('-')
        # compt = [int(c) for c in compt]
        last_compt = [int(v) for v in last_compt]
        last_compt = date(last_compt[1], last_compt[0], 1)

        # list_compts = []
        while first_compt <= last_compt:
            compt = first_compt
            first_compt = first_compt + \
                relativedelta.relativedelta(months=1)

            compt_appended = f'{compt.month:02d}-{compt.year}'
            # list_compts.append(compt_appended)
            yield compt_appended


for compt in ate_atual_compt(get_compt(-13)):
    sleep(5)
    pygui.write(compt)
    sleep(.5)
    pygui.hotkey("enter")
    sleep(.5)
    press()
    sleep(.5)
    for i in range(3):
        if i >= 1:
            pygui.hotkey("backspace")
        sleep(.5)
        pygui.hotkey("enter")
        sleep(.5)
    press("F9")
    sleep(.5)

    press("F10")

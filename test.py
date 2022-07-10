from time import sleep
from pyautogui import click

MIN = 15
for i in range(MIN):
    sleep(60)
    click(500, 500, clicks=0)

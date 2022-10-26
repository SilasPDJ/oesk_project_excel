from pgdas_fiscal_oesk import Consultar
import sys
from time import sleep
from default.interact import all_keys

import webbrowser as wb
# wb.open("https://www.google.com.br")
import pyautogui as pygui
from clipboard import paste, copy
import ctypes
from default.sets import InitialSetting, get_compt


def jscript_exec(scrpt: str, open_console=False, close_console=False, delay=2.5):
    # WIN is a constant in fact
    if open_console:
        all_keys("ctrl", "shift", "j")
        sleep(1)
        ctypes.windll.user32.SetCursorPos(2759, 769)
        pygui.click(WIN.midright[0]-300, WIN.midright[1])
        # pygui.hotkey("tab")
    copy(scrpt)
    sleep(.25)
    pygui.hotkey("ctrl", "v")
    sleep(.25)
    pygui.hotkey("enter")
    sleep(1)
    if close_console:
        all_keys("ctrl", "shift", "j")  # close_console
    sleep(delay)


# declara Funcoes
FINDSPECIFC = '''
    let findSpecificELement =  (element, text) =>{
        for (let el of document.querySelectorAll(element)) {
        if (el.textContent.includes(text)) {
            return el
        }
        }
    };
    '''
# ---------------------

CHROMEPATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe %s --incognito"

# Focus mainWindow


def init():
    wb.get(CHROMEPATH)
    wb.open("https://cav.receita.fazenda.gov.br/autenticacao/login")
    while True:
        try:
            pygui.getActiveWindow
            win = pygui.getWindowsWithTitle("eCAC - Centro")[0]
            pygui.click(win.center, clicks=0)
        except IndexError:
            sleep(5)
        else:
            return win


def login():
    script = '''
    let login = document.querySelector("#login-dados-certificado");
    let loginInput = login.getElementsByTagName('input')[0];
    loginInput.click();
    '''
    jscript_exec(script)
    script = '''
    certDigital = document.querySelector("#cert-digital");
    certDigital.getElementsByTagName("a");
    let anchors = certDigital.getElementsByTagName("a");
    anchors[0].click();
    '''
    jscript_exec(script, close_console=True)

    [pygui.hotkey("tab") for i in range(3)]
    sleep(1)
    pygui.hotkey("enter")
    sleep(5)
    pygui.hotkey("tab")


# ALTERA PERFIL DE ACESSO


def dividas_ativas_complete(cnpj, compt=None):
    global WIN
    WIN = init()
    jscript_exec(FINDSPECIFC, True)
    login()

    script = f'''
    {FINDSPECIFC}
    findSpecificELement("span", "Alterar perfil de acesso").click();
    cnpj = document.querySelector("#txtNIPapel2");

    cnpj.value = "{cnpj}";
    formPJ = document.querySelector("#formPJ");
    formPJ.querySelector('input[type="button"]').click();
    '''
    jscript_exec(script, True)

    script = f'''
    {FINDSPECIFC}
    findSpecificELement("a", "Dívida Ativa").click();
    findSpecificELement("a", "Débitos Inscritos em Dívida").click();
    '''
    jscript_exec(script)

    sleep(3.5)
    script = '''
    findSpecificELement("span", "Negociar Dívida").click();


    '''

    jscript_exec(script)


# pj = "07083804000140"  # CNPJ de TESTE
# pj = sys.argv[-1]

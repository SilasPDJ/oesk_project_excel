from time import sleep
from default.interact import all_keys

import webbrowser as wb
# wb.open("https://www.google.com.br")
import pyautogui as pygui
from clipboard import paste, copy
import ctypes


def jscript_exec(scrpt: str, open_console=False, delay=1):
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
    sleep(delay)


# Focus mainWindow
def init():
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


WIN = init()

# declara Funcoes


def declare_funcoes():
    jscript_exec(
        '''
    let findSpecificELement =  (element, text) =>{
        for (let el of document.querySelectorAll(element)) {
        if (el.textContent.includes(text)) {
            return el
        }
        }
    };
    ''', True
    )


declare_funcoes()
# ----


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
    jscript_exec(script)

    [pygui.hotkey("tab") for i in range(3)]
    sleep(1)
    pygui.hotkey("enter")
    sleep(5)
    pygui.hotkey("tab")


login()
cnpj = "07083804000140"
script = f'''
findSpecificELement("span", "Alterar perfil de acesso").click();
cnpj = document.querySelector("#txtNIPapel2");

cnpj.value = "07083804000140";
formPJ = document.querySelector("#formPJ")
formPJ.querySelector('input[type="button"]').click()

'''
jscript_exec(script)


script = '''
findSpecificELement("a", "Dívida Ativa").click();
findSpecificELement("a", "Débitos Inscritos em Dívida").click();
'''
jscript_exec(script)


sleep(3.5)
script = '''
findSpecificELement("span", "Negociar Dívida").click();


''', True

jscript_exec(*script)


# jscript_exec()

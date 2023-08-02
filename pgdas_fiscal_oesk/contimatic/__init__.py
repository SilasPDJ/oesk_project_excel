from default.sets import InitialSetting
from default.interact import *
from time import sleep
import pyautogui as pygui
from os import path


class Contimatic(InitialSetting):
    def __init__(self, client_path):
        self.client_path = client_path

    def registronta(self):
        """
        :return: True: prossegue, False: não prosssegue
        """
        registronta = False
        # TODO: e se for o almeida com XML???
        for f in self.files_get_anexos_v4(self.client_path, file_type='xml'):
            registronta = True

        for f in self.files_get_anexos_v4(self.client_path, file_type='csv'):
            registronta = True
        if registronta is False:
            print('\033[1;31m NÃO TEMOS xml OU csv PARA IMPORTAR\033[m')
            return False
            # pois não haverá csv ou xml para importar

        for f in self.files_get_anexos_v4(self.client_path, file_type='pdf'):
            if 'ISS' in f.upper() and 'REGISTRO' in f.upper():  # ISSQN
                registronta = False
                break
            else:
                registronta = True
        return registronta

    def __read_login(self, admin=False):
        """
        :return: password

        """
        filepath = path.dirname(__file__)
        filepath += '/../data_clients_files/contimatic.txt'
        with open(filepath) as f:
            passwords = f.readlines()

        if not admin:
            return passwords[1].split()
        else:
            return passwords[0].split()

    def __make_screenshot(self):
        sc = pygui.screenshot(region=(300, 10, 10, 10))
        sc.save("O:/test.png")
        return sc

    def abre_ativa_programa(self, name):
        """
        :param name: nameProgram

        * Caso o programa 'name' não esteja aberto, ele abre pelo autoSky
        * Caso 'name' está aberto, ele é ativado
        # Auto.Sky opened
        :return:
        """
        login, passwd = self.__read_login()
        # _sname = f'{name} Phoenix'

        def faz_login():
            # Faz login em qualquer aplicativo
            sleep(7)
            __title = '(Remoto)'
            for w in pygui.getWindowsWithTitle(__title):
                print(w.title)
                if w.title.strip() == __title:
                    ativa_janela(w)
                    pygui.move(0, -125)
                    # moveTo X move...
                    pygui.doubleClick()
                    pygui.write(login)
                    pygui.hotkey('tab')
                    pygui.write(passwd)
                    foritab(2, 'tab')
                    pygui.hotkey('enter')
                    break

        while True:
            # with screenshot
            rgb = (102, 203, 234)
            try:
                searched = pygui.getWindowsWithTitle(name)
                searched = searched[0]
                ativa_janela(searched)

            except IndexError:
                print('index error')
                auto_sky_window = pygui.getWindowsWithTitle('Auto.Sky')[0]
                ativa_janela(auto_sky_window)
                pygui.write(name)
                pygui.hotkey('enter')
                faz_login()
                sleep(15)
            finally:
                sleep(2)
                _screenshot = self.__make_screenshot()
                print(_screenshot.getpixel((5, 5)), rgb)
                if _screenshot.getpixel((5, 5)) != rgb:
                    print('activating...')
                    pygui.click(150, 0)
                    # just to focus...
                    sleep(3)
                else:
                    print('DONE activation')
                    break
                if name.upper().strip() in pygui.getActiveWindowTitle().upper():
                    print('DONE activation and break')
                    break

    def activating_client(self, client_cnpj):
        x, y = 30, 60
        sleep(5)
        pygui.click(x, y)
        sleep(.7)
        # ativa empresa

        pygui.write(self.first_and_last_day_compt(self.compt_used, '')[1])

        foritab(6, 'tab', interval=0.13)  # PESQUISA
        pygui.hotkey('enter')
        sleep(1.5)
        all_keys('shift', 'tab')
        sleep(1)
        foritab(6, 'down', interval=0.13)  # PESQUISAR POR CGC[CNPJ]
        sleep(.5)
        foritab(1, 'tab')  # Digite a frase contida no texto
        all_keys(client_cnpj)
        print(f'{client_cnpj}:^~30')

        all_keys('ctrl', 'down')
        foritab(2, 'enter', interval=1)
        sleep(1)

        pygui.hotkey('tab', 'enter', interval=1)
        # Caso apareça aquela mensagem chata

        # ##################################################### PAREUI DAQUI, SELECIONEI JÁ... MAS TESTAR...
        # sleep(20)

    def formatar_cnpj(self, cnpj):
        cnpj = str(cnpj)
        if len(cnpj) < 14:
            cnpj = cnpj.zfill(11)
        cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        print(cnpj)  # 123.456.789-00
        return cnpj

    @staticmethod
    def start_walk_menu():
        x, y = 30, 30
        pygui.click(x, y)
    # free onedrive diskspace

    @staticmethod
    def free_ondrv_dskspace(path):
        from subprocess import run
        run('attrib +U -P "' + path + '"')

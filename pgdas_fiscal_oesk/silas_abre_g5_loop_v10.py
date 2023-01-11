import os
from typing import final
import pyautogui as pygui
from time import sleep

from default.interact import *
# from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts

# from pgdas_fiscal_oesk.contimatic import InitialSetting
from pgdas_fiscal_oesk.contimatic import Contimatic

from pgdas_fiscal_oesk.relacao_nfs import NfCanceled

# from default.webdriver_utilities import *
from subprocess import Popen

"""
from LE_NF_CANCELADAS_cor import main as nf_canceled
import ATIVA_EMPRESA
import PROGRAMA_REQUIRED
import NEEDED_PANDAS
from datetime import datetime
import os
"""

# um por um?
# vai p/ NEEDED_PANDAS

# ctrl_shift+M
pygui.PAUSE = 0.02


class G5(Contimatic):

    def __init__(self, *args, compt):
        __r_social, __cnpj, __cpf, __cod_simples, __valor_competencia, imposto_a_calcular, nf_out, nf_in = args
        __client = __r_social
        self.compt_used = compt
        self.__client = __client
        self.client_path = self.files_pathit(__client)
        self.contimatic_folder = self.files_pathit('contimaticG5')
        super().__init__(self.client_path)
        if imposto_a_calcular == 'ISS':
            print(__client)
            # Se tem 3valores[excel], tem XML. Se não tem, não tem
            # (pois o xml e excel vem do ginfess_download)....

            if self.registronta() and "ok" != nf_out.lower() not in ['s', 'ok', 'ok0']:
                self.abre_ativa_programa('G5 ')  # vscode's cause
                self.activating_client(self.formatar_cnpj(__cnpj))
                # - IMPORTA NF
                self.importa_nfs_iss()

                # ISS somente
                timesleep_import = 5.5
                all_xls_inside = self.files_get_anexos_v4(
                    self.client_path, file_type='xlsx')
                relacao_notas = all_xls_inside[0] if len(
                    all_xls_inside) == 1 else IndexError()
                # clientes com arquivo fora do ABC, xlsx != csv...
                if not isinstance(relacao_notas, IndexError):
                    self.nfcanceladas = NfCanceled(relacao_notas)
                    _wb_exists = self.walget_searpath(f'{__r_social[:__r_social.find(" ")]}_{__cnpj}.xlsx',
                                                      self.client_path, 2)
                    self.excel_iss_file = dict(
                        enumerate(_wb_exists)).get(0, False)
                    if _wb_exists:
                        timesleep_import = self.nfcanceladas.conta_qtd_nfs()
                    else:
                        timesleep_import = 10
                else:
                    timesleep_import = 30
                    print('\033[1;31m self.nfcanceladas is None \033[m')
                    self.nfcanceladas = None

                sleep(timesleep_import)

                __wcenter = pygui.getActiveWindow().center

                pygui.click(*__wcenter, clicks=0)
                pygui.move(320, -310)
                sleep(1)
                pygui.click()
                try:
                    self.mk_nf_canceladas()
                except Exception as e:
                    print(e)
                    pass
                    # REPOD pegar qual exception
                self.gera_relatorio_iss()
                self.foxit_save__iss(__cnpj)
                sleep(3)
                # F4
                # TODO: Salvar dentro do local de salvar relatorio, client_path
            elif "ok" == nf_out:
                self.abre_ativa_programa('G5 ')  # vscode's cause
                self.activating_client(self.formatar_cnpj(__cnpj))
                self.foxit_save__iss(__cnpj)

        elif imposto_a_calcular == 'ICMS':

            print(__client, nf_out)
            _already_exist = self.walget_searpath(
                "APUR_ICMS", self.client_path, 2)

            _already_exist += self.walget_searpath(
                "LIVRO_ENTRADA", self.client_path, 2)
            _already_exist += self.walget_searpath(
                "LIVRO_SAIDA", self.client_path, 2)
            if not _already_exist:
                self.abre_ativa_programa('G5 ')
                self.activating_client(self.formatar_cnpj(__cnpj))
                self.__ativa_robo_once(pygui.getActiveWindow())
                if nf_out.upper() != "NÃO HÁ":
                    if "ok" != nf_out.lower() != "s":  # != ent saidas importadas
                        self.importa_nf_icms_saidas()  # saídas somente
                    else:
                        self.__saida_entrada('s')
                    self.foxit_save__icms()
                self.abre_ativa_programa('G5 ')
                if '0' not in nf_in:
                    # entradas não zeraram
                    self.importa_nf_icms_entradas()
                    # self.__saida_entrada('e')
                    self.foxit_save__icms()
                    all_keys('alt', 'f4')

                # apuração ICMS
                self.abre_ativa_programa('G5')
                pygui.hotkey('f2')
                sleep(.5)
                foritab(6, 'enter')
                sleep(20)
                self.foxit_save__icms()

                all_keys('alt', 'f4')
                print('fim')

    @ staticmethod
    def __ativa_robo_once(window: pygui.Window):
        pygui.FAILSAFE = False
        pygui.click(window.topright, clicks=0)
        pygui.move(-140, 50)
        pygui.FAILSAFE = True
        rgb = (91, 91, 91)
        _screensear = pygui.screenshot(region=(1770, 55, 30, 20))

        if _screensear.getpixel((15, 10)) == rgb:
            pygui.click()

    @ staticmethod
    def __gotowincenter(win):
        if isinstance(win, str):
            win = pygui.getWindowsWithTitle(win)[0]
        elif not isinstance(win, pygui.Window):
            raise ValueError('must be', str, 'or', pygui.Window)
        win.activate()
        pygui.click(*win.center, clicks=0)
        return win

    def __saida_entrada(self, key):
        self.abre_ativa_programa('G5 ')
        all_keys('ctrl', 'shift', key)

        foritab(7, 'enter')
        sleep(10)

    def importa_nf_icms_saidas(self):

        def ativa_foxit_openexplorer():
            self.__gotowincenter('Foxit Reader')
            pygui.getActiveWindow().maximize()
            pygui.move(-820, -360)
            sleep(10)
            pygui.rightClick()
            sleep(.5)
            foritab(3, 'up')
            pygui.hotkey('enter')

        def go2_g5_import_params():
            pygui.hotkey('alt')
            # eu smp ↑↑
            foritab(6, 'down')
            foritab(1, 'right', 'down', 'enter',)

        def robotimatic_config_path(_path2import: str, opt: int = None):
            """
            path2import: path2import typed
            """
            sleep(4)
            _win = pygui.getActiveWindow()
            _import_opcoes = ('SAIDAS', 'nfentrada',
                              'cte-saida', 'cte-entrada',
                              'cte-sat', 'sped', 'nfp', 'nfse-tomado',
                              'nfse-prestado')
            _import_opcoes = {k: v for k, v in enumerate(_import_opcoes)}
            if opt is not None:
                foritab(3, 'up')
                foritab(2, 'tab')
                foritab(opt, 'right')
                sleep(.5)
                pygui.hotkey('enter')
                # seleciona quais são
                sleep(1)
            pygui.click(_win.center, clicks=0)
            pygui.move(0, -170)  # write
            pygui.click()  # write
            all_keys('ctrl', 'a')
            sleep(.5)
            pygui.hotkey('backspace')
            sleep(.5)
            pygui.write(_path2import)

            pygui.click(_win.center, clicks=0)
            pygui.move(250, 250)  # gravar
            pygui.click()  # gravar
            sleep(1)  # gravar
            pygui.hotkey('enter')
            sleep(.5)
            all_keys('alt', 'f4')  # close import config
            sleep(1)
            self.abre_ativa_programa('G5')
            # go2robo options

        # abre explorer
        if not self.walget_searpath('dirsInCloud.txt', self.client_path, 2):
            self.__saida_entrada('e')
            self.__saida_entrada('s')
            ativa_foxit_openexplorer()
            sleep(2)
            self.__gotowincenter('Foxit Reader')
            pygui.hotkey('alt', 'f4')
            sleep(2)
            self.__foxit_explorer_write('I:\\SILAS_NFS')
        path2import = self.__xml_send2cloud_icms()
        print(path2import)
        print('Only Once')
        self.abre_ativa_programa('G5')
        sleep(1)
        # pathchecker = path2import.split('\\')[-1].upper()

        go2_g5_import_params()
        robotimatic_config_path(path2import)  # ↑
        sleep(2)
        self.go2robo_options()
        sleep(1)
        foritab(1, 'up', 'right', 'enter', interval=0.25)
        # aí tem que sleepar pq ta importando, TODO: calcular o sleep
        segs = self._while_importing()
        sleep(5)
        print(segs)
        # SÓ É PRECISO IMPORTAR 1X PQ AS SAÍDAS ESTÃO JUNTAS

    def _while_importing(self):
        cont = 0
        c = 10
        # TODO: Necessário fechar o foxit depois de abrir o server explorer
        while "FOXIT READER" not in pygui.getActiveWindowTitle().upper() or "LIVRO_SAIDA" not in pygui.getActiveWindowTitle().upper():
            print('sleeping', pygui.getActiveWindowTitle().upper())
            sleep(c)
            cont += c
            pygui.click(pygui.getActiveWindow().midtop)
            self.__saida_entrada('s')
        return cont

    def importa_nf_icms_entradas(self):
        self.go2robo_options()
        foritab(1, 'up', 'right', 'up', 'enter', interval=0.25)
        sleep(60)

    @ staticmethod
    def go2robo_options():
        pygui.FAILSAFE = False  # Robo_Options
        pygui.click(pygui.getActiveWindow().topright,
                    clicks=0)
        # COMO ATIVAR ROBÔ AUTOMÁTICO?
        pygui.move(-105, 50)
        pygui.FAILSAFE = True
        pygui.click()

    def __xml_send2cloud_icms(self):
        volta = os.getcwd()

        def __canb_pathdir(pd: str):
            canb_pathdir = os.path.join(pd, 'XML', 'Autorizadas')
            if os.path.exists(canb_pathdir):
                return canb_pathdir

        def __local_explorer_copy2(pathdir):
            canbpd = __canb_pathdir(pathdir)
            pathdir = canbpd if canbpd is not None else pathdir
            _p = Popen(f'explorer "{pathdir}"')

            sleep(3)
            all_keys('ctrl', 'a')
            sleep(1)
            all_keys('ctrl', 'c')
            _p.terminate()
            # return os.listdir(pathdir)
            # CLEISON/MARCO WAY...

        def createfolder(w, enters=2):
            # createfolder
            all_keys('ctrl', 'shift', 'n')
            pygui.write(w)
            sleep(.5)

            foritab(enters, 'enter', interval=.5)
            sleep(2)

        def foxitpath_creation_exists():
            for _, dirnames, __ in os.walk(self.client_path):
                # unique filespath, is checked
                unfpath = f'{self.client_path}/{dirnames[0]}'

                # if find xml is in folder... RETURN no es mercadolibre

                if not os.path.exists(f'{unfpath}/.autosky'):  # searpath?
                    SILASNFS_WINDOW.activate()
                    # importg5_file_confirmation = '.imes'
                    if not os.path.exists(f'{self.contimatic_folder}/.imes'):
                        createfolder(self.compt_used)
                        open(f'{self.contimatic_folder}/.imes', 'w').close()
                        # pra nao criar o mes duas vezes
                    else:
                        self.__foxit_explorer_write(
                            f'I:\\SILAS_NFS\\{self.compt_used}')
                        # se o mes ja foi criado então desconsidera

                    createfolder(self.__client)
                    [createfolder(_clientf__, enters=1)
                        for _clientf__ in dirnames]
                    [open(
                        f'{self.client_path}/{_clientf__}/.autosky', 'w').close()
                        for _clientf__ in dirnames]
                    # cria os dois CERTIFICADOS

                returned = True
                for __dn in dirnames:
                    mysetpath = os.path.join(
                        self.client_path, __dn)

                    myset = set(self.files_get_anexos_v4(
                        mysetpath, 'xml')) or None
                    if myset is None:
                        returned = False
                    else:
                        return True
                        # AS ENTRADAS NÃO FICAM AQUI
                        # pois se achar, é pq n tem mais oq procurar...
                else:
                    if len(dirnames) == 0:
                        print(
                            f'\033[1;31m Não houve notas ICMS de {self.__client}\033[m')
                        # Se existir dir, ele já vai procurar...
                        return False
                    else:
                        mercadolibr = os.walk(self.client_path)
                        mercadolibr = list(mercadolibr)
                        if len(mercadolibr[1][1]) >= 1:
                            # se tiver pasta dentro de pasta...
                            return 'LIBRE'
                return returned
                # sempre vai existir, pq criará se não...
        SILASNFS_WINDOW = self.__gotowincenter(
            'SILAS_NFS')
        libre_or_normal = foxitpath_creation_exists()
        if libre_or_normal is not False:
            # TODO: fazer listdir dentro... e procurar outros documentos, etc
            # os.chdir(self.client_path)

            for _, dirnames, __ in os.walk(self.client_path):
                pathimport = False
                for clientf in dirnames:
                    __mypath = os.path.join(self.client_path, clientf)
                    # abspath pega o chdir atual
                    listfoldersindir = [os.path.join(__mypath, d) for d in os.listdir(
                        __mypath) if os.path.isdir(os.path.join(__mypath, d)) and d.upper() != 'OUTROS DOCUMENTOS']

                    filesincloud_checkerpath = os.path.join(
                        self.client_path, clientf, 'dirsInCloud.txt')

                    if libre_or_normal == 'LIBRE':
                        try:
                            __lfid = [os.path.join(__mypath, d) for d in os.listdir(
                                __mypath) if d.upper() == 'OUTROS DOCUMENTOS'][0]
                            listfoldersindir += [os.path.join(__lfid, dd)
                                                 for dd in os.listdir(__lfid)]
                        except IndexError:
                            pass
                        for __mainfolder in listfoldersindir:
                            __dircreation = pathimport = f'I:\\SILAS_NFS\\{self.compt_used}\\{self.__client}\\{clientf}'
                            # yield mainfolder
                            mainfolder__lastfolder = __mainfolder.split(
                                '\\')[-1]
                            if mainfolder__lastfolder.upper() != 'CT-E':  # não é necessário
                                pathimport += '\\NFsSaidas'
                                # vai mudar os yields....

                                canbpd = __canb_pathdir(__mainfolder)
                                _1xpathdir = canbpd if canbpd is not None else __mainfolder
                                sleeplen = len(os.listdir(
                                    _1xpathdir)) / 17 + 10

                                if not os.path.exists(filesincloud_checkerpath):
                                    __local_explorer_copy2(__mainfolder)
                                    SILASNFS_WINDOW.activate()

                                    # if folder.upper() != 'OUTROS DOCUMENTOS':
                                    if __mainfolder == listfoldersindir[0]:
                                        SILASNFS_WINDOW.activate()
                                        sleep(1)
                                        self.__foxit_explorer_write(
                                            __dircreation)
                                        sleep(.5)
                                        pygui.click(
                                            SILASNFS_WINDOW.center, clicks=0)
                                        sleep(.5)
                                        createfolder('NFsSaidas')
                                    # else:
                                    #     self.__foxit_explorer_write(pathimport)

                                    sleep(1.5)
                                    all_keys('ctrl', 'v')
                                    print(sleeplen, 'sleep time')
                                    sleep(sleeplen)
                                    pygui.hotkey('esc')
                                print('next client, atual: ', __mainfolder)
                    else:
                        __lfid = [d for d in os.listdir(
                            __mypath)]
                        # pathimport = f'I:\\SILAS_NFS\\{self.compt_used}\\{self.__client}\\{clientf}'
                        pathimport = f'I:\\SILAS_NFS\\{self.compt_used}\\{self.__client}'
                        if not os.path.exists(filesincloud_checkerpath):
                            sleeplen = len(__lfid) / 20 + 10
                            __local_explorer_copy2(__mypath)
                            SILASNFS_WINDOW.activate()
                            self.__foxit_explorer_write(
                                pathimport)
                            sleep(1)
                            all_keys('ctrl', 'v')
                            print(sleeplen, 'sleep time')
                            sleep(sleeplen)
                            open(filesincloud_checkerpath, 'w').close()
                        # return pathimport
                    if not os.path.exists(filesincloud_checkerpath):
                        open(filesincloud_checkerpath, 'w').close()
                    # self.free_ondrv_dskspace(f'{_mainpath}\*.')
                    # TODO: importar NFs... path//to//folder/*.xml
                    return pathimport
        # yield the import

    def importa_nfs_iss(self):
        def exe_bt_executar(import_items=True):
            def minimenu_gotmore_opts() -> bool:
                possible_rgbs = [(76, 171, 52), (130, 224, 89), (21, 124, 13)]
                imbutton = pygui.screenshot(
                    'is_sp_city.png', region=(841, 791, 20, 20))
                if imbutton.getpixel((5, 5)) in possible_rgbs:
                    return 841+5, 791+5
                return False
            # g5 opts menu is bigger
            gotmore_x_y = minimenu_gotmore_opts()
            if gotmore_x_y:
                pygui.click(gotmore_x_y)
            else:
                if import_items:
                    pygui.click(pygui.getActiveWindow().center, clicks=0)
                    pygui.move(10, 100)
                    pygui.click()

                pygui.click(pygui.getActiveWindow().center, clicks=0)
                pygui.move(0, 200)
                pygui.click()
                foritab(4, "enter", interval=2)

            # FUNCIONAL P/ TUDO MENOS REPOD

        def preenche_arqpath(arqpath):
            pygui.click(pygui.getActiveWindow().center, clicks=0)
            sleep(1)
            pygui.move(0, -235)
            pygui.click(duration=1)
            print(arqpath)
            foritab(2, 'space', 'backspace')
            sleep(1)
            pygui.write(arqpath)

        ARQSPATH = self.__get_xml_nf_csv()
        for contarq in range(len(ARQSPATH)):
            if contarq >= 1:
                pygui.hotkey('alt', 'f4')
            foritab(1, 'alt', 'right')
            foritab(2, 'down')
            foritab(1, 'right', 'up', 'up', 'enter')
            sleep(5)
            preenche_arqpath(ARQSPATH[contarq])

            if os.path.basename(ARQSPATH[contarq]).upper().startswith("TOMADOR"):
                sleep(2.5)
                pygui.click(x=823, y=382)

            exe_bt_executar()
            # TODO: reformular exe_executar p/ pegar a parte verde do print
            if len(ARQSPATH) > 1:
                sleep(30)

    def gera_relatorio_iss(self):
        sleep(1)
        # generate PDF relat. Prestados 56 #51
        self.start_walk_menu()
        foritab(3, 'right')
        foritab(6, 'down')
        # foritab(5, 'enter', interval=.25)
        foritab(1, 'enter', interval=.25)
        foritab(3, 'up', interval=.2)
        foritab(1, 'enter', interval=.25)
        foritab(4, 'enter', interval=.25)
        # generate pdf

        sleep(8)

    def __foxit_explorer_write(self, path):
        pygui.hotkey('f4')
        sleep(.5)
        pygui.hotkey('ctrl', 'a')
        pygui.hotkey('delete')
        pygui.write(path, interval=0.0125)
        pygui.hotkey('enter')
        sleep(1)

    def foxit_save__icms(self, add2file=None):
        all_keys('ctrl', 'shift', 's')
        sleep(.5)
        pygui.hotkey('home')
        sleep(.25)
        self.__foxit_explorer_write(self.client_path)
        pygui.hotkey('f4', 'enter', 'enter', interval=.5)
        winexplorer = pygui.getActiveWindow()
        winexplorer.moveRel(0, 100)
        pygui.click(clicks=0)
        pygui.hotkey('enter', 'enter', 'enter', 'enter', 'enter')
        sleep(2)
        pygui.hotkey('return', 'return', duration=1, interval=1)
        sleep(5)

    def foxit_save__iss(self, add2file):

        filename = f"Registro_ISS-{add2file}"
        all_keys('ctrl', 'shift', 's')
        sleep(.5)
        pygui.write(filename)
        sleep(.25)
        pygui.hotkey('f4')
        sleep(.5)
        pygui.hotkey('ctrl', 'a')
        pygui.hotkey('delete')
        pygui.write(self.client_path)
        pygui.hotkey('enter')
        sleep(1)
        pygui.hotkey('f4', 'enter', 'enter', interval=.5)
        winexplorer = pygui.getActiveWindow()
        winexplorer.moveRel(0, 100)
        pygui.click(clicks=0)
        pygui.hotkey('enter', 'enter', 'enter', 'enter', 'enter')
        sleep(2)
        pygui.hotkey('return', 'return', duration=1, interval=1)
        # pygui.hotkey('alt', 'f4')

    def mk_nf_canceladas(self) -> int:

        sleep(2)
        self.start_walk_menu()
        print('right down enter enter')
        pygui.hotkey('right', 'down', 'enter', 'enter', interval=.5)
        sleep(2)
        print('NF canceled')
        if self.nfcanceladas:
            self.nfcanceladas.action()

    def __get_xml_nf_csv(self, max_files_amount=2) -> list:
        importable_files = self.files_get_anexos_v4(
            self.client_path, file_type='xml')

        if len(importable_files) == 0:
            importable_files = self.files_get_anexos_v4(
                self.client_path, file_type='csv')

        def transform2typable(f: str):
            ff = f.split('\\')
            file = f'\\\\{ff[-1]}'
            final = '\\'.join(ff[:-1]) + file
            return final

        final_files = list(map(transform2typable,
                               importable_files[:max_files_amount]))
        return final_files

    def start_walk_menu(self):  # overriden, not necessary
        x, y = 30, 30
        pygui.click(x, y)

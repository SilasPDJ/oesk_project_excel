import os
import pyautogui as pygui
from time import sleep

from default.interact import *
# from default.sets import InitialSetting
from default.webdriver_utilities.wbs import WDShorcuts

# from pgdas_fiscal_oesk.contimatic import InitialSetting
from pgdas_fiscal_oesk.contimatic import Contimatic

from pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados, NfCanceled

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


class G5(Contimatic):

    def __init__(self, *args, compt):
        __r_social, __cnpj, __cpf, __cod_simples, __valor_competencia, imposto_a_calcular, nf_out = args
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

            if self.registronta() and "ok" != nf_out.lower() != "s":
                meus_3_valores_atuais = tres_valores_faturados(
                    self.client_path)
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
                self.nfcanceladas = NfCanceled(relacao_notas)

                if tres_valores_faturados(self.client_path):
                    timesleep_import = self.nfcanceladas.conta_qtd_nfs()
                sleep(timesleep_import)

                __wcenter = pygui.getActiveWindow().center

                pygui.click(*__wcenter, clicks=0)
                pygui.move(320, -300)
                sleep(1)
                pygui.click()
                self.mk_nf_canceladas()

                self.gera_relatorio_iss()
                self.foxit_save(__cnpj)
                sleep(3)
                # F4
                # TODO: Salvar dentro do local de salvar relatorio, client_path
        elif imposto_a_calcular == 'ICMS':
            print(__client, nf_out)

            if "ok" != nf_out.lower() != "s":  # primeiro saídas
                self.abre_ativa_programa('G5 ')
                # self.activating_client(self.formatar_cnpj(__cnpj))
                self.importa_nf_icms(nf_out)

    @staticmethod
    def __gotowincenter(win):
        win = pygui.getWindowsWithTitle(win)[0]
        win.activate()
        pygui.click(*win.center, clicks=0)

    def importa_nf_icms(self, nfout):

        def saida_entrada(key):
            self.abre_ativa_programa('G5 ')
            all_keys('ctrl', 'shift', key)

            foritab(7, 'enter')
            sleep(10)

        def ativa_foxit_openexplorer():
            self.__gotowincenter('Foxit Reader')
            pygui.getActiveWindow().maximize()
            pygui.move(-820, -360)
            sleep(2)
            pygui.rightClick()
            sleep(.5)
            foritab(3, 'up')
            pygui.hotkey('enter')

        def robotimatic_config_path(_path2import):
            sleep(4)
            _win = pygui.getActiveWindow()
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

        # abre explorer
        if not self.walget_searpath('dirsInCloud.txt', self.client_path, 2):
            saida_entrada('e')
            saida_entrada('s')
            sleep(2)
            ativa_foxit_openexplorer()
            sleep(2)
            self.__foxit_explorer_write('I:\\SILAS_NFS')

        listofdirs = list()
        for path2import in self.__xml_send2cloud_icms():
            if isinstance(path2import, list):
                for path2i in path2import:
                    print(path2i)
                    # listofdirs.append(path2i)
            else:
                listofdirs.append(path2import)
                # print(path2import)

        for path2import in listofdirs:
            self.abre_ativa_programa('G5')
            sleep(1)
            pathchecker = path2import.split('\\')[-1].upper()
            if pathchecker in ['NF-E DE DEVOLUÇÃO', 'NF-E DE VENDA', 'NF']:
                # if pathchecker in ['NF-E DE VENDA', 'NF']:
                # foritab(1, 'alt', 'right', 'down', 'right')
                pygui.hotkey('alt')
                # eu smp ↑↑
                foritab(6, 'down')
                foritab(1, 'right', 'down', 'enter',)
                robotimatic_config_path(path2import)  # ↑
                all_keys('alt', 'f4')  # close import config

                self.abre_ativa_programa('G5')
                pygui.FAILSAFE = False  # Ativa robô
                pygui.click(pygui.getActiveWindow().topright,
                            clicks=0)
                pygui.move(-105, 50)
                pygui.FAILSAFE = True
                pygui.click()
                foritab(1, 'up', 'right', 'down', 'enter', interval=0.25)
                # aí tem que sleepar pq ta importando, TODO: calcular o sleep
                sleep(70)

                # pygui.click()

    def __xml_send2cloud_icms(self):

        def copyfolder_vd(clientf__, folder) -> len:
            returned = 0

            volta = os.getcwd()
            # vd = venda/devolução
            mainSearched = 'XML', 'Autorizadas'

            # os.mkdir('ok')  # se tiver certificado vai pro prox

            # for folder in searched1st[:-1]:
            os.chdir(self.client_path)
            os.chdir(clientf__)
            # venda, devolução...
            if clientf__ != folder:  # ...
                try:
                    os.chdir(folder)
                except FileNotFoundError:
                    print('return 1')
                    return 1
                try:
                    [os.chdir(ms) for ms in mainSearched]
                except FileNotFoundError:
                    print('linha 152. Passing, no problem')
                    # Não existe...
                    returned += 1200  # incrementa segundos, outros documentos
            pathdir = os.getcwd()
            _p = Popen(f'explorer "{pathdir}"')
            sleep(3)
            all_keys('ctrl', 'a')
            sleep(0.5)
            [all_keys('ctrl', 'c') for i in range(2)]
            os.chdir(volta)
            _p.terminate()
            return len(os.listdir(pathdir)) + returned
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
                    self.__gotowincenter('SILAS_NFS')
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
        libre_or_normal = foxitpath_creation_exists()
        if libre_or_normal is not False:
            # TODO: fazer listdir dentro... e procurar outros documentos, etc
            # os.chdir(self.client_path)

            for _, dirnames, __ in os.walk(self.client_path):
                for clientf in dirnames:
                    mypath = os.path.join(self.client_path, clientf)
                    listfoldersindir = [d for d in os.listdir(
                        mypath) if os.path.isdir(os.path.join(mypath, d))]

                    filesincloud_checkerpath = os.path.join(
                        self.client_path, clientf, 'dirsInCloud.txt')

                    if libre_or_normal == 'LIBRE':
                        for folder in listfoldersindir:
                            yielded = f'I:\\SILAS_NFS\\{self.compt_used}\\{self.__client}\\{clientf}'
                            if folder.upper() != 'OUTROS DOCUMENTOS':
                                yield yielded + f'\\{folder}'
                            else:
                                yield [os.path.join(yielded, d) for d in os.listdir(
                                    os.path.join(mypath, folder)) if os.path.isdir(os.path.join(mypath, folder, d))]

                            if not os.path.exists(filesincloud_checkerpath):
                                self.__foxit_explorer_write('I:\\SILAS_NFS')

                                sleeplen = copyfolder_vd(clientf, folder)
                                self.__gotowincenter('SILAS_NFS')
                                self.__foxit_explorer_write(
                                    yielded)
                                if folder.upper() != 'OUTROS DOCUMENTOS':
                                    createfolder(folder)

                                all_keys('ctrl', 'v')
                                print(sleeplen/20+10, 'sleep time')
                                sleep(sleeplen/20+10)
                            print('next client, atual: ', folder)
                        if not os.path.exists(filesincloud_checkerpath):
                            open(filesincloud_checkerpath, 'w').close()
                    else:
                        yielded = f'I:\\SILAS_NFS\\{self.compt_used}\\{self.__client}\\{clientf}'
                        yield yielded
                        if not os.path.exists(filesincloud_checkerpath):
                            self.__foxit_explorer_write('I:\\SILAS_NFS')
                            sleeplen = copyfolder_vd(clientf, clientf)
                            self.__gotowincenter('SILAS_NFS')
                            self.__foxit_explorer_write(
                                yielded)
                            all_keys('ctrl', 'v')
                            print(sleeplen/20+10, 'sleep time')
                            sleep(sleeplen/20+10)
                            open(filesincloud_checkerpath, 'w').close()

                    # self.free_ondrv_dskspace(f'{_mainpath}\*.')
                    # TODO: importar NFs... path//to//folder/*.xml
                return
        # yield the import

    def importa_nfs_iss(self):
        def exe_bt_executar(import_items=True):
            if import_items:
                pygui.click(pygui.getActiveWindow().center, clicks=0)
                pygui.move(-206, 87)
                pygui.click()

            pygui.click(pygui.getActiveWindow().center, clicks=0)
            pygui.move(-25, 150)
            pygui.click()
            for _ in range(3):
                sleep(2)
                pygui.hotkey('enter')

        def preenche_arqpath():
            pygui.click(pygui.getActiveWindow().center, clicks=0)
            sleep(1)
            pygui.move(0, -225)
            pygui.click(duration=1)
            arqpath = self.__get_xml()
            print(arqpath)
            foritab(2, 'space', 'backspace')
            sleep(1)
            pygui.write(arqpath)

        foritab(1, 'alt', 'right')
        foritab(2, 'down')
        foritab(1, 'right', 'up', 'up', 'enter')
        sleep(5)

        preenche_arqpath()
        exe_bt_executar()

    def gera_relatorio_iss(self):
        sleep(1)
        # generate PDF relat. Prestados 56 #51
        self.start_walk_menu()
        foritab(3, 'right')
        foritab(6, 'down')
        # foritab(5, 'enter', interval=.25)
        foritab(1, 'enter', interval=.25)
        foritab(1, 'enter', interval=.25)
        foritab(5, 'down', interval=.25)
        foritab(4, 'enter', interval=.25)
        # generate pdf

        sleep(7.5)

    def __foxit_explorer_write(self, path):
        pygui.hotkey('f4')
        sleep(.5)
        pygui.hotkey('ctrl', 'a')
        pygui.hotkey('delete')
        pygui.write(path, interval=0.0125)
        pygui.hotkey('enter')
        sleep(1)

    def foxit_save(self, add2file):
        filename = f"Registro_ISS-{add2file}"
        all_keys('ctrl', 'shift', 's')
        sleep(.5)
        sleep(.25)
        self.__foxit_explorer_write(self.client_path)
        pygui.write(filename)
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
        self.nfcanceladas.action()

    def __get_xml(self):
        b = self.files_get_anexos_v4(self.client_path, file_type='xml')
        b = b[0]
        b = b.split('\\')
        file = f'\\\\{b[-1]}'
        final = '\\'.join(b[:-1]) + file
        return final

    def start_walk_menu(self):
        x, y = 30, 30
        pygui.click(x, y)

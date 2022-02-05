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
            print(__client)

            if "ok" != nf_out.lower() != "s":  # primeiro saídas
                self.abre_ativa_programa('G5 ')
                # self.activating_client(self.formatar_cnpj(__cnpj))
                self.importa_nf_icms()

    @staticmethod
    def __gotowincenter(win):
        win = pygui.getWindowsWithTitle(win)[0]
        win.activate()
        pygui.click(*win.center, clicks=0)

    def importa_nf_icms(self):

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

        # False kkkk
        saida_entrada('e')
        saida_entrada('s')
        sleep(2)
        ativa_foxit_openexplorer()
        sleep(2)
        self.__foxit_explorer_write('I:\\SILAS_NFS')

        # o tipo icms ja ta checado
        # if os.path.isdir(os.path.join(self.client_path, os.listdir(self.client_path)[0])):
        self.__xml_mercadolivre_icms()
        # #################### \*.xml, assim......
        # que importa tudo

        # test = self.files_get_anexos_v4(
        #     client_folder, 'xml')

        # self.__gotowincenter(self.__client)

    def __xml_mercadolivre_icms(self):

        def copyfolder_vd(clientf__, folder) -> len:
            volta = os.getcwd()
            # vd = venda/devolução
            mainSearched = 'XML', 'Autorizadas'

            # os.mkdir('ok')  # se tiver certificado vai pro prox

            # for folder in searched1st[:-1]:
            os.chdir(self.client_path)
            os.chdir(clientf__)
            # venda, devolução...
            os.chdir(folder)
            [os.chdir(ms) for ms in mainSearched]
            pathdir = os.getcwd()

            Popen(f'explorer "{pathdir}"')
            sleep(3)
            all_keys('ctrl', 'a')
            sleep(0.5)
            [all_keys('ctrl', 'c') for i in range(2)]
            os.chdir(volta)
            return len(os.listdir(pathdir))
            # CLEISON/MARCO WAY...

        def createfolder(w, enters=2):
            # createfolder
            all_keys('ctrl', 'shift', 'n')
            pygui.write(w)
            sleep(.5)

            foritab(enters, 'enter', interval=.5)
            sleep(2)

        def foxitpath_creation_exists():
            self.__gotowincenter('SILAS_NFS')
            for _, dirnames, __ in os.walk(self.client_path):
                # unique filespath, is checked
                unfpath = f'{self.client_path}/{dirnames[0]}'

                # if find xml is in folder... RETURN no es mercadolibre

                if not os.path.exists(f'{unfpath}/.autosky'):
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
                        returned = False
                    else:
                        mercadolibr = os.walk(self.client_path)
                        mercadolibr = list(mercadolibr)
                        if len(mercadolibr[1][1]) >= 1:
                            # se tiver pasta dentro de pasta...
                            returned = True
                print(returned)
                return returned
                # sempre vai existir, pq criará se não...

        if foxitpath_creation_exists():
            seard_mercadolivre = ['NF-e de venda',
                                  'NF-e de devolução', 'Outros documentos', ]

            for _, dirnames, __ in os.walk(self.client_path, 1):
                for clientf in dirnames:
                    for folder in seard_mercadolivre[:-1]:
                        self.__foxit_explorer_write('I:\\SILAS_NFS')
                        sleeplen = copyfolder_vd(clientf, folder)

                        self.__gotowincenter('SILAS_NFS')
                        self.__foxit_explorer_write(
                            f'I:\\SILAS_NFS\\{self.compt_used}\\{self.__client}\\{clientf}')
                        createfolder(folder)
                        all_keys('ctrl', 'v')
                        print(sleeplen/20+10, 'sleep time')
                        sleep(sleeplen/20+10)
                        # _mainpath = os.path.join(self.client_path, clientf)
                        # self.free_ondrv_dskspace(f'{_mainpath}\*.')
                        # na vdd funciona só com arquivos

                break
                # pra executar somente 1x...

        # searched1st[-1] #(outros doc/cte)
        # IMPORTAR UMA POR UMA NF

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

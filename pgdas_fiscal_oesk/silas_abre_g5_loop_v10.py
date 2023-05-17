import os
from typing import final
from typing_extensions import override
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

    def __init__(self, *args: str, compt):
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
            if self.registronta():
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
                self._ativa_robo_once(pygui.getActiveWindow())
                self.abre_ativa_programa('G5 ')
                # remove o if...
                # entradas não zeraram
                self.caminho_autorizadas_destino, self.caminho_canceladas_destino = self._settar_destino_icms()
                self.importa_nf_icms_saidas()

                # self.importa_nf_icms_entradas()
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
    def _ativa_robo_once(window: pygui.Window):
        pygui.FAILSAFE = False
        pygui.click(window.topright, clicks=0)
        pygui.move(-140, 50)
        pygui.FAILSAFE = True
        rgb = (91, 91, 91)
        _screensear = pygui.screenshot(region=(1770, 55, 30, 20))

        if _screensear.getpixel((15, 10)) == rgb:
            pygui.click()

    @ staticmethod
    def __gotowinscenter(*wins):
        for win in wins:
            if isinstance(win, str):
                try:
                    win = pygui.getWindowsWithTitle(win)[0]
                except IndexError:
                    continue
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

    def _robotimatic_config_path(self, _path2import: str, opt: int = None):
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

    def _extract_folder(self) -> bool:
        import zipfile

        zips_path = self.files_get_anexos_v4(self.client_path, 'zip')
        if len(zips_path) == 1:
            with zipfile.ZipFile(zips_path[0], 'r') as zip_ref:
                # extract the contents of the zip file to a folder
                zip_ref.extractall(os.path.join(self.client_path, "NFS"))
                return True
        elif len(zips_path) >= 1:
            print('\033[1;31mMais de um zip path\033[m')

        else:
            print(f'\033[1;33mAinda sem zip para {self.client_path}\033[m')
        return False

    def importa_nf_icms_saidas(self):

        def go2_g5_import_params():
            pygui.hotkey('alt')
            # eu smp ↑↑
            foritab(6, 'down')
            foritab(1, 'right', 'down', 'enter',)

        if self._extract_folder():
            self._xml_send2cloud_icms()
            for path2import in [self.caminho_autorizadas_destino, self.caminho_canceladas_destino]:
                if path2import == '':
                    continue
                print(path2import, 'sou o path2import')
                print('Only Once')
                self.abre_ativa_programa('G5')
                sleep(1)
                # pathchecker = path2import.split('\\')[-1].upper()

                go2_g5_import_params()
                self._robotimatic_config_path(path2import)  # ↑
                sleep(2)
                self._go2robo_options()
                sleep(1)
                foritab(1, 'up', 'right', 'enter', interval=0.25)
                # aí tem que sleepar pq ta importando, TODO: calcular o sleep
                segs = self._while_importing(path2import)
                print(f'{path2import}. sleeping: ', segs, )
                print('Espere para excluir automaticamente')
                sleep(segs)
                self._remove_icms_folders()

                # SÓ É PRECISO IMPORTAR 1X PQ AS SAÍDAS ESTÃO JUNTAS

    def importa_nf_icms_entradas(self):
        self._go2robo_options()
        foritab(1, 'up', 'right', 'up', 'enter', interval=0.25)
        sleep(60)

    def _while_importing(self, path: os.PathLike):
        segs = len(os.listdir(path)) * 0.45
        return segs
        pass

    @ staticmethod
    def _go2robo_options():
        pygui.FAILSAFE = False  # Robo_Options
        pygui.click(pygui.getActiveWindow().topright,
                    clicks=0)
        # COMO ATIVAR ROBÔ AUTOMÁTICO?
        pygui.move(-105, 50)
        pygui.FAILSAFE = True
        pygui.click()

    def _settar_destino_icms(self) -> tuple[os.PathLike, os.PathLike]:
        main_diretorio = self.client_path
        path_autorizadas = os.path.join(
            main_diretorio, 'NFS_AUTORIZADAS')
        path_canceladas = os.path.join(
            main_diretorio, 'NFS_CANCELADAS')

        try:
            os.makedirs(path_autorizadas)
            os.makedirs(path_canceladas)
        except FileExistsError:
            pass

        return path_autorizadas, path_canceladas

    def _xml_send2cloud_icms(self):
        def _move_arquivos(moved_dir_path: os.PathLike, destiny: os.PathLike):
            from shutil import move
            while len(os.listdir(moved_dir_path)) > 0:
                for file in os.listdir(moved_dir_path):
                    src_fullpath = os.path.join(moved_dir_path, file)
                    move(src_fullpath, destiny)

        DIRETORIO = os.path.join(self.client_path, 'NFS')
        if all(os.path.isdir(os.path.join(DIRETORIO, item)) for item in os.listdir(DIRETORIO)):
            # Define se é mercado livre ou arqiuvo normal
            DIRETORIO = os.path.join(DIRETORIO, 'Emitidas_Mercado_Livre')
        else:
            self.caminho_canceladas_destino = ''
            # pois não é template mercado livre(????)

        list_path_autorizadas = []
        list_path_canceladas = []
        # settar destino ()

        # Passa por devolução e venda e appenda à lista de autorizadas/canceladas
        for tipo_nf in ['NF-e de devolução', 'NF-e de venda']:
            _path = os.path.join(DIRETORIO, tipo_nf, 'XML')
            _autorizadas = os.path.join(_path, 'Autorizadas')
            _canceladas = os.path.join(_path, 'Canceladas')
            if os.path.exists(_autorizadas):
                list_path_autorizadas.append(_autorizadas)
            if os.path.exists(_canceladas):
                list_path_canceladas.append(_canceladas)

        # Passa por CTe e appenda na lista de autorizadas
        for tipo_nf in ['CT-e', 'Notas de retiro simbólica', 'Notas de transferência']:
            _path = os.path.join(DIRETORIO, 'Outros documentos', tipo_nf)
            if os.path.exists(_path):
                list_path_autorizadas.append(_path)

        # se continuarem vazio é porque o template NÃO é do mercado livre
        if not list_path_autorizadas:
            list_path_autorizadas.append(DIRETORIO)

        for aut_path in list_path_autorizadas:
            _move_arquivos(
                aut_path, self.caminho_autorizadas_destino)

        for aut_path in list_path_canceladas:
            _move_arquivos(
                aut_path, self.caminho_canceladas_destino)

    def _remove_icms_folders(self):
        os.remove(self.caminho_autorizadas_destino)
        os.remove(self.caminho_canceladas_destino)
        os.remove(os.path.join(self.client_path, 'NFS'))

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
            foritab(1, 'alt', 'right')
            foritab(2, 'down')
            foritab(1, 'right', 'up', 'up', 'enter')
            sleep(5)
            preenche_arqpath(ARQSPATH[contarq])

            if os.path.basename(ARQSPATH[contarq]).upper().startswith("TOMADOR"):
                sleep(2.5)
                pygui.click(x=981, y=356)

            exe_bt_executar()
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

        # filename = f"Registro_ISS-{add2file}"
        filename = f'{self.client_path}'
        pygui.hotkey('left')
        all_keys('ctrl', 'shift', 's')
        sleep(1)
        # pygui.hotkey("enter")  # ...
        pygui.write(filename)
        sleep(2)
        pygui.hotkey('return', 'return', duration=1, interval=1)
        # pygui.hotkey('alt', 'f4')

    def foxit_save__iss(self, add2file):
        sleep(.5)
        pygui.hotkey('enter')  # fica perguntando onde salvar...
        sleep(1)
        filename = f"Registro_ISS-{add2file}"
        filename = os.path.join(self.client_path, filename)
        all_keys('ctrl', 'shift', 's')
        sleep(1)
        pygui.hotkey("enter")  # ...
        sleep(1)
        pygui.write(filename)
        sleep(3.5)
        pygui.hotkey('return', duration=1, interval=1)
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

    @override
    def start_walk_menu(self):  # overriden, not necessary
        # this decorator is not obligatory, but it's a good practice
        x, y = 30, 30
        pygui.click(x, y)

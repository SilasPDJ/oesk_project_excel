# import pgdas_fiscal_oesk
# from pgdas_fiscal_oesk import rotina_pgdas

from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import InitialSetting, get_compt
from pgdas_fiscal_oesk import Consultar

from time import sleep
import pyautogui as pygui
from default.interact import *


from pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados, NfCanceled

from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas_v2 import PgdasDeclaracao
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
from pgdas_fiscal_oesk.silas_abre_g5_loop_v8 import G5
# from win10toast import ToastNotifier
import os
os.system('d:/PROGRAMAS/oesk_project_excel-master/venv/Scripts/activate.bat')
COMPT = get_compt(-1)

CONS = Consultar(COMPT)
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

TOTAL_CLIENTES = len(list(consultar_compt()))
IMPOSTOS_POSSIVEIS = ['ICMS, ISS']


def any_to_str(*args):
    for v in args:
        yield "".join(str(v))


class JROnly(InitialSetting):

    def __init__(self, *args, compt):
        __r_social, self.__cnpj, __cpf, __cod_simples, __valor_competencia, imposto_a_calcular, nf_out = args
        __client = __r_social

        self.compt_used = compt
        self.client_path = self.files_pathit(__client)

        meus_3_valores_atuais = tres_valores_faturados(self.client_path)
        # Se tem 3valores[excel], tem XML. Se não tem, não tem
        # (pois o xml e excel vem do ginfess_download)....

        registronta = self.registronta()

        # if meus_3_valores_atuais and registronta and "ok" != nf_out.lower() != "s": ########## G5
    def make_it(self):
        all_xls_inside = self.files_get_anexos_v4(
            self.client_path, file_type='xlsx')
        relacao_notas = all_xls_inside[0] if len(
            all_xls_inside) == 1 else IndexError()
        self.activating_client(self.formatar_cnpj(self.__cnpj))
        # pygui.getActiveWindow().maximize()
        # # Agora vai ser por cnpj...
        # self.start_walk_menu()
        # foritab(2, 'right')
        # foritab(7, 'down')
        # pygui.hotkey('right')
        # foritab(7, 'down')
        # pygui.hotkey('enter')

    def get_xml(self, cliente):
        b = self.files_get_anexos_v4(self.client_path, file_type='xml')
        b = b[0]
        b = b.split('\\')
        file = f'\\\\{b[-1]}'
        final = '\\'.join(b[:-1]) + file
        return final

    def formatar_cnpj(self, cnpj):
        cnpj = str(cnpj)
        if len(cnpj) < 14:
            cnpj = cnpj.zfill(11)
        cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        print(cnpj)  # 123.456.789-00
        return cnpj

    def registronta(self):
        """
        :return: se tiver pdf que tem ISS e REGISTRO
        """
        registronta = False
        for f in self.files_get_anexos_v4(self.client_path, file_type='xml'):
            return True

        for f in self.files_get_anexos_v4(self.client_path, file_type='csv'):
            return True

        for f in self.files_get_anexos_v4(self.client_path, file_type='pdf'):
            if 'ISS' in f.upper():
                registronta = False
                break
            else:
                registronta = True
        return registronta

    def abre_programa(self, name, path=False):
        """
        :param name: path/to/nameProgram
        :param path: False => contmatic, True => any path
        :return: winleft+r open
        """

        if path is False:
            programa = contmatic_select_by_name(name)
        else:
            programa = name

        senha = '240588140217'
        sleep(1)
        pygui.hotkey('winleft', 'r')
        # pesquisador
        sleep(1)
        pygui.write(programa)
        sleep(1)
        pygui.hotkey('enter')

        sleep(10)

        # p.write(senha)
        # p.hotkey('tab', 'enter', interval=.5)

        pygui.sleep(5)
        # pygui.click(x=1508, y=195) # fecha a janela inicial no G5

    def activating_client(self, client_cnpj):
        x, y = 30, 60
        sleep(2)
        pygui.click(x, y)

        # ativa empresa

        pygui.write(self.first_and_last_day_compt(self.compt_used, '')[1])

        foritab(6, 'tab')  # PESQUISA
        pygui.hotkey('enter')
        sleep(.5)
        all_keys('shift', 'tab')
        sleep(1)
        foritab(6, 'down', interval=.1)  # PESQUISAR POR CGC[CNPJ]
        sleep(.5)
        foritab(1, 'tab')  # Digite a frase contida no texto
        all_keys(client_cnpj)
        print(f'{client_cnpj}:^~30')

        all_keys('ctrl', 'down')
        foritab(2, 'enter', interval=.5)
        sleep(1)

        pygui.hotkey('tab', 'enter', interval=.5)
        # Caso apareça aquela mensagem chata

        # ##################################################### PAREUI DAQUI, SELECIONEI JÁ... MAS TESTAR...
        # sleep(20)

    def importa_nfs(self):
        sleep(2.5)
        w3 = pygui.getActiveWindow()
        pygui.click(w3.center, clicks=0)
        pygui.move(0, 150)
        pygui.click()

    def start_walk_menu(self):
        x, y = 30, 30
        pygui.click(x, y)


for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
    razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = list(
        any_to_str(*compt_vals))
    __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
        any_to_str(*geral))
    envio = envio.upper()
    email = email.strip()
    dividas_ativas = dividas_ativas.strip().lower()

    jonly = JROnly(razao_social, cnpj, cpf, codigo_simples,
        valor_tot, imposto_a_calcular, nf_out, compt=COMPT)
    if e == 0:
        jonly.abre_programa('Jr')
    
    jonly.make_it()
    print('PRESSIONE F1 PARA ATIVAR O PROXIMO CLIENTE')
    # ToastNotifier().show_toast("Pressione F9 para ativar o próximo cliente", duration=10)
    press_key_b4('f1')
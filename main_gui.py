from locale import format_string
from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
from pgdas_fiscal_oesk.rotinas_dividas_v2 import RotinaDividas
from pgdas_fiscal_oesk.send_dividas import SendDividas
from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua, ginfess_driver
from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar

from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui

import tkinter as tk
from default.interact.autocomplete_entry import AutocompleteEntry
from ttkwidgets import autocomplete as ttkac

from threading import Thread
import os
import sys
import subprocess
import clipboard

from pgdas_fiscal_oesk.silas_jr import JR


COMPT = get_compt(int(sys.argv[1])) if len(sys.argv) > 1 else get_compt(-1)

CONS = Consultar(COMPT)
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt
getfieldnames = CONS.get_fieldnames

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

TOTAL_CLIENTES = len(list(consultar_compt()))
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']


class Backend:
    # TODO: lista de clientes a segu9ir
    def __init__(self):
        pass

    @staticmethod
    def any_to_str(*args):
        for v in args:
            yield "".join(str(v))

    def full_pgdas(self):
        LIST_ECAC = []
        LIST_NORMAL = []
        LIST_ISS = []
        SEM_MOV_ONLY = {"simples": [], "ecac": []}

        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()
            dividas_ativas = dividas_ativas.strip().lower()
            proc_ecac = proc_ecac.lower()
            imposto_a_calcular = imposto_a_calcular.upper()

            print(razao_social)

            def append_me(obj_list):
                if float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan']:
                    if imposto_a_calcular != 'LP':
                        obj_list.append((razao_social, cnpj, cpf,
                                        codigo_simples, valor_tot, proc_ecac, None))
                elif imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                    all_valores = get_all_valores(
                        sem_ret, com_ret, anexo, valor_tot)

                    if all_valores:
                        obj_list.append(
                            (razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac, all_valores))
                    elif all_valores is False:
                        obj_list.append((razao_social, cnpj, cpf,
                                        codigo_simples, valor_tot, proc_ecac, None))
                    else:  # None
                        raise ValueError(
                            f'{razao_social.upper()} possui problemas na planilha')

            if declarado.upper() != 'S' and declarado != 'OK':
                print(declarado, valor_tot, imposto_a_calcular)
                # float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan'] or...
                # não há certeza de quem das outras planilhas ta sem mov
                # mas isso não é uma coisa que interfere
                if imposto_a_calcular == "SEM_MOV":
                    if proc_ecac == "sim":
                        append_me(SEM_MOV_ONLY['ecac'])
                    else:
                        append_me(SEM_MOV_ONLY['simples'])

                elif proc_ecac == "sim":
                    append_me(LIST_ECAC)

                else:
                    if imposto_a_calcular == "ISS":
                        append_me(LIST_ISS)
                    else:
                        append_me(LIST_NORMAL)

            # PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
            #             compt=COMPT, driver=pgdas_driver)
            # Não tem mais arg all_valores (está embutido)

        SEM_MOV_ONLY['simples']

        full = SEM_MOV_ONLY['simples'] + LIST_ISS +\
            LIST_NORMAL + SEM_MOV_ONLY['ecac'] + LIST_ECAC

        # return LIST_ECAC, LIST_NORMAL
        return full

    def full_g5(self, specific=None):
        """
        #  Organiza o G5 para fazer primeiro ISS, depois ICMS
        """
        LIST_ISS = []
        LIST_ICMS = []

        def get_order():

            for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
                razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                    self.any_to_str(*compt_vals))
                _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                    self.any_to_str(*geral))
                envio = envio.upper()
                email = email.strip()
                dividas_ativas = dividas_ativas.strip().lower()
                proc_ecac = proc_ecac.lower()
                TUPLA_DATA = (razao_social, cnpj, cpf,
                              codigo_simples, valor_tot, imposto_a_calcular, nf_out, nf_in)

                def append_me(obj_list):
                    if imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                        obj_list.append(TUPLA_DATA)

                if imposto_a_calcular != "SEM_MOV":
                    if nf_out.lower().strip() != 'não há' or nf_in.lower().strip() != 'não há':
                        if imposto_a_calcular.upper() == "ISS":
                            append_me(LIST_ISS)
                        elif imposto_a_calcular.upper() == "ICMS":
                            append_me(LIST_ICMS)

                if specific == razao_social:
                    return [TUPLA_DATA]  # important for loop
            full = LIST_ISS + LIST_ICMS
            # return LIST_ECAC, LIST_NORMAL
            return full
        for v in get_order():
            G5(*v, compt=COMPT)

    def ginfess_abcdfirst(self, specific=""):
        # mudar specific de None pra ""
        from pgdas_fiscal_oesk._folders_preset import PreSetsFromGinfess

        # ordenação diferente de g5 def
        def can_be_next(c: int, gs: str) -> bool:
            gs = gs.lower()
            if c == 0:
                return "gissonline" in gs
            elif c == 1:
                return True
            else:
                return False

        for cont in range(2):
            for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
                razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                    self.any_to_str(*compt_vals))
                _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                    self.any_to_str(*geral))
                envio = envio.upper()
                email = email.strip()
                dividas_ativas = dividas_ativas.strip().lower()
                proc_ecac = proc_ecac.lower()
                pre_sets = PreSetsFromGinfess()

                if ginfess_link != 'nan' and can_be_next(cont, gissonline):
                    if specific == "" or specific == razao_social:
                        DownloadGinfessGui(razao_social, cnpj, ginfess_cod,
                                           ginfess_link,  compt=COMPT, show_driver=False)

                if nf_in.upper() != 'NÃO HÁ' or (nf_out.upper() != 'NÃO HÁ' and imposto_a_calcular != 'ISS'):
                    pre_sets.files_pathit(razao_social, COMPT)
                    print('\033[1;31m', razao_social, '\033[m')
                    # ICMS folder creation
        # TODO: validar essa função...

    def full_dividas(self):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()
            dividas_ativas = dividas_ativas.strip().lower()
            proc_ecac = proc_ecac.lower()
            if dividas_ativas != 'não há':
                yield razao_social, cnpj, dividas_ativas

    def call_func_v2(self, FUNC, specific=None):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()
            dividas_ativas = dividas_ativas.strip().lower()

            def pgdas():
                print(razao_social)

                if declarado.upper() != 'S' and declarado != 'OK':
                    print(declarado, valor_tot, imposto_a_calcular)
                    if float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan']:
                        # if imposto_a_calcular == 'SEM_MOV':
                        PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                        compt=COMPT)
                    elif imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                        all_valores = get_all_valores(
                            sem_ret, com_ret, anexo, valor_tot)
                        print(all_valores)
                        if all_valores:
                            PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                            compt=COMPT,
                                            all_valores=all_valores)
                        elif all_valores is False:
                            PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                            compt=COMPT,)
                        else:  # None
                            raise ValueError(
                                f'{razao_social.upper()} possui problemas na planilha')

            def gias():
                if imposto_a_calcular == 'LP' and ginfess_cod != 'nan' and declarado != 'S':
                    GIA(razao_social, proc_ecac.replace('.', ''), *ginfess_cod.split('//'),
                        compt=COMPT)
                # Login e senha estão vindo de ginfess cod, pois o "ginfess" deles é a GIA

            def giss():
                if giss_login.lower().strip() not in ['ginfess cód', 'não há'] and giss_login != 'nan':
                    print(giss_login)
                    try:
                        GissGui([razao_social, cnpj, giss_login],
                                compt=COMPT, first_compt=get_compt(-1))
                    except Exception as e:
                        GissGui([razao_social, cnpj, giss_login],
                                compt=COMPT, first_compt=get_compt(-2))

            def pgdasmail():
                # Eu devo tratar o envio aqui, mas por enquanto ta la
                PgDasmailSender(razao_social, cnpj, cpf, declarado, valor_tot,
                                imposto_a_calcular, envio, email=email, compt=COMPT, all_valores=[])

            def dividasmail():
                if dividas_ativas != 'não há':
                    if div_envios in ('', 'nan'):
                        SendDividas(razao_social, div_envios,
                                    email=email, compt=COMPT)

            def jr():
                if 'OK' != declarado.upper() != 'S':
                    JR(razao_social, cnpj, compt=COMPT)

            if specific == '':
                eval(f'{FUNC}()')
            else:
                # specific_list = specific.split(";")
                # specific_list = [c.strip() for c in specific]
                if razao_social == specific:
                    return eval(f'{FUNC}()')
                else:
                    pass

    def after_ginfess(self, event):

        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()
            dividas_ativas = dividas_ativas.strip().lower()
            if imposto_a_calcular.upper() == "ISS":
                ExcelValuesPreensh(razao_social, cnpj, cpf,
                                   main_xl_path=main_file, compt=COMPT)
        prgm = sys.executable
        # os.execl(prgm, prgm, * sys.argv)


class MainApplication(tk.Frame, Backend):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.root = parent
        LABELS = []

        optmenu_data = CONS.clients_list(0)
        self.selected_client = AutocompleteEntry(optmenu_data, self.get_v_total, root,
                                                 listboxLength=0, width=60)

        self.__getfieldnames = getfieldnames()
        excel_col = ttkac.AutocompleteEntry(
            self.root, list(self.__getfieldnames))

        self.valorADeclarar = self.button(
            f'', self.get_v_total)
        bt_abre_pasta = self.button(
            'Abre e copia pasta de: ', self.abre_pasta, 'black', 'lightblue')
        bt_copia = self.button(
            'Copia Campo [F4]', lambda: self.get_dataclipboard(excel_col.get()
                                                               ), 'black', 'lightblue')
        bt_das = self.button('Gerar PGDAS', lambda: self.call_func_v2(
            'pgdas', self.selected_client.get()))
        bt_das_full = self.button('Gerar PGDAS FULL', lambda:
                                  PgdasDeclaracaoFull(
                                      *self.full_pgdas(), compt=COMPT),
                                  bg='darkgray')

        bt_gias = self.button('Fazer GIAS', lambda: self.call_func_v2(
            'gias', self.selected_client.get()))
        bt_ginfess = self.button(
            'Fazer Ginfess', lambda: self.ginfess_abcdfirst(self.selected_client.get()))
        bt_giss = self.button('Fazer Giss', lambda: self.call_func_v2(
            'giss', self.selected_client.get()))
        bt_g5 = self.button('Fazer G5', lambda: self.full_g5(
            self.selected_client.get()), bg="#F0AA03")
        bt_jr = self.button('Fazer JR', lambda: self.call_func_v2(
            'jr', self.selected_client.get()), bg="#556353")
        bt_sendpgdas = self.button('Enviar PGDAS', lambda: self.call_func_v2(
            'pgdasmail', self.selected_client.get()), bg='red')
        bt_dividas_rotina = self.button('Rotina FULL Dívidas', lambda: RotinaDividas(
            *self.full_dividas(), compt=COMPT), bg='darkgray')
        bt_dividasmail = self.button('Enviar Dívidas', lambda: self.call_func_v2(
            'dividasmail', self.selected_client.get()), bg='red')

        self.__pack(bt_abre_pasta, bt_copia, self.valorADeclarar, bt_das, bt_das_full, bt_gias, bt_ginfess,
                    bt_giss, bt_g5, bt_jr, bt_sendpgdas, bt_dividas_rotina, bt_dividasmail)
        self.selected_client.focus_force()
        self.__pack(self.selected_client, excel_col)
        self.increment_header_tip(
            LABELS, "Pressione F5 após atualizar a planilha")
        # TIPS
        self.__pack(*LABELS)

        # bt binds
        self.root.bind("<F5>", self._restart_after_updt)
        self.root.bind("<F4>", lambda x: self.get_dataclipboard(
            excel_col.get()
        ))
        self.root.bind("<F12>", self.after_ginfess)

    # functions
    def get_v_total(self):
        import locale
        from locale import format_string
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        v = self.get_dataclipboard('Valor Total')
        v_fat = format_string('%.2f', float(v), 1)
        clipboard.copy(v_fat)  # increment

        self.valorADeclarar['text'] = f' VALOR FATURADO: R$ {v_fat}'

    def abre_pasta(self):
        folder = "\\".join(main_folder.split('/')[:-1])
        folder = os.path.join(
            folder, COMPT[3:], COMPT, self.selected_client.get())
        if not os.path.exists(folder):
            os.makedirs(folder)
        subprocess.Popen(f'explorer "{folder}"')
        clipboard.copy(folder)
        self.selected_client

    def get_dataclipboard(self, campo: str):
        # input(campo)
        if campo == '':
            campo = "CNPJ"
        indcampo = CONS.get_fieldnames().index(campo)
        selected_list_values = list(
            self.any_to_str(*CONS.clients_list(indcampo)))
        whoindex = self.__get_clienid(self.selected_client.get())
        returned = str(selected_list_values[whoindex])
        clipboard.copy(returned)
        return returned

    def __get_clienid(self, client_name):
        cg = consultar_compt()
        clientid = False
        cloops = [cloops[0] for cloops in cg]
        clientid = cloops.index(client_name)
        return clientid

    # restart program method
    @staticmethod
    def _restart_after_updt(e):
        prgm = sys.executable
        os.execl(prgm, prgm, * sys.argv)

    # increment tip for list b4 packing
    @staticmethod
    def increment_header_tip(labels: list, tip: str, font=("Currier", 12), fg="#000"):
        labels.append(
            tk.Label(root, text=tip, font=font, fg=fg))

    # Elements and placements
    @ staticmethod
    def __pack(*els, x=50, y=10, fill='x', side=tk.TOP, expand=0):
        try:
            x1, x2 = x
        except TypeError:
            x1, x2 = x, x

        try:
            y1, y2 = y
        except TypeError:
            y1, y2 = y, y
        for el in els:
            el.pack(padx=(x1, x2), pady=(
                y1, y2), fill=fill, side=side, expand=expand)

    @ staticmethod
    def change_state(*args, change_to=None):
        """
        :param args: elements [buttons]
        :param change_to: Change state to [normal, disabled, ...], if None changes to opposite, 0 -> disabled, 1 -> normal
        :return:
        """
        for bt in args:
            bt_state = bt['state']
            if change_to is None:
                if bt_state == 'normal':
                    bt['state'] = 'disabled'
                else:
                    bt['state'] = 'normal'
            else:
                if str(change_to).lower().strip() == 'disabled' or str(change_to).lower().strip() == 'normal':
                    pass
                elif not isinstance(change_to, int):
                    print(f'{bt} em estado NORMLA')
                    change_to = 'normal'
                else:
                    change_to = 'disabled' if change_to == 0 else 'normal'

                bt['state'] = change_to

    def button(self, text, command=None, fg='#fff', bg='#000',):
        bt = tk.Button(self, text=text, command=lambda: self.start(
            command), fg=fg, bg=bg)
        return bt
        # threading...

    def refresh(self):
        self.root.update()
        self.root.after(1000, self.refresh)

    def start(self, stuff):
        self.refresh()
        Thread(target=stuff).start()
    # threading


if __name__ == "__main__":
    root = tk.Tk()
    root.title = 'Autoesk'

    b = MainApplication(root)
    b.pack(side="top", fill="both", expand=True)

    root.geometry('500x800')
    root.mainloop()


from pgdas_fiscal_oesk.rotinas_dividas_v2 import RotinaDividas
from pgdas_fiscal_oesk.send_dividas import SendDividas
from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
from pgdas_fiscal_oesk.silas_abre_g5_loop_v8 import G5
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, pgdas_driver_ua, ginfess_driver
from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar

from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
from pgdas_fiscal_oesk.rotina_pgdas_v2 import PgdasDeclaracao as PgdasDeclaracaoFull
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui

import tkinter as tk
from default.interact.autocomplete_entry import AutocompleteEntry, matches
from threading import Thread
import os
import subprocess

COMPT = get_compt(-1)

CONS = Consultar(COMPT)
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE

TOTAL_CLIENTES = len(list(consultar_compt()))
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']


class Backend:
    def __init__(self):
        pass

    @staticmethod
    def any_to_str(*args):
        for v in args:
            yield "".join(str(v))

    def get_data(self):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = list(
                self.any_to_str(*compt_vals))
            __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            yield __razao_social

    def full_pgdas(self):
        LIST_ECAC = []
        LIST_NORMAL = []
        SEM_MOV_ONLY = {"simples": [], "ecac": []}

        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = list(
                self.any_to_str(*compt_vals))
            __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()
            dividas_ativas = dividas_ativas.strip().lower()
            proc_ecac = proc_ecac.lower()

            print(razao_social)

            def append_me(obj_list):
                if float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan']:
                    # if imposto_a_calcular == 'SEM_MOV':
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
                    append_me(LIST_NORMAL)

            # PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
            #             compt=COMPT, driver=pgdas_driver)
            # Não tem mais arg all_valores (está embutido)

        SEM_MOV_ONLY['simples']

        full = SEM_MOV_ONLY['simples'] + \
            SEM_MOV_ONLY['ecac'] + LIST_NORMAL + LIST_ECAC

        # return LIST_ECAC, LIST_NORMAL
        return full

    def full_dividas(self):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = list(
                self.any_to_str(*compt_vals))
            __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()
            dividas_ativas = dividas_ativas.strip().lower()
            proc_ecac = proc_ecac.lower()
            if dividas_ativas != 'não há':
                yield razao_social, cnpj, dividas_ativas

    def call_func_v2(self, FUNC, specific=None):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = list(
                self.any_to_str(*compt_vals))
            __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = list(
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
                    GissGui([razao_social, cnpj, giss_login],
                            compt=COMPT)

            def ginfess():
                if ginfess_link != 'nan':
                    DownloadGinfessGui(razao_social, cnpj, ginfess_cod,
                                       ginfess_link,  compt=COMPT)

            def g5():
                G5(razao_social, cnpj, cpf, codigo_simples,
                   valor_tot, imposto_a_calcular, nf_out, compt=COMPT)

            def pgdasmail():
                # Eu devo tratar o envio aqui, mas por enquanto ta la
                PgDasmailSender(razao_social, cnpj, cpf, declarado, valor_tot,
                                imposto_a_calcular, envio, email=email, compt=COMPT, all_valores=[])

            def dividasmail():
                if dividas_ativas != 'não há':
                    if div_envios in ('', 'nan'):
                        SendDividas(razao_social, div_envios,
                                    email=email, compt=COMPT)

            if specific == '':
                eval(f'{FUNC}()')
            else:
                if razao_social == specific:
                    return eval(f'{FUNC}()')
                else:
                    pass

            # não abrir mais a GIA de uma vez
            # TODO: refatorar os programas pra abrir somente 1x


class MainApplication(tk.Frame, Backend):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.root = parent
        optmenu_data = list(self.get_data())
        self.selected_client = AutocompleteEntry(optmenu_data, root,
                                                 listboxLength=0, width=60, matchesFunction=matches)

        bt_abre_pasta = self.button(
            'Abre pasta de: ', self.abre_pasta, bg='lightblue')
        bt_das = self.button('Gerar PGDAS', lambda: self.call_func_v2(
            'pgdas', self.selected_client.get()))
        bt_das_full = self.button('Gerar PGDAS FULL', lambda:
                                  PgdasDeclaracaoFull(
                                      *self.full_pgdas(), compt=COMPT),
                                  bg='darkgray')

        bt_gias = self.button('Fazer GIAS', lambda: self.call_func_v2(
            'gias', self.selected_client.get()))
        bt_ginfess = self.button('Fazer Ginfess', lambda: self.call_func_v2(
            'ginfess', self.selected_client.get()))

        bt_giss = self.button('Fazer Giss', lambda: self.call_func_v2(
            'giss', self.selected_client.get()))
        bt_g5 = self.button('Fazer G5', lambda: self.call_func_v2(
            'g5', self.selected_client.get()))
        bt_sendpgdas = self.button('Enviar PGDAS', lambda: self.call_func_v2(
            'pgdasmail', self.selected_client.get()), bg='red')
        bt_dividas_rotina = self.button('Rotina FULL Dívidas', lambda: RotinaDividas(
            *self.full_dividas(), compt=COMPT), bg='darkgray')
        bt_dividasmail = self.button('Enviar Dívidas', lambda: self.call_func_v2(
            'dividasmail', self.selected_client.get()), bg='red')
        self.__pack(bt_abre_pasta)
        self.__pack(bt_das)
        self.__pack(bt_das_full)
        self.__pack(bt_gias)
        self.__pack(bt_ginfess)

        self.__pack(bt_giss)
        self.__pack(bt_g5)
        self.__pack(bt_sendpgdas)
        self.__pack(bt_dividas_rotina)
        self.__pack(bt_dividasmail)

        self.__pack(self.selected_client)

    # functions
    def abre_pasta(self):
        folder = "\\".join(main_folder.split('/')[:-1])
        folder = os.path.join(
            folder, COMPT[3:], COMPT, self.selected_client.get())
        if not os.path.exists(folder):
            os.makedirs(folder)
        subprocess.Popen(f'explorer "{folder}"')
        self.selected_client

    # Elements and placements

    @ staticmethod
    def __pack(el, x=50, y=10, fill='x', side=tk.TOP, expand=0):
        try:
            x1, x2 = x
        except TypeError:
            x1, x2 = x, x

        try:
            y1, y2 = y
        except TypeError:
            y1, y2 = y, y

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

    root.geometry('500x600')

    root.mainloop()

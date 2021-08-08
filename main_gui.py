
from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
from pgdas_fiscal_oesk.silas_abre_g5_loop_v8 import G5
from pgdas_fiscal_oesk.gias import GIA
from default.webdriver_utilities.pre_drivers import pgdas_driver, ginfess_driver
from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar

from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui

import tkinter as tk
from default.interact.autocomplete_entry import AutocompleteEntry, matches
from threading import Thread


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

    def get_data(self):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = compt_vals
            __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = geral
            yield __razao_social

    def call_func_v2(self, FUNC, specific=None):
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, div_envios = compt_vals
            __razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas, proc_ecac = geral

            def pgdas():
                print(razao_social)

                if str(declarado).upper() != 'S' and str(declarado) != 'OK':
                    print(declarado, valor_tot, imposto_a_calcular)
                    if valor_tot == 0 or str(valor_tot) == 'nan':
                        if imposto_a_calcular == 'SEM_MOV':
                            PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                            compt=COMPT, driver=pgdas_driver)
                        elif imposto_a_calcular == 'LP' and str(ginfess_cod != 'nan'):
                            # GIA
                            GIA(razao_social, cnpj, *ginfess_cod.split('//'),
                                compt=COMPT, driver=pgdas_driver)
                        else:
                            print('passed', razao_social)
                    elif imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                        all_valores = get_all_valores(
                            sem_ret, com_ret, anexo, valor_tot)
                        print(all_valores)

                        if all_valores:
                            PgdasDeclaracao(razao_social, cnpj, cpf, codigo_simples, valor_tot, proc_ecac,
                                            compt=COMPT, driver=pgdas_driver,
                                            all_valores=all_valores)
                        else:
                            raise ValueError(
                                f'{razao_social.upper()} possui problemas na planilha')

            def giss():
                if str(giss_login).lower().strip() not in ['ginfess cód', 'não há'] and str(giss_login) != 'nan':
                    print(str(giss_login))
                    GissGui([razao_social, cnpj, giss_login],
                            pgdas_driver, COMPT)

            def ginfess():
                if str(ginfess_link) != 'nan':
                    DownloadGinfessGui(razao_social, cnpj, str(ginfess_cod),
                                       ginfess_link, driver=ginfess_driver, compt=COMPT)

            def g5():
                G5(razao_social, cnpj, cpf, codigo_simples,
                   valor_tot, imposto_a_calcular, compt=COMPT)

            def pgdasmail():
                PgDasmailSender(razao_social, cnpj, cpf, declarado, valor_tot,
                                imposto_a_calcular, envio, email=email, compt=COMPT, all_valores=[])

            if specific == '':
                eval(f'{FUNC}()')
            else:
                if razao_social == specific:
                    return eval(f'{FUNC}()')
                else:
                    pass


class MainApplication(tk.Frame, Backend):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.root = parent
        optmenu_data = list(self.get_data())
        self.selected_client = AutocompleteEntry(optmenu_data, root,
                                                 listboxLength=0, width=60, matchesFunction=matches)

        bt_das = self.button('Gerar PGDAS', lambda: self.call_func_v2(
            'pgdas', self.selected_client.get()))
        bt_ginfess = self.button('Fazer Ginfess', lambda: self.call_func_v2(
            'ginfess', self.selected_client.get()))
        bt_giss = self.button('Fazer Giss', lambda: self.call_func_v2(
            'giss', self.selected_client.get()))
        bt_g5 = self.button('Fazer G5', lambda: self.call_func_v2(
            'g5', self.selected_client.get()))
        bt_sendpgdas = self.button('Enviar PGDAS', lambda: self.call_func_v2(
            'pgdasmail', self.selected_client.get()))
        self.__pack(bt_das)
        self.__pack(bt_ginfess)
        self.__pack(bt_giss)
        self.__pack(bt_g5)
        self.__pack(bt_sendpgdas)

        self.__pack(self.selected_client)

    # functions
    def optmenu_value(self, _var: tk.StringVar):
        return _var.get()

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

    root.geometry('500x500')

    root.mainloop()
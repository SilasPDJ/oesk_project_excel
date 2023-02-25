
from default.interact import press_key_b4
from pgdas_fiscal_oesk.ginfess_excel_values import ExcelValuesPreensh
from pgdas_fiscal_oesk.rotina_dividas_v3 import dividas_ativas_complete as rotina_dividas
from pgdas_fiscal_oesk.send_dividas import SendDividas
from pgdas_fiscal_oesk.send_pgdamail import PgDasmailSender
from pgdas_fiscal_oesk.silas_abre_g5_loop_v10 import G5
# from pgdas_fiscal_oesk.silas_abre_g5_loop_v9_iss import G5
from pgdas_fiscal_oesk.gias import GIA
from default.sets import get_compt
from pgdas_fiscal_oesk import Consultar

from default.sets import get_all_valores

from pgdas_fiscal_oesk.rotina_pgdas import PgdasDeclaracao
from pgdas_fiscal_oesk.rotina_pgdas_v3 import PgdasDeclaracao as PgdasDeclaracaoFull
from pgdas_fiscal_oesk.giss_online_pt11 import GissGui
from pgdas_fiscal_oesk.ginfess_download import DownloadGinfessGui
from selenium.common.exceptions import UnexpectedAlertPresentException

import sys

from pgdas_fiscal_oesk.silas_jr import JR

COMPT = get_compt(int(sys.argv[1])) if len(sys.argv) > 1 else get_compt(-1)
GIAS_GISS_COMPT = get_compt(int(sys.argv[2])) if len(
    sys.argv) > 2 else get_compt(-2)

CONS = Consultar(COMPT)
consultar_geral = CONS.consultar_geral
consultar_compt = CONS.consultar_compt
getfieldnames = CONS.get_fieldnames

main_folder = CONS.MAIN_FOLDER
main_file = CONS.MAIN_FILE
TOTAL_CLIENTES = len(list(consultar_compt()))
IMPOSTOS_POSSIVEIS = ['ICMS', 'ISS']
# TODO: GUI para impostos possiveis
# IMPOSTOS_POSSIVEIS.clear()
# addentry vai virar um objeto p/ funcionar corretamente c/ outras entry_row


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
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()

            proc_ecac = proc_ecac.lower()
            imposto_a_calcular = imposto_a_calcular.upper()

            print(razao_social)
            # corrigir o full para enviar email junto quando chegar SQL
            TUPLA_DATA = (razao_social, cnpj, cpf,
                          codigo_simples, valor_tot, proc_ecac)

            def append_me(obj_list):
                if float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan']:
                    if imposto_a_calcular != 'LP':
                        obj_list.append((*TUPLA_DATA, None))
                elif imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                    all_valores = get_all_valores(
                        sem_ret, com_ret, anexo, valor_tot)

                    if all_valores:
                        obj_list.append(
                            (*TUPLA_DATA, all_valores))
                    elif all_valores is False:
                        obj_list.append((*TUPLA_DATA, None))
                    else:  # None
                        raise ValueError(
                            f'{razao_social.upper()} possui problemas na planilha')
            if declarado.upper() != 'S' and declarado.upper() != 'OK' and (sem_ret != "nan" or com_ret != "nan"):
                # ret!='nan' remove o erro de declarar sem o "zerou na planilha"
                # Não precisa mais ficar necessariamente ficar marcando "OK"
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

    def full_g5(self, specifics=[]):
        """
        #  Organiza o G5 para fazer primeiro ISS, depois ICMS
        """
        LIST_ISS = []
        LIST_ICMS = []

        def get_order():

            for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
                razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, imposto_a_calcular = list(
                    self.any_to_str(*compt_vals))
                _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, proc_ecac = list(
                    self.any_to_str(*geral))
                envio = envio.upper()
                email = email.strip()

                proc_ecac = proc_ecac.lower()
                TUPLA_DATA = (razao_social, cnpj, cpf,
                              codigo_simples, valor_tot, imposto_a_calcular, nf_out, nf_in)

                def append_me(obj_list):
                    if imposto_a_calcular.strip() in IMPOSTOS_POSSIVEIS:
                        obj_list.append(TUPLA_DATA)

                if len(specifics) > 1 or specifics[0].get() != "":
                    for specific in specifics:
                        if imposto_a_calcular == "SEM_MOV":
                            print(
                                f"\033[1;31mEmpresa {razao_social} não tem movimento...\033[m;")
                        elif specific.get() == razao_social:
                            append_me(LIST_ISS)
                            # Nos 'específicos' não me importo com a ordem
                else:
                    if imposto_a_calcular != "SEM_MOV":
                        if nf_out.lower().strip() != 'não há' or nf_in.lower().strip() != 'não há':
                            if imposto_a_calcular.upper() == "ISS":
                                append_me(LIST_ISS)
                            elif imposto_a_calcular.upper() == "ICMS":
                                append_me(LIST_ICMS)
                        # return [TUPLA_DATA]  # important for loop
            full = LIST_ISS + LIST_ICMS
            # return LIST_ECAC, LIST_NORMAL
            return full
        for v in get_order():
            G5(*v, compt=COMPT)

    def ginfess_abcdfirst(self, specifics=[]):
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
                razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, imposto_a_calcular = list(
                    self.any_to_str(*compt_vals))
                _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, proc_ecac = list(
                    self.any_to_str(*geral))
                envio = envio.upper()
                email = email.strip()

                proc_ecac = proc_ecac.lower()
                pre_sets = PreSetsFromGinfess()

                if ginfess_link != 'nan' and can_be_next(cont, gissonline):
                    if len(specifics) > 1 or specifics[0].get() != "":
                        for specific in specifics:
                            if specific.get() == razao_social:
                                DownloadGinfessGui(razao_social, cnpj, ginfess_cod,
                                                   ginfess_link,  compt=COMPT, show_driver=True)
                    else:
                        DownloadGinfessGui(razao_social, cnpj, ginfess_cod,
                                           ginfess_link,  compt=COMPT, show_driver=False)

                if nf_in.upper() != 'NÃO HÁ' or (nf_out.upper() != 'NÃO HÁ' and imposto_a_calcular != 'ISS'):
                    pre_sets.files_pathit(razao_social, COMPT)
                    print('\033[1;31m', razao_social, '\033[m')
                    # ICMS folder creation

    def call_func_v3(self, FUNC, specifics=[]):

        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()

            def pgdas():
                print(razao_social)

                if declarado.upper() != 'OK' and imposto_a_calcular != 'LP' and (sem_ret != "nan" or com_ret != "nan"):
                    # ret!='nan' remove o erro de declarar sem o "zerou na planilha"
                    # NÃO PRECISA MAIS NECESSARIAMENTE FICAR MARCANDO COM OK...
                    print(declarado, valor_tot, imposto_a_calcular)
                    # if float(valor_tot) == 0 or str(valor_tot) in ['zerou', 'nan']:
                    if str(valor_tot) == "0":
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
                else:
                    print(
                        f"Não irei declarar {razao_social}, pois não 'zerou' ou não declarou valor")

            def gias():
                if imposto_a_calcular == 'LP' and ginfess_cod != 'nan' and declarado != 'S':
                    GIA(razao_social, proc_ecac.replace('.', ''), *ginfess_cod.split('//'),
                        compt=COMPT, first_compt=GIAS_GISS_COMPT)

                # Login e senha estão vindo de ginfess cod, pois o "ginfess" deles é a GIA

            def giss():
                if giss_login.lower().strip() not in ['ginfess cód', 'não há'] and giss_login != 'nan':
                    print(giss_login)
                    gcont = -2
                    while True:
                        try:
                            # GissGui([razao_social, cnpj, giss_login],
                            #         compt=COMPT, first_compt=get_compt(gcont))
                            GissGui([razao_social, cnpj, giss_login],
                                    compt=COMPT, first_compt=get_compt(gcont))
                            gcont -= 1
                            break
                        except UnexpectedAlertPresentException:
                            pass
                        except Exception as e:
                            raise e

            def pgdasmail():
                # Eu devo tratar o envio aqui, mas por enquanto ta la
                PgDasmailSender(razao_social, cnpj, cpf, declarado, valor_tot,
                                imposto_a_calcular, envio, email=email, compt=COMPT, all_valores=[])

            def dividasmail():
                return
                SendDividas

            def jr():
                if 'OK' != declarado.upper() != 'S':
                    JR(razao_social, cnpj, compt=COMPT)
            if len(specifics) > 1 or specifics[0].get() != "":
                for specific in specifics:
                    if razao_social == specific.get():
                        eval(f'{FUNC}()')
            else:
                eval(f'{FUNC}()')

    def after_ginfess(self, event):
        shall_sleep = True
        for e, (geral, compt_vals) in enumerate(zip(consultar_geral(), consultar_compt())):
            razao_social, declarado, nf_out, nf_in, sem_ret, com_ret, valor_tot, anexo, envio, imposto_a_calcular = list(
                self.any_to_str(*compt_vals))
            _razao_social, cnpj, cpf, codigo_simples, email, gissonline, giss_login, ginfess_cod, ginfess_link, proc_ecac = list(
                self.any_to_str(*geral))
            envio = envio.upper()
            email = email.strip()

            if imposto_a_calcular.upper() == "ISS":
                ExcelValuesPreensh(razao_social, cnpj, cpf,
                                   main_xl_path=main_file, compt=COMPT, shall_sleep=shall_sleep)
                shall_sleep = False
        prgm = sys.executable
        # os.execl(prgm, prgm, * sys.argv)

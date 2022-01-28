from datetime import date
from .pathmanager import Dirs
from .now import Now
import os

# @ staticmethod


def get_compt(m_cont=-1, y_cont=0, past_only=True, sep='-'):
    from datetime import timedelta, datetime
    from dateutil.relativedelta import relativedelta
    month = datetime.now().month
    year = datetime.now().year

    now_date = date(year, month, 1)

    if past_only:
        m_cont = m_cont * (-1) if m_cont > 0 else m_cont
        y_cont = y_cont * (-1) if y_cont > 0 else y_cont
        # force to be negative

    now_date = now_date + relativedelta(months=m_cont)
    now_date = now_date + relativedelta(years=y_cont)
    month, year = now_date.month, now_date.year
    compt = f'{month:02d}{sep}{year}'
    return compt


def get_all_valores(sem_ret, com_ret, anexo, valor_tot):
    def split_sep_vals(val, withme=';'):
        val = str(val)
        try:
            return val.split(withme)
            # print('valorA;valorB___valorC;valorD  valorTotal')

        except AttributeError:
            return list(val)

    def greater_than(l1, l2):
        return len(l1) > len(l2)
    sem_ret = split_sep_vals(sem_ret)
    com_ret = split_sep_vals(com_ret)
    anexo = split_sep_vals(anexo)

    # retorna False para não prosseguir, pois o número de anexos não bate com o número de valores entre ;
    if greater_than(sem_ret, com_ret):
        if greater_than(anexo, sem_ret) or greater_than(sem_ret, anexo):
            return False
    elif greater_than(com_ret, sem_ret):
        if greater_than(anexo, com_ret) or greater_than(com_ret, anexo):
            return False
    else:
        # tanto faz porque com_ret == sem_ret
        if greater_than(anexo, sem_ret) or greater_than(sem_ret, anexo):
            return False

    all_valores = []
    soma_total = 0
    for c in range(len(anexo)):
        try:
            sr = sem_ret[c]
        except IndexError:
            sr = 0
        try:
            cr = com_ret[c]
        except IndexError:
            cr = 0
        # Se o valor não foi escrito, é considerado 0

        anx = anexo[c]
        try:
            soma_total += float(sr) + float(cr)
        except ValueError:
            return False
        all_valores.append({'valor_n_retido': sr,
                            'valor_retido': cr, 'anexo': anx})

    if float(soma_total) == float(valor_tot):
        return all_valores
    else:
        print(soma_total, type(soma_total), valor_tot, type(valor_tot))
        print('Vou retornar None')


class Initial:
    main_path = os.path.dirname(os.path.realpath(__file__))
    main_path += '\with_titlePATH.txt'

    @classmethod
    def getset_folderspath(cls, folder_path_only=True):
        """Seleciona onde estão as pastas e planihas

        Returns:
            [type]: [description]
        """
        # filepath = os.path.realpath(__file__)
        # os.path.dirname(filepath)
        returned = False
        try:

            with open(cls.main_path) as f:
                returned = f.read()
        # except FileNotFoundError:
        except (OSError, FileNotFoundError) as e:
            e('WITH TITLE PATH NOT EXISTENTE ')
            returned = cls.__select_path_if_not_exists()

        finally:
            if returned and folder_path_only:
                returned = os.path.dirname(returned)
            return returned

    def __select_path_if_not_exists(self, some_message="SELECIONE ONDE ESTÁ SUA PLANILHA.", savit=main_path):
        """[summary]
        Args:
            some_message (str, optional): []. Defaults to "SELECIONE ONDE ESTÃO SUAS PLANILHAS".
            savit (str, optional): customizable, where to save the info
        Returns:
            [type]: [description]
        """
        from tkinter import Tk, filedialog, messagebox
        root = Tk()
        root.withdraw()
        root = Tk()
        root.withdraw()
        # sh_management = SheetPathManager(file_with_name)
        way = None
        while way is None:
            way = filedialog.askopenfilename(title=some_message, filetypes=[
                                             ("Excel files", ".xlsx .xls .xlsm .csv")])
            if len(way) <= 0:
                way = None
                resp = messagebox.askokcancel(
                    'ATENÇÃO!', message='Favor, selecione uma pasta ou clique em CANCELAR.')
                if not resp:
                    return False
            else:
                wf = open(savit, 'w')
                wf.write(way)
                root.quit()
                return way

    def trata_money_excel(self, faturado):

        faturado = str(faturado).lower().strip()
        if 'nan' in faturado or 'zerou' in faturado or float(faturado) == 0:
            faturado = 'SEM VALOR DECLARADO'
            return faturado
        faturado = f'{float(faturado):,.2f}'
        faturado = faturado.replace('.', 'v')
        faturado = faturado.replace(',', '.')
        faturado = faturado.replace('v', ',')
        return faturado


class InitialSetting(Initial, Dirs, Now):

    @classmethod
    def files_pathit(cls, pasta_client, insyear=None, ano=None):
        from dateutil import relativedelta as du_rl

        """[summary]

        Args:
            pasta_client (str): client folder name
            insyear (str): inside year (competencia or whatever). Defaults then call get_compt_only() as default
            ano (str,[optional]): year folder. Defaults to None.

        Returns:
            [type]: [description]
        """
        insyear = get_compt() if insyear is None else insyear
        compt = insyear
        if ano is None:
            # ano = ''.join([insyear[e+1:] for e in range(len(insyear)) if insyear[e] not in '0123456789'])
            ill_split = ''.join([v for v in compt if v not in '0123456789'])
            mes, ano = compt.split(ill_split)
            try:
                int(ano)
            except ValueError:
                print(
                    f'if ano is None split ainda não encontrado,\n    ano = ano mês anterior')
                ano = date(cls.y(), cls.m(), 1) - du_rl.relativedelta(months=1)
                # Se ele não achar o ano vindo do split...

        __path = cls.getset_folderspath()
        path_final = [*str(__path).split('/')[:-1],
                      ano, insyear, pasta_client]
        salva_path = Dirs.pathit(*path_final)
        return salva_path

    def certif_feito(self, save_path, add=''):
        """
        certificado de que está feito
        :param save_path: nome da pasta 
        :param add: um adicional no nome do arquivo
        :return: caminho+ nome_arquivo jpeg
        """
        type_arquivo = 'png'
        try:
            save = r'{}\\{}-SimplesNacionalDeclarado.{}'.format(
                save_path, add, type_arquivo)
            print(save, '---------> SAVE')
            return save
        except FileNotFoundError:
            print('NÃO CONSEGUI RETORNAR SAVE')

    def first_and_last_day_compt(self, compt, sep='/', zdate_wontbe_greater=False):
        """
        ELE JÁ PEGA O ANTERIOR MAIS PROX
        :param str compt:(competencia or whatever). Defaults then call cls.get_compt_only() as default
        :param sep: separates month/year
        # É necessario o will_be pois antes dele é botado ao contrário
        # tipo: 20200430
        # ano 2020, mes 04, dia 30... (exemplo)
        :return: ÚLTIMO DIA DO MES
        """
        from datetime import date, timedelta
        from dateutil.relativedelta import relativedelta

        ill_split = ''.join([v for v in compt if v not in '0123456789'])
        mes, ano = compt.split(ill_split)
        mes, ano = int(mes), int(ano)
        #  - timedelta(days=1)
        # + relativedelta(months=1)

        last_now = date(ano, mes, 1) + relativedelta(months=1)
        last_now -= timedelta(days=1)
        first_now = date(ano, mes, 1)
        z, a = last_now, first_now

        if zdate_wontbe_greater:
            # last_only
            _check, _dia_hj = self.__check_date_greater_than_today(z)
            if _check:
                z = _dia_hj

        br1st = f'{a.day:02d}{sep}{a.month:02d}{sep}{a.year}'
        brlast = f'{z.day:02d}{sep}{z.month:02d}{sep}{z.year}'
        print(br1st, brlast)
        return br1st, brlast

    def __check_date_greater_than_today(self, mydt: date):
        from datetime import datetime as dt
        dia_hj = dt.now()
        return mydt.day > dia_hj.day, dia_hj

    @staticmethod
    def ate_atual_compt(compt_atual, first_compt=None):
        from datetime import date
        from dateutil import relativedelta
        if first_compt is None:
            yield compt_atual
        else:
            first_compt = first_compt.split('-')
            if len(first_compt) == 1:
                first_compt = first_compt.split('/')
            first_compt = [int(val) for val in first_compt]
            first_compt = date(first_compt[1], first_compt[0], 1)

            # next_date = first_compt + relativedelta.relativedelta(months=1)

            last_compt = compt_atual.split('-')
            # compt = [int(c) for c in compt]
            last_compt = [int(v) for v in last_compt]
            last_compt = date(last_compt[1], last_compt[0], 1)

            # list_compts = []
            while first_compt <= last_compt:

                compt = first_compt
                first_compt = first_compt + \
                    relativedelta.relativedelta(months=1)
                compt_appended = f'{compt.month:02d}-{compt.year}'
                # list_compts.append(compt_appended)
                yield compt_appended

    # yield list_compts

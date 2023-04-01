from datetime import date, datetime
from .pathmanager import Dirs
from .now import Now
import os

# @ staticmethod


def compt_to_date_obj(compt) -> date:
    return Now.str_to_date(compt, "%m-%Y")


def calc_date_compt_offset(m_cont=-1, y_cont=0, past_only=True, sep='-') -> date:
    """ - returns `date` object based on the two first arguments
    Args:
        m_cont (int, optional): referes to month before/after now. Defaults to -1.
        y_cont (int, optional): refers to year before/after now. Defaults to 0.
        past_only (bool, optional): only returns the past, because of competencia. 
        Defaults to True.
    Returns:
        date: datetime.date making the counters with relativedelta
    """
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
    return now_date


def get_compt(m_cont=-1, y_cont=0, past_only=True, format_str='-') -> str:
    """ - returns `str` based on the two first arguments with the format option,
    calls compt_as_date first, 
    Args:
        m_cont (int, optional): referes to month before/after now. Defaults to -1.
        y_cont (int, optional): refers to year before/after now. Defaults to 0.
        past_only (bool, optional): only returns the past, because of competencia. 
        Defaults to True.
        format (str, optional): if len(format) > 2 it retuns what is set on the string.
        Defaults to 2 characters + '%m-%Y'
    Returns:
        str: A string representing the month and year in the specified format.
    """
    now_date = calc_date_compt_offset(m_cont, y_cont, past_only)
    if len(format_str) <= 2:
        return now_date.strftime(f'%m{format_str}%Y')
    else:
        return now_date.strftime(format_str)


def get_all_valores(sem_ret, com_ret, anexo, valor_tot) -> list:
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
    __main_path = os.path.dirname(os.path.realpath(__file__))
    __main_path = os.path.join(__main_path, 'with_titlePATH.txt')

    @classmethod
    def getset_folderspath(cls, folder_path_only=True):
        """Seleciona onde estão as pastas e planihas

        Returns:
            [type]: [description]
        """
        # filepath = os.path.realpath(__file__)
        # os.path.dirname(filepath)
        mainpath = False
        try:

            with open(cls.__main_path) as f:
                mainpath = f.read()
        # except FileNotFoundError:
        except (OSError, FileNotFoundError) as e:
            # e('WITH TITLE PATH NOT EXISTENTE ')
            mainpath = cls.__select_path_if_not_exists(cls)

        if mainpath and folder_path_only:
            return mainpath
        else:
            return os.path.join(mainpath, "__EXCEL POR COMPETENCIAS__", "NOVA_FORMA_DE_DADOS.xlsm")

    def __select_path_if_not_exists(self, some_message="SELECIONE ONDE ESTÁ SUA PASTA PRINCIPAL", savit=__main_path):
        """[summary]
        Args:
            some_message (str, optional): []. Defaults to "SELECIONE ONDE ESTÁ SUA PASTA PRINCIPAL".
            savit (str, optional): customizable, where to save the info
        Returns:
            [type]: [description]
        """
        from tkinter import Tk, filedialog, messagebox
        # sh_management = SheetPathManager(file_with_name)
        way = None
        while way is None:
            way = filedialog.askdirectory(title=some_message)
            if len(way) <= 0:
                way = None
                resp = messagebox.askokcancel(
                    'ATENÇÃO!', message='Favor, selecione uma pasta ou clique em CANCELAR.')
                if not resp:
                    return False
            else:
                wf = open(savit, 'w')
                wf.write(way)
                return way


class InitialSetting(Initial, Dirs, Now):

    @ classmethod
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
        path_final = [__path,
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
        try:
            save = os.path.join(save_path, f"{add}.png")
            print(save, '---------> SAVE')
            return save
        except FileNotFoundError:
            print('NÃO CONSEGUI RETORNAR SAVE')

    @staticmethod
    def convert_img2pdf(filepath_png: str, filepath_newpdf: str, mainpath=None, excluir_png=True):
        from PIL import Image
        # GiaScreenShoot.png
        # f'Recibo_{compt}.pdf'
        if mainpath is not None:
            filepath_png = os.path.join(mainpath, filepath_png)
            filepath_newpdf = os.path.join(mainpath, filepath_newpdf)
        image1 = Image.open(filepath_png)
        try:
            im1 = image1.convert('RGB')
        except ValueError:
            im1 = image1
        im1.save(filepath_newpdf)
        if excluir_png:
            os.remove(filepath_png)

    @ staticmethod
    def ate_atual_compt(compt_atual, first_compt=None):
        from datetime import date
        from dateutil import relativedelta
        if first_compt is None or first_compt == compt_atual:
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

    def trata_money_excel(self, faturado):
        # TODO: refaturar em _backend com foco em já definir os valores e pegar do bd se tem DAS pendentes ou não
        if faturado is None:
            faturado = 0
        faturado = float(faturado)
        faturado = str(faturado).lower().strip()
        if faturado == 'das_pend':
            return 'ATENÇÃO, HÁ BOLETO(S) DO PGDAS PENDENTE(S)'
        if 'nan' in faturado or 'zerou' in faturado or float(faturado) == 0:
            faturado = 'SEM VALOR A PAGAR'
            return faturado
        faturado = f'{float(faturado):,.2f}'
        faturado = faturado.replace('.', 'v')
        faturado = faturado.replace(',', '.')
        faturado = faturado.replace('v', ',')
        return faturado
    # yield list_compts

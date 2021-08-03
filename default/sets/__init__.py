from datetime import datetime
from .pathmanager import Dirs
from .now import Now
import os

# @ staticmethod


def get_compt(m_cont=-1, y_cont=0, past_only=True, sep='-'):
    from datetime import date, datetime
    from datetime import timedelta
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
        soma_total += float(sr) + float(cr)
        all_valores.append({'valor_n_retido': sr,
                            'valor_retido': cr, 'anexo': anx})

    if soma_total == valor_tot:
        return all_valores


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


class InitialSetting(Initial, Dirs, Now):

    @classmethod
    def files_pathit(cls, pasta_client, insyear=None, ano=None):
        from dateutil import relativedelta as du_rl
        from datetime import date

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
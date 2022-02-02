
import win32com.client as win32
from pyperclip import paste
from itertools import count
import os
from time import sleep
from pgdas_fiscal_oesk.contimatic import InitialSetting as SetPaths
from pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados, NfCanceled


def npl(letra):
    # npl = numero_pra_letra
    letra = letra.upper()
    letras = tuple(range(97, 123))
    # letras = (chr(l).upper() for l in letras)
    # [] ou ()...
    # return [letras for l in letras if l == letra]
    letras = [chr(l).upper() for l in letras]
    default_letras = letras.copy()

    letters3cols = False
    # Se contem 3 colunas...
    for l1 in default_letras:
        for l2 in default_letras:
            letras.append(f'{l1}{l2}')
            try:
                return [letras.index(lett)+1 for lett in letras if lett == letra][0]
            except IndexError:
                letters3cols = True
                # Funciona, testado com AB. Procura até achar e retornar index
    if letters3cols:
        for l1 in default_letras:
            for l2 in default_letras:
                for l3 in default_letras:
                    letras.append(f'{l1}{l2}{l3}')
                    try:
                        return [letras.index(lett)+1 for lett in letras if lett == letra][0]
                    except IndexError:
                        pass
                    # Funciona, testado com AAA. Procura até achar e retornar index


def rowcalc(where: str, rowcont: int):
    wherenum = int(where[-2:]) + rowcont
    where = where[:-2]+str(wherenum)
    return where


def not_used_get_values_range(rng, filename):
    param1selection = None
    w3c = win32
    xlapp = w3c.Dispatch('Excel.Application')
    # xlwb = xlapp.Workbooks.Open('C:/_SIMPLES/MEXENDO.xlsx', True, True, None)
    # somente leitura
    wb = xlapp.Workbooks.Open(filename)
    AS = wb.ActiveSheet
    for cont, row in enumerate(AS.Range(rng)):
        # AS = wb.ActiveSheet
        """
        Estou num range... Estou selecionando e copiando/colando os valores dele
        row.Address
        legal
        """
        if cont == 1:
            param1selection = row.Address

        razao_social = row.Value
        if row.Value is not None:
            # print(row.Row)
            selection1_val2 = row.Address
            # print(selection1_val2)
        else:
            param2selection = row.Address

            razoes_sociais = AS.Range(
                f'{param1selection}:{rowcalc(param2selection, -1)}')
            # razoes_sociais.Select()
            valores = razoes_sociais.Copy()
            return paste()


# row.Value, row.Row, row.Column, row.Address


class VbaUtilities(SetPaths):
    # ainda não vou usar o próprio, vou usar o mexendo
    # filename = 'C:/_SIMPLES/MEXENDO.xlsx'
    DIZPEXCEL = win32.Dispatch('Excel.Application')
    DIZPEXCEL.Visible = True

    def __init__(self, filename):
        self.filename = filename
        self.wb = self.DIZPEXCEL.Workbooks.Open(filename)
        self.AS = self.wb.ActiveSheet

    def horizontal_alignment(self, req: int):
        xlLeft, xlRight, xlCenter = -4131, -4152, -4108
        tup = xlLeft, xlCenter,  xlRight
        try:
            return tup[req]
        except IndexError:
            print('horzontal alignment retornado None')
            return None

    def atiby_name(self, name):
        worksheet_iss = self.DIZPEXCEL.Worksheets(name)
        worksheet_iss.Activate()

        self.AS = worksheet_iss
        # necessário pois outra é ativada...

    def get_filled_values(self, rng):
        AS = self.AS
        for row in AS.Range(rng):
            if row.Value is not None:
                # r_sociais.append(row.Value)
                yield row.Value, row.Address
            else:
                break

    def trata_3valores_ydm(self, valor):
        return '0' if valor == 0 or valor is None else valor


class YouDidMe(VbaUtilities):

    def __init__(self):
        super().__init__(filename=f'{self.getset_folderspath()}/mexendo.xlsm')

    def preenche_iss_valores(self):

        AS = self.AS
        xlapp = self.DIZPEXCEL
        sleep(2)
        self.atiby_name('01-2022')

        for (e, row_row) in zip(count(start=0, step=1), self.get_filled_values('A:A')):

            if e != 0:
                cell_value, cell_address = row_row
                cell_address = AS.Range(cell_address)

                cli_path = self.files_pathit(cell_value)
                # self.__client_path = cli_path
                input(tres_valores_faturados(cli_path))
                try:
                    total, com_ret, sem_ret = [
                        float(v) for v in tres_valores_faturados(cli_path)]
                except TypeError:
                    total, com_ret, sem_ret = '0', '0', '0'
                com_ret = '0' if com_ret is None else com_ret
                sem_ret = '0' if sem_ret is None else sem_ret

                if com_ret == sem_ret:
                    sem_ret = com_ret = 'zerou'

                print(sem_ret, com_ret, total)

                cell_address.Offset(1, npl('F')).Select()
                if xlapp.ActiveCell.Value is None:
                    cell_address.Offset(
                        1, npl('E')).Value = self.trata_3valores_ydm(sem_ret)

                xlapp.ActiveCell.Offset(1, 2).Select()
                if xlapp.ActiveCell.Value is None:
                    xlapp.ActiveCell.Offset(
                        1, 1).Value = self.trata_3valores_ydm(com_ret)

                # removi o total, pois já tem a fórmula
        self.DIZPEXCEL.Quit()

    def checka_declaracoes_e_valida(self):
        sheets = '01-2021'

        for sheet in sheets:
            self.atiby_name(sheet)
            sleep(2)
            for (e, row_row) in zip(count(start=0, step=1), self.get_filled_values('A:A')):
                if e != 0:
                    cell_value, cell_address = row_row
                    cell_address = self.AS.Range(cell_address)

                    cli_path = self._files_path_v3(cell_value)

                    celE = cell_address.Offset(1, npl('E'))
                    celE.Select()
                    for file in os.listdir(cli_path):
                        if file.lower().endswith('.pdf') and file.upper().startswith('PGDASD'):
                            celE.Value = 'S'

                            celE.HorizontalAlignment = self.horizontal_alignment(
                                1)
                        else:
                            pass
                            # celE.Value = 'OK'
        self.wb.Close()
        # self.wb.Close(SaveChanges=False)
        self.DIZPEXCEL.Quit()


ydm = YouDidMe()
ydm.preenche_iss_valores()

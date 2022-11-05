import pandas as pd


class NfCanceled:

    import pyautogui as pygui
    import openpyxl
    from time import sleep
    import os

    def __init__(self, path_cliente_plan):
        openpyxl = self.openpyxl
        pygui = self.pygui
        self.path_cliente_plan = path_cliente_plan
        self.folder = self.os.path.dirname(path_cliente_plan)
        self.file_canceladas = f'{self.folder}\\NF_canceladas.txt'
        self.file_needed = f'{self.folder}\\NF-needed.txt'

        # print('RGB =', tuple(int(color_in_hex[i:i + 2],

    def __faz_tudo_por_todos(self):

        openpyxl = self.openpyxl
        pygui = self.pygui
        path_cliente_plan = self.path_cliente_plan

        folder = self.os.path.dirname(path_cliente_plan)
        self.file_canceladas = f'{folder}\\NF_canceladas.txt'
        self.file_needed = f'{folder}\\NF-needed.txt'
        try:
            wb = openpyxl.load_workbook(path_cliente_plan)
            pode_breakar = False
            # ws = wb[nome_excel_atual]
            wsnames = wb.sheetnames[0]
            ws = wb[wsnames]

            canceled = open(self.file_canceladas, 'w')
            wanted = open(self.file_needed, 'w')

            for enu, row in enumerate(ws.iter_rows(max_col=1)):  # tem o max_row ainda

                if enu > 0:
                    for cell in row:
                        print(cell.value, end=' ')
                        # this gives you Hexadecimal value of the color
                        color_in_hex = cell.fill.start_color.index
                        if color_in_hex != '00000000':

                            canceled.write(f'{cell.value}\n')
                            print('HEX =', color_in_hex)
                            # TROCA O VALOR E SALVA O LIVRO (Coluna chamada Valor)
                        else:

                            wanted.write(f'{cell.value}\n')
                        if str(cell.value).strip().capitalize() == 'None':
                            print('\033[1;31m FALSE\033[m')
                            pode_breakar = True
                if pode_breakar:
                    return enu
                    # break
            canceled.close()
            wanted.close()
        except FileNotFoundError:
            input('NÃO CONSEGUI ENCONTRAR, inputing LE_NF_CANCELADAS, Provavelmente ALMEIDA, enter somente............................')
            pygui.hotkey('alt', 'tab')

    def conta_qtd_nfs(self):
        return self.__faz_tudo_por_todos()

    def action(self):
        self.__faz_tudo_por_todos()
        sleep = self.sleep
        pygui = self.pygui
        file = open(self.file_canceladas, 'r')

        # p.hotkey('alt', 'tab')
        sleep(1)
        readfile = file
        for r in readfile:

            print(r)
            # pyperclip.copy(str(r).strip())

            pygui.click(x=753, y=265)  # Acha
            sleep(.9)
            # pyperclip.paste()
            for rr in r.strip():
                pygui.write(rr)
                sleep(0.02)
            sleep(2)
            pygui.hotkey('return')
            sleep(2)
            pygui.click(x=1032, y=262)  # Apaga

            sleep(1)
            # apaga
            pygui.hotkey('return')
            # apaga
        for r in readfile:
            print(r)

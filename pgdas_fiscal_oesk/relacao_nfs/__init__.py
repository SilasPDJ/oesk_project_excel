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

    def __faz_tudo_por_todos(self) -> int:
        openpyxl = self.openpyxl
        pygui = self.pygui
        path_cliente_plan = self.path_cliente_plan

        folder = self.os.path.dirname(path_cliente_plan)
        self.file_canceladas = f'{folder}\\NF_canceladas.txt'
        self.file_needed = f'{folder}\\NF-needed.txt'
        with open(self.file_canceladas, 'w') as fcanceladas, open(self.file_needed, 'w') as fneeded:
            fcanceladas
            df = pd.read_excel(self.path_cliente_plan)
            is_nf_valid = df['NF cancelada'] == False
            nfs_valid = df.loc[is_nf_valid, 'Nº NF'].to_list()
            nfs_invalid = df.loc[~is_nf_valid, 'Nº NF'].to_list()

            fcanceladas.write('\n'.join([str(int(nf)) for nf in nfs_invalid]))

            fneeded.write('\n'.join([str(int(nf)) for nf in nfs_valid]))
        return len(nfs_valid) - len(nfs_invalid)

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


if __name__ == "__main__":
    a = NfCanceled(
        r"O:\OneDrive\_FISCAL-2021\2023\02-2023\Exatitec Calibracoes e Servicos Eireli\Exatitec_30368291000136.xlsx")
    a.conta_qtd_nfs()

from main import *


class MainApplication(tk.Frame, Backend):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.root = parent
        LABELS = []
        self.ENTRIES_CLI = []

        optmenu_data = CONS.clients_list(0)
        __frame_entris_cli = tk.Frame(
            self.root)  # entries_frame client

        self.selected_client = AutocompleteEntry(optmenu_data, self.get_v_total, __frame_entris_cli,
                                                 listboxLength=0, width=100)

        self.__getfieldnames = getfieldnames()
        excel_col = ttkac.AutocompleteEntry(
            self.root, list(self.__getfieldnames))

        self.valorADeclarar = self.button(
            f'', self.get_v_total)
        bt_abre_pasta = self.button(
            'Abre e copia pasta de [F1]: ', self.abre_pasta, 'black', 'lightblue')
        bt_copia = self.button(
            'Copia Campo [F4]', lambda: self.get_dataclipboard(excel_col.get()
                                                               ), 'black', 'lightblue')
        bt_das = self.button('Gerar PGDAS', lambda: self.call_func_v3(
            'pgdas', self.ENTRIES_CLI))
        bt_das_full = self.button('Gerar PGDAS FULL', lambda:
                                  PgdasDeclaracaoFull(
                                      *self.full_pgdas(), compt=COMPT),
                                  bg='darkgray')

        bt_gias = self.button('Fazer GIAS', lambda: self.call_func_v3(
            'gias', self.ENTRIES_CLI))
        bt_ginfess = self.button(
            'Fazer Ginfess', lambda: self.ginfess_abcdfirst(self.ENTRIES_CLI))
        bt_giss = self.button('Fazer Giss', lambda: self.call_func_v3(
            'giss', self.ENTRIES_CLI))
        bt_g5 = self.button('Fazer G5', lambda: self.full_g5(
            self.ENTRIES_CLI), bg="#F0AA03")
        bt_jr = self.button('Fazer JR', lambda: self.call_func_v3(
            'jr', self.ENTRIES_CLI), bg="#556353")
        bt_sendpgdas = self.button('Enviar PGDAS', lambda: self.call_func_v3(
            'pgdasmail', self.ENTRIES_CLI), bg='red')
        bt_dividas_rotina = self.button(
            'Rotina FULL Dívidas', self.full_dividas, bg='darkgray')
        bt_dividasmail = self.button('Enviar Dívidas', lambda: self.call_func_v3(
            'dividasmail', self.ENTRIES_CLI), bg='red')

        self.addentry(self.ENTRIES_CLI, __frame_entris_cli,
                      self.selected_client)

        self.__pack(__frame_entris_cli, fill=tk.BOTH)
        # self.__pack(self.selected_client, excel_col)
        self.__pack(excel_col)

        self.__pack(bt_abre_pasta, bt_copia, self.valorADeclarar, bt_das, bt_das_full, bt_gias, bt_ginfess,
                    bt_giss, bt_g5, bt_jr, bt_sendpgdas, bt_dividas_rotina, bt_dividasmail)
        self.selected_client.focus_force()
        self.increment_header_tip(
            LABELS, "CONTROL + / CONTROL - / F5 = resetar")
        self.increment_header_tip(
            LABELS, "F1 p/ abrir pasta")
        self.increment_header_tip(
            LABELS, "Pressione Control+F5 após atualizar a planilha")
        self.increment_header_tip(
            LABELS, "F12 p/ auto preencher GINFESS")
        # TIPS
        self.__pack(*LABELS)

        # bt binds
        self.root.bind_all("<Control-F5>", self._restart_after_updt)
        self.root.bind_all("<Control-plus>",
                           lambda x: self.addentry(self.ENTRIES_CLI, __frame_entris_cli))
        self.root.bind_all("<Control-minus>",
                           lambda x: self.rmventry(self.ENTRIES_CLI, __frame_entris_cli))

        self.root.bind("<F5>", lambda x: self.reset_entries(
            self.ENTRIES_CLI, __frame_entris_cli))
        self.root.bind("<F4>", lambda x: self.get_dataclipboard(
            excel_col.get()
        ))
        self.root.bind("<F1>", lambda x: self.abre_pasta())
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

    def reset_entries(self, list_entries, frame):
        # frame.winfo_children()[indx].destroy()
        for entry in frame.winfo_children()[-1::-1]:
            if len(frame.winfo_children()) > 1:  # security
                entry.destroy()
        list_entries[0].focus_force()

    @staticmethod
    def addentry(list_entries, frame, add_only=False):
        """
        ### add entries to widget
        - add_only is the Entry added (default is False)
        - grid is being used
        - list_entries = the list to be appended
        - frame = tk.Frame Widget (makes the possibility to use other system in the main app)
        """

        global entry_row
        if not add_only:
            ent = AutocompleteEntry(CONS.clients_list(0), None, frame,
                                    listboxLength=0, width=100)
            ent.grid(row=entry_row, column=0)
            list_entries.append(ent)
        else:
            add_only.grid(row=entry_row, column=0)
            list_entries.append(add_only)
        entry_row += 1

    @staticmethod
    def rmventry(list_entries, frame, indx=-1):
        """
        ### remove entry from widget
        - GIVEN the indx = index
        - grid is being used
        - frame = tk.Frame Widget (makes the possibility to use other system in the main app)
        """
        # for widgets in frame.winfo_children():
        if len(frame.winfo_children()) > 1:  # security
            frame.winfo_children()[indx-1].focus_force()
            frame.winfo_children()[indx].destroy()
            # list_entries.pop()
            del list_entries[-1]

    # increment tip for list b4 packing
    @staticmethod
    def increment_header_tip(labels: list, tip: str, font=("Currier", 12), fg="#000"):
        labels.append(
            tk.Label(ROOT, text=tip, font=font, fg=fg))

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
    ROOT = tk.Tk()
    ROOT.title = 'Autoesk'

    b = MainApplication(ROOT)
    b.pack(side="top", fill="both", expand=True)

    ROOT.geometry('500x900')
    ROOT.mainloop()
